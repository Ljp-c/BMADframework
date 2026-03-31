# 用户故事模板（User Story Template）

> 本模板用于快速创建标准化的用户故事。每个故事应该可以在一个 Sprint 内完成。删除此说明后提交。

---

## 故事基本信息

| 项目 | 详情 |
|------|------|
| **故事 ID** | [如：US-001 或 EPIC-1-STORY-1] |
| **故事标题** | [简洁、清晰的描述，如："用户可以通过邮箱登陆"] |
| **所属 Epic** | [如：User Authentication & Authorization] |
| **优先级** | [P0 / P1 / P2 - 与 PRD 对应] |
| **Story Points** | [估算工作量，如：5 points] |
| **分配给** | [开发者名称] |
| **状态** | [Backlog / In Progress / Code Review / Done] |
| **创建日期** | [YYYY-MM-DD] |
| **目标 Sprint** | [如：Sprint-10 / Q2-Iteration-1] |

---

## 1. 用户故事描述

### 用户故事主文本（User Story Narrative）

```
作为一个 [用户角色，如："邮箱用户"]

我想要 [特性/功能，如："使用邮箱和密码登陆系统"]

以便 [业务价值/收益，如："更快地访问我的个人仪表板，而无需记住多个身份验证方式"]
```

### 背景与上下文
[说明为什么要实现这个故事，补充必要的业务背景，例如：
- 当前用户反馈
- 竞品分析
- 市场趋势
等]

---

## 2. 验收标准 (Acceptance Criteria)

### Scenario 1: 新用户首次邮箱注册

```gherkin
Given 用户在登陆页面
When 用户点击 "使用邮箱注册"
And 填写邮箱地址 "user@example.com"
And 设置密码符合要求（至少 8 个字符，包含大小写和数字）
And 点击 "注册"
Then 系统发送确认邮件到该邮箱
And 用户收到提示 "验证邮件已发送，请检查邮箱"
And 点击邮件中的链接后，账户激活
And 用户可以用邮箱和密码登陆系统
```

### Scenario 2: 已有用户使用邮箱密码登陆

```gherkin
Given 用户已在系统中注册账户（邮箱已激活）
When 用户在登陆页输入邮箱和正确密码
And 点击 "登陆"
Then 系统验证邮箱和密码
And 登陆成功，重定向到用户仪表板
And 显示欢迎信息 "欢迎回来，[用户名]"
```

### Scenario 3: 密码错误

```gherkin
Given 用户在登陆页面
When 用户输入正确的邮箱
And 输入错误的密码
And 点击 "登陆"
Then 系统显示错误提示 "邮箱或密码错误"
And 登陆失败
And 用户仍在登陆页面
```

### Scenario 4: 忘记密码

```gherkin
Given 用户在登陆页面
When 用户点击 "忘记密码"
And 输入注册邮箱
And 点击 "发送重置链接"
Then 系统发送密码重置邮件
And 用户在邮件中点击链接
And 跳转到重置密码页面
And 输入新密码并确认
And 密码更新成功，提示 "密码已重置，请重新登陆"
```

### Scenario 5: 防暴力破解

```gherkin
Given 用户在登陆页面
When 用户连续 5 次输入错误密码
Then 系统锁定该邮箱账户 15 分钟
And 显示提示 "账户已被暂时锁定，请于 [时间] 后重试或重置密码"
And 用户在锁定期间无法尝试登陆
```

---

## 3. 技术说明

### 后端 API 需求

#### Endpoint 1: POST /api/auth/register
**用途**: 用户注册

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "验证邮件已发送",
  "userId": "usr_12345",
  "nextStep": "verify-email"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "该邮箱已被注册",
  "errorCode": "EMAIL_ALREADY_EXISTS"
}
```

#### Endpoint 2: POST /api/auth/login
**用途**: 用户登陆

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "expiresIn": 3600,
  "user": {
    "id": "usr_12345",
    "email": "user@example.com",
    "firstName": "John"
  }
}
```

**Error Response (401 Unauthorized)**:
```json
{
  "success": false,
  "error": "邮箱或密码错误",
  "errorCode": "INVALID_CREDENTIALS"
}
```

#### Endpoint 3: POST /api/auth/forgot-password
**用途**: 发送密码重置邮件

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "重置邮件已发送"
}
```

---

### 设计相关

| 组件 | 当前状态 | 设计稿链接 |
|------|----------|-----------|
| 登陆页面 | [ ] 未开始 / [ ] 进行中 / [ ] 完成 | [Figma 链接] |
| 注册页面 | [ ] 未开始 / [ ] 进行中 / [ ] 完成 | [Figma 链接] |
| 密码重置流程 | [ ] 未开始 / [ ] 进行中 / [ ] 完成 | [Figma 链接] |

---

### 相关依赖或组件

| 依赖项 | 类型 | 状态 | 说明 |
|--------|------|------|------|
| 邮件服务（如 SendGrid） | 第三方库 | [必须/可选] | 用于发送验证和重置邮件 |
| 密码加密库（如 bcrypt） | 第三方库 | 必须 | 安全存储用户密码 |
| 用户数据库表 | 基础设施 | 必须 | users 和 password_reset_tokens 表 |
| OAuth 集成（可选） | 功能扩展 | 可选 | 支持 Google/企业微信登陆 |

---

## 4. 非功能需求

| 需求 | 详情 |
|------|------|
| **安全性** | 密码采用 bcrypt 加密; 会话采用 JWT；防 SQL 注入和 XSS 攻击 |
| **性能** | 登陆响应时间 < 2 秒; 邮件发送 < 5 秒 |
| **可用性** | 登陆页面必须在移动设备上可用; 清晰的错误提示 |
| **合规性** | 遵守 GDPR 和本地隐私法规 |
| **日志** | 记录所有登陆尝试、失败原因; 敏感信息（密码）不记录 |

---

## 5. 相关文件与功能

### 关联的其他故事
- [ ] US-002: 社交媒体登陆 (依赖本故事)
- [ ] US-010: 用户权限管理 (受本故事影响)

### 相关代码/模块
- Backend: `src/auth/` - 认证模块
- Frontend: `src/pages/auth/` - 认证相关页面
- Database: `migrations/001_create_users_table.sql`

### 参考文档
- 项目 PRD: [链接]
- API 规范: [链接]
- 安全规范: [链接]

---

## 6. 工作分解 (Task Breakdown)

### 前端任务
- [ ] **TASK-001**: 创建注册页面 UI (Story Points: 3)
  - 表单验证（邮箱格式、密码强度）
  - 提交按钮交互反馈
  - 错误提示展示

- [ ] **TASK-002**: 创建登陆页面 UI (Story Points: 2)
  - 邮箱和密码输入框
  - "忘记密码" 链接
  - 登陆按钮状态管理

- [ ] **TASK-003**: 集成认证 API (Story Points: 3)
  - 调用后端注册、登陆、重置密码接口
  - 处理响应和错误
  - 保存 Token (localStorage / sessionStorage)

### 后端任务
- [ ] **TASK-004**: 实现注册接口 (Story Points: 5)
  - 邮箱验证和去重
  - 密码加密存储
  - 生成验证。令牌和发送邮件

- [ ] **TASK-005**: 实现登陆接口 (Story Points: 4)
  - 凭证验证
  - JWT Token 生成
  - 防暴力破解逻辑

- [ ] **TASK-006**: 实现重置密码接口 (Story Points: 4)
  - 发送重置邮件
  - 令牌验证
  - 密码更新逻辑

### 测试任务
- [ ] **TASK-007**: 单元测试 - 后端认证逻辑 (Story Points: 3)
- [ ] **TASK-008**: 集成测试 - API 端到端 (Story Points: 4)
- [ ] **TASK-009**: UI 测试 - 前端交互流程 (Story Points: 2)

---

## 7. 验收与部署

### 完成标准（Definition of Done）
- [ ] 代码编写完成
- [ ] 单元测试通过率 >= 80%
- [ ] 代码评审通过（至少 1 人）
- [ ] 集成测试通过
- [ ] UI/UX 测试通过
- [ ] 文档更新（API 文档、用户文档）
- [ ] 功能在测试环境验证通过

### 部署计划
- **测试环境**: [日期] - 开发完成后立即部署
- **UAT 环境**: [日期] - 通过单元测试后部署
- **生产环境**: [日期] - 通过 UAT 后部署

---

## 8. 备注与讨论

### 设计决策
- [为什么选择邮箱作为主登陆方式，而不是手机号]
- [为什么设置 15 分钟的锁定期]

### 后续考虑
- [ ] 支持双因素认证 (2FA)
- [ ] 支持生物识别登陆 (Touch ID / Face ID)
- [ ] 支持单点登陆 (SSO)

### 疑问与待定事项
- [ ] [某个设计决策是否还需要讨论？]
- [ ] [某个技术实现方案是否需要确认？]

---

## 版本历史

| 版本 | 日期 | 作者 | 变更描述 |
|------|------|------|----------|
| v 0.1 | [YYYY-MM-DD] | [PM] | 初稿 |
| v 1.0 | [YYYY-MM-DD] | [PM] | 评审通过 |
