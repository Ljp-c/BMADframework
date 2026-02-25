# Task: Create Architecture (创建系统架构文档) - 智能体任务流程

## 任务描述

> **Architect**: 我是本任务的执行者，负责基于产品需求文档设计整体系统架构，包括技术选型、系统分层、数据架构、API设计、基础设施规划等。

---

## 对话场景：任务执行过程

### 场景1：任务启动

**PM**: PRD已完成，请进行架构设计。

**Architect**: 收到任务。让我确认输入：

**输入检查**:
- [x] docs/prd.md - 产品需求文档
- [x] 非功能性需求
- [x] 技术约束条件
- [x] 团队技术能力评估

### 场景2：需求分析

**Architect**: Step 1: 需求分析

**PM**: 关键需求：

| 类别 | 需求 | 优先级 |
|------|------|--------|
| 功能 | 收藏管理、AI估价 | P0 |
| 性能 | 页面响应 < 3秒 | P0 |
| 性能 | 估价响应 < 5秒 | P0 |
| 可用性 | 99% | P1 |
| 成本 | < 150元/月 | P0 |

**Architect**: 技术约束识别：
- 必须支持移动端
- 不能使用IP图像
- 数据加密存储
- MVP周期3周

### 场景3：架构设计

**Architect**: Step 2: 架构设计

**架构风格选择**：Serverless单体架构

**理由**：
- 零运维成本
- 自动弹性扩展
- 快速部署上线
- 极低运营成本

**Dev**: 这个架构适合MVP阶段。

### 场景4：技术选型

**Architect**: Step 3: 技术选型

**前端技术栈**:
| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 14.x | 全栈框架 |
| React | 18.x | UI框架 |
| TypeScript | 5.x | 类型系统 |
| Tailwind CSS | 3.x | 样式框架 |

**后端技术栈**:
| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js API Routes | 14.x | Serverless API |
| Supabase | 2.x | 数据库+认证 |

**第三方服务**:
| 服务 | 用途 |
|------|------|
| DeepSeek API | AI估价 |
| Polar.sh | 支付订阅 |

**DesignArchitect**: 前端技术栈确认，符合团队经验。

### 场景5：数据架构设计

**Architect**: Step 4: 数据架构设计

**数据模型**:
```
User 1:N Collection
Collection 1:N Valuation
PriceData (独立表)
```

**主要数据表**:
- users（用户）
- collections（收藏）
- valuations（估价）
- price_data（预设价格）

**Dev**: 数据模型清晰，我来创建迁移脚本。

### 场景6：API设计

**Architect**: Step 5: API设计

**API规范**:
- RESTful设计
- JSON数据格式
- JWT认证
- 版本控制：/api/v1/

**核心API**:
| 接口 | 方法 | 描述 |
|------|------|------|
| /auth/login | POST | 用户登录 |
| /collections | GET/POST | 收藏管理 |
| /valuations | POST | 生成估价 |

### 场景7：基础设施规划

**Architect**: Step 6: 基础设施规划

**部署架构**:
```
用户 → Vercel CDN → Next.js App → Supabase
```

**CI/CD**:
- GitHub + Vercel自动部署
- PR预览环境
- Main生产环境

**Dev**: 部署流程清晰，我来配置CI/CD。

### 场景8：安全设计

**Architect**: Step 7: 安全设计

**认证安全**:
- Supabase Auth
- JWT Token（HttpOnly Cookie）
- 微信OAuth支持

**数据安全**:
- HTTPS强制
- 敏感数据加密
- 行级安全（RLS）

**QA**: 安全设计完善，我来准备安全测试用例。

### 场景9：审核确认

**Architect**: Step 6: 审核与确认

**ProjectManager**: 架构设计通过评审。

**Architect**: 任务完成。输出物：
- [x] docs/architecture.md - 系统架构文档
- [x] docs/tech-stack.md - 技术栈文档
- [x] docs/data-models.md - 数据模型文档
- [x] docs/api-reference.md - API参考文档
- [x] docs/environment.md - 环境文档

**下一步**：传递给前端架构师进入Phase 4。

---

## 输入

- `docs/prd.md` - 产品需求文档
- 非功能性需求
- 技术约束条件
- 团队技术能力评估

## 输出

- `docs/architecture.md` - 系统架构文档
- `docs/tech-stack.md` - 技术栈文档
- `docs/data-models.md` - 数据模型文档
- `docs/api-reference.md` - API参考文档
- `docs/environment.md` - 环境与基础设施文档

## 执行步骤

### Step 1: 需求分析
- [ ] 阅读PRD理解功能需求
- [ ] 分析非功能性需求
- [ ] 识别技术约束
- [ ] 评估系统复杂度

### Step 2: 架构设计
- [ ] 确定架构风格
- [ ] 设计系统分层
- [ ] 划分服务边界
- [ ] 设计服务通信机制

### Step 3: 技术选型
- [ ] 评估技术方案
- [ ] 选择后端技术栈
- [ ] 选择前端技术栈
- [ ] 选择数据库方案

### Step 4: 数据架构设计
- [ ] 设计数据模型
- [ ] 定义数据关系
- [ ] 设计数据访问层
- [ ] 规划数据迁移策略

### Step 5: API设计
- [ ] 设计API规范
- [ ] 定义接口契约
- [ ] 设计认证授权机制
- [ ] 编写API文档

### Step 6: 基础设施规划
- [ ] 设计部署架构
- [ ] 规划CI/CD流程
- [ ] 设计监控告警方案
- [ ] 规划灾难恢复策略

### Step 7: 安全设计
- [ ] 设计安全架构
- [ ] 定义安全策略
- [ ] 规划数据保护方案
- [ ] 设计审计日志

---

## 质量检查清单

- [ ] 架构满足所有功能需求
- [ ] 非功能性需求已考虑
- [ ] 技术选型有充分理由
- [ ] 系统可扩展
- [ ] 数据模型合理
- [ ] API设计规范
- [ ] 安全措施完善
- [ ] 部署方案可行
- [ ] 监控告警已规划
- [ ] 灾难恢复方案已制定

---

## 交付验收标准

1. 架构文档完整
2. 技术选型合理有依据
3. 数据模型设计完整
4. API文档规范
5. 基础设施规划可行
6. 已通过架构评审

## 下一步

架构文档完成后，传递给 **Design Architect (前端/UX架构师)** 进入 Phase 4: 创建前端架构文档
