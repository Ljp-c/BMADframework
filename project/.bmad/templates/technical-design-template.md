# 技术设计文档模板（Technical Design Document Template）

> 本模板用于快速创建完整的技术设计文档。用于指导开发团队的实现。删除此说明后提交。

---

## 1. 文档信息

| 项目 | 详情 |
|------|------|
| **文档版本** | v 1.0 |
| **文档日期** | [YYYY-MM-DD] |
| **设计主题** | [如：用户认证子系统架构设计] |
| **技术负责人** | [名称、联系方式] |
| **相关故事** | [如：US-001, US-002] |
| **最后更新** | [日期] |

---

## 2. 设计概述

### 背景
[说明为什么需要进行这个设计，问题陈述和业务背景，如：
- 当前系统存在的问题
- 新功能实现的需求
- 性能或可维护性改进]

### 设计目标
1. [具体目标 1，如：支持多种登陆方式（邮箱、手机、第三方）]
2. [具体目标 2，如：确保系统安全性和数据隐私]
3. [具体目标 3，如：支持 1000+ 并发用户]
4. [具体目标 4，如：降低 API 响应时间至 < 200ms]

### 设计约束
| 约束项 | 说明 |
|--------|------|
| **技术栈** | [如：Node.js 18+, PostgreSQL 13+, Redis 7+] |
| **第三方依赖** | [不能使用某些库或服务] |
| **兼容性** | [需要支持的浏览器、操作系统版本] |
| **性能指标** | [如：P99 延迟 < 500ms] |
| **资源限制** | [如：内存 < 512MB] |
| **合规要求** | [如：GDPR, SOC2] |

---

## 3. 高层架构

### 架构模式
[选择适用的架构模式，如：
- 分层架构 (Layered Architecture)
- 微服务架构 (Microservices)
- 事件驱动架构 (Event-Driven)
- 无服务架构 (Serverless)
]

### 整体架构图（文字描述）

```
┌─────────────────────────────────────────────────┐
│              Client Layer (Web/Mobile)           │
│  (React Frontend / Vue Frontend / Mobile App)   │
└────────────────┬────────────────────────────────┘
                 │ HTTPS/HTTP2
┌────────────────▼────────────────────────────────┐
│          API Gateway / Load Balancer             │
│         (Rate Limiting, Authentication)         │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│          Microservices Layer                     │
├─────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│ │ Auth Service │  │ User Service │  │ ... MS │ │
│ └──────────────┘  └──────────────┘  └────────┘ │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Data Layer (Databases, Cache)           │
├─────────────────────────────────────────────────┤
│ ┌────────────┐  ┌─────────┐  ┌─────────────┐  │
│ │ PostgreSQL │  │ Redis   │  │ Elasticsearch│  │
│ └────────────┘  └─────────┘  └─────────────┘  │
└─────────────────────────────────────────────────┘
```

### 核心组件说明

| 组件 | 职责 | 技术栈 | 备注 |
|------|------|--------|------|
| **API Gateway** | 路由、限流、认证 | Kong / Nginx | 入口层 |
| **Auth Service** | 用户认证、授权 | Node.js + Express | 核心服务 |
| **User Service** | 用户管理 | Node.js + TypeORM | 核心服务 |
| **Database** | 数据持久化 | PostgreSQL | 主数据库 |
| **Cache Layer** | 缓存加速 | Redis | 热点数据 |
| **Message Queue** | 异步处理 | RabbitMQ / Kafka | 解耦服务 |

---

## 4. 核心模块/组件设计

### 模块 1: 认证服务 (Auth Service)

#### 职责
- 用户登陆、注册、登出
- 令牌管理（JWT 生成、验证、刷新）
- 权限检查

#### 核心类/模块结构

```
src/auth/
├── controllers/
│   ├── authController.ts       # API 路由处理器
│   └── tokenController.ts      # Token 管理
├── services/
│   ├── authService.ts          # 业务逻辑
│   ├── passwordService.ts      # 密码加密、验证
│   └── tokenService.ts         # Token 生成、验证
├── models/
│   ├── User.ts                 # 用户模型
│   └── RefreshToken.ts         # 刷新令牌模型
├── middleware/
│   ├── authMiddleware.ts       # 认证中间件
│   └── roleMiddleware.ts       # 权限检查中间件
├── utils/
│   ├── jwtUtils.ts             # JWT 工具函数
│   └── passwordUtils.ts        # 密码相关工具
└── tests/
    ├── authService.test.ts
    └── ...
```

#### 主要类设计

**AuthService 类**:
```typescript
class AuthService {
  // 用户注册
  async register(email: string, password: string, name: string): Promise<User>
  
  // 用户登陆
  async login(email: string, password: string): Promise<{accessToken, refreshToken}>
  
  // 验证令牌
  async verifyToken(token: string): Promise<TokenPayload>
  
  // 刷新令牌
  async refreshToken(refreshToken: string): Promise<string>
  
  // 登出
  async logout(userId: string): Promise<void>
}
```

#### 数据流

```
用户提交登陆请求
    ↓
authController.login()
    ↓
authService.login(email, password)
    ├─ 从数据库查询用户
    ├─ 验证密码 (bcrypt.compare)
    ├─ 生成 JWT Token
    └─ 保存 Refresh Token 到数据库
    ↓
返回 accessToken 和 refreshToken 给客户端
```

---

### 模块 2: 用户服务 (User Service)

#### 职责
- 用户信息管理（获取、更新、删除）
- 用户角色和权限管理
- 用户搜索和列表

#### 核心接口

```typescript
interface IUserService {
  // 获取用户信息
  getUserById(userId: string): Promise<User>
  
  // 更新用户信息
  updateUser(userId: string, updates: Partial<User>): Promise<User>
  
  // 删除用户（软删除）
  deleteUser(userId: string): Promise<void>
  
  // 获取用户权限列表
  getUserPermissions(userId: string): Promise<Permission[]>
  
  // 设置用户角色
  setUserRole(userId: string, roleId: string): Promise<void>
}
```

---

## 5. 接口定义 (API Spec)

### Endpoint: POST /api/auth/login

**功能描述**: 用户登陆

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "rememberMe": true
}
```

**响应体 (200 OK)**:
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600,
    "user": {
      "id": "usr_12345",
      "email": "user@example.com",
      "name": "John Doe",
      "roles": ["user", "premium_member"]
    }
  }
}
```

**错误响应 (401 Unauthorized)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "邮箱或密码错误"
  }
}
```

**错误响应 (429 Too Many Requests)**:
```json
{
  "success": false,
  "error": {
    "code": "TOO_MANY_ATTEMPTS",
    "message": "登陆尝试过多，请于 15 分钟后重试"
  }
}
```

---

## 6. 数据结构设计

### 用户表 (users)

```sql
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  avatar_url TEXT,
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  INDEX idx_email (email),
  INDEX idx_created_at (created_at)
);
```

### 刷新令牌表 (refresh_tokens)

```sql
CREATE TABLE refresh_tokens (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  revoked BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_id (user_id),
  INDEX idx_expires_at (expires_at)
);
```

### 缓存设计 (Redis)

**Key 格式**:
```
- auth:jwt:{userId} -> JWT Payload (TTL: 1 小时)
- auth:blacklist:{token} -> 1 (TTL: 7 天，用于登出后防止令牌重用)
- user:profile:{userId} -> User 对象 JSON (TTL: 1 小时)
```

---

## 7. 算法说明

### 密码加密与验证算法

**加密**:
```python
# 使用 bcrypt，salt rounds = 12
password_hash = bcrypt.hash(password, rounds=12)
```

**验证**:
```python
is_valid = bcrypt.verify(user_input_password, stored_hash)
```

### JWT 令牌生成算法

**Payload**:
```json
{
  "sub": "usr_12345",
  "email": "user@example.com",
  "roles": ["user", "premium"],
  "iat": 1234567890,
  "exp": 1234571490
}
```

**签名**: HMAC-SHA256 with secret key

---

## 8. 流程设计

### 用户登陆流程 (Sequence Diagram)

```
Client              API Gateway        Auth Service       Database
  │                     │                    │                  │
  ├──POST /api/auth/login──>│                 │                  │
  │                         ├──forward req──>│                  │
  │                         │                 ├──query user──>│
  │                         │                 │<──user data───┤
  │                         │                 │
  │                         │           [验证密码]
  │                         │
  │                         │        [生成 JWT Token]
  │                         │
  │                         │        ├──save refresh_token──>│
  │                         │        │<─────────────────────┤
  │                         │<─response with tokens──│
  │                         │<─────JSON─────────┤
  │<──JSON response───────┤
  │
  [存储 accessToken 和 refreshToken]
```

---

## 9. 性能考虑

### 性能优化策略

| 优化项 | 方案 | 预期效果 |
|--------|------|----------|
| **缓存** | Redis 缓存用户信息和权限 | 减少 DB 查询 50% |
| **异步处理** | 使用消息队列处理发送邮件 | 提升 API 响应时间 |
| **数据库索引** | 在 email、user_id 字段建索引 | 查询速度提升 10x |
| **连接池** | 数据库连接池 (size: 20) | 提升并发能力 |
| **CDN** | 静态资源 CDN 加速 | 减少网络延迟 30% |

### 性能指标目标

| 指标 | 目标值 |
|------|--------|
| 登陆 API P99 延迟 | < 200ms |
| 用户信息查询 P99 延迟 | < 100ms |
| 并发用户支持 | 1000+ |
| 数据库查询时间 | < 50ms |

---

## 10. 安全考虑

### 安全威胁与防护

| 威胁 | 防护措施 |
|------|----------|
| **SQL 注入** | 使用 ORM (TypeORM) + Parameterized Queries |
| **XSS 攻击** | 前端输入验证 + 后端输出转义 + CSP 头 |
| **CSRF** | CSRF Token + SameSite Cookie 属性 |
| **暴力破解** | IP 限流 + 账户锁定机制 |
| **会话劫持** | HTTPS + Secure Cookie + HttpOnly 属性 |
| **密码泄露** | bcrypt 加密 + 不在日志中记录密码 |
| **Token 窃取** | 短期有效期 + Refresh Token 轮换 |
| **DDoS** | 速率限制 + WAF + DDoS 防护服务 |

### 安全检查清单
- [ ] 所有通信使用 HTTPS
- [ ] 敏感数据加密存储
- [ ] 定期安全审计
- [ ] 依赖库漏洞扫描
- [ ] 代码安全审查

---

## 11. 可扩展性设计

### 水平扩展
- 使用微服务架构，每个服务独立部署和扩展
- 使用负载均衡器分发流量
- 数据库读写分离 (主从复制)

### 垂直扩展
- 代码优化和缓存策略
- 数据库分区和索引优化

### 未来扩展点
- [ ] 支持多租户架构
- [ ] 支持 OAuth2 社交登陆
- [ ] 支持双因素认证
- [ ] 支持单点登陆 (SSO)

---

## 12. 依赖项清单

### 第三方库

| 库 | 版本 | 用途 | 必须/可选 |
|-----|------|------|----------|
| express | ^4.18.0 | Web 框架 | 必须 |
| typeorm | ^0.3.0 | ORM | 必须 |
| jsonwebtoken | ^9.0.0 | JWT 处理 | 必须 |
| bcryptjs | ^2.4.3 | 密码加密 | 必须 |
| redis | ^4.5.0 | 缓存 | 必须 |
| nodemailer | ^6.9.0 | 邮件发送 | 可选 |
| joi | ^17.9.0 | 输入验证 | 可选 |

### 外部服务

| 服务 | 用途 | SLA |
|------|------|-----|
| SendGrid / SMTP | 邮件发送 | 99.9% |
| PostgreSQL | 数据库 | 99.99% |
| Redis | 缓存 | 99.9% |

---

## 13. 测试策略

### 单元测试
- 单元测试覆盖率 >= 80%
- 测试框架：Jest / Mocha

### 集成测试
- API 端到端测试
- 数据库集成测试

### 性能测试
- 负载测试 (1000 并发用户)
- 响应时间报告

### 安全测试
- 依赖库漏洞扫描 (每周)
- 代码安全审查 (每次提交)

---

## 14. 部署与发布

### 部署环境

| 环境 | 用途 | 部署时机 |
|------|------|----------|
| 开发 (dev) | 本地开发 | 实时 |
| 测试 (staging) | 功能验证 | 每个 PR |
| 生产 (production) | 用户访问 | 每周或按需 |

### 部署步骤
1. 构建 Docker 镜像
2. 推送镜像到仓库
3. 使用 Kubernetes 部署
4. 健康检查
5. 灰度发布 (金丝雀)

---

## 15. 监控与日志

### 关键监控指标
- API 响应时间 (P50, P99)
- 错误率
- 内存使用率
- CPU 使用率
- 数据库连接数

### 日志策略
- 日志级别：DEBUG, INFO, WARN, ERROR
- 敏感信息不记录 (密码、Token)
- 日志保留期：30 天

---

## 16. 版本历史

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| v 0.1 | [YYYY-MM-DD] | [Tech Lead] | 初稿 |
| v 1.0 | [YYYY-MM-DD] | [Tech Lead] | 完成评审 |

---

## 附录：参考资料

- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [12 Factor App](https://12factor.net/)
