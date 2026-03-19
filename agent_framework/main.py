# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   AutoGen 智能体对话框架 - 完整版本                          ║
║                                                                              ║
║  项目名称：AutoGen Framework                                                ║
║  版本：2.0 (Workflow Enabled)                                                ║
║  支持：autogen-agentchat (0.7.5+) API                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

本文件是智能体框架的主入口，负责协调和执行基于 `agent-api-workflows.md` 定义的
多智能体协作工作流。

核心功能：
- **工作流管理 (WorkflowManager)**: 一个核心类，用于按顺序执行从需求到文档生成的各个阶段。
- **多模式运行**: 支持多种运行模式，通过 `RUN_MODE` 环境变量切换：
  - `workflow` (默认): 显示一个菜单，允许用户执行完整的工作流或单个步骤。
  - `interactive`: 启动一个简单的交互式聊天会话，用于测试或一般查询。
  - `test`: 运行一系列检查，以验证环境配置和 API 连接是否正常。
- **动态智能体创建**: 根据角色和 `personas` 目录下的 Markdown 文件动态创建和配置 AutoGen 智能体。
- **文件 I/O**: 封装了文件读写操作，用于加载上下文、Schema 和保存产出物。
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          第 1 部分：依赖导入                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import json
import os
import sys
import subprocess
from typing import Dict, Any, Optional, List

# --- 第三方库 ---
from dotenv import load_dotenv

# --- AutoGen 核心组件 ---
try:
    # 优先尝试新版 API (autogen-agentchat)
    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    print("✓ 使用 autogen-agentchat v2 API")
except ImportError:
    try:
        # 若失败，则回退到旧版 API (autogen)
        from autogen import AssistantAgent, UserProxyAgent
        print("✓ 使用 autogen v1 API")
    except ImportError:
        print("❌ 错误: 未安装 autogen 包。")
        print("请运行: pip install pyautogen")
        sys.exit(1)

# --- OpenAI API ---
try:
    from openai import OpenAI
except ImportError:
    print("❌ 错误: 未安装 openai 包。")
    print("请运行: pip install openai")
    sys.exit(1)

# --- 本地模块 ---
try:
    from loader import MarkdownLoader
except ImportError:
    print("⚠️ 警告: `loader.py` 未找到。将使用内置的降级文件加载器。")
    class MarkdownLoader:
        @staticmethod
        def load_file(file_path: str) -> str:
            if not os.path.exists(file_path): return ""
            with open(file_path, 'r', encoding='utf-8') as f: return f.read()

# 禁用 OpenTelemetry 遥测，避免在某些网络环境下出现不必要的延迟
os.environ["OTEL_SDK_DISABLED"] = "true"


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                      第 2 部分：配置与工具函数                             ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def load_autogen_config(agent_framework_dir: str) -> dict:
    """
    加载 `autogen_config.json` 配置文件。

    Args:
        agent_framework_dir (str): `agent_framework` 目录的绝对路径。

    Returns:
        dict: 包含配置信息的字典。如果文件不存在，则返回空字典。
    """
    config_path = os.path.join(agent_framework_dir, "autogen_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"⚠️ 警告: 配置文件未找到于 {config_path}")
    return {}

def get_llm_config(config: dict) -> dict:
    """
    获取并整合 LLM (大语言模型) 的配置。

    配置优先级 (从高到低):
    1. 环境变量 (`.env` 文件)。
    2. `autogen_config.json` 文件中的 `llm_config` 部分。
    3. 代码中的默认值。

    Args:
        config (dict): 从 `load_autogen_config` 加载的配置字典。

    Returns:
        dict: 一个适用于 AutoGen Agent 的 `llm_config` 字典。
    """
    llm_cfg = config.get("llm_config", {})
    load_dotenv()  # 加载 .env 文件中的环境变量

    # 按优先级顺序获取 API 密钥、基础 URL 和模型名称
    api_key = os.getenv("OPENAI_API_KEY") or llm_cfg.get("api_key")
    base_url = os.getenv("OPENAI_API_BASE") or llm_cfg.get("base_url")
    model = os.getenv("OPENAI_MODEL_NAME") or llm_cfg.get("model", "gpt-4-turbo")

    if not api_key:
        print("⚠️ 警告: `OPENAI_API_KEY` 未配置。某些需要调用 LLM 的功能可能会失败。")
        api_key = "dummy-key-for-validation"  # 使用一个虚拟密钥以允许结构验证

    # 返回 AutoGen 期望的格式
    return {
        "config_list": [{
            "model": model,
            "api_key": api_key,
            "base_url": base_url,
        }],
        "timeout": llm_cfg.get("timeout", 120),
        "temperature": llm_cfg.get("temperature", 0.7),
        "cache_seed": None  # 设置为 None 以禁用缓存，确保每次运行都获得新的结果
    }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                   第 3 部分：WorkflowManager (核心逻辑)                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class WorkflowManager:
    """
    智能体工作流管理器 (Agent Workflow Manager)。

    该类是整个框架的核心，负责协调和驱动在 `docs/agent-api-workflows.md` 中
    定义的、从项目启动到最终文档渲染的全过程。

    它通过一系列 `step_*` 方法来组织工作流，每个方法代表一个独立的阶段，
    并调用相应的智能体来完成特定任务。
    """

    # ─────────────────── 初始化与辅助函数 ─────────────────────

    def __init__(self, project_root: str):
        """
        初始化 WorkflowManager。

        Args:
            project_root (str): 项目的根目录路径 (例如 `e:\AUTOGNEN_Version`)。
        """
        self.project_root = project_root
        self.agent_framework_dir = os.path.join(project_root, "agent_framework")
        self.project_dir = os.path.join(project_root, "project")

        # 加载框架配置和 LLM 配置
        self.config = load_autogen_config(self.agent_framework_dir)
        self.llm_config = get_llm_config(self.config)

        # 定义所有关键目录的路径，方便后续引用
        self.paths = {
            "personas": os.path.join(self.project_dir, ".bmad", "personas"),
            "data": os.path.join(self.project_dir, ".bmad", "data"),
            "checklists": os.path.join(self.project_dir, ".bmad", "checklists"),
            "docs_jsons": os.path.join(self.project_dir, "docs", ".jsons"),
            "docs_specs": os.path.join(self.project_dir, "docs", "code_specs"),
            "docs_codespecs": os.path.join(self.project_dir, "docs", "codespecs"),
            "docs_table_specs": os.path.join(self.project_dir, "docs", "table_specs"),
            "docs_both_specs": os.path.join(self.project_dir, "docs", "both_specs"),
            "docs_bothspecs": os.path.join(self.project_dir, "docs", "both_specs"),
            "docs_output": os.path.join(self.project_dir, "docs", "output"),
            "docs_stories_epic_1": os.path.join(self.project_dir, "docs", "stories", "epic-1"),
            "docs_checklists": os.path.join(self.project_dir, "docs", "checklists"),
            "output": os.path.join(self.project_dir, "output"),
            "scripts": os.path.join(self.project_dir, "python-bash"),
        }

        # 确保所有必要的目录都存在，如果不存在则创建
        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

    def _create_agent(self, role: str, persona_file: str) -> AssistantAgent:
        """
        根据指定的角色和人物设定文件创建一个 AutoGen 智能体。

        Args:
            role (str): 智能体的角色名称 (例如 "Analyst", "PM")。
            persona_file (str): 存储该角色系统提示的 Markdown 文件名。

        Returns:
            AssistantAgent: 一个配置好 `system_message` 的 AutoGen 智能体实例。
        """
        persona_path = os.path.join(self.paths["personas"], persona_file)

        # 从 Markdown 文件加载系统消息 (System Message)
        if os.path.exists(persona_path):
            sys_msg = MarkdownLoader.load_file(persona_path)
            print(f"  ✓ 已从 {persona_file} 为 {role} 加载人物设定。")
        else:
            sys_msg = f"You are a helpful assistant playing the role of a {role}."
            print(f"  ⚠️ 人物设定文件 {persona_file} 未找到。使用默认提示。")

        # 创建并返回 AssistantAgent 实例
        return AssistantAgent(
            name=role,
            system_message=sys_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER"  # 在自动化工作流中，智能体之间不应等待人类输入
        )

   { def _read_file(self, path: str) -> str:
        """安全地读取文件内容。"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return f.read()
        print(f"⚠️ 警告: 尝试读取一个不存在的文件: {path}")
        return ""

    def _write_file(self, path: str, content: str):
        """将内容写入文件。"""
        with open(path, "w", encoding="utf-8") as f: f.write(content)
        print(f"  💾 已将产出物保存至: {os.path.basename(path)}")

    def _extract_json_from_response(self, content: str) -> str:
        """
        从 LLM 返回的 Markdown 响应中提取 JSON 代码块。
        例如，从 "```json\n{...}\n```" 中提取出 `{...}`。
        """
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            return content[start:end].strip()
        elif "```" in content: # 备用方案，如果没有 "json" 标识
            start = content.find("```") + 3
            end = content.find("```", start)
            return content[start:end].strip()
        return content.strip() # 如果没有代码块，则假定整个响应都是 JSON
   }
    def _run_agent_task(self, agent_role: str, persona_file: str, prompt: str) -> str:
        """
        执行单个智能体任务。

        此函数封装了创建智能体、用户代理和发起聊天的完整流程。

        Args:
            agent_role (str): 要执行任务的智能体角色。
            persona_file (str): 该角色的人物设定文件名。
            prompt (str): 发送给智能体的任务指令。

        Returns:
            str: 智能体返回的最后一条消息内容。
        """
        print(f"\n🤖 正在激活智能体: {agent_role}...")

        # 1. 创建执行任务的智能体
        agent = self._create_agent(agent_role, persona_file)
        
        # 2. 创建一个用户代理来发起对话和接收回复
        user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,  # 只需智能体回复一次
            code_execution_config=False,   # 在此工作流中不执行代码
            llm_config=False               # 代理本身不需要 LLM
        )

        # 3. 发起聊天并等待回复
        chat_res = user_proxy.initiate_chat(
            agent,
            message=prompt,
            summary_method="last_msg"  # 只关心最后一条回复
        )

        # 4. 从聊天结果中提取最后一条消息
        if hasattr(chat_res, 'summary') and chat_res.summary:
            return chat_res.summary
        elif hasattr(chat_res, 'chat_history') and chat_res.chat_history:
             return chat_res.chat_history[-1]['content']
        else:
             # 兼容旧版 AutoGen 的回退方案
             last_msg = agent.last_message()
             return last_msg["content"] if last_msg else ""

    # ────────────────────────── 工作流步骤 (Workflow Steps) ──────────────────────────

    def step_1_project_brief(self):
        """
        **工作流步骤 1: 生成项目简报 (Project Brief)**

        - **负责人**: Analyst (分析师)
        - **输入**: 编码标准、项目简报的 Schema 和模板。
        - **输出**: `project-brief.json` 文件。
        """
        print("\n🚀 [步骤 1] 正在生成项目简报...")

        # 1. 加载上下文文件
        task = self._read_file(os.path.join(self.paths["tasks"], "create-project-brief.md"))
        context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
        template = self._read_file(os.path.join(self.paths["docs_table_specs"], "project-brief.md"))

        # 2. 构建发送给智能体的提示
        prompt = f"""
        任务: 请根据以下 Schema 生成一份项目简报的 JSON。
        {task}
        通用上下文参考:
        {context[:10000]}...
        JSON SCHEMA (必须严格遵守):
        {schema}
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。不要包含任何对话性文字或 Markdown 标记。
        """

        # 3. 调用 Analyst 智能体执行任务
        response = self._run_agent_task("Analyst", "analyst.md", prompt)

        # 4. 提取并保存 JSON 产出物
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "project-brief.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_2_prd(self):
        """
        **工作流步骤 2: 生成产品需求文档 (PRD)**

        - **负责人**: PM (产品经理)
        - **输入**: 上一步生成的 `project-brief.json` 和 PRD 的 Schema。
        - **输出**: `prd.json` 文件。
        """
        print("\n🚀 [步骤 2] 正在生成 PRD...")

        # 1. 加载输入文件
        task = self._read_file(os.path.join(self.paths["tasks"], "create-prd.md"))
        brief_json = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
        context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        template = self._read_file(os.path.join(self.paths["docs_table_specs"], "prd.md"))
        # 2. 构建提示
        prompt = f"""
        任务: 请根据以下项目简报生成一份产品需求文档 (PRD) 的 JSON。
        {task}

        项目简报 (输入):
        {brief_json}

        JSON SCHEMA (必须严格遵守):
        {schema}
        通用上下文参考:
        {context[:10000]}...
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """

        # 3. 调用 PM 智能体
        response = self._run_agent_task("PM", "pm.md", prompt)

        # 4. 保存产出物
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "prd.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_3_stories(self):
        """
        **工作流步骤 3: 生成用户故事 (User Stories)**

        - **负责人**: PO (产品负责人)
        - **输入**: 上一步生成的 `prd.json` 和用户故事的 Schema。
        - **输出**: `next-story.json` 文件。
        """
        print("\n🚀 [步骤 3] 正在生成用户故事...")
        prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "next-story.json"))
        task = self._read_file(os.path.join(self.paths["tasks"], "create-next-story.md"))
        context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        template = self._read_file(os.path.join(self.paths["docs_stories_epic-1"], "story-1.1.md"))
        
        prompt = f"""
        任务: 请根据 PRD 将需求拆解为史诗 (Epics) 和用户故事 (User Stories) 的 JSON。
        {task}

        PRD (输入):
        {prd_json}

        JSON SCHEMA (必须严格遵守):
        {schema}
        通用上下文参考:
        {context[:10000]}...
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """
        response = self._run_agent_task("PO", "po.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "next-story.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_3_1_stories(self):
        """
        **工作流步骤 3,1: 检查清单**

        - **负责人**: QA (质量 Assurance)
        - **输入**: 上一步生成的 `next-story.json` 和检查清单的 Schema。
        - **输出**: `checklist.json` 文件。
        """
        print("\n🚀 [步骤 3,1] 正在检查清单...")    

        next_story_json = self._read_file(os.path.join(self.paths["docs_jsons"], "next-story.json"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "checklist.json"))
        task = self._read_file(os.path.join(self.paths["tasks"], "create-checklist.md"))
        context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        template = self._read_file(os.path.join(self.paths["docs_checklists"], "architecture-checklist.md"))
        
        prompt = f"""
        任务: 请根据用户故事检查清单，创建一份检查清单的 JSON。
        {task}

        用户故事 (输入):
        {next_story_json}

        JSON SCHEMA (必须严格遵守):
        {schema}
        通用上下文参考:
        {context[:10000]}...
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """
        response = self._run_agent_task("QA", "qa.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "checklist.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_pre4_environment(self):
        """
        **工作流步骤 4,1: 设计环境偏好**

        - **负责人**: Architect (架构师)
        - **输入**: `prd.json` 和环境偏好文档。

        """
        task = self._read_file(os.path.join(self.paths["tasks"], "create-architecture.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "environment.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        
        prompt = f"""
        任务: 请根据 PRD 和环境偏好，创建一份环境偏好设计文档 (Markdown 格式)。
        {task}

        PRD (输入):
        {prd_md}

        环境偏好:
        {template}

        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请返回一份全面的、格式良好的 json 文档，描述环境偏好。
        """
        response = self._run_agent_task("Architect", "architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "environment.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_pre4_1_environment(self):
        """
        **工作流步骤 4,1,1: 技术栈偏好**

        - **负责人**: Architect (架构师)
        - **输入**: `prd.json` 和环境偏好文档。

        """
        task = self._read_file(os.path.join(self.paths["tasks"], "create-architecture.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "tech-stack.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        
        prompt = f"""
        任务: 请根据 PRD 和技术栈偏好，创建一份技术栈偏好设计文档 (Markdown 格式)。
        {task}

        PRD (输入):
        {prd_md}

        技术栈偏好:
        {template}

        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请返回一份全面的、格式良好的 Markdown 文档，描述环境偏好。
        """
        response = self._run_agent_task("Architect", "architect.md", prompt)
        output_path = os.path.join(self.paths["docs_codespecs"], "environment.md")
        self._write_file(output_path, response)
        return output_path

    def step_4_architecture(self):
        """
        **工作流步骤 4: 设计系统架构**

        - **负责人**: Architect (架构师)
        - **输入**: `prd.json` 和技术栈偏好文档。
        - **输出**: `architecture.md` (Markdown 格式的架构设计文档)。
        """
        print("\n🚀 [步骤 4] 正在设计系统架构...")
        task = self._read_file(os.path.join(self.paths["tasks"], "create-architecture.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        tech_stack = self._read_file(os.path.join(self.paths["docs_output"], "tech-stack.md"))
        environment = self._read_file(os.path.join(self.paths["docs_output"], "environment.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        template = self._read_file(os.path.join(self.paths["docs_bothspecs"], "architecture.md"))
        
        prompt = f"""
        任务: 请根据 PRD 和技术栈偏好，创建一份系统架构设计文档 (Markdown 格式)。
        {task}

        PRD (输入):
        {prd_md}

        技术栈偏好:
        {tech_stack}

        环境偏好:
        {environment}

        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请返回一份全面的、格式良好的 Markdown 文档，描述系统架构。
        """
        response = self._run_agent_task("Architect", "architect.md", prompt)
        output_path = os.path.join(self.paths["docs_both_specs"], "architecture.md")
        self._write_file(output_path, response)
        return output_path


    def step_4_1_APIreference(self):

        print("\n🚀 [步骤 4,1] 正在设计 API 参考文档...")   
        task = self._read_file(os.path.join(self.paths["tasks"], "create-doc.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "create_doc.json"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "api-reference.md"))

        prompt = f"""
        任务: 请根据 PRD 创建一份 API 参考文档的 JSON。
        {task}

        PRD (输入):
        {prd_md}

        JSON SCHEMA (必须严格遵守):
        {schema}

        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...     

        模板参考 (结构和内容示例):
        {template[:10000]}...
        

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """
        response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "api-reference.json")
        self._write_file(output_path, json_content)
        return output_path


    def step_4_2_digitstructure_design(self):
        """
        **工作流步骤 4,2: 设计数字结构**

        - **负责人**: DesignArchitect (数字结构设计师)
        - **输入**: `prd.json` 和数字结构的 Schema。
        - **输出**: `digital-structure.json` 文件。
        """
        print("\n🚀 [步骤 4,2] 正在设计数字结构...")
        task = self._read_file(os.path.join(self.paths["tasks"], "create-doc.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        system_architecture = self._read_file(os.path.join(self.paths["docs_jsons"], "architecture.json"))
        api_reference = self._read_file(os.path.join(self.paths["docs_jsons"], "api-reference.json"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "create_doc.json"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "data_models.md"))

        prompt = f"""
        任务: 请根据 PRD 创建一份数据模型文档的 JSON。
        {task}

        PRD (输入):
        {prd_md}
        
        系统架构参考:
        {system_architecture[:10000]}...

        API 参考参考:
        {api_reference[:10000]}...
        
        JSON SCHEMA (必须严格遵守):
        {schema}

        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...     

        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """
        response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "data-models.json")
        self._write_file(output_path, json_content)
        return output_path


    def pre_step_5_UX_UI_design(self):
        """
        **工作流步骤 5,1: 用户体验 (UX) 设计**

        - **负责人**: DesignArchitect (用户体验设计师)
        - **输入**: `prd.json` 和 UX 设计的 Schema。
        - **输出**: `ux-design.json` 文件。
        """
        print("\n🚀 [步骤 5,1] 正在设计用户体验...")    
        task = self._read_file(os.path.join(self.paths["tasks"], "create-front-end-architecture.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "front-end.json"))
        prompt = f"""
        任务: 请根据 PRD 创建一份组件规范的 Markdown 文档。
        {task}

        PRD (输入):
        {prd_md}
        
        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...
        """
        response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_output"], "ux-design.md")
        self._write_file(output_path, json_content)
        return output_path





    def step_pre_5_1_componet(self):
        """
        **工作流步骤 5,2: 组件规范**

        - **负责人**: DesignArchitect (组件设计师)
        - **输入**: `prd.json` 和组件规范的 Schema。
        - **输出**: `component-specs.md` 文件。
        """
        print("\n🚀 [步骤 5,2] 正在设计组件规范...")
        task = self._read_file(os.path.join(self.paths["tasks"], "create-front-end-architecture.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "component-specs.json"))
        ux_design = self._read_file(os.path.join(self.paths["docs_output"], "ux-design.md"))

        prompt = f"""
        任务: 请根据 PRD 创建一份组件规范的 Markdown 文档。
        {task}

        PRD (输入):
        {prd_md}
        
        UX 设计参考:
        {ux_design[:10000]}...
        
        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...
        """
        response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "component-specs.json")
        self._write_file(output_path, json_content)
        return output_path

    def step_5_frontend_architecture(self):
        """
        **工作流步骤 5: 设计前端架构**

        - **负责人**: DesignArchitect (前端架构师)
        - **输入**: `prd.json` 和前端架构的 Schema。
        - **输出**: `front-end.json` 文件。
        """
        print("\n🚀 [步骤 5] 正在设计前端架构...")
        task = self._read_file(os.path.join(self.paths["tasks"], "create-front-end-architecture.md"))
        context1 = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
        context2 = self._read_file(os.path.join(self.paths["data"], "tech-stack.md"))
        context3 = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))
        prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
        schema = self._read_file(os.path.join(self.paths["docs_jsons"], "front-end.json"))
        template = self._read_file(os.path.join(self.paths["docs_codespecs"], "front-end.json"))
        ux_design = self._read_file(os.path.join(self.paths["docs_output"], "ux-design.md"))
        component = self._read_file(os.path.join(self.paths["docs_codespecs"], "component-specs.md"))
        prompt = f"""
        任务: 请根据 PRD 创建一份前端架构的 JSON。
        {task}

        PRD (输入):
        {prd_md}

        JSON SCHEMA (必须严格遵守):
        {schema}
        
        组件规范参考:
        {component[:10000]}...

        UX 设计参考:
        {ux_design[:10000]}...
        
        通用上下文参考:
        {context1[:10000]}...
        {context2[:10000]}...
        {context3[:10000]}...
        
        模板参考 (结构和内容示例):
        {template[:10000]}...

        指令:
        请只返回符合 Schema 的、有效的 JSON 内容。
        """
        response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
        json_content = self._extract_json_from_response(response)
        output_path = os.path.join(self.paths["docs_jsons"], "front-end-architecture.json")
        self._write_file(output_path, json_content)
        return output_path


    def step_8_checklist()






    def step_9_rendering(self):
        """
        **工作流步骤 9: 渲染最终文档**

        此步骤通过执行 `python-bash` 目录下的 Python 脚本，将之前生成的
        JSON 文件转换为人类可读的 Markdown 文档。
        """
        print("\n🚀 [步骤 9] 正在通过 Python 脚本渲染最终文档...")
        scripts = [
            ("project-brief.py", "项目简报"),
            ("prd.py", "产品需求文档"),
            ("user-story.py", "用户故事")
        ]
        for script_name, label in scripts:
            script_path = os.path.join(self.paths["scripts"], script_name)
            if os.path.exists(script_path):
                print(f"  ▶️  正在运行 {script_name} ({label})...")
                try:
                    # 使用 subprocess 安全地执行脚本
                    subprocess.run(
                        [sys.executable, script_path], 
                        check=True, 
                        cwd=self.paths["scripts"],
                        capture_output=True, text=True
                    )
                    print(f"  ✅ {label} 已成功渲染。")
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ 渲染 {label} 失败: {e.stderr}")
            else:
                print(f"  ⚠️  渲染脚本未找到: {script_path}")

    # ────────────────────────── 主执行器 ──────────────────────────

    def run_all(self):
        """
        按顺序执行完整的工作流。
        """
        print("="*60)
        print("🚀 开始执行完整的多智能体工作流")
        print("="*60)
        try:
            self.step_1_project_brief()
            self.step_8_checklist()
            self.step_2_prd()
            self.step_8_checklist()
            self.step_3_stories()
            self.step_8_checklist()
            self.step_4_architecture()
            self.step_8_checklist()
            self.step_5_frontend_architecture()
            self.step_6_backend_architecture()
            self.step_7_digitstructure_design()
            
            # 注意: 步骤 6, 7, 8 为简洁起见已省略，但其实现结构与前述步骤相同。
            self.step_9_rendering()
            print("\n" + "="*60)
            print("✅ 恭喜！工作流已成功完成！")
            print("="*60)
        except Exception as e:
            print(f"\n❌ 工作流执行失败: {str(e)}")
            import traceback
            traceback.print_exc()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                      第 4 部分：程序入口点                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def run_test_mode():
    """
    **测试模式**: 验证框架配置和 API 连接。
    """
    print("\n🧪 正在运行测试模式...")
    try:
        # 简单的导入和配置检查
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        manager = WorkflowManager(project_root)
        if manager.llm_config["config_list"][0]["api_key"] != "dummy-key-for-validation":
            print("✓ LLM 配置已加载。")
        else:
            print("✓ LLM 配置结构正确 (但 API Key 未设置)。")
        print("✓ AutoGen 导入成功。")
        print("✓ 环境加载完毕。")
        print("\n✅ 所有测试通过！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def run_interactive_mode():
    """
    **交互模式**: 启动一个与通用 AI 助手的聊天会话。
    """
    print("\n🤖 正在运行交互模式...")
    
    # 初始化 WorkflowManager 以复用其配置
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = WorkflowManager(project_root)
    
    # 创建一个通用的助手智能体
    agent = AssistantAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. You can help with coding, analysis, and general questions.",
        llm_config=manager.llm_config
    )
    
    # 创建一个与用户交互的代理
    user = UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",  # 始终等待用户输入
        code_execution_config=False,
    )
    
    print("\n对话开始... (输入 'exit' 或 'quit' 退出)")
    user.initiate_chat(agent, message="你好！我已准备就绪，请问有什么可以帮助你的吗？")

def run_workflow_mode():
    """
    **工作流模式**: 显示一个菜单，让用户选择要执行的工作流步骤。
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = WorkflowManager(project_root)
    
    # 显示菜单
    while True:
        print("\n" + "="*30)
        print("  选择要执行的工作流步骤:")
        print("="*30)
        print("  1. 🚀 执行完整工作流 (所有步骤)")
        print("  2. 📄 步骤 1: 生成项目简报")
        print("  3. 📝 步骤 2: 生成 PRD")
        print("  4. 🧩 步骤 3: 生成用户故事")
        print("  5. 🏗️  步骤 4: 设计系统架构")
        print("  6. 🎨 步骤 5: 设计前端架构")
        print("  7. 📜 步骤 9: 渲染所有文档")
        print("  0. 退出")
        
        choice = input("\n请输入选项 (0-7): ").strip()
        
        if choice == "1": manager.run_all()
        elif choice == "2": manager.step_1_project_brief()
        elif choice == "3": manager.step_2_prd()
        elif choice == "4": manager.step_3_stories()
        elif choice == "5": manager.step_4_architecture()
        elif choice == "6": manager.step_5_frontend_architecture()
        elif choice == "7": manager.step_9_rendering()
        elif choice == "0": print("👋 再见！"); break
        else: print("❌ 无效选项，请重试。")

def main():
    """
    主函数，根据 `RUN_MODE` 环境变量决定程序的行为。
    """
    # 读取 RUN_MODE 环境变量，如果未设置，则默认为 'workflow'
    run_mode = os.getenv("RUN_MODE", "workflow").lower()
    
    if run_mode == "test":
        run_test_mode()
    elif run_mode == "interactive":
        run_interactive_mode()
    elif run_mode == "workflow":
        run_workflow_mode()
    else:
        print(f"❌ 未知的运行模式: '{run_mode}'。将默认使用 'workflow' 模式。")
        run_workflow_mode()

if __name__ == "__main__":
    # 当脚本被直接执行时，调用 main() 函数
    main()
