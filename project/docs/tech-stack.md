# 技术栈文档 (Tech Stack) - 智能体对话记录

## 文档信息

> **Architect**: 本文档记录了技术选型阶段的智能体对话交互过程。基于架构设计，我与开发团队讨论确定了具体的技术栈选择。

---

## 第一轮对话：技术栈概览

### 话题：整体技术栈规划

**Architect**: 根据架构设计，我来介绍整体技术栈规划。

```
┌─────────────────────────────────────────────────────────────┐
│                         前端技术栈                           │
│  Next.js 14 + React 18 + TypeScript + Tailwind CSS         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         后端技术栈                           │
│  Next.js API Routes + Supabase + TypeScript                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         数据存储                             │
│  Supabase PostgreSQL + Supabase Auth                       │
└─────────────────────────────────────────────────────────────┘
```

**Dev**: 请详细说明每个技术的选择理由。

---

## 第二轮对话：前端技术栈

### 话题：核心框架选择

**Architect**: 前端核心框架选型：

| 技术 | 版本 | 用途 | 选择理由 |
|------|------|------|----------|
| Next.js | 14.x | 全栈框架 | SSR/SSG支持、API Routes、Vercel原生支持 |
| React | 18.x | UI框架 | 组件化、生态丰富、团队熟悉 |
| TypeScript | 5.x | 类型系统 | 类型安全、开发体验好、减少运行时错误 |
| Tailwind CSS | 3.x | 样式框架 | 原子化CSS、快速开发、体积小 |

**DesignArchitect**: React 18的选择我很赞同，支持Server Components可以提升性能。

**Dev**: Next.js 14的优势是什么？

**Architect**: Next.js 14核心优势：
1. **App Router**：新的路由系统，支持RSC
2. **Server Actions**：简化表单处理
3. **自动优化**：图片、字体、脚本优化
4. **Vercel集成**：一键部署，边缘函数支持

### 话题：状态管理与UI组件

**Dev**: 状态管理方案如何选择？

**Architect**: 状态管理分层：

| 技术 | 版本 | 用途 |
|------|------|------|
| Zustand | 4.x | 全局状态（用户信息、UI状态） |
| React Query | 5.x | 服务端状态（收藏列表、估价数据） |
| useState/useReducer | - | 组件本地状态 |

**DesignArchitect**: UI组件库如何选择？

**Architect**: UI组件方案：

| 技术 | 版本 | 用途 |
|------|------|------|
| Tailwind CSS | 3.x | 样式框架 |
| Radix UI | 1.x | 无样式组件（可访问性） |
| Lucide Icons | latest | 图标库 |
| Headless UI | 1.x | 复杂交互组件 |

**选择理由**：
- 不依赖完整UI库，保持轻量
- Radix UI保证可访问性
- Tailwind提供样式自由度

---

## 第三轮对话：后端技术栈

### 话题：运行时与框架

**Architect**: 后端技术栈：

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js API Routes | 14.x | Serverless API |
| TypeScript | 5.x | 类型系统 |
| Supabase JS SDK | 2.x | 数据库客户端 |

**Dev**: 为什么选择Next.js API Routes而不是独立后端？

**Architect**: 选择Next.js API Routes的原因：
1. **统一技术栈**：前后端同一项目，简化开发
2. **Serverless原生**：无需管理服务器
3. **快速迭代**：热重载、自动部署
4. **成本极低**：Vercel免费层支持API Routes

### 话题：数据库与认证

**Dev**: 数据库方案如何选择？

**Architect**: 数据库方案：

| 技术 | 版本 | 用途 |
|------|------|------|
| Supabase PostgreSQL | 16.x | 主数据库 |
| Supabase Auth | - | 用户认证 |
| Supabase RLS | - | 行级安全 |

**选择Supabase的理由**：
- PostgreSQL强大的关系型数据库
- 内置认证服务（支持微信登录）
- 行级安全策略（数据隔离）
- 免费层支持（500MB存储）
- 实时订阅功能

**Dev**: 认证方案的具体实现？

**Architect**: 认证实现：
- Supabase Auth处理用户注册/登录
- 支持Email和微信OAuth
- JWT Token存储在HttpOnly Cookie
- 中间件验证Token有效性

---

## 第四轮对话：第三方服务

### 话题：AI与支付服务

**Architect**: 第三方服务集成：

| 服务 | 提供方 | 用途 | 定价 |
|------|--------|------|------|
| AI估价 | DeepSeek | 智能估价分析 | 按调用计费（<100元/月） |
| 支付 | Polar.sh | 订阅支付管理 | 按交易收费（5%+手续费） |

**Dev**: DeepSeek API的调用方式？

**Architect**: DeepSeek API调用：

```typescript
// API调用示例
const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.DEEPSEEK_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'deepseek-chat',
    messages: [
      { role: 'system', content: '你是一个潮玩估价专家...' },
      { role: 'user', content: `请估价：${modelInfo}` }
    ]
  })
});
```

**Dev**: Polar.sh的集成方式？

**Architect**: Polar.sh集成：
1. 创建产品和订阅计划
2. 前端嵌入Polar Checkout
3. Webhook处理订阅事件
4. 更新用户订阅状态

---

## 第五轮对话：基础设施

### 话题：部署与CI/CD

**Architect**: 基础设施方案：

| 技术 | 用途 |
|------|------|
| Vercel | 应用托管（自动CI/CD） |
| GitHub | 代码仓库 |
| GitHub Actions | 自动化测试 |

**Dev**: 部署流程是什么？

**Architect**: 部署流程：

```
开发者 Push 代码
      │
      ▼
GitHub 触发 Webhook
      │
      ▼
Vercel 自动构建
      │
      ├─ 安装依赖
      ├─ 类型检查
      ├─ 构建优化
      └─ 单元测试
      │
      ▼
部署到边缘网络
      │
      ├─ PR → 预览环境
      └─ Main → 生产环境
```

---

## 对话总结

**Architect**: 技术栈选型完成：

**前端**：Next.js 14 + React 18 + TypeScript + Tailwind CSS
**后端**：Next.js API Routes + Supabase
**数据存储**：Supabase PostgreSQL + Auth
**AI服务**：DeepSeek API
**支付服务**：Polar.sh
**部署**：Vercel

**Dev**: 确认技术栈。我将开始搭建开发环境。

**QA**: 我会基于这些技术准备测试环境。

**ProjectManager**: 技术选型通过，开始Phase 4前端架构设计。

---

**文档版本**: 1.0  
**最后更新**: 2026年3月3日  
**下一步**: 参见 [front-end-architecture.md](./front-end-architecture.md)
