# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               AutoGen 智能体对话框架 - 完整版本（基于工作流）               ║
║                                                                              ║
║  项目名称：AutoGen Framework                                                ║
║  版本：2.1 (Workflow Phase Enabled)                                          ║
║  支持：autogen-agentchat (0.7.5+) API                                       ║
║  工作流规范：agent-api-workflows.md                                         ║
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
  - `full`: 执行完整工作流（从 Phase 0 到 Phase 11）。
- **动态智能体创建**: 根据角色和 `personas` 目录下的 Markdown 文件动态创建和配置 AutoGen 智能体。
- **文件 I/O**: 封装了文件读写操作，用于加载上下文、Schema 和保存产出物。

工作流阶段（来自 agent-api-workflows.md）：
  - Phase 0: 通用上下文（系统约束）
  - Phase 1: 项目简报生成（1.1 & 1.2）
  - Phase 2: PRD 生成（2.1 & 2.2）
  - Phase 3: 用户故事策划（3.1 & 3.2）
  - Phase 4: 系统架构设计（4.1 & 4.2）
  - Phase 5: 前端架构设计（5.1 & 5.2 & 5.3）
  - Phase 6: API 参考整理（6.1）
  - Phase 7: 数据模型设计（7.1）
  - Phase 8: 质量检查循环（8.1）
  - Phase 9: 渲染与发布
  - Phase 10: 智能体协作协议
  - Phase 11: 智能体动态沟通与问题解决机制
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          第 1 部分：依赖导入                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import json
import os
import sys
import subprocess
from typing import Dict, Any, Optional, List
from datetime import datetime

# --- 第三方库 ---
from dotenv import load_dotenv

# --- AutoGen 核心组件 ---
try:
    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    print("✓ 使用 autogen-agentchat v2 API")
except ImportError:
    try:
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
    """加载 `autogen_config.json` 配置文件。"""
    config_path = os.path.join(agent_framework_dir, "autogen_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"⚠️ 警告: 配置文件未找到于 {config_path}")
    return {}

def get_llm_config(config: dict) -> dict:
    """获取并整合 LLM (大语言模型) 的配置。"""
    llm_cfg = config.get("llm_config", {})
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY") or llm_cfg.get("api_key")
    base_url = os.getenv("OPENAI_API_BASE") or llm_cfg.get("base_url")
    model = os.getenv("OPENAI_MODEL_NAME") or llm_cfg.get("model", "gpt-4-turbo")

    if not api_key:
        print("⚠️ 警告: `OPENAI_API_KEY` 未配置。某些需要调用 LLM 的功能可能会失败。")
        api_key = "dummy-key-for-validation"

    return {
        "config_list": [{
            "model": model,
            "api_key": api_key,
            "base_url": base_url,
        }],
        "timeout": llm_cfg.get("timeout", 120),
        "temperature": llm_cfg.get("temperature", 0.7),
        "cache_seed": None
    }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                   第 3 部分：WorkflowManager (核心逻辑)                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class WorkflowManager:
    """
    智能体工作流管理器 - 基于 agent-api-workflows.md 规范设计。

    该类负责协调和驱动从项目启动到最终文档渲染的全过程，
    支持 Phase 0 到 Phase 11 的所有工作流阶段。
    """

    def __init__(self, project_root: str):
        """初始化 WorkflowManager。"""
        self.project_root = project_root
        self.agent_framework_dir = os.path.join(project_root, "agent_framework")
        self.project_dir = os.path.join(project_root, "project")

        self.config = load_autogen_config(self.agent_framework_dir)
        self.llm_config = get_llm_config(self.config)
        self.global_context = ""

        # 定义所有关键目录路径
        self.paths = {
            "personas": os.path.join(self.project_dir, ".bmad", "personas"),
            "data": os.path.join(self.project_dir, ".bmad", "data"),
            "checklists": os.path.join(self.project_dir, ".bmad", "checklists"),
            "sessions": os.path.join(self.project_dir, ".bmad", "sessions"),
            "docs_jsons": os.path.join(self.project_dir, "docs", ".jsons"),
            "docs_specs": os.path.join(self.project_dir, "docs", "code_specs"),
            "docs_codespecs": os.path.join(self.project_dir, "docs", "codespecs"),
            "docs_table_specs": os.path.join(self.project_dir, "docs", "table_specs"),
            "docs_both_specs": os.path.join(self.project_dir, "docs", "both_specs"),
            "docs_output": os.path.join(self.project_dir, "docs", "output"),
            "docs_checklists": os.path.join(self.project_dir, "docs", "checklists"),
            "output": os.path.join(self.project_dir, "output"),
            "scripts": os.path.join(self.project_dir, "python-bash"),
        }

        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

        # 工作流执行历史追踪
        self.execution_log = []

    def _log_phase(self, phase_num: int, phase_name: str, status: str, details: str = ""):
        """记录工作流阶段的执行情况。"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": f"Phase {phase_num}",
            "name": phase_name,
            "status": status,
            "details": details
        }
        self.execution_log.append(log_entry)
        print(f"  📋 [记录] {phase_name}: {status}")

    def _create_agent(self, role: str, persona_file: str) -> AssistantAgent:
        """根据指定的角色和人物设定文件创建一个 AutoGen 智能体。"""
        persona_path = os.path.join(self.paths["personas"], persona_file)

        if os.path.exists(persona_path):
            sys_msg = MarkdownLoader.load_file(persona_path)
            print(f"  ✓ 已从 {persona_file} 为 {role} 加载人物设定。")
        else:
            sys_msg = f"You are a helpful assistant playing the role of a {role}."
            print(f"  ⚠️ 人物设定文件 {persona_file} 未找到。使用默认提示。")

        return AssistantAgent(
            name=role,
            system_message=sys_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER"
        )

    def _read_file(self, path: str) -> str:
        """安全地读取文件内容。"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: return f.read()
        print(f"⚠️ 警告: 尝试读取一个不存在的文件: {path}")
        return ""

    def _write_file(self, path: str, content: str):
        """将内容写入文件。"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f: f.write(content)
        print(f"  💾 已将产出物保存至: {os.path.basename(path)}")

    def _extract_json_from_response(self, content: str) -> str:
        """从 LLM 返回的 Markdown 响应中提取 JSON 代码块。"""
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            return content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            return content[start:end].strip()
        return content.strip()

    def _run_agent_task(self, agent_role: str, persona_file: str, prompt: str) -> str:
        """执行单个智能体任务。"""
        print(f"\n🤖 正在激活智能体: {agent_role}...")

        agent = self._create_agent(agent_role, persona_file)
        user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
            llm_config=False
        )

        chat_res = user_proxy.initiate_chat(
            agent,
            message=prompt,
            summary_method="last_msg"
        )

        if hasattr(chat_res, 'summary') and chat_res.summary:
            return chat_res.summary
        elif hasattr(chat_res, 'chat_history') and chat_res.chat_history:
             return chat_res.chat_history[-1]['content']
        else:
             last_msg = agent.last_message()
             return last_msg["content"] if last_msg else ""

    # ════════════════════════════════════════════════════════════════════════
    # 工作流阶段实现 (按 agent-api-workflows.md 顺序)
    # ════════════════════════════════════════════════════════════════════════

    def _get_consolidated_context(self) -> str:
        """
        根据 Phase 0 定义，读取所有核心上下文文件并合并为一个大字符串。
        """
        context_files = [
            (os.path.join(self.paths["data"], "coding-standards.md"), "编码标准"),
            (os.path.join(self.paths["data"], "glossary.md"), "词汇表"),
            (os.path.join(self.paths["data"], "tech-preferences.md"), "技术偏好"),
            (os.path.join(self.paths["docs_codespecs"], "tech-stack.md"), "技术栈"),
            (os.path.join(self.paths["docs_codespecs"], "environment.md"), "环境"),
        ]
        
        consolidated = "# GLOBAL CONTEXT & CONSTRAINTS\n\n"
        for file_path, label in context_files:
            if os.path.exists(file_path):
                content = self._read_file(file_path)
                consolidated += f"## {label} ({os.path.basename(file_path)})\n{content}\n\n"
        return consolidated

    # ─────────────────────── PHASE 0: 通用上下文 ─────────────────────────
    def phase_0_load_context(self):
        """
        PHASE 0: 加载并整合通用上下文（系统约束）

        按照 agent-api-workflows.md 第 0 节，加载并整合所有关键上下文文件。
        """
        print("\n" + "="*70)
        print("🔄 PHASE 0: 加载并整合通用上下文")
        print("="*70)

        try:
            self.global_context = self._get_consolidated_context()
            
            # 同时打印一下加载状态
            context_files = [
                (os.path.join(self.paths["data"], "coding-standards.md"), "编码标准"),
                (os.path.join(self.paths["data"], "glossary.md"), "词汇表"),
                (os.path.join(self.paths["data"], "tech-preferences.md"), "技术偏好"),
                (os.path.join(self.paths["docs_codespecs"], "tech-stack.md"), "技术栈"),
                (os.path.join(self.paths["docs_codespecs"], "environment.md"), "环境"),
            ]

            loaded_files = 0
            for file_path, label in context_files:
                if os.path.exists(file_path):
                    print(f"  ✓ {label} 已加载")
                    loaded_files += 1
                else:
                    print(f"  ⚠️ {label} 未找到: {file_path}")

            print(f"  ✓ 全局上下文已整合 (约 {len(self.global_context)} 字符)")
            self._log_phase(0, "整合通用上下文", "SUCCESS", f"已加载 {loaded_files}/{len(context_files)} 个上下文文件")
            return True
        except Exception as e:
            self._log_phase(0, "整合通用上下文", "FAILED", str(e))
            return False

    # ─────────────────────── PHASE 1: 项目简报生成 ─────────────────────────
    def phase_1_1_generate_project_brief(self):
        """
        PHASE 1.1: 生成项目简报 JSON

        - 负责人: Analyst (分析师)
        - 输入: 通用上下文、人物性格、业务需求、Schema、模板
        - 输出: project-brief.json
        """
        print("\n" + "="*70)
        print("🚀 PHASE 1.1: 生成项目简报 JSON")
        print("="*70)

        try:
            # 加载输入文件
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
            template = self._read_file(os.path.join(self.paths["docs_table_specs"], "project-brief.md"))

            prompt = f"""
            任务: 请根据以下 Schema 生成一份项目简报的 JSON。
            
            通用上下文参考:
            {context[:5000]}
            
            JSON SCHEMA (必须严格遵守):
            {schema[:5000]}
            
            模板参考 (结构和内容示例):
            {template[:5000]}

            指令:
            请只返回符合 Schema 的、有效的 JSON 内容。
            不要包含任何对话性文字或 Markdown 标记。
            """

            response = self._run_agent_task("Analyst", "analyst.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "project-brief.json")
            self._write_file(output_path, json_content)

            self._log_phase(1.1, "生成项目简报 JSON", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(1.1, "生成项目简报 JSON", "FAILED", str(e))
            raise

    def phase_1_2_validate_project_brief(self):
        """
        PHASE 1.2: 结构校验与补全（项目简报）

        - 负责人: Analyst (分析师)
        - 输入: project-brief.json、Schema
        - 输出: 校验报告、补全后的 JSON
        """
        print("\n" + "="*70)
        print("✅ PHASE 1.2: 项目简报结构校验与补全")
        print("="*70)

        try:
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
            brief_json = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
            glossary = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请校验以下项目简报 JSON 是否符合 Schema，
            并标出缺失/不合规的字段，给出补全后的 JSON。

            JSON SCHEMA:
            {schema[:5000]}

            项目简报 JSON:
            {brief_json[:5000]}

            参考 (词汇表):
            {glossary[:5000]}

            指令:
            1. 检查 JSON 是否符合 Schema 的所有 required 字段。
            2. 如有缺失或错误，请列出并提供修正建议。
            3. 返回完整的、有效的项目简报 JSON。
            """

            response = self._run_agent_task("Analyst", "analyst.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "project-brief-validated.json")
            self._write_file(output_path, json_content)

            self._log_phase(1.2, "项目简报校验", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(1.2, "项目简报校验", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 2: PRD 生成 ─────────────────────────
    def phase_2_1_generate_prd(self):
        """
        PHASE 2.1: 生成 PRD JSON

        - 负责人: PM (产品经理)
        - 输入: project-brief.json、PRD Schema、模板
        - 输出: prd.json
        """
        print("\n" + "="*70)
        print("🚀 PHASE 2.1: 生成 PRD JSON")
        print("="*70)

        try:
            brief_json = self._read_file(os.path.join(self.paths["docs_jsons"], "project-brief.json"))
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            template = self._read_file(os.path.join(self.paths["docs_table_specs"], "prd.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请根据项目简报生成一份产品需求文档 (PRD) 的 JSON。

            项目简报 (输入):
            {brief_json[:5000]}

            JSON SCHEMA (必须严格遵守):
            {schema[:5000]}
            
            通用上下文参考:
            {context[:5000]}
            
            模板参考 (结构和内容示例):
            {template[:5000]}

            指令:
            请只返回符合 Schema 的、有效的 JSON 内容。
            """

            response = self._run_agent_task("PM", "pm.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "prd.json")
            self._write_file(output_path, json_content)

            self._log_phase(2.1, "生成 PRD JSON", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(2.1, "生成 PRD JSON", "FAILED", str(e))
            raise

    def phase_2_2_validate_prd(self):
        """
        PHASE 2.2: PRD 结构校验与补全

        - 负责人: PM (产品经理)
        - 输入: prd.json、Schema
        - 输出: 校验报告、补全后的 JSON
        """
        print("\n" + "="*70)
        print("✅ PHASE 2.2: PRD 结构校验与补全")
        print("="*70)

        try:
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            glossary = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请校验以下 PRD JSON 是否符合 Schema，
            并标出缺失/不合规的字段，给出补全后的 JSON。

            JSON SCHEMA:
            {schema[:5000]}

            PRD JSON:
            {prd_json[:5000]}

            参考 (词汇表):
            {glossary[:5000]}

            指令:
            1. 检查 JSON 是否符合 Schema 的所有 required 字段（step1~step6、appendix）。
            2. 如有缺失或错误，请列出并提供修正建议。
            3. 返回完整的、有效的 PRD JSON。
            """

            response = self._run_agent_task("PM", "pm.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "prd-validated.json")
            self._write_file(output_path, json_content)

            self._log_phase(2.2, "PRD 校验", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(2.2, "PRD 校验", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 3: 用户故事策划 ─────────────────────────
    def phase_3_1_generate_stories(self):
        """
        PHASE 3.1: 生成用户故事拆分策略与故事骨架 JSON

        - 负责人: PO (产品负责人)
        - 输入: PRD JSON、next-story Schema
        - 输出: 包含 epics、story_splitting、dependencies 等的 JSON
        """
        print("\n" + "="*70)
        print("🚀 PHASE 3.1: 生成用户故事拆分策略")
        print("="*70)

        try:
            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "next-story.json"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请根据 PRD 的功能需求，生成一份用户故事拆分策略与故事骨架的 JSON。

            PRD (输入):
            {prd_json[:5000]}

            JSON SCHEMA (必须严格遵守):
            {schema[:5000]}

            通用上下文参考:
            {context[:5000]}

            指令:
            请返回包含以下结构的 JSON：
            - epics: 各个史诗（大功能块）
            - story_splitting: 故事拆分策略
            - story_dependencies: 故事依赖关系
            - story_priorities: 故事优先级排列
            """

            response = self._run_agent_task("PO", "po.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "next-story.json")
            self._write_file(output_path, json_content)

            self._log_phase(3.1, "生成用户故事策略", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(3.1, "生成用户故事策略", "FAILED", str(e))
            raise

    def phase_3_2_invest_check_stories(self):
        """
        PHASE 3.2: INVEST 自检与故事细化

        - 负责人: PO / Dev (产品负责人 / 开发)
        - 输入: next-story.json、INVEST 定义（来自 glossary.md）
        - 输出: 完整故事明细（含 INVEST 自检结果）
        """
        print("\n" + "="*70)
        print("✅ PHASE 3.2: INVEST 自检与故事细化")
        print("="*70)

        try:
            stories_json = self._read_file(os.path.join(self.paths["docs_jsons"], "next-story.json"))
            glossary = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
            context = self._read_file(os.path.join(self.paths["data"], "coding-standards.md"))

            prompt = f"""
            任务: 请对用户故事进行 INVEST 自检并细化每个故事。

            INVEST 定义 (来自词汇表):
            {glossary[:5000]}

            用户故事 JSON:
            {stories_json[:5000]}

            编码规范:
            {context[:5000]}

            指令:
            对于每个用户故事，请检查其是否满足 INVEST 标准：
            - I (Independent): 独立性
            - N (Negotiable): 可协商性
            - V (Valuable): 价值性
            - E (Estimable): 可估计性
            - S (Small): 小粒度
            - T (Testable): 可测试性

            然后针对每个故事提供：
            - user_story: 用户故事描述
            - acceptance_criteria: 验收标准
            - technical_notes: 技术说明
            - dependencies: 依赖关系
            - test_scenarios: 测试场景
            - task_breakdown: 任务分解
            """

            response = self._run_agent_task("PO", "po.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "user-stories-detailed.json")
            self._write_file(output_path, json_content)

            self._log_phase(3.2, "故事 INVEST 自检", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(3.2, "故事 INVEST 自检", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 4: 系统架构设计 ─────────────────────────
    def phase_4_1_generate_architecture(self):
        """
        PHASE 4.1: 生成系统架构文档草稿

        - 负责人: Architect (系统架构师)
        - 输入: PRD、tech-stack.md、environment.md、架构模板
        - 输出: architecture.md (Markdown 文档)
        """
        print("\n" + "="*70)
        print("🚀 PHASE 4.1: 生成系统架构文档草稿")
        print("="*70)

        try:
            prd_md = self._read_file(os.path.join(self.paths["output"], "prd.md"))
            if not prd_md:  # 如果 prd.md 不存在，尝试从 JSON 读取（需要渲染）
                prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
                prd_md = prd_json

            tech_stack = self._read_file(os.path.join(self.paths["docs_specs"], "tech-stack.md"))
            environment = self._read_file(os.path.join(self.paths["docs_specs"], "environment.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
            template = self._read_file(os.path.join(self.paths["docs_both_specs"], "architecture.md"))

            prompt = f"""
            任务: 请根据 PRD 和技术栈偏好，创建一份系统架构设计文档 (Markdown 格式)。

            PRD (输入):
            {prd_md[:5000]}

            技术栈偏好:
            {tech_stack[:5000]}

            环境偏好:
            {environment[:5000]}

            通用上下文参考:
            {context[:5000]}

            模板参考:
            {template[:5000]}

            指令:
            请返回一份全面的、格式良好的 Markdown 文档，包含：
            - 系统整体设计
            - 主要模块划分
            - 技术选型理由
            - 数据流和交互流程
            - 可扩展性考虑
            """

            response = self._run_agent_task("Architect", "architect.md", prompt)
            output_path = os.path.join(self.paths["docs_both_specs"], "architecture.md")
            self._write_file(output_path, response)

            self._log_phase(4.1, "生成系统架构文档", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(4.1, "生成系统架构文档", "FAILED", str(e))
            raise

    def phase_4_2_architecture_checklist(self):
        """
        PHASE 4.2: 架构质量检查与改进

        - 负责人: Architect (系统架构师)
        - 输入: architecture.md、architecture-checklist.md
        - 输出: 改进版架构文档
        """
        print("\n" + "="*70)
        print("✅ PHASE 4.2: 架构质量检查与改进")
        print("="*70)

        try:
            arch_doc = self._read_file(os.path.join(self.paths["docs_both_specs"], "architecture.md"))
            checklist = self._read_file(os.path.join(self.paths["checklists"], "architecture-checklist.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请按照检查清单对架构设计进行评审，
            提出修改建议并产出改进版本的文档。

            架构设计文档:
            {arch_doc[:5000]}

            检查清单:
            {checklist[:5000]}

            参考:
            {context[:5000]}

            指令:
            1. 逐项检查架构是否满足清单中的所有要求。
            2. 标出不足之处。
            3. 返回改进后的架构 Markdown 文档。
            """

            response = self._run_agent_task("Architect", "architect.md", prompt)
            output_path = os.path.join(self.paths["docs_both_specs"], "architecture-improved.md")
            self._write_file(output_path, response)

            self._log_phase(4.2, "架构质量检查", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(4.2, "架构质量检查", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 4.3: UV/UX 设计 ─────────────────────────
    def phase_4_3_uv_ux_design(self):
        """
        PHASE 4.3: UV/UX 设计（新增阶段）
        根据 PRD 设计交互原型说明。
        """
        print("\n" + "="*70)
        print("🎨 PHASE 4.3: UV/UX 设计")
        print("="*70)

        try:
            template_path = os.path.join(self.paths["docs_tablespecs"], "uv-ux.md")
            if not os.path.exists(template_path):
                print("  ⏭️  UV/UX 模板未找到，跳过此阶段。")
                return

            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd-validated.json"))
            if not prd_json:
                prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))

            template = self._read_file(template_path)

            prompt = f"""
            任务: 基于 PRD 生成系统的 UV/UX 设计说明。
            
            全局上下文:
            {self.global_context[:2000]}
            
            PRD 内容:
            {prd_json[:3000]}
            
            模板参考:
            {template[:3000]}
            
            指令: 请产出包含 用户路径(User Flow)、核心交互组件、视觉风格定义 的 Markdown 文档。
            """
            
            response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
            output_path = os.path.join(self.paths["docs_output"], "uv-ux-design.md")
            self._write_file(output_path, response)
            
            self._log_phase(4.3, "UV/UX 设计", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(4.3, "UV/UX 设计", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 5: 前端架构设计 ─────────────────────────
    def phase_5_1_generate_frontend_architecture(self):
        """
        PHASE 5.1: 生成前端架构 JSON

        - 负责人: DesignArchitect (前端架构师)
        - 输入: PRD、front-end.json Schema、API 参考草稿（可选）
        - 输出: front-end-architecture.json
        """
        print("\n" + "="*70)
        print("🚀 PHASE 5.1: 生成前端架构 JSON")
        print("="*70)

        try:
            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            schema = self._read_file(os.path.join(self.paths["docs_jsons"], "front-end.json"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))
            api_ref = self._read_file(os.path.join(self.paths["docs_specs"], "api-reference.md"))

            prompt = f"""
            任务: 请根据 PRD 生成一份前端架构的结构化 JSON。

            PRD (输入):
            {prd_json[:5000]}

            JSON SCHEMA (必须严格遵守):
            {schema[:5000]}

            API 参考:
            {api_ref[:3000]}

            通用上下文参考:
            {context[:5000]}

            指令:
            请返回包含以下内容的 JSON：
            - technology_stack: 技术选型
            - routing: 路由设计
            - state_management: 状态管理
            - api_integration: API 层设计
            - performance: 性能优化策略
            - accessibility: 可访问性标准
            - testing: 测试与质量保证
            """

            response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
            json_content = self._extract_json_from_response(response)
            output_path = os.path.join(self.paths["docs_jsons"], "front-end-architecture.json")
            self._write_file(output_path, json_content)

            self._log_phase(5.1, "生成前端架构 JSON", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(5.1, "生成前端架构 JSON", "FAILED", str(e))
            raise

    def phase_5_2_render_frontend_architecture(self):
        """
        PHASE 5.2: 渲染前端架构文档草稿

        - 负责人: DesignArchitect (前端架构师)
        - 输入: front-end-architecture.json、front-end-architecture.md 模板
        - 输出: front-end-architecture.md (Markdown 文档)
        """
        print("\n" + "="*70)
        print("📝 PHASE 5.2: 渲染前端架构文档草稿")
        print("="*70)

        try:
            frontend_json = self._read_file(os.path.join(self.paths["docs_jsons"], "front-end-architecture.json"))
            template = self._read_file(os.path.join(self.paths["docs_specs"], "front-end-architecture.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请根据前端架构 JSON 和模板，
            渲染生成一份格式良好的前端架构 Markdown 文档。

            前端架构 JSON:
            {frontend_json[:5000]}

            模板参考:
            {template[:5000]}

            参考:
            {context[:5000]}

            指令:
            请返回一份组织清晰的 Markdown 文档，
            包含技术栈、路由、状态管理、API 集成等详细内容。
            """

            response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
            output_path = os.path.join(self.paths["docs_specs"], "front-end-architecture.md")
            self._write_file(output_path, response)

            self._log_phase(5.2, "渲染前端架构文档", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(5.2, "渲染前端架构文档", "FAILED", str(e))
            raise

    def phase_5_3_frontend_architecture_checklist(self):
        """
        PHASE 5.3: 前端架构质量检查与改进

        - 负责人: DesignArchitect (前端架构师)
        - 输入: front-end-architecture.md、frontend-architecture-checklist.md
        - 输出: 改进版前端架构文档
        """
        print("\n" + "="*70)
        print("✅ PHASE 5.3: 前端架构质量检查与改进")
        print("="*70)

        try:
            frontend_doc = self._read_file(os.path.join(self.paths["docs_specs"], "front-end-architecture.md"))
            checklist = self._read_file(os.path.join(self.paths["checklists"], "frontend-architecture-checklist.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请按照检查清单对前端架构设计进行评审，
            提出修改建议并产出改进版本的文档。

            前端架构文档:
            {frontend_doc[:5000]}

            检查清单:
            {checklist[:5000]}

            参考:
            {context[:5000]}

            指令:
            1. 逐项检查前端架构是否满足清单中的所有要求。
            2. 标出不足之处。
            3. 返回改进后的前端架构 Markdown 文档。
            """

            response = self._run_agent_task("DesignArchitect", "design-architect.md", prompt)
            output_path = os.path.join(self.paths["docs_specs"], "front-end-architecture-improved.md")
            self._write_file(output_path, response)

            self._log_phase(5.3, "前端架构质量检查", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(5.3, "前端架构质量检查", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 6: API 参考整理 ─────────────────────────
    def phase_6_1_generate_api_reference(self):
        """
        PHASE 6.1: 汇总并规范 API 参考

        - 负责人: Architect (架构师)
        - 输入: PRD JSON、user-stories JSON、API 参考模板
        - 输出: api-reference.md (Markdown 文档)
        """
        print("\n" + "="*70)
        print("🚀 PHASE 6.1: 汇总并规范 API 参考")
        print("="*70)

        try:
            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            stories = self._read_file(os.path.join(self.paths["docs_jsons"], "user-stories-detailed.json"))
            template = self._read_file(os.path.join(self.paths["docs_specs"], "api-reference.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请根据 PRD 和用户故事中的技术说明，
            汇总并生成一份规范的 API 参考文档。

            PRD (输入):
            {prd_json[:5000]}

            用户故事 (含 API 接口):
            {stories[:5000]}

            模板参考:
            {template[:5000]}

            参考:
            {context[:5000]}

            指令:
            请返回一份完整的 API 参考文档 (Markdown 格式)，包含：
            - 端点列表
            - HTTP 方法
            - 请求参数和格式
            - 响应格式
            - 错误码定义
            - 认证方式
            - 速率限制
            """

            response = self._run_agent_task("Architect", "architect.md", prompt)
            output_path = os.path.join(self.paths["docs_specs"], "api-reference.md")
            self._write_file(output_path, response)

            self._log_phase(6.1, "生成 API 参考", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(6.1, "生成 API 参考", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 7: 数据模型设计 ─────────────────────────
    def phase_7_1_generate_data_models(self):
        """
        PHASE 7.1: 生成数据模型草稿

        - 负责人: Architect (架构师)
        - 输入: PRD JSON、API 参考、data-models.md 模板
        - 输出: data-models.md (Markdown 文档)
        """
        print("\n" + "="*70)
        print("🚀 PHASE 7.1: 生成数据模型草稿")
        print("="*70)

        try:
            prd_json = self._read_file(os.path.join(self.paths["docs_jsons"], "prd.json"))
            api_ref = self._read_file(os.path.join(self.paths["docs_specs"], "api-reference.md"))
            template = self._read_file(os.path.join(self.paths["docs_specs"], "data-models.md"))
            context = self._read_file(os.path.join(self.paths["data"], "glossary.md"))

            prompt = f"""
            任务: 请根据 PRD 和 API 参考，
            生成一份数据模型设计文档。

            PRD (输入，尤其是 dataRequirements):
            {prd_json[:5000]}

            API 参考 (草稿):
            {api_ref[:5000]}

            模板参考:
            {template[:5000]}

            参考:
            {context[:5000]}

            指令:
            请返回一份数据模型文档 (Markdown 格式)，包含：
            - 实体列表
            - 字段定义
            - 数据类型
            - 约束条件
            - ER 图或关系描述
            - 数据示例
            """

            response = self._run_agent_task("Architect", "architect.md", prompt)
            output_path = os.path.join(self.paths["docs_specs"], "data-models.md")
            self._write_file(output_path, response)

            self._log_phase(7.1, "生成数据模型", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(7.1, "生成数据模型", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 8: 质量检查循环 ─────────────────────────
    def phase_8_1_quality_checklist(self):
        """
        PHASE 8.1: 智能质量评审循环 (LLM-based)

        - 负责人: QA / 架构师
        - 输入: 所有产出文档、对应的检查清单
        - 输出: 修订后的最终产物 (*-final.md)
        """
        print("\n" + "="*70)
        print("🧐 PHASE 8.1: 智能质量评审")
        print("="*70)

        try:
            # 定义评审项目：名称, 原文档路径, 检查清单路径, 执行角色
            review_configs = [
                ("系统架构", 
                 os.path.join(self.paths["docs_both_specs"], "architecture.md"), 
                 os.path.join(self.paths["checklists"], "architecture-checklist.md"), 
                 "Architect"),
                ("前端架构", 
                 os.path.join(self.paths["docs_codespecs"], "front-end-architecture.md"), 
                 os.path.join(self.paths["checklists"], "frontend-architecture-checklist.md"), 
                 "DesignArchitect"),
                ("API 参考", 
                 os.path.join(self.paths["docs_codespecs"], "api-reference.md"), 
                 os.path.join(self.paths["checklists"], "api-checklist.md"), 
                 "Architect"),
                ("数据模型", 
                 os.path.join(self.paths["docs_codespecs"], "data-models.md"), 
                 os.path.join(self.paths["checklists"], "data-model-checklist.md"), 
                 "Architect"),
            ]

            print("  📋 执行深度评审：")
            for name, path, checklist_path, role in review_configs:
                if os.path.exists(path):
                    print(f"    🔍 正在评审: {name} (执行者: {role})")
                    content = self._read_file(path)
                    
                    # 尝试加载清单，如果不存在则使用通用评审指令
                    checklist = self._read_file(checklist_path) if os.path.exists(checklist_path) else "由专家进行一般性质量审核。"
                    
                    prompt = f"""
                    任务: 请作为 {role} 专家，对照以下检查清单评审产出文档。
                    
                    检查清单:
                    {checklist}
                    
                    文档内容:
                    {content[:5000]}
                    
                    指令:
                    1. 逐项检查文档是否满足清单要求。
                    2. 如果发现不足，请在文档中进行补充或修正。
                    3. 直接返回改进后的【完整】文档内容（Markdown）。
                    """
                    
                    persona_file = f"{role.lower()}.md"
                    if role == "DesignArchitect": persona_file = "design-architect.md"
                    
                    improved_content = self._run_agent_task(role, persona_file, prompt)
                    
                    # 保存改进后的新文件
                    output_path = path.replace(".md", "-final.md").replace(".json", "-final.md")
                    self._write_file(output_path, improved_content)
                else:
                    print(f"    ⚠️ {name} 文档未找到: {path}")

            self._log_phase(8.1, "智能评审循环", "SUCCESS", "所有可用产物已完成评审并生成 final 版本")
            return True
        except Exception as e:
            self._log_phase(8.1, "智能评审循环", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 9: 渲染与发布 ─────────────────────────
    def phase_9_rendering_and_publishing(self):
        """
        PHASE 9: 渲染与发布 - 通过本地脚本执行

        此步骤执行 `python-bash` 目录下的 Python 脚本，
        将 JSON 文件转换为人类可读的 Markdown 文档。
        """
        print("\n" + "="*70)
        print("🚀 PHASE 9: 渲染与发布")
        print("="*70)

        try:
            scripts = [
                ("project-brief.py", "项目简报"),
                ("prd.py", "产品需求文档"),
                ("user-story.py", "用户故事"),
            ]

            success_count = 0
            for script_name, label in scripts:
                script_path = os.path.join(self.paths["scripts"], script_name)
                if os.path.exists(script_path):
                    print(f"  ▶️  正在运行 {script_name} ({label})...")
                    try:
                        subprocess.run(
                            [sys.executable, script_path],
                            check=True,
                            cwd=self.paths["scripts"],
                            capture_output=True, 
                            text=True,
                            timeout=120
                        )
                        print(f"  ✅ {label} 已成功渲染。")
                        success_count += 1
                    except subprocess.CalledProcessError as e:
                        print(f"  ❌ 渲染 {label} 失败: {e.stderr}")
                    except subprocess.TimeoutExpired:
                        print(f"  ⏱️ 渲染 {label} 超时")
                else:
                    print(f"  ⚠️ 渲染脚本未找到: {script_path}")

            self._log_phase(9, "渲染与发布", "SUCCESS", f"成功渲染 {success_count}/{len(scripts)} 个文档")
            return True
        except Exception as e:
            self._log_phase(9, "渲染与发布", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 10: 智能体协作协议 ─────────────────────────
    def phase_10_agent_collaboration_protocol(self):
        """
        PHASE 10: 智能体协作协议

        在此阶段，系统会记录智能体之间的协作关系和信息传递协议。
        本阶段为该阶段的文档化记录。
        """
        print("\n" + "="*70)
        print("🤝 PHASE 10: 智能体协作协议")
        print("="*70)

        try:
            # 生成协作协议文档（可选）
            collaboration_doc = """
# 智能体协作协议

## 核心交互模型
智能体协作遵循"文档即协议 (Document as Protocol)"原则。
所有交互通过结构化数据进行，并记录在 Session 中。

## 协作角色
- Analyst: 分析师 - 负责项目简报
- PM: 产品经理 - 负责 PRD 生成
- PO: 产品负责人 - 负责用户故事策划
- Architect: 系统架构师 - 负责系统架构设计
- DesignArchitect: 前端/设计架构师 - 负责前端架构和设计
- QA: 质量保证 - 负责质量检查

## 信息流
1. 需求输入 → Analyst → 项目简报
2. 项目简报 → PM → PRD
3. PRD → PO → 用户故事
4. PRD + 故事 → Architect → 系统架构
5. PRD → DesignArchitect → 前端架构
6. 架构 → QA → 质量检查
7. 所有产物 → 渲染脚本 → Markdown 输出
            """

            output_path = os.path.join(self.paths["docs_both_specs"], "agent-collaboration-protocol.md")
            self._write_file(output_path, collaboration_doc)

            self._log_phase(10, "智能体协作协议", "SUCCESS", f"已保存至 {output_path}")
            return output_path
        except Exception as e:
            self._log_phase(10, "智能体协作协议", "FAILED", str(e))
            raise

    # ─────────────────────── PHASE 11: 动态沟通与问题解决 ─────────────────────────
    def phase_11_dynamic_session(self, topic="技术方案可行性讨论"):
        """
        PHASE 11: 智能体动态沟通与问题解决机制

        在此阶段，系统模拟多个智能体针对关键决策点进行多轮对话协商。
        目标是在遇到不确定性时，通过对话达成一致结论。
        """
        print("\n" + "="*70)
        print("💬 PHASE 11: 动态沟通与问题解决机制 (Clarification Loop)")
        print("="*70)

        try:
            session_history = []
            participants = ["PM", "Architect"]
            current_query = f"针对当前的主题——'{topic}'，请 PM 启动讨论，说明核心待决策点。"
            
            print(f"  📌 主题: {topic}")
            
            for round_num in range(1, 4):  # 最多执行 3 轮交互轮次 (PM <-> Architect)
                print(f"\n  ══ 轮次 {round_num} ══")
                
                # 1. PM 提出需求或要求澄清
                pm_req = f"历史背景:\n{json.dumps(session_history, ensure_ascii=False)}\n\n当前上下文/指令: {current_query if round_num == 1 else '根据架构师意见进行决策或追问。'}"
                pm_res = self._run_agent_task("PM", "pm.md", pm_req)
                session_history.append({"round": round_num, "sender": "PM", "content": pm_res})
                
                # 2. Architect 分析并回复
                arch_req = f"全局上下文:\n{self.global_context[:1000]}\n\nPM 的指示:\n{pm_res}\n\n历史对话:\n{json.dumps(session_history, ensure_ascii=False)}"
                arch_res = self._run_agent_task("Architect", "architect.md", arch_req)
                session_history.append({"round": round_num, "sender": "Architect", "content": arch_res})
                
                # 检查是否达成最终共识
                if "CONCLUDED" in arch_res.upper() or "CONCLUDED" in pm_res.upper():
                    print("  🤝 智能体已达成共识，会话结束。")
                    break
                
                current_query = "上文的架构分析是否能完全闭环？如果有疑问请继续讨论。"

            # 持久化会话记录
            session_file = os.path.join(self.paths["sessions"], f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            self._write_file(session_file, json.dumps({"topic": topic, "messages": session_history}, ensure_ascii=False, indent=2))
            
            # 同时更新 Session 索引
            self._update_session_index(topic, session_file)

            self._log_phase(11, "动态会话循环", "SUCCESS", f"完成了 {len(session_history)//2} 轮高质量对话")
            return session_file
        except Exception as e:
            self._log_phase(11, "动态会话循环", "FAILED", str(e))
            raise

    def _update_session_index(self, topic, path):
        """更新 Session 索引文件。"""
        index_path = os.path.join(self.paths["sessions"], "session_index.json")
        index = {"sessions": []}
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f: index = json.load(f)
        
        index["sessions"].append({
            "id": f"sess-{datetime.now().strftime('%H%M%S')}",
            "topic": topic,
            "path": path,
            "timestamp": datetime.now().isoformat()
        })
        
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    # ════════════════════════════════════════════════════════════════════════
    # 工作流执行器 (Workflow Orchestrators)
    # ════════════════════════════════════════════════════════════════════════

    def run_all(self):
        """
        按顺序执行完整的工作流（Phase 0 到 Phase 11）。
        """
        print("\n" + "="*70)
        print("🚀 开始执行完整的多智能体工作流 (Phase 0 ~ Phase 11)")
        print("="*70)

        try:
            # PHASE 0: 加载通用上下文
            self.phase_0_load_context()

            # PHASE 1: 项目简报生成
            self.phase_1_1_generate_project_brief()
            self.phase_1_2_validate_project_brief()

            # PHASE 2: PRD 生成
            self.phase_2_1_generate_prd()
            self.phase_2_2_validate_prd()

            # PHASE 3: 用户故事策划
            self.phase_3_1_generate_stories()
            self.phase_3_2_invest_check_stories()

            # PHASE 4: 系统架构设计
            self.phase_4_1_generate_architecture()
            self.phase_4_2_architecture_checklist()
            
            # NEW: PHASE 4.3: UV/UX 设计
            self.phase_4_3_uv_ux_design()

            # PHASE 5: 前端架构设计
            self.phase_5_1_generate_frontend_architecture()
            self.phase_5_2_render_frontend_architecture()
            self.phase_5_3_frontend_architecture_checklist()

            # PHASE 6: API 参考整理
            self.phase_6_1_generate_api_reference()

            # PHASE 7: 数据模型设计
            self.phase_7_1_generate_data_models()

            # PHASE 8: 质量检查循环
            self.phase_8_1_quality_checklist()

            # PHASE 9: 渲染与发布
            self.phase_9_rendering_and_publishing()

            # PHASE 10: 智能体协作协议
            self.phase_10_agent_collaboration_protocol()

            # PHASE 11: 动态沟通与问题解决
            self.phase_11_dynamic_session()

            # 输出执行日志
            self._print_execution_log()

            print("\n" + "="*70)
            print("✅ 恭喜！完整工作流已成功完成！")
            print("="*70)

        except Exception as e:
            print(f"\n❌ 工作流执行失败: {str(e)}")
            import traceback
            traceback.print_exc()
            self._print_execution_log()

    def run_phase_range(self, start_phase: int, end_phase: int):
        """
        执行指定范围内的 Phase。

        Args:
            start_phase (int): 起始阶段
            end_phase (int): 结束阶段
        """
        print(f"\n🚀 执行工作流 Phase {start_phase} ~ Phase {end_phase}")

        phase_methods = {
            0: self.phase_0_load_context,
            1.1: self.phase_1_1_generate_project_brief,
            1.2: self.phase_1_2_validate_project_brief,
            2.1: self.phase_2_1_generate_prd,
            2.2: self.phase_2_2_validate_prd,
            3.1: self.phase_3_1_generate_stories,
            3.2: self.phase_3_2_invest_check_stories,
            4.1: self.phase_4_1_generate_architecture,
            4.2: self.phase_4_2_architecture_checklist,
            4.3: self.phase_4_3_uv_ux_design,
            5.1: self.phase_5_1_generate_frontend_architecture,
            5.2: self.phase_5_2_render_frontend_architecture,
            5.3: self.phase_5_3_frontend_architecture_checklist,
            6.1: self.phase_6_1_generate_api_reference,
            7.1: self.phase_7_1_generate_data_models,
            8.1: self.phase_8_1_quality_checklist,
            9: self.phase_9_rendering_and_publishing,
            10: self.phase_10_agent_collaboration_protocol,
            11: self.phase_11_dynamic_session,
        }

        try:
            for phase, method in sorted(phase_methods.items()):
                if start_phase <= phase <= end_phase:
                    method()
            self._print_execution_log()
        except Exception as e:
            print(f"\n❌ 执行失败: {str(e)}")
            self._print_execution_log()

    def _print_execution_log(self):
        """打印执行日志摘要。"""
        print("\n" + "="*70)
        print("📊 执行日志摘要")
        print("="*70)
        for entry in self.execution_log:
            status_icon = "✅" if entry["status"] == "SUCCESS" else "❌"
            print(f"{status_icon} [{entry['phase']}] {entry['name']}: {entry['status']}")
        print("="*70)


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                      第 4 部分：运行模式与入口点                           ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def run_test_mode():
    """**测试模式**: 验证框架配置和 API 连接。"""
    print("\n🧪 正在运行测试模式...")
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        manager = WorkflowManager(project_root)
        print("✓ LLM 配置已加载。")
        print("✓ AutoGen 导入成功。")
        print("✓ 环境加载完毕。")
        print("\n✅ 所有测试通过！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def run_interactive_mode():
    """**交互模式**: 启动一个与通用 AI 助手的聊天会话。"""
    print("\n🤖 正在运行交互模式...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = WorkflowManager(project_root)
    
    agent = AssistantAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant.",
        llm_config=manager.llm_config
    )
    
    user = UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        code_execution_config=False,
    )
    
    print("\n对话开始... (输入 'exit' 或 'quit' 退出)")
    user.initiate_chat(agent, message="你好！我已准备就绪。")

def run_workflow_mode():
    """**工作流模式**: 显示菜单让用户选择执行的工作流步骤。"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = WorkflowManager(project_root)
    
    while True:
        print("\n" + "="*50)
        print("   选择要执行的工作流阶段 (基于 agent-api-workflows.md)")
        print("="*50)
        print("  0️⃣  执行完整工作流 (Phase 0 ~ 11)")
        print("  1️⃣  PHASE 1: 项目简报生成")
        print("  2️⃣  PHASE 2: PRD 生成")
        print("  3️⃣  PHASE 3: 用户故事策划")
        print("  4️⃣  PHASE 4: 系统架构设计")
        print("  5️⃣  PHASE 5: 前端架构设计")
        print("  6️⃣  PHASE 6: API 参考整理")
        print("  7️⃣  PHASE 7: 数据模型设计")
        print("  8️⃣  PHASE 8: 质量检查循环")
        print("  9️⃣  PHASE 9: 渲染与发布")
        print(" 10️⃣  PHASE 10: 智能体协作协议")
        print(" 11️⃣  PHASE 11: 动态沟通机制")
        print("  99️⃣  退出")
        
        choice = input("\n请输入选项: ").strip()
        
        try:
            if choice == "0": manager.run_all()
            elif choice == "1": manager.phase_1_1_generate_project_brief(); manager.phase_1_2_validate_project_brief()
            elif choice == "2": manager.phase_2_1_generate_prd(); manager.phase_2_2_validate_prd()
            elif choice == "3": manager.phase_3_1_generate_stories(); manager.phase_3_2_invest_check_stories()
            elif choice == "4": manager.phase_4_1_generate_architecture(); manager.phase_4_2_architecture_checklist()
            elif choice == "5": manager.phase_5_1_generate_frontend_architecture(); manager.phase_5_2_render_frontend_architecture(); manager.phase_5_3_frontend_architecture_checklist()
            elif choice == "6": manager.phase_6_1_generate_api_reference()
            elif choice == "7": manager.phase_7_1_generate_data_models()
            elif choice == "8": manager.phase_8_1_quality_checklist()
            elif choice == "9": manager.phase_9_rendering_and_publishing()
            elif choice == "10": manager.phase_10_agent_collaboration_protocol()
            elif choice == "11": manager.phase_11_dynamic_session()
            elif choice == "99": print("👋 再见！"); break
            else: print("❌ 无效选项，请重试。")
        except Exception as e:
            print(f"❌ 执行出错: {e}")

def main():
    """主函数，根据 `RUN_MODE` 环境变量决定程序的行为。"""
    run_mode = os.getenv("RUN_MODE", "workflow").lower()
    
    if run_mode == "test":
        run_test_mode()
    elif run_mode == "interactive":
        run_interactive_mode()
    elif run_mode == "full":
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        manager = WorkflowManager(project_root)
        manager.run_all()
    elif run_mode == "workflow":
        run_workflow_mode()
    else:
        print(f"❌ 未知的运行模式: '{run_mode}'。将默认使用 'workflow' 模式。")
        run_workflow_mode()

if __name__ == "__main__":
    main()
