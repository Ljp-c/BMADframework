# 多智能体系统指南 (Multi-Agent System Guide)

本指南旨在帮助您将现有的提示词工程转化为可执行的多智能体系统。

## 为什么选择 CrewAI？

经过分析您的项目结构 (`project/.bmad/personas` 和 `project/.bmad/tasks`)，我们推荐使用 **CrewAI** 框架。

- **Personas (角色) -> Agents**: 您的 `pm.md`, `dev.md` 等文件直接对应 CrewAI 中的 `Agent` 概念（包含 Role, Goal, Backstory）。
- **Tasks (任务) -> Tasks**: 您的 `create-prd.md`, `create-architecture.md` 等文件直接对应 CrewAI 中的 `Task` 概念（包含 Description, Expected Output）。
- **Checklists (检查清单) -> Quality Assurance**: 可以作为 Task 的一部分，或者由专门的 QA Agent 执行。

## 快速开始

### 1. 环境准备

确保您已安装 Python 3.10+。

```bash
cd agent_framework
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env` 并填入您的 OpenAI API Key。

```bash
cp .env.example .env
# 编辑 .env 文件
# OPENAI_API_KEY=sk-...
```

### 3. 运行示例

我们提供了一个示例脚本 `main.py`，它演示了如何加载 Product Manager 角色并执行 Create PRD 任务。

```bash
python main.py
```

## 代码结构

- `agent_framework/`
  - `loader.py`: 负责解析 Markdown 文件，提取 Role, Goal, Description 等信息。
  - `main.py`: 主程序，组装 Agent 和 Task，并启动 Crew。
  - `requirements.txt`: 依赖列表。

## 如何扩展？

要添加更多智能体协作（例如 PM -> Architect -> Developer），您可以修改 `main.py`：

```python
# 1. 加载更多角色
architect_agent = create_agent_from_markdown('.../architect.md')
dev_agent = create_agent_from_markdown('.../dev.md')

# 2. 定义更多任务
arch_task = create_task_from_markdown('.../create-architecture.md', architect_agent)
code_task = create_task_from_markdown('.../create-next-story.md', dev_agent)

# 3. 组装 Crew
crew = Crew(
    agents=[pm_agent, architect_agent, dev_agent],
    tasks=[prd_task, arch_task, code_task],
    process=Process.sequential # 顺序执行
)
```

## 其他框架推荐

除了 CrewAI，以下框架也值得考虑：

1.  **LangGraph**: 如果您需要非常复杂的循环逻辑（例如：代码编写 -> 测试失败 -> 自动修复 -> 再测试），LangGraph 提供了更底层的控制能力。
2.  **AutoGen**: 如果您更关注“对话式”的协作，即 Agent 之间通过自由对话来解决问题，而不是严格的任务流，AutoGen 是一个不错的选择。
3.  **MetaGPT**: 如果您的目标是生成整个软件项目，MetaGPT 预置了标准的软件开发 SOP（标准作业程序），可能比自己从头搭建更快。

但考虑到您已经有了非常详细的 Markdown 定义，**CrewAI** 是目前最直接、最轻量级的集成方案。
