# 测试计划模板（Test Plan Template）

> 本模板用于快速创建完整的测试计划。删除此说明后提交。

---

## 1. 文档信息

| 项目 | 详情 |
|------|------|
| **文档版本** | v 1.0 |
| **文档日期** | [YYYY-MM-DD] |
| **测试范围** | [如：用户认证功能] |
| **质量保证负责人** | [名称、联系方式] |
| **相关故事** | [如：US-001, US-002] |
| **最后更新** | [日期] |

---

## 2. 测试范围与目标

### 测试范围（In Scope）

| 模块/功能 | 测试类型 | 优先级 |
|-----------|----------|--------|
| 用户注册 | 单元、集成、UI | P0 |
| 用户登陆 | 单元、集成、UI | P0 |
| 密码重置 | 单元、集成 | P0 |
| 权限验证 | 单元、集成 | P0 |
| API 性能 | 性能测试 | P1 |
| 安全验证 | 安全测试 | P0 |

### 测试范围外（Out of Scope）
- 依赖库的功能测试（假设已由库维护者验证）
- 第三方服务的功能测试（如邮件服务）

### 测试目标
1. **功能完整性**: 覆盖所有需求，功能实现正确
2. **质量指标**: 
   - 单元测试覆盖率 >= 80%
   - 集成测试覆盖率 >= 70%
   - 缺陷修复率 >= 90%
3. **性能目标**:
   - API 响应时间 P99 < 200ms
   - 支持 1000+ 并发用户
4. **安全目标**: 通过 OWASP Top 10 漏洞检测

---

## 3. 测试类型详解

### 3.1 单元测试 (Unit Test)

**目的**: 验证各个函数和类的契约

**范围**: 每个函数、方法、类

**工具**: Jest, Mocha, pytest

**覆盖范围**:

| 被测对象 | 测试用例数 | 覆盖率目标 |
|----------|----------|----------|
| AuthService | 20+ | 90%+ |
| PasswordService | 15+ | 90%+ |
| TokenService | 12+ | 85%+ |
| Middleware | 10+ | 85%+ |

**示例测试用例**:
```typescript
describe('AuthService.login()', () => {
  it('应该返回 token 当凭证正确时', async () => {
    // Arrange
    const mockUser = { id: '123', email: 'test@example.com', password_hash: 'xxx' };
    // Act
    const result = await authService.login('test@example.com', 'password');
    // Assert
    expect(result.accessToken).toBeDefined();
  });
  
  it('应该抛出错误当邮箱不存在时', async () => {
    // Arrange
    // Act & Assert
    await expect(authService.login('nonexistent@example.com', 'password')).rejects.toThrow('用户不存在');
  });
});
```

### 3.2 集成测试 (Integration Test)

**目的**: 验证不同模块之间的交互

**范围**: 跨越多个模块的功能

**工具**: Jest + Supertest (API 测试), Postman, Newman

**测试场景**:
1. 完整的登陆流程（API -> Service -> Database）
2. 用户注册和邮件验证流程
3. 密码重置流程
4. 权限验证流程

**示例集成测试**:
```typescript
describe('POST /api/auth/login', () => {
  it('应该返回 token 当登陆成功时', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'password123' })
      .expect(200);
    
    expect(response.body.data.accessToken).toBeDefined();
    expect(response.body.data.user.email).toBe('test@example.com');
  });
});
```

### 3.3 系统测试 (System Test)

**目的**: 验证整个系统的功能和表现

**范围**: 整个应用从前端到后端

**测试场景**:
1. 完整的用户注册、登陆、使用、登出流程
2. 多个用户并发操作
3. 数据一致性校验

### 3.4 性能测试 (Performance Test)

**目的**: 验证系统在并发和负载下的表现

**工具**: Apache JMeter, Locust, k6

**性能测试计划**:

| 测试场景 | 用户数 | 测试时长 | 目标 |
|---------|--------|----------|------|
| 常规负载 | 100-500 | 10 分钟 | 响应时间 < 200ms |
| 峰值负载 | 500-1000 | 5 分钟 | 响应时间 < 500ms |
| 压力测试 | 1000+ | 直至系统崩溃 | 记录崩溃点 |

**性能测试脚本**（k6 示例）:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100,           // 虚拟用户数
  duration: '10m',    // 测试时长
};

export default function() {
  let response = http.post('http://localhost:3000/api/auth/login', {
    email: 'user@example.com',
    password: 'password123',
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);
}
```

### 3.5 安全测试 (Security Test)

**目的**: 识别和验证安全漏洞

**工具**: OWASP ZAP, Burp Suite, Snyk

**安全测试清单**:
- [ ] SQL 注入检测
- [ ] XSS 漏洞检测
- [ ] CSRF 防护验证
- [ ] 跨域资源共享 (CORS) 配置检查
- [ ] 密钥管理审查
- [ ] 依赖库漏洞扫描
- [ ] API 认证和授权测试

### 3.6 用户验收测试 (UAT)

**目的**: 验证产品是否满足业务需求

**参与者**: 产品经理、业务方、支持团队

**验收标准**:
- [ ] 功能符合 PRD 描述
- [ ] 用户界面易用
- [ ] 文档完整清晰
- [ ] 性能可接受
- [ ] 已知缺陷都在可接受范围内

---

## 4. 测试环境要求

### 测试环境配置

| 环境 | 用途 | 配置要求 |
|------|------|----------|
| **开发环境** | 开发过程中本地单元测试 | Node 18+, Docker, PostgreSQL 13+, Redis 7+ |
| **测试环境** | 集成和系统测试 | 与生产环境相同的硬件配置 (至少 50%) |
| **性能测试环境** | 负载和压力测试 | 与生产环境相同的配置 |
| **UAT 环境** | 用户验收测试 | 与生产环境相同 |

### 依赖服务

| 服务 | 要求 | 部署方式 |
|------|------|----------|
| PostgreSQL | v13+ | Docker 容器 |
| Redis | v7+ | Docker 容器 |
| SMTP | 邮件测试 | Mailhog (本地测试) / SendGrid (测试环境) |

---

## 5. 测试数据准备

### 测试账户

| 账户类型 | 邮箱 | 密码 | 用途 |
|---------|------|------|------|
| 普通用户 | test-user@example.com | Pass123456 | 基本功能测试 |
| 高级用户 | test-premium@example.com | Pass123456 | 高级功能测试 |
| 管理员 | test-admin@example.com | Pass123456 | 管理功能测试 |
| 已禁用 | test-disabled@example.com | Pass123456 | 权限测试 |

### 测试数据集

| 数据集 | 数据量 | 用途 |
|--------|--------|------|
| 用户数据 | 10,000 条 | 性能测试 |
| 审计日志 | 100,000 条 | 日志查询性能 |
| Token 数据 | 50,000 条 | 缓存性能 |

### 数据初始化脚本

提供一个初始化脚本，能够：
1. 创建测试数据库
2. 运行数据库迁移
3. 种植测试数据
4. 设置测试配置

```bash
#!/bin/bash
# 初始化测试环境
docker-compose up -d
npm run migrate
npm run seed:test-data
```

---

## 6. 测试工具与框架

### 单元和集成测试

```json
{
  "testing": {
    "framework": "Jest",
    "version": "^29.0.0",
    "description": "单元和集成测试框架"
  },
  "api-testing": {
    "framework": "Supertest",
    "version": "^6.3.0",
    "description": "HTTP API 测试库"
  },
  "test-data": {
    "tool": "Faker.js",
    "version": "^8.0.0",
    "description": "生成虚假测试数据"
  }
}
```

### 性能测试

```bash
npm install -g k6              # 性能测试工具
# 或使用 Apache JMeter / Locust
```

### 安全测试

```bash
npm audit                       # 扫描依赖漏洞
npx snyk test                   # Snyk 漏洞扫描
# 或使用 OWASP ZAP / Burp Suite
```

---

## 7. 测试执行计划

### 测试时间表

| 阶段 | 测试类型 | 开始日期 | 持续时长 | 里程碑 |
|------|---------|----------|----------|--------|
| Phase 1 | 单元测试 | [Date] | 2 周 | Unit Test Coverage >= 80% |
| Phase 2 | 集成测试 | [Date] | 2 周 | API 端到端测试通过 |
| Phase 3 | 性能测试 | [Date] | 1 周 | 性能指标达标 |
| Phase 4 | UAT | [Date] | 1 周 | 业务方签核 |

### 每日测试流程

```
9:00  - 编写新代码
11:00 - 单元测试 (自动)
15:00 - 集成测试 (自动)
17:00 - 手工功能测试
18:00 - 测试报告生成
```

---

## 8. 风险评估与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 测试环境不稳定 | Medium | High | 准备备用环境，CI/CD 健康检查 |
| 测试数据不足 | Medium | Medium | 提前生成足够的测试数据 |
| 第三方服务故障 | Low | High | Mock 第三方服务，设置超时 |
| 人力不足 | Medium | Medium | 自动化测试覆盖关键路径 |

---

## 9. 缺陷管理

### 缺陷等级定义

| 等级 | 说明 | 例子 |
|------|------|------|
| **Critical** | 功能完全不可用 | 登陆接口返回 500 错误 |
| **High** | 主要功能受影响 | 登陆失败率 > 1% |
| **Medium** | 功能有限制但可规避 | 邮件延迟 > 5 分钟 |
| **Low** | 用户体验差但不影响使用 | UI 排版不对齐 |

### 缺陷修复 SLA

| 等级 | 确认时间 | 修复时间 | 验证时间 |
|------|----------|----------|----------|
| Critical | 2 小时 | 4 小时 | 2 小时 |
| High | 4 小时 | 24 小时 | 4 小时 |
| Medium | 8 小时 | 48 小时 | 8 小时 |
| Low | 5 天 | 10 天 | 2 天 |

### 缺陷追踪系统
- 使用 Jira / GitHub Issues 追踪
- 每个缺陷需要包含：标题、描述、重现步骤、截图/日志、优先级、分配者

---

## 10. 成功标准与退出标准

### 成功标准（Entry Criteria）
- [ ] 所有需求已实现并代码评审通过
- [ ] 开发环境变更已完成
- [ ] 测试计划已编写并评审通过
- [ ] 测试数据已准备就绪
- [ ] 测试工具已安装配置

### 退出标准（Exit Criteria）
- [ ] 单元测试覆盖率 >= 80%
- [ ] Critical 和 High 级缺陷都已修复并验证
- [ ] 性能指标达到预期目标
- [ ] 安全漏洞扫描通过 (0 High+ 级漏洞)
- [ ] UAT 通过，业务方签核
- [ ] 测试报告已生成

---

## 11. 测试报告与指标

### 测试覆盖率指标

```
单元测试覆盖率：[目标 >= 80%]
集成测试覆盖率：[目标 >= 70%]
功能覆盖率：[目标 = 100%]
```

### 缺陷分布

```
Critical: [X] High: [X] Medium: [X] Low: [X]
已修复: [X%]
未修复: [X%]
```

### 性能测试结果汇总

```
平均响应时间: [Xms]
P95 响应时间: [Xms]
P99 响应时间: [Xms]
错误率: [X%]
吞吐量: [X req/s]
```

---

## 12. 测试自动化

### CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Automated Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run unit tests
        run: npm run test:unit
      - name: Run integration tests
        run: npm run test:integration
      - name: Upload coverage
        run: npm run test:coverage
```

### 自动化测试套件

| 测试套件 | 触发时机 | 执行时间 | 失败行为 |
|---------|---------|----------|---------|
| Smoke Test | 每个 PR | 5 分钟 | 阻止 Merge |
| Unit Tests | 每个 Commit | 10 分钟 | 阻止 Merge |
| Integration Tests | Pull Request | 20 分钟 | 警告 |
| Regression Tests | 夜间运行 | 30 分钟 | 邮件通知 |

---

## 13. 测试资源计划

### 人员配置

| 角色 | 人数 | 职责 |
|------|------|------|
| QA Lead | 1 | 测试计划制定、监督、报告 |
| 功能测试员 | 2 | 功能和系统测试执行 |
| 自动化测试员 | 1 | 自动化脚本编写和维护 |
| 性能测试员 | 1 | 性能和负载测试 |

### 工具投入

| 工具 | 成本 | 用途 |
|------|------|------|
| Jest (开源) | 0 | 单元测试 |
| k6 (开源) | 0 | 性能测试 |
| Jira | ¥100/月 | 缺陷追踪 |
| 测试环境 (云) | ¥500/月 | 测试执行 |

---

## 14. 变更管理

### 范围变更
如果功能需求变更，需要：
1. 识别对测试的影响
2. 调整测试计划和时间表
3. 更新测试用例
4. 重新评估覆盖率目标

### 发现新缺陷
新发现的 Critical 或 High 缺陷需要：
1. 记录在 Jira 中
2. 分配给开发团队
3. 重新执行相关测试用例
4. 验证修复

---

## 版本历史

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| v 0.1 | [YYYY-MM-DD] | [QA Lead] | 初稿 |
| v 1.0 | [YYYY-MM-DD] | [QA Lead] | 完成评审 |
