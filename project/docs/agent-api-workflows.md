# 智能体框架 API 调用流程与输入文件清单

## 使用方式
- 本文档列出从“项目简报 → PRD → 故事 → 架构 → 前端架构 → API → 数据模型 → 质量检查 → 渲染发布”的全流程中，每一次 API 调用应传入的文件。
- 路径均为绝对路径（Windows）。将“通用上下文”作为每次调用的系统/约束提示，Schema/模板作为结构/格式约束，上游产物作为业务输入。

---

## 0. 通用上下文（所有调用均建议注入）
- 业务与规范
  - e:\AUTOGNEN_Version\project\.bmad\data\coding-standards.md
  - e:\AUTOGNEN_Version\project\.bmad\data\glossary.md
  - e:\AUTOGNEN_Version\project\.bmad\data\tech-preferences.md
- 技术参考（按需注入）
  - e:\AUTOGNEN_Version\project\docs\code_specs\tech-stack.md
  - e:\AUTOGNEN_Version\project\docs\code_specs\environment.md
  - e:\AUTOGNEN_Version\project\docs\code_specs\api-reference.md
  - e:\AUTOGNEN_Version\project\docs\code_specs\data-models.md
  - e:\AUTOGNEN_Version\project\docs\code_specs\front-end-architecture.md
  - e:\AUTOGNEN_Version\project\docs\both_specs\architecture.md

---

## 1. 项目简报生成（Project Brief）
### 调用 1.1：生成项目简报 JSON（遵循 Schema）
- 传入文件
  - 通用上下文（第 0 节所列文件的必要子集）
  - 人物性格prosonal
  - 业务需求
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\project-brief.json
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\table_specs\project-brief.md
- 输出期望
  - 有效且完整的“项目简报 JSON”（符合 Schema 的 required/约束）

### 调用 1.2：结构校验与补全（可选）
- 传入文件
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\project-brief.json
  - 上一步生成的“项目简报 JSON”内容
- 输出期望
  - 标出缺失/不合规字段并给出补全后的 JSON

---

## 2. PRD 生成
### 调用 2.1：生成 PRD JSON（遵循 Schema）
- 传入文件
  - 通用上下文
  - 上一步“项目简报 JSON”（调用 1.1/1.2 输出）
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\prd.json
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\table_specs\prd.md
- 输出期望
  - 有效 PRD JSON（包含 step1~step6 与 appendix 的结构）

### 调用 2.2：结构校验与补全（可选）
- 传入文件
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\prd.json
  - 上一步生成的“PRD JSON”
- 输出期望
  - 标出缺失/不合规字段并给出补全后的 JSON

---

## 3. Epic/用户故事策划（Next Story）
### 调用 3.1：生成拆分策略与故事骨架 JSON
- 传入文件
  - 通用上下文
  - PRD JSON（调用 2.x 输出）
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\next-story.json
- 输出期望
  - 包含 epics、story_splitting、story_dependencies、story_priorities 等结构化 JSON

### 调用 3.2：INVEST 自检与故事细化
- 传入文件
  - 通用上下文（尤其：e:\AUTOGNEN_Version\project\.bmad\data\glossary.md 中 INVEST 定义）
  - 上一步“故事 JSON”（调用 3.1 输出）
- 输出期望
  - 完整的故事明细（user_story、acceptance_criteria、technical_notes、dependencies、test_scenarios、task_breakdown 等）并含 INVEST 自检结果

---

## 4. 系统架构设计
### 调用 4.1：生成系统架构文档草稿
- 传入文件
  - 通用上下文
  - PRD MD（调用 2.x 输出）
  - 技术/环境参考：
    - e:\AUTOGNEN_Version\project\docs\code_specs\tech-stack.md
    - e:\AUTOGNEN_Version\project\docs\code_specs\environment.md
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\both_specs\architecture.md
- 输出期望
  - 系统架构 Markdown 草稿

### 调用 4.2：质量检查与改进
- 传入文件
  - 架构草稿（调用 4.1 输出）
  - e:\AUTOGNEN_Version\project\.bmad\checklists\architecture-checklist.md
- 输出期望
  - 按检查清单提出修改建议并产出改进版草稿

---
## UV/UX设计

 - 传入文件
  - 通用上下文
  - PRD MD（调用 2.x 输出）
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\table_specs\uv-ux.md  



## 5. 前端架构设计
### 调用 5.1：生成前端架构 JSON（遵循 Schema）
- 传入文件
  - 通用上下文
  - PRD MD（调用 2.x 输出）
  - Schema：e:\AUTOGNEN_Version\project\docs\.jsons\front-end.json
  - （可选）API 参考草稿（若已完成第 6 步）：e:\AUTOGNEN_Version\project\docs\code_specs\api-reference.md
- 输出期望
  - 前端架构结构化 JSON（包含技术选型、路由、状态、API 层、性能、可访问性、标准与测试等）

### 调用 5.2：渲染前端架构文档草稿
- 传入文件
  - 上一步“前端架构 JSON”（调用 5.1 输出）
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\code_specs\front-end-architecture.md
- 输出期望
  - 前端架构 Markdown 草稿

### 调用 5.3：质量检查与改进
- 传入文件
  - 前端架构草稿（调用 5.2 输出）
  - e:\AUTOGNEN_Version\project\.bmad\checklists\frontend-architecture-checklist.md
- 输出期望
  - 按清单完善后的草稿

---

## 6. API 参考整理
### 调用 6.1：汇总并规范 API 参考
- 传入文件
  - 通用上下文
  - PRD JSON（调用 2.x 输出）
  - 用户故事 JSON（调用 3.x 输出，使用 technical_notes.api_interfaces 字段）
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\code_specs\api-reference.md
- 输出期望
  - 规范化的 API 参考草稿（端点、方法、请求/响应、错误码等）

---

## 7. 数据模型设计
### 调用 7.1：生成数据模型草稿
- 传入文件
  - 通用上下文
  - PRD JSON（调用 2.x 输出，尤其 step4.detailedDescription.dataRequirements）
  - API 参考草稿（调用 6.1 输出）
  - 模板/参考：e:\AUTOGNEN_Version\project\docs\code_specs\data-models.md
- 输出期望
  - 数据模型文档草稿（实体关系、字段定义、约束与示例）

---

## 8. 质量检查循环（收尾）
### 调用 8.1：针对各产物执行检查清单
- 传入文件（按产物选择对应清单）
  - 架构草稿 ?6?2 e:\AUTOGNEN_Version\project\.bmad\checklists\architecture-checklist.md
  - 前端架构草稿 ?6?2 e:\AUTOGNEN_Version\project\.bmad\checklists\frontend-architecture-checklist.md
  - 故事就绪度/INVEST ?6?2 e:\AUTOGNEN_Version\project\.bmad\data\glossary.md 中 INVEST 定义 + next-story JSON
- 输出期望
  - 问题清单与修订后的最终稿

---

## 9. 渲染与发布（本地脚本执行，非 API 调用）
- 项目简报渲染：
  - 脚本：e:\AUTOGNEN_Version\project\python-bash\project-brief.py
  - 输入：调用 1.x 产出的“项目简报 JSON”
  - 输出：项目简报 Markdown
- PRD 渲染：
  - 脚本：e:\AUTOGNEN_Version\project\python-bash\prd.py
  - 输入：调用 2.x 产出的“PRD JSON”
  - 输出：PRD Markdown
- 用户故事渲染：
  - 脚本：e:\AUTOGNEN_Version\project\python-bash\user-story.py
  - 输入：用户故事 JSON（建议保存为 e:\AUTOGNEN_Version\project\docs\.jsons\user_stories.json 或调整脚本 JSON_FILE 配置）
  - 输出：按模式拆分的用户故事 Markdown

---

## 10. 智能体协作协议 (Agent Collaboration Protocol)

本章节定义智能体之间如何通过结构化数据进行交互，以驱动上述 1-9 的工作流程。

### 10.1 核心交互模型

智能体协作遵循“**文档即协议 (Document as Protocol)**”原则。交互载荷（Payload）应包含上下文指针、动作指令和产物路径。

**标准交互载荷结构 (JSON)**

```json
{
  "interaction_id": "uuid-v4",
  "timestamp": "ISO8601",
  "sender": "RoleName (e.g., Analyst)",
  "receiver": "RoleName (e.g., PM)",
  "action": "DRAFT | REVIEW | REVISE | APPROVE | HANDOFF",
  "workflow_step": "1.1",
  "context": {
    "system_prompts": ["path/to/persona.md", "path/to/coding-standards.md"],
    "references": ["path/to/upstream-artifact.json"]
  },
  "payload": {
    "target_schema": "path/to/schema.json",
    "target_template": "path/to/template.md",
    "content_data": { ... } // 或者指向 "path/to/draft.json"
  },
  "comments": "自然语言描述任务意图"
}
```

### 10.2 角色协作矩阵

根据 `.bmad/personas` 定义，各阶段的协作流如下：

#### 阶段 1: 项目启动 (Brief)
- **User -> Analyst**: 提供原始需求（自然语言）。
- **Analyst (Self)**: 调用 `Step 1.1` 生成项目简报 JSON。
- **Analyst -> User**: 提交简报草稿请求确认。

#### 阶段 2: 产品定义 (PRD)
- **Analyst -> PM**: 移交项目简报 (Handoff)。
- **PM (Self)**: 调用 `Step 2.1` 生成 PRD JSON。
- **PM -> Architect**: 请求技术可行性评审 (Review)。
  - *Input*: PRD JSON
  - *Output*: Feasibility Report (Approved / Changes Requested)
- **PM -> Design Architect**: 请求 UX 评审 (Review)。

#### 阶段 3: 需求细化 (Story)
- **PM -> PO**: 移交定稿 PRD (Handoff)。
- **PO (Self)**: 调用 `Step 3.1` 生成用户故事 JSON。
- **PO -> Architect / Dev**: 请求 INVEST 与技术依赖检查 (Review)。

#### 阶段 4: 架构设计 (Architecture)
- **PM -> Architect**: 启动系统架构设计。
- **Architect (Self)**: 调用 `Step 4` 生成架构文档与数据模型。
- **PM -> Design Architect**: 启动前端架构设计。
- **Design Architect (Self)**: 调用 `Step 5` 生成前端架构。
- **Architect <-> Design Architect**: 接口契约对齐 (Sync)。

#### 阶段 5: 开发与测试 (Implementation)
- **PO -> Dev**: 分发用户故事 (Task Assignment)。
- **Architect -> Dev**: 提供技术规范与 API 定义。
- **Dev (Self)**: 编写代码。
- **Dev -> QA**: 提测 (Handoff)。
- **QA (Self)**: 基于故事生成测试用例并执行。

### 10.3 关键交互原语示例

**1. 请求起草 (Request Draft)**
*场景：PM 要求 Architect 设计架构*
```json
{
  "sender": "PM",
  "receiver": "Architect",
  "action": "DRAFT",
  "workflow_step": "4.1",
  "context": { "references": ["docs/.jsons/prd.json"] },
  "payload": { "target_schema": "docs/both_specs/architecture.md" }
}
```

**2. 提交评审 (Request Review)**
*场景：Architect 提交架构文档给 PM 和 Dev 评审*
```json
{
  "sender": "Architect",
  "receiver": "PM",
  "action": "REVIEW",
  "payload": { "content_path": "docs/both_specs/architecture.md" },
  "comments": "请确认架构是否满足所有非功能需求"
}
```

**3. 反馈意见 (Review Feedback)**
*场景：PM 反馈架构设计缺漏*
```json
{
  "sender": "PM",
  "receiver": "Architect",
  "action": "REVISE",
  "payload": {
    "status": "CHANGES_REQUESTED",
    "review_comments": [
      { "location": "Section 3.2", "issue": "未包含灾备方案" }
    ]
  }
}
```

## 11. 智能体动态沟通与问题解决机制 (Agent Dynamic Communication)

目前的 **Steps 1-9** 主要是基于“文档流转”的线性工作流（流水线模式），适合确定性任务。但在面对不确定性、复杂决策或冲突时，智能体需要脱离文档流转，进入**“动态会话模式 (Dynamic Session Mode)”**。

本章节定义智能体如何进行**非线性、即时、多轮**的沟通与协作。

### 11.1 沟通场景分类

| 场景类型 | 描述 | 参与者示例 | 触发条件 |
| :--- | :--- | :--- | :--- |
| **澄清 (Clarification)** | 针对模糊需求的提问与回答 | PM <-> Architect | 需求有歧义、技术可行性存疑 |
| **协商 (Negotiation)** | 在冲突约束下寻求平衡点 | PM <-> PO <-> Dev | 范围 vs 时间冲突、资源不足 |
| **头脑风暴 (Brainstorm)** | 开放式探索解决方案 | Design Architect <-> Architect | 架构选型、复杂交互设计 |
| **决策 (Decision Making)** | 多方投票或达成共识 | All Stakeholders | 重大变更、里程碑确认 |

### 11.2 动态会话启用场景与调用清单

当触发以下任一场景时，智能体应暂停流水线，初始化一个 Session。

#### 场景 A: 需求澄清 (Clarification)
**触发条件**: 接收方发现输入文档（如 PRD）存在歧义、缺失或逻辑矛盾。

**调用 11.A：发起澄清会话**
- 传入文件
  - 通用上下文（角色定义、编码规范）
  - 存在问题的上游产物（如 PRD JSON）
  - 相关的下游约束（如 技术栈文档、架构检查清单）
  - *Initiator Payload*: `{ "type": "QUERY", "target": "PRD.step3.F001", "question": "..." }`
- 输出期望
  - 会话记录 JSON（含 Q&A）
  - **修订后的上游产物**（如 补全了细节的 PRD JSON）

---

#### 场景 B: 技术/资源协商 (Negotiation)
**触发条件**: 需求超出技术边界、预算限制或时间表冲突（如架构师评估 PRD 不可行）。

**调用 11.B：发起协商会话**
- 传入文件
  - 通用上下文
  - 冲突源文档（如 PRD JSON - 需求方）
  - 约束文档（如 environment.md, tech-stack.md - 限制方）
  - 历史会话记录（如有）
  - *Initiator Payload*: `{ "type": "CHALLENGE", "reason": "技术栈不支持高并发", "proposal": "降级或加资源" }`
- 输出期望
  - 会话结论 JSON（含 Consensus）
  - **变更计划**（Scope Adjustment Plan）

---

#### 场景 C: 架构决策/头脑风暴 (Decision/Brainstorm)
**触发条件**: 面临多个技术方案选择，需要权衡利弊（如选型 SQL vs NoSQL）。

**调用 11.C：发起决策会话**
- 传入文件
  - 通用上下文
  - 业务背景（PRD JSON）
  - 候选方案参考（如 官方文档片段、竞品分析）
  - 架构设计草稿（architecture.md）
  - *Initiator Payload*: `{ "type": "PROPOSAL", "options": ["Option A", "Option B"], "criteria": ["成本", "性能"] }`
- 输出期望
  - 决策记录 JSON（含 Rationale）
  - **架构文档更新草稿**

---

### 11.3 动态会话协议 (Session Protocol)

智能体通过创建**会话 (Session)** 来管理沟通上下文。

**会话结构 (JSON)**

```json
{
  "session_id": "uuid-v4",
  "topic": "关于 F001 实时性要求的技术可行性讨论",
  "status": "OPEN | CONCLUDED | STALLED",
  "participants": ["PM", "Architect"],
  "context_refs": [
    "docs/table_specs/prd.md#F001",
    "docs/code_specs/tech-stack.md"
  ],
  "messages": [
    {
      "id": "msg-001",
      "sender": "PM",
      "timestamp": "ISO8601",
      "type": "QUERY | PROPOSAL | COUNTER_PROPOSAL | AGREE | DISAGREE",
      "content": "用户要求 F001 必须在 100ms 内响应，目前的架构能支持吗？",
      "sentiment": "NEUTRAL"
    },
    {
      "id": "msg-002",
      "sender": "Architect",
      "timestamp": "ISO8601",
      "type": "ANSWER",
      "content": "目前的 PostgreSQL 架构很难稳定达到 100ms。建议引入 Redis 缓存层，但这会增加运维成本。",
      "references": ["docs/code_specs/architecture.md#Database"]
    }
  ],
  "conclusion": {
    "summary": "同意引入 Redis，但需限制缓存数据量。",
    "action_items": [
      { "assignee": "Architect", "task": "更新架构文档，增加 Redis 组件" },
      { "assignee": "PM", "task": "更新 PRD 非功能需求，注明成本增加风险" }
    ]
  }
}
```

### 11.3 交互原语 (Primitives)

在会话中，智能体应使用以下原语进行交互，而非仅发送大段文本：

1.  **Request Clarification (请求澄清)**
    *   *语义*: "我不理解 X，请提供更多信息。"
    *   *Payload*: `{ "target": "PRD Section 3.1", "question": "..." }`

2.  **Propose Solution (提出方案)**
    *   *语义*: "针对问题 Y，我建议方案 Z。"
    *   *Payload*: `{ "problem": "...", "solution": "...", "pros": [], "cons": [] }`

3.  **Challenge (质疑/挑战)**
    *   *语义*: "我不同意方案 Z，因为..."
    *   *Payload*: `{ "target_proposal_id": "...", "reason": "违反安全规范 SEC001" }`

4.  **Concede (让步)**
    *   *语义*: "我接受你的观点，虽然我有保留意见。"
    *   *Payload*: `{ "condition": "仅限本次迭代" }`

5.  **Commit (承诺)**
    *   *语义*: "我确认可以完成任务 X。"
    *   *Payload*: `{ "task_id": "...", "eta": "..." }`

### 11.4 Session 技术实现方案：外部状态循环 (External State Loop)

由于智能体 API 本身是**无状态 (Stateless)** 的，实现多轮对话的关键在于**外部状态管理**。我们需要通过维护一个 JSON 文件（Session State）来模拟有状态的会话。

**核心原理**

`Next_Response = Agent_API(System_Prompt + Context_Files + Session_History + Current_Instruction)`

**实现步骤 (伪代码逻辑)**

1.  **初始化 (Init)**
    *   创建一个 JSON 文件（如 `sessions/session_001.json`），写入初始 Topic、Context 引用和第一条 Query 消息。

2.  **主控循环 (Orchestrator Loop)**
    *   **Read**: 读取 `session_001.json`。
    *   **Check**: 检查状态。如果 `status == "CONCLUDED"`，结束循环。
    *   **Decide**: 根据最后一条消息，决定下一个发言的角色（Sender）。
        *   *规则*: 如果上一条是 `QUERY`，下一条通常是 `ANSWER`；如果是 `PROPOSAL`，下一条可能是 `AGREE/DISAGREE`。
    *   **Construct Prompt**:
        *   *System*: 加载当前发言角色的定义（如 `architect.md`）。
        *   *Context*: 加载 `context_refs` 中的文件内容（如 `prd.json`）。
        *   *History*: 将 Session 中的所有 `messages` 转换为对话历史格式。
    *   **Call API**: 调用 LLM API，获取响应。
    *   **Update**: 将 API 返回的内容作为新消息追加到 `session_001.json` 的 `messages` 列表中，并更新 `status`。
    *   **Repeat**: 下一轮循环。

**Python 实现示例 (伪代码)**

```python
def run_session_loop(session_file):
    while True:
        session = load_json(session_file)
        
        if session['status'] == 'CONCLUDED':
            break
            
        # 1. 决定下一个发言者 (简单的轮转逻辑)
        last_msg = session['messages'][-1]
        next_role = get_next_speaker(last_msg['sender'], session['participants'])
        
        # 2. 构建 Prompt
        system_prompt = load_file(f".bmad/personas/{next_role.lower()}.md")
        context_content = ""
        for ref in session['context_refs']:
            context_content += load_file(ref) + "\n"
            
        history_text = format_history(session['messages'])
        
        full_prompt = f"""
        {system_prompt}
        
        相关上下文:
        {context_content}
        
        对话历史:
        {history_text}
        
        请作为 {next_role} 回复下一条消息。请使用 JSON 格式返回，包含 type, content 等字段。
        """
        
        # 3. 调用 API (无状态)
        response = call_llm_api(full_prompt)
        
        # 4. 更新 Session 状态 (持久化)
        new_msg = parse_json(response)
        session['messages'].append(new_msg)
        
        # 检查是否结束会话
        if new_msg['type'] == 'AGREE' and 'action_items' in new_msg:
            session['status'] = 'CONCLUDED'
            session['conclusion'] = new_msg['content']
            
        save_json(session_file, session)
```

### 11.5 冲突管理 (Conflict Management)

#### 11.5.1 冲突检测标准 (Detection Criteria)

主控循环 (Orchestrator Loop) 应在每一轮对话后检查以下条件。若满足任一条件，将 Session 状态置为 `STALLED`：

1.  **死锁循环 (Deadlock Loop)**:
    *   连续 **3次** 交互均为 `DISAGREE` 或 `CHALLENGE` 类型。
    *   同一提案 (Proposal) 被拒绝并重提超过 **3次**。

2.  **会话超时 (Session Timeout)**:
    *   单次会话轮次超过 **20轮** 仍未达成 `CONCLUDED`。

3.  **显式求助 (Explicit Help)**:
    *   任意智能体发出 `type: "HELP"` 消息，或内容包含“无法达成一致”、“请求仲裁”等关键词。

#### 11.5.2 解决机制 (Resolution Strategies)

当会话状态变为 `STALLED` 时，触发升级机制：

1.  **引入仲裁者 (Arbiter)**: 引入上一级角色（如 User 或 Lead Architect）进行裁决。
2.  **投票 (Voting)**: 所有参与者对提案进行投票。
3.  **搁置 (Table)**: 记录问题，暂时跳过，继续其他议题。

### 11.6 Session 存储与管理 (Storage & Management)

所有的 Session 交互记录必须持久化存储，以便审计、回溯和上下文恢复。

#### 11.6.1 目录结构

建议在项目根目录下建立 `.bmad/sessions` 目录：

```
project/
├── .bmad/
│   ├── sessions/
│   │   ├── active/           # 进行中的会话
│   │   │   ├── session_20231027_prd_clarification.json
│   │   │   └── session_20231028_arch_decision.json
│   │   └── archive/          # 已结束的会话
│   │       ├── session_20231001_brief_review.json
│   │       └── ...
```

#### 11.6.2 命名规范

Session 文件名应具有语义，便于人类和智能体检索：

`session_{YYYYMMDD}_{topic_slug}_{uuid_short}.json`

*   示例: `session_20231027_prd_auth_flow_a1b2.json`

#### 11.6.3 索引文件 (Session Index)

为了快速查找相关讨论，维护一个 `session_index.json`：

```json
{
  "sessions": [
    {
      "id": "session_20231027_...",
      "path": ".bmad/sessions/active/session_20231027_....json",
      "status": "OPEN",
      "topic": "PRD Auth Flow Clarification",
      "related_files": ["docs/table_specs/prd.md"]
    }
  ]
}
```

### 11.7 Session 与工作流的集成映射 (Integration Mapping)

Session 不是独立的孤岛，它必须挂载到具体的工作流步骤上。当 Session 达成 `CONCLUDED` 状态时，其结论（Conclusion）必须转化为对特定步骤产物（JSON）的修改。

#### 11.7.1 挂载点映射表

Session 应根据其**发起时的上下文**（Workflow Step）自动关联到对应的产物文件：

| Session 类型 | 典型发生阶段 | 挂载目标 Step | 输入上下文 (Context) | 输出更新目标 (Target Artifact) |
| :--- | :--- | :--- | :--- | :--- |
| **需求澄清** | 1. 项目简报 | **Step 1.1** | `project-brief.json` | 更新 `project-brief.json` 的模糊字段 |
| **需求澄清** | 2. PRD 定义 | **Step 2.1** | `prd.json` | 更新 `prd.json` 的 Step1-3 字段 |
| **技术协商** | 2. PRD 定义 | **Step 2.1** | `prd.json` + `tech-stack.md` | 修改 `prd.json` 的可行性范围或非功能需求 |
| **用户故事细化** | 3. Story 策划 | **Step 3.1** | `next-story.json` | 拆分/合并 `user_stories` 列表，更新 AC |
| **架构决策** | 4. 架构设计 | **Step 4** | `architecture.md` (Draft) | 更新架构设计草稿中的决策点 |
| **接口对齐** | 5. 前端/API | **Step 5 & 6** | `front-end.json` + API Draft | 同步更新 `front-end.json` 和 API 文档 |
| **测试策略讨论** | 5. 开发实施 | **Step 5 (QA)** | 用户故事 + 验收标准 | 更新测试计划或补充边界测试用例 |

#### 11.7.2 集成动作 (Merge Action)

在 Session 结束时，主控程序应执行 **Merge Action** 以实现闭环：

1.  **提取结论**: 从 Session 最后一条消息或 `conclusion` 字段提取变更指令（例如：“将 F001 的响应时间要求从 100ms 放宽到 500ms”）。
2.  **定位目标**: 根据 Session 启动时记录的 `workflow_step` (如 `2.1`) 找到对应的目标 JSON 文件 (如 `prd.json`)。
3.  **应用变更**:
    *   *自动模式*: 调用智能体，传入 JSON + 变更指令，要求返回更新后的 JSON。
    *   *手动模式*: 生成 Patch 或 Todo 提示用户手动修改。
4.  **重新渲染**: 触发 Step 9 的渲染脚本，生成最新的 Markdown 文档，确保文档与沟通结果一致。

---

## 附：调用载荷组织建议
- system/context：第 0 节“通用上下文”子集（按流程挑选）
- constraints：对应流程检查清单（如需要）
- schema_or_template：
  - 生成结构化数据 → 传入对应 .jsons 下的 Schema 文件全文
  - 生成文档草稿 → 传入对应 docs 下模板（table_specs 或 code_specs）
- inputs：上游产物（如 项目简报 JSON、PRD JSON、用户故事 JSON 等）
- output_format：明确“返回有效 JSON（严格符合 Schema）”或“返回 Markdown 草稿”

