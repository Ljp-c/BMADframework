# BMADframework 详细使用指南

> **BMAD** = Business Model Analysis & Design（商业模型分析与设计）

本文档详细说明如何使用 BMADframework 进行 AI 驱动的代码自动生成和文档创建。

---

## 📌 目录

1. [核心概念](#核心概念)
2. [快速开始](#快速开始)
3. [项目结构详解](#项目结构详解)
4. [工作流程](#工作流程)
5. [实战教程：从零到一创建项目](#实战教程从零到一创建项目)
6. [配置详解](#配置详解)
7. [常见问题](#常见问题)
8. [高级用法](#高级用法)

---

## 核心概念

### 什么是 BMADframework？

BMADframework 是一个多智能体（Multi-Agent）系统框架，它使用 AI 自动化整个软件项目的生命周期：

```
业务分析 → PRD编写 → 架构设计 → 前端设计 → 用户故事 → 代码编写 → 质量保证
   ⬇️        ⬇️        ⬇️        ⬇️        ⬇️        ⬇️        ⬇️
  分析师    产品经理   系统架构   前端架构   产品负责人  开发工程师   QA专家
```

### 三大核心组件

#### 1️⃣ **Personas（角色）**
每个角色代表一个 AI 智能体，具有独特的专业知识、目标和工作风格。例如：
- **产品经理** (PM): 专注于编写 PRD 和定义产品特性
- **系统架构师** (Architect): 设计系统架构、技术栈、数据模型
- **开发工程师** (Developer): 根据文档生成可执行代码

**位置**: `project/.bmad/personas/*.md`

#### 2️⃣ **Tasks（任务）**
每个任务定义了特定角色要完成的工作，包括：
- 任务描述（要做什么）
- 预期输出（应该输出什么）
- 输入依赖（需要什么前置信息）

**位置**: `project/.bmad/tasks/*.md`

#### 3️⃣ **Architecture（架构配置）**
JSON 配置文件定义了：
- 所有智能体和它们的能力
- 工作流程（7 个阶段）
- 阶段之间的数据流动

**位置**: `agent_framework/agent_architecture.json`

---

## 快速开始

### 前置要求

- Python 3.10+
- 有效的 LLM API Key（OpenAI、DeepSeek、Kimi 等）
- 网络连接

### 5 分钟快速启动

#### 1️⃣ 环境安装

```powershell
cd e:\BMADframework\agent_framework
pip install -r requirements.txt
```

#### 2️⃣ 配置 API

复制示例文件：
```powershell
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API Key：

**选项 A：使用 OpenAI**
```ini
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL_NAME=gpt-4-turbo
```

**选项 B：使用国内模型（推荐，便宜且快速）**

DeepSeek 示例：
```ini
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL_NAME=deepseek-chat
```

Kimi 示例：
```ini
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_BASE=https://api.moonshot.cn/v1
OPENAI_MODEL_NAME=moonshot-v1-8k
```

#### 3️⃣ 测试连接

```powershell
python test_connection.py
```

如果看到模型响应，说明配置成功 ✅

#### 4️⃣ 查看架构（无需 API）

```powershell
$env:RUN_MODE = "architecture"
python main.py
```

输出应该显示所有 agents 和 phases：
```
Architecture Summary
Agents: 7
Phases: 7
- phase-1: Project Brief -> analyst
- phase-2: PRD -> pm
- phase-3: System Architecture -> architect
- phase-4: Front-end Architecture -> design-architect
- phase-5: Stories -> po
- phase-6: Implementation -> dev
- phase-7: Quality Assurance -> qa
```

---

## 项目结构详解

```
BMADframework/
├── agent_framework/                    # AI 智能体框架（核心）
│   ├── main.py                        # 主程序入口 - 启动多智能体协作
│   ├── loader.py                      # Markdown 解析器 - 加载角色和任务
│   ├── agent_architecture.json        # 架构配置 - 定义工作流程
│   ├── requirements.txt               # Python 依赖
│   ├── .env                          # 环境配置（请勿提交到 Git）
│   ├── .env.example                  # 环境配置模板
│   ├── test_connection.py            # 测试 LLM 连接
│   └── test_crewai_minimal.py        # CrewAI 最小测试
│
├── project/
│   ├── .bmad/                         # BMAD 配置目录（需要创建）
│   │   ├── personas/                 # AI 角色定义文件
│   │   │   ├── analyst.md           # 业务分析师角色
│   │   │   ├── pm.md                # 产品经理角色
│   │   │   ├── architect.md         # 系统架构师角色
│   │   │   ├── design-architect.md  # 前端架构师角色
│   │   │   ├── po.md                # 产品负责人角色
│   │   │   ├── dev.md               # 开发工程师角色
│   │   │   └── qa.md                # QA 专家角色
│   │   │
│   │   ├── tasks/                    # AI 任务定义文件
│   │   │   ├── create-project-brief.md
│   │   │   ├── create-prd.md
│   │   │   ├── create-architecture.md
│   │   │   ├── create-front-end-architecture.md
│   │   │   ├── create-next-story.md
│   │   │   └── (其他任务文件)
│   │   │
│   │   └── checklists/               # 质量检查清单
│   │       ├── prd-checklist.md
│   │       ├── architecture-checklist.md
│   │       ├── frontend-architecture-checklist.md
│   │       └── story-ready-checklist.md
│   │
│   ├── docs/                         # 📄 输出的文档目录
│   │   ├── project-brief.md         # 项目简报（AI 生成）
│   │   ├── prd.md                   # 产品需求文档（AI 生成）
│   │   ├── architecture.md          # 系统架构文档（AI 生成）
│   │   ├── tech-stack.md            # 技术栈文档（AI 生成）
│   │   ├── api-reference.md         # API 参考（AI 生成）
│   │   ├── data-models.md           # 数据模型（AI 生成）
│   │   ├── environment.md           # 环境配置（AI 生成）
│   │   ├── front-end-architecture.md # 前端架构（AI 生成）
│   │   ├── component-specs.md       # 组件规范（AI 生成）
│   │   └── stories/                 # 用户故事（AI 生成）
│   │       ├── epic-1/
│   │       │   ├── story-1.1.md
│   │       │   ├── story-1.2.md
│   │       │   └── story-1.3.md
│   │       └── epic-2/
│   │           ├── story-2.1.md
│   │           └── story-2.2.md
│   │
│   └── src/                         # 💻 输出的源代码目录（当前为空）
│
├── README_AGENTS.md                 # 多智能体系统指南
├── README_MODELS.md                 # 模型配置指南
└── USAGE_GUIDE_CN.md               # 本文档
```

### 重要说明

- **需要创建的目录**: `project/.bmad/` 及其所有子目录
- **输出会覆盖**: `project/docs/` 和 `project/src/` 中的文件
- **模板文件**: 在 `project/docs/` 中已有空的模板文件可参考

---

## 工作流程

### 7 个阶段详解

#### Phase 1: 项目简报 (Project Brief)
- **负责人**: 分析师 (analyst)
- **输入**: 用户提供的项目背景
- **输出**: `project/docs/project-brief.md`
- **目的**: 理解业务需求、市场背景、问题陈述

#### Phase 2: PRD (产品需求文档)
- **负责人**: 产品经理 (pm)
- **输入**: 项目简报
- **输出**: `project/docs/prd.md`
- **目的**: 定义产品功能、用户需求、验收标准

#### Phase 3: 系统架构
- **负责人**: 系统架构师 (architect)
- **输入**: PRD
- **输出**: 
  - `architecture.md` (整体架构)
  - `tech-stack.md` (技术选型)
  - `data-models.md` (数据模型)
  - `api-reference.md` (API 设计)
  - `environment.md` (部署环境)
- **目的**: 设计技术方案、技术栈、系统分层

#### Phase 4: 前端架构
- **负责人**: 前端架构师 (design-architect)
- **输入**: PRD、系统架构
- **输出**:
  - `front-end-architecture.md` (前端架构)
  - `component-specs.md` (组件规范)
- **目的**: 设计 UI/UX、组件库、前端路由

#### Phase 5: 用户故事 (Stories)
- **负责人**: 产品负责人 (po)
- **输入**: PRD、系统架构、前端架构
- **输出**: 多个 story 文件
- **目的**: 将功能分解为可执行的用户故事

#### Phase 6: 代码实现
- **负责人**: 开发工程师 (dev)
- **输入**: 所有用户故事
- **输出**: `project/src/` (源代码)
- **目的**: 根据故事生成可执行的代码

#### Phase 7: 质量保证
- **负责人**: QA 专家 (qa)
- **输入**: 源代码、所有文档
- **输出**: 测试报告和改进建议
- **目的**: 验证代码质量、文档完整性

---

## 实战教程：从零到一创建项目

本教程以创建"AI 代码助手工具"为例。

### 第一步：准备项目基础目录

创建必要的目录结构：

```powershell
# 进入项目目录
cd e:\BMADframework\project

# 创建 .bmad 目录结构
mkdir -p .bmad\personas
mkdir -p .bmad\tasks
mkdir -p .bmad\checklists
```

### 第二步：定义角色（Personas）

在 `project/.bmad/personas/` 目录下创建角色文件。

#### 2.1 创建产品经理角色 `pm.md`

```markdown
# 产品经理 (Product Manager)

## 角色定义

您是一位经验丰富的产品经理，具有 5+ 年的 B2B SaaS 产品管理经验。

## 主要职责

- 将业务需求转化为清晰的产品需求
- 定义产品功能、优先级和验收标准
- 与所有利益相关者沟通协作
- 编写专业的 PRD 文档

## 专业知识

- 产品设计最佳实践
- 用户研究和需求分析
- 竞品分析
- 项目管理方法论（Agile/Scrum）

## 工作风格

- 数据驱动的决策制定
- 用户中心的设计思维
- 清晰的文档和沟通
```

#### 2.2 创建系统架构师角色 `architect.md`

```markdown
# 系统架构师 (System Architect)

## 角色定义

您是一位资深系统架构师，具有 10+ 年的分布式系统设计经验。

## 主要职责

- 根据 PRD 设计完整的系统架构
- 选择合适的技术栈
- 设计数据模型和 API 规范
- 考虑可扩展性、安全性、性能

## 专业知识

- 云计算平台（AWS/Azure/GCP）
- 微服务架构
- 数据库设计（SQL/NoSQL）
- API 设计最佳实践
- 系统安全和合规

## 工作风格

- 架构决策要基于权衡（Trade-offs）
- 考虑长期可维护性和扩展性
- 清晰的文档和图表说明
```

#### 2.3 创建开发工程师角色 `dev.md`

```markdown
# 全栈开发工程师 (Full-stack Developer)

## 角色定义

您是一位高级全栈开发工程师，精通现代 Web 开发技术栈。

## 主要职责

- 根据架构设计实现代码
- 编写高质量、可维护的代码
- 确保代码符合最佳实践
- 实现单元测试和集成测试

## 技术栈

- 后端: Python (FastAPI/Django)、Node.js
- 前端: React、Vue、TypeScript
- 数据库: PostgreSQL、MongoDB
- 容器化: Docker、Kubernetes
- CI/CD: GitHub Actions、GitLab CI

## 工作风格

- 代码优先遵循 SOLID 原则
- 100% 代码覆盖率测试
- 详细的代码注释和文档
```

### 第三步：定义任务（Tasks）

在 `project/.bmad/tasks/` 目录下创建任务文件。

#### 3.1 创建 PRD 任务 `create-prd.md`

```markdown
# 任务：编写产品需求文档 (PRD)

## 任务描述

基于项目简报，您需要编写一份专业的产品需求文档 (PRD)。该文档应包含：

1. **产品概述**
   - 产品愿景
   - 目标用户
   - 市场定位

2. **功能需求**
   - 核心功能列表（优先级排序）
   - 每个功能的详细描述和用例

3. **非功能需求**
   - 性能要求（响应时间、吞吐量等）
   - 安全要求（认证、授权、加密）
   - 可用性要求（99.9% 正常运行时间）
   - 可扩展性需求

4. **用户界面需求**
   - 主要界面流程
   - 用户交互设计

5. **验收标准**
   - 明确的测试用例
   - 性能基准

## 输出要求

生成的 PRD 应该：
- 使用 Markdown 格式
- 包含详细的表格和列表
- 清晰的层级结构
- 专业且易于理解

## 质量标准

- 功能完整性：100%
- 文档清晰度：易于理解
- 验收标准：可量化
```

#### 3.2 创建架构任务 `create-architecture.md`

```markdown
# 任务：设计系统架构

## 任务描述

基于 PRD，设计完整的系统架构。包括：

1. **系统架构图**
   - 总体架构（分层设计）
   - 组件关系
   - 数据流

2. **技术栈选择**
   - 后端框架和版本
   - 前端框架和版本
   - 数据库选择（主从关系）
   - 消息队列
   - 缓存方案

3. **数据模型**
   - Entity Relationship Diagram (ERD)
   - 主要数据实体定义
   - 关键字段说明

4. **API 设计**
   - RESTful API 规范
   - 常见接口示例
   - 错误处理

5. **部署架构**
   - 开发环境配置
   - 生产环境配置
   - 高可用方案

## 输出要求

- 架构文档使用 Markdown 格式
- 包含清晰的架构图表
- 技术决策要有理由说明

## 质量标准

- 架构完整性和合理性
- 文档清晰度
- 考虑到可扩展性和维护性
```

### 第四步：配置架构 JSON

编辑 `agent_framework/agent_architecture.json`（已预配置，通常不需要修改）。

关键字段说明：
- `agents`: 定义所有 AI 智能体
- `phases`: 定义工作流程的 7 个阶段
- `handoffs`: 定义阶段之间的数据交接

### 第五步：运行框架

#### 方式 1：直接模式（快速测试）

```powershell
cd e:\BMADframework\agent_framework
python main.py
```

这会执行 `run_direct()` 函数，直接调用产品经理角色生成 PRD。

#### 方式 2：CrewAI 模式（完整流程）

```powershell
cd e:\BMADframework\agent_framework
$env:RUN_MODE = "crewai"
python main.py
```

这会执行完整的 7 个阶段（如果已定义所有必要文件）。

#### 方式 3：仅验证架构（无需 API）

```powershell
cd e:\BMADframework\agent_framework
$env:RUN_MODE = "architecture"
python main.py
```

输出将显示所有 agents 和 phases，以及缺失的文件。

### 第六步：检查输出

运行完成后，检查生成的文档：

```powershell
# 查看生成的 PRD
Get-Content e:\BMADframework\project\docs\prd.md

# 查看生成的架构
Get-Content e:\BMADframework\project\docs\architecture.md

# 列出生成的代码（如果有）
Get-ChildItem e:\BMADframework\project\src\
```

### 第七步：迭代和优化

根据输出结果，您可以：

1. **调整角色定义**: 修改 `personas/*.md` 文件，改进 AI 的行为
2. **优化任务描述**: 修改 `tasks/*.md` 文件，提供更清晰的要求
3. **手动编辑输出**: 手动修改生成的文档和代码
4. **添加约束条件**: 在任务中添加特定的技术要求或设计模式

---

## 配置详解

### .env 环境变量

#### 必需变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `OPENAI_API_KEY` | LLM API Key | `sk-xxxxx` |

#### 可选变量

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `OPENAI_API_BASE` | API Base URL | OpenAI | `https://api.deepseek.com` |
| `OPENAI_MODEL_NAME` | 模型名称 | `gpt-4-turbo` | `deepseek-chat` |
| `OPENAI_PROXY` | 代理 URL | 无 | `http://127.0.0.1:7890` |
| `RUN_MODE` | 运行模式 | `direct` | `crewai`, `architecture` |
| `START_PHASE` | 起始阶段 | 无 | `phase-2` |
| `END_PHASE` | 结束阶段 | 无 | `phase-5` |

#### 示例 .env 文件

```ini
# 基础配置
OPENAI_API_KEY=sk-xxxxx

# 使用 DeepSeek（推荐，便宜且快速）
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL_NAME=deepseek-chat

# 或使用 Kimi
# OPENAI_API_BASE=https://api.moonshot.cn/v1
# OPENAI_MODEL_NAME=moonshot-v1-8k

# 如果需要代理
# OPENAI_PROXY=http://127.0.0.1:7890

# 仅运行特定阶段（可选）
# START_PHASE=phase-3
# END_PHASE=phase-5
```

### agent_architecture.json 详解

#### 1. Agents 部分

```json
{
  "id": "pm",                         // 唯一标识
  "name": "Product Manager",          // 显示名称
  "persona_file": "project/.bmad/personas/pm.md",  // 角色文件路径
  "primary_outputs": [                // 该角色的主要输出
    "project/docs/prd.md"
  ]
}
```

#### 2. Phases 部分

```json
{
  "id": "phase-2",                    // 唯一标识
  "name": "PRD",                      // 阶段名称
  "owner": "pm",                      // 负责人 agent ID
  "task_file": "project/.bmad/tasks/create-prd.md",  // 任务文件
  "inputs": [                         // 输入依赖（前置输出）
    "project/docs/project-brief.md"
  ],
  "outputs": [                        // 输出文件
    "project/docs/prd.md"
  ],
  "gates": [                          // 质量检查清单
    "project/.bmad/checklists/prd-checklist.md"
  ]
}
```

#### 3. Handoffs 部分

定义阶段之间的数据交接：

```json
{
  "from": "pm",                       // 源 agent
  "to": "architect",                  // 目标 agent
  "artifacts": [                      // 交接的文档
    "project/docs/prd.md"
  ]
}
```

---

## 常见问题

### Q1: 如何只运行特定阶段？

**答**: 使用 `START_PHASE` 和 `END_PHASE` 环境变量：

```powershell
$env:START_PHASE = "phase-3"   # 从系统架构开始
$env:END_PHASE = "phase-5"     # 到用户故事结束
$env:RUN_MODE = "crewai"
python main.py
```

### Q2: 生成的代码质量不好怎么办？

**答**: 有几个改进方向：

1. **改进开发工程师的角色定义** (`dev.md`)
   - 添加更多技术细节
   - 指定代码风格指南
   - 提供代码示例

2. **改进任务描述** (`create-next-story.md`)
   - 提供详细的实现要求
   - 指定设计模式
   - 要求添加单元测试

3. **使用更强大的模型**
   - 从 `gpt-3.5-turbo` 升级到 `gpt-4-turbo`
   - 或使用 DeepSeek R1（推理模型）

### Q3: API 连接超时怎么办？

**答**: 检查以下几点：

1. 确认 API Key 正确：
   ```powershell
   python test_connection.py
   ```

2. 如果在国内访问 OpenAI，需要配置代理：
   ```ini
   OPENAI_PROXY=http://127.0.0.1:7890
   ```

3. 增加超时时间（在 `main.py` 中修改 `timeout=120.0`）

### Q4: 如何修改生成的文档？

**答**: 您有完全的控制权：

1. 自动生成后，手动编辑 `project/docs/` 中的文件
2. 下一次运行时，这些文件会被覆盖（建议备份重要的文件）
3. 如果要保留手动修改，应该：
   - 在任务文件中指明保留部分
   - 或者将手动修改的版本重命名到不同目录

### Q5: 如何添加新的角色或阶段？

**答**: 三个步骤：

1. **创建角色文件** `project/.bmad/personas/my-role.md`
2. **创建任务文件** `project/.bmad/tasks/my-task.md`
3. **编辑架构配置** `agent_framework/agent_architecture.json`
   - 在 `agents` 数组中添加新 agent
   - 在 `phases` 数组中添加新 phase
   - 在 `handoffs` 数组中定义数据流

### Q6: 支持哪些编程语言？

**答**: 取决于您的开发工程师角色定义。默认支持：

- **后端**: Python (FastAPI/Django), Node.js (Express/NestJS), Java
- **前端**: React, Vue, Angular, TypeScript
- **全栈**: Next.js, NuxtJS

您可以在 `dev.md` 中修改支持的技术栈。

### Q7: 如何处理多轮迭代？

**答**: 推荐工作流程：

```
第1次运行: 生成初始版本
   ↓
手动审核和修改
   ↓
第2次运行: 基于修改后的文档继续生成
   ↓
迭代直到满意
```

关键是保持角色和任务文件的版本控制（使用 Git）。

---

## 高级用法

### 1. 自定义 LLM 行为

#### 修改 Temperature（创意度）

在 `loader.py` 中调整 temperature：

```python
# 0.0 = 确定性（适合代码）
# 1.0 = 创意性（适合文案）
temperature = 0.6
```

#### 使用不同的模型

在 `.env` 中配置多个模型，然后在 `main.py` 中为不同角色使用不同模型：

```python
# 编写文档使用 GPT-4
pm_llm = LLM(model="gpt-4-turbo", ...)

# 写代码使用 DeepSeek
dev_llm = LLM(model="deepseek-chat", ...)
```

### 2. 添加质量检查（Gates）

在 `agent_architecture.json` 中的 `gates` 字段定义检查清单：

```json
{
  "id": "phase-2",
  "gates": [
    "project/.bmad/checklists/prd-checklist.md"
  ]
}
```

创建检查清单文件 `prd-checklist.md`：

```markdown
# PRD 质量检查清单

## 必需内容
- [ ] 产品愿景清晰
- [ ] 目标用户明确
- [ ] 核心功能列表完整
- [ ] 非功能需求定义

## 格式要求
- [ ] 使用 Markdown 格式
- [ ] 包含表格和图表
- [ ] 无语法错误

## 可行性
- [ ] 功能可在 6 个月内完成
- [ ] 技术方案现实可行
- [ ] 资源投入估算合理
```

### 3. 并行执行阶段

修改 `main.py` 中的 `Crew` 配置：

```python
# 顺序执行（默认）
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential
)

# 并行执行（需要小心依赖关系）
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.hierarchical  # 或 Process.concurrent
)
```

### 4. 集成到 CI/CD

创建 GitHub Actions 工作流 `.github/workflows/generate-docs.yml`：

```yaml
name: Auto-generate Docs

on:
  push:
    paths:
      - 'project/.bmad/**'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: |
          cd agent_framework
          pip install -r requirements.txt
      
      - name: Generate docs
        run: |
          cd agent_framework
          RUN_MODE=crewai python main.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add project/docs/ project/src/
          git commit -m "Auto-generate docs and code"
          git push
```

### 5. 监控和日志

启用详细日志：

```python
# 在 main.py 中
import logging
logging.basicConfig(level=logging.DEBUG)

# 或在运行时
python main.py 2>&1 | tee output.log
```

---

## 最佳实践总结

### ✅ Do（应该做）

1. **定期备份**
   - 备份 `project/.bmad/` 目录
   - 备份生成的高质量文档

2. **版本控制**
   - 所有角色和任务文件使用 Git 管理
   - 标签重要版本

3. **循序渐进**
   - 先生成项目简报
   - 再生成 PRD
   - 最后才生成代码

4. **质量检查**
   - 使用 gates 定义质量标准
   - 手动审核关键文档

5. **文档维护**
   - 定期更新角色和任务定义
   - 记录优化历史

### ❌ Don't（不应该做）

1. **直接依赖 AI 输出**
   - 总是要进行人工审核
   - 特别是安全相关的代码

2. **忽视错误信息**
   - 检查 `test_connection.py` 的输出
   - 查看详细的错误日志

3. **过度定制**
   - 不要修改 `loader.py` 和 `main.py` 的核心逻辑
   - 通过角色和任务文件来调整行为

4. **混乱的文件结构**
   - 坚持 `.bmad/personas/` 和 `.bmad/tasks/` 的结构
   - 不要随意移动文件

---

## 总结

BMADframework 提供了一套完整的工具链，用于自动化软件项目的生命周期：

1. **快速启动**: 5 分钟配置，立即开始生成文档
2. **灵活扩展**: 通过角色和任务定义自定义 AI 行为
3. **质量保证**: 内置检查清单机制
4. **完整流程**: 从需求到代码的一站式解决方案
5. **易于维护**: 所有配置都是 Markdown 和 JSON 格式

**下一步**: 根据 [实战教程](#实战教程从零到一创建项目) 创建您的第一个项目！

---

## 附录：命令参考

```powershell
# 环境安装
cd e:\BMADframework\agent_framework
pip install -r requirements.txt

# 测试连接
python test_connection.py

# 查看架构
$env:RUN_MODE = "architecture"; python main.py

# 运行直接模式（快速测试）
python main.py

# 运行完整流程
$env:RUN_MODE = "crewai"; python main.py

# 运行特定阶段
$env:START_PHASE = "phase-3"; $env:END_PHASE = "phase-5"; $env:RUN_MODE = "crewai"; python main.py

# 查看生成的文档
Get-Content e:\BMADframework\project\docs\prd.md
Get-Content e:\BMADframework\project\docs\architecture.md

# 查看日志
python main.py 2>&1 | Tee-Object -FilePath output.log
```

---

**文档版本**: 1.0  
**最后更新**: 2026年2月  
**作者**: BMADframework 团队
