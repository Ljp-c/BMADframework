# Tech Preferences (技术偏好) - 智能体对话记录

## 文档信息

> **Architect**: 本文档记录了技术偏好讨论的智能体对话交互过程。基于项目需求和团队经验，我们确定了技术偏好和选型决策。

---

## 第一轮对话：前端技术偏好

### 话题：前端框架选择

**Architect**: 讨论前端技术偏好。

**Dev**: 前端框架我的偏好是Next.js。

**Architect**: 理由是什么？

**Dev**: 选择Next.js的理由：

| 优势 | 说明 |
|------|------|
| SSR/SSG支持 | 提升首屏性能和SEO |
| App Router | 新的路由系统，更灵活 |
| API Routes | 前后端统一部署 |
| Vercel原生支持 | 一键部署，自动优化 |
| React生态 | 团队熟悉，生态丰富 |

**DesignArchitect**: 同意。Next.js的Server Components可以优化性能。

### 话题：状态管理选择

**Dev**: 状态管理我偏好Zustand + React Query。

**Architect**: 为什么选择这个组合？

**Dev**: 理由：

**Zustand**:
- 轻量级（< 1KB）
- 无Provider包裹
- TypeScript友好
- 学习成本低

**React Query**:
- 服务端状态管理
- 自动缓存和刷新
- 离线支持
- 与REST API完美配合

**Architect**: 同意。分离全局状态和服务端状态是好的实践。

### 话题：样式方案选择

**DesignArchitect**: 样式方案我偏好Tailwind CSS。

**Architect**: 为什么选择Tailwind？

**DesignArchitect**: 理由：

| 优势 | 说明 |
|------|------|
| 原子化CSS | 快速开发，无需写CSS |
| 一致性 | 设计系统内置 |
| 体积小 | 生产环境只包含使用的类 |
| 响应式 | 内置响应式前缀 |
| 深色模式 | 内置深色模式支持 |

---

## 第二轮对话：后端技术偏好

### 话题：后端框架选择

**Dev**: 后端我偏好Next.js API Routes。

**Architect**: 为什么不用Express或NestJS？

**Dev**: 对于MVP阶段，选择Next.js API Routes的原因：

| 对比项 | Next.js API Routes | Express/NestJS |
|--------|-------------------|----------------|
| 部署复杂度 | 低（Vercel自动） | 高（需要服务器） |
| 开发成本 | 低 | 中 |
| 运维成本 | 无 | 有 |
| 扩展性 | 中 | 高 |

**Architect**: 同意。MVP阶段优先考虑快速上线和低成本。

### 话题：数据库选择

**Architect**: 数据库我偏好Supabase（PostgreSQL）。

**Dev**: 为什么选择Supabase而不是自建数据库？

**Architect**: 理由：

**Supabase优势**:
- 免费层支持（500MB存储）
- 内置认证服务
- 行级安全策略
- 实时订阅
- Dashboard管理界面
- 无运维成本

**Dev**: 同意。对于MVP阶段，Supabase足够使用。

---

## 第三轮对话：第三方服务偏好

### 话题：AI服务选择

**Architect**: AI估价服务选择DeepSeek API。

**Dev**: 为什么选择DeepSeek而不是OpenAI？

**Architect**: 理由：

| 对比项 | DeepSeek | OpenAI |
|--------|----------|--------|
| 价格 | 更低 | 较高 |
| 中文支持 | 更好 | 一般 |
| API稳定性 | 稳定 | 稳定 |
| 响应速度 | 快 | 快 |

**Dev**: 同意。DeepSeek更适合中文场景和成本控制。

### 话题：支付服务选择

**PM**: 支付服务选择Polar.sh。

**Dev**: 为什么选择Polar.sh？

**PM**: 理由：

**Polar.sh优势**:
- 支持订阅支付
- 无需企业资质
- 国际支付支持
- Webhook集成
- 开发者友好

**Dev**: 对于个人开发者，Polar.sh是更好的选择。

---

## 第四轮对话：基础设施偏好

### 话题：托管平台选择

**Dev**: 托管平台我偏好Vercel。

**Architect**: 理由是什么？

**Dev**: 理由：

| 优势 | 说明 |
|------|------|
| 免费层 | 支持1万用户访问 |
| 自动部署 | GitHub集成 |
| 边缘网络 | 全球CDN加速 |
| 预览环境 | PR自动预览 |
| 零运维 | 无需管理服务器 |

### 话题：代码仓库选择

**Dev**: 代码仓库我偏好GitHub。

**Architect**: 理由？

**Dev**: 
- Vercel原生集成
- Actions CI/CD支持
- Pull Request流程
- Issue管理
- 团队协作

---

## 第五轮对话：开发工具偏好

### 话题：包管理器选择

**Dev**: 包管理器我偏好pnpm。

**Architect**: 为什么选择pnpm？

**Dev**: 理由：

| 对比项 | pnpm | npm | yarn |
|--------|------|-----|------|
| 安装速度 | 快 | 中 | 快 |
| 磁盘空间 | 省 | 多 | 中 |
| 幽灵依赖 | 无 | 有 | 有 |
| 单体仓库 | 支持 | 一般 | 支持 |

### 话题：代码质量工具

**Dev**: 代码质量工具偏好：

| 工具 | 用途 |
|------|------|
| ESLint | 代码检查 |
| Prettier | 代码格式化 |
| TypeScript | 类型检查 |
| Husky | Git Hooks |
| lint-staged | 提交前检查 |

---

## 技术偏好汇总

### 前端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 14.x | 全栈框架 |
| React | 18.x | UI框架 |
| TypeScript | 5.x | 类型系统 |
| Tailwind CSS | 3.x | 样式方案 |
| Zustand | 4.x | 全局状态 |
| React Query | 5.x | 服务端状态 |

### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js API Routes | 14.x | Serverless API |
| Supabase | 2.x | 数据库+认证 |

### 第三方服务
| 服务 | 用途 |
|------|------|
| DeepSeek API | AI估价 |
| Polar.sh | 支付订阅 |

### 基础设施
| 技术 | 用途 |
|------|------|
| Vercel | 应用托管 |
| GitHub | 代码仓库 |
| pnpm | 包管理器 |

---

## 对话总结

**Architect**: 技术偏好确定完成。

**Dev**: 确认所有技术选择，准备开始开发。

**PM**: 技术选择合理，符合MVP快速上线的目标。

---

**文档版本**: 1.0  
**最后更新**: 2026年3月3日
