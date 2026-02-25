# 环境与基础设施文档 (Environment) - 智能体对话记录

## 文档信息

> **Dev**: 本文档记录了环境配置阶段的智能体对话交互过程。基于架构设计，我定义了开发、测试和生产环境的配置。

---

## 第一轮对话：环境概览

### 话题：环境规划

**Dev**: 环境规划如下：

| 环境名称 | 用途 | 域名 | 访问权限 |
|----------|------|------|----------|
| Development | 本地开发 | localhost:3000 | 开发者 |
| Preview | PR预览 | *.vercel.app | 团队 |
| Production | 生产环境 | tidevault.app | 公开 |

**Architect**: 各环境的资源配置如何？

**Dev**: 资源配置：

| 环境 | Vercel | Supabase | 说明 |
|------|--------|----------|------|
| Development | 本地 | 开发实例 | 本地开发环境 |
| Preview | 免费层 | 开发实例 | PR预览 |
| Production | 免费层 | 生产实例 | 线上环境 |

---

## 第二轮对话：基础设施配置

### 话题：计算资源

**Dev**: 计算资源配置：

| 环境 | 规格 | 数量 | 说明 |
|------|------|------|------|
| Development | 本地机器 | 1 | 开发调试 |
| Preview | Vercel Serverless | 自动 | PR预览 |
| Production | Vercel Serverless | 自动扩展 | 生产环境 |

**Architect**: Vercel免费层的限制是什么？

**Dev**: Vercel免费层限制：
- 带宽：100GB/月
- 函数执行：100GB-Hrs/月
- 并发构建：1个
- 支持1万用户访问

### 话题：数据库配置

**Dev**: Supabase配置：

| 环境 | PostgreSQL | Auth | Storage |
|------|------------|------|---------|
| Development | 500MB | 开启 | 1GB |
| Production | 500MB | 开启 | 1GB |

**QA**: 数据库备份策略是什么？

**Dev**: 备份策略：
- Supabase自动每日备份（Pro版）
- 免费版需手动导出
- 重要数据定期导出SQL

---

## 第三轮对话：CI/CD配置

### 话题：流水线设计

**Dev**: CI/CD流水线：

```
Code Push → Build → Test → Deploy
```

**Architect**: 请展示GitHub Actions配置。

**Dev**: 

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Type check
        run: pnpm type-check
      
      - name: Lint
        run: pnpm lint
      
      - name: Test
        run: pnpm test
      
      - name: Build
        run: pnpm build
```

### 话题：部署流程

**Dev**: Vercel自动部署流程：

```
开发者 Push 代码
      │
      ▼
GitHub 触发 Webhook
      │
      ▼
Vercel 自动构建
      │
      ├─ 安装依赖 (pnpm install)
      ├─ 类型检查 (tsc --noEmit)
      ├─ 代码检查 (eslint)
      ├─ 单元测试 (jest)
      └─ 构建优化 (next build)
      │
      ▼
部署到边缘网络
      │
      ├─ PR → 预览环境 (pr-xxx.vercel.app)
      └─ Main → 生产环境 (tidevault.app)
```

---

## 第四轮对话：监控与日志

### 话题：监控配置

**Dev**: 监控方案：

| 监控类型 | 工具 | 指标 |
|----------|------|------|
| 基础设施 | Vercel Analytics | PV/UV、响应时间 |
| 应用错误 | Sentry | 错误追踪 |
| 用户行为 | Google Analytics | 用户行为 |

**QA**: 告警如何配置？

**Dev**: 告警配置：

| 告警名称 | 条件 | 级别 | 通知方式 |
|----------|------|------|----------|
| 服务不可用 | 健康检查失败 | P0 | 邮件+短信 |
| 高错误率 | 错误率 > 5% | P1 | 邮件 |
| 慢响应 | 响应时间 > 5秒 | P2 | 邮件 |

### 话题：日志管理

**Dev**: 日志级别：

```
DEBUG: 调试信息（仅开发环境）
INFO: 重要操作日志
WARNING: 警告信息
ERROR: 错误信息
CRITICAL: 关键错误
```

**日志示例**:

```typescript
// 结构化日志
logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  timestamp: new Date().toISOString()
});

logger.error('Valuation failed', {
  collectionId,
  error: error.message,
  stack: error.stack
});
```

---

## 第五轮对话：安全配置

### 话题：SSL/TLS配置

**Dev**: SSL/TLS配置：

| 环境 | 证书类型 |
|------|----------|
| Development | 本地自签名 |
| Preview | Vercel自动配置 |
| Production | Vercel自动配置（Let's Encrypt） |

### 话题：密钥管理

**Dev**: 密钥管理方案：

| 密钥类型 | 存储位置 |
|----------|----------|
| 数据库密码 | Supabase管理 |
| API密钥 | Vercel环境变量 |
| JWT密钥 | Supabase管理 |
| 第三方密钥 | Vercel环境变量 |

**环境变量配置**:

```bash
# .env.local (本地开发)
NEXT_PUBLIC_SUPABASE_URL=xxx
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx
DEEPSEEK_API_KEY=xxx
POLAR_ACCESS_TOKEN=xxx
```

---

## 第六轮对话：本地开发环境

### 话题：开发环境搭建

**Dev**: 本地开发环境搭建步骤：

```bash
# 1. 克隆项目
git clone https://github.com/xxx/tidevault.git
cd tidevault

# 2. 安装依赖
pnpm install

# 3. 配置环境变量
cp .env.example .env.local
# 编辑 .env.local 填入实际值

# 4. 启动开发服务器
pnpm dev

# 5. 运行测试
pnpm test
```

**Architect**: Supabase本地实例如何配置？

**Dev**: Supabase本地配置：

```bash
# 安装Supabase CLI
npm install -g supabase

# 登录
supabase login

# 关联项目
supabase link --project-ref xxx

# 启动本地实例
supabase start
```

---

## 对话总结

**Dev**: 环境与基础设施配置完成：

1. **环境规划**：Development、Preview、Production
2. **CI/CD**：GitHub Actions + Vercel自动部署
3. **监控**：Vercel Analytics + Sentry + GA
4. **安全**：SSL/TLS + 密钥管理
5. **本地开发**：完整的环境搭建指南

**Architect**: 配置方案合理，满足项目需求。

**QA**: 我会验证各环境配置正确性。

---

**文档版本**: 1.0  
**最后更新**: 2026年3月7日
