# Coding Standards (编码规范) - 智能体对话记录

## 文档信息

> **Dev**: 本文档记录了编码规范讨论的智能体对话交互过程。我们确定了团队的编码规范，确保代码风格统一、可读性强、易于维护。

---

## 第一轮对话：通用原则

### 话题：核心编码原则

**Dev**: 我来定义团队编码规范。首先明确核心原则。

**Architect**: 请说明核心原则。

**Dev**: 

**1. 可读性优先**: 代码首先是给人看的，其次才是给机器执行的

**2. 一致性**: 保持代码风格的一致性

**3. 简洁性**: 简单直接的解决方案优于复杂的方案

**4. 可维护性**: 编写易于理解和修改的代码

### 话题：命名规范

**Dev**: 命名规范：

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量 | camelCase | `userName`, `totalCount` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 函数 | camelCase | `getUserInfo` |
| 类/组件 | PascalCase | `UserService` |
| 接口 | PascalCase | `IUser` 或 `User` |
| 文件名 | kebab-case | `user-service.ts` |
| 组件文件 | PascalCase | `Button.tsx` |

**命名要有意义**:

```typescript
// ❌ 不好的命名
const d = new Date();
function process(data) { }

// ✅ 好的命名
const currentDate = new Date();
function validateUserData(userData) { }
```

---

## 第二轮对话：TypeScript规范

### 话题：类型定义

**Dev**: TypeScript类型定义规范：

```typescript
// ✅ 使用 interface 定义对象类型
interface User {
  id: string;
  name: string;
  email: string;
}

// ✅ 使用 type 定义联合类型
type Status = 'active' | 'inactive' | 'pending';

// ✅ 避免使用 any
function processData(data: unknown) {
  if (typeof data === 'string') {
    // ...
  }
}
```

**Architect**: 函数定义有什么规范？

**Dev**: 函数定义规范：

```typescript
// ✅ 明确参数和返回类型
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ 可选参数放在最后
function createUser(name: string, email: string, role?: UserRole): User {
  // ...
}

// ✅ 使用默认参数
function greet(name: string, greeting: string = 'Hello'): string {
  return `${greeting}, ${name}!`;
}
```

---

## 第三轮对话：React规范

### 话题：组件定义

**Dev**: React组件规范：

```typescript
// ✅ 函数组件 + TypeScript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
}
```

**DesignArchitect**: Hooks有什么规范？

**Dev**: Hooks规范：

```typescript
// ✅ Hooks 放在组件顶部
function UserProfile({ userId }: UserProfileProps) {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();
  
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
  
  // ...
}

// ✅ 自定义 Hook 以 use 开头
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    // ...
  }, [userId]);
  
  return { user };
}
```

---

## 第四轮对话：文件组织

### 话题：文件结构

**Dev**: 文件组织规范：

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
├── hooks/
│   ├── useUser.ts
│   └── useApi.ts
├── services/
│   ├── api.ts
│   └── user.service.ts
├── types/
│   ├── user.ts
│   └── api.ts
└── utils/
    ├── format.ts
    └── validation.ts
```

### 话题：导入顺序

**Dev**: 导入顺序规范：

```typescript
// 1. 外部依赖
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// 2. 内部模块（绝对路径）
import { Button } from '@/components/Button';
import { useUser } from '@/hooks/useUser';

// 3. 相对路径
import { LocalComponent } from './LocalComponent';

// 4. 样式文件
import styles from './Component.module.css';

// 5. 类型导入（单独分组）
import type { User } from '@/types/user';
```

---

## 第五轮对话：Git规范

### 话题：分支命名

**Dev**: Git分支命名规范：

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | feature/描述 | feature/user-auth |
| 修复 | fix/描述 | fix/login-error |
| 重构 | refactor/描述 | refactor/user-service |
| 文档 | docs/描述 | docs/api-documentation |

### 话题：Commit规范

**Dev**: Commit规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:

| 类型 | 描述 |
|------|------|
| feat | 新功能 |
| fix | 修复Bug |
| docs | 文档更新 |
| style | 代码格式 |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具 |

**示例**:

```
feat(auth): 添加用户登录功能

- 实现登录表单验证
- 添加JWT认证
- 添加登录状态持久化

Closes #123
```

---

## 第六轮对话：测试规范

### 话题：测试文件命名

**Dev**: 测试文件命名规范：

| 类型 | 命名 | 示例 |
|------|------|------|
| 单元测试 | *.test.ts | user.test.ts |
| 组件测试 | *.test.tsx | Button.test.tsx |
| 集成测试 | *.spec.ts | api.spec.ts |

### 话题：测试结构

**Dev**: 测试结构规范：

```typescript
describe('UserService', () => {
  describe('getUser', () => {
    it('should return user when user exists', async () => {
      // Arrange
      const userId = '123';
      
      // Act
      const user = await userService.getUser(userId);
      
      // Assert
      expect(user).toBeDefined();
      expect(user.id).toBe(userId);
    });
    
    it('should throw error when user not found', async () => {
      // ...
    });
  });
});
```

---

## 对话总结

**Dev**: 编码规范定义完成：

1. **命名规范**：camelCase/PascalCase/kebab-case
2. **TypeScript规范**：类型定义、函数定义
3. **React规范**：组件定义、Hooks规范
4. **文件组织**：目录结构、导入顺序
5. **Git规范**：分支命名、Commit规范
6. **测试规范**：测试命名、测试结构

**Architect**: 规范清晰，团队统一遵守。

**QA**: 我会基于规范编写测试用例。

---

## 代码审查清单

### 提交前检查
- [ ] 代码符合命名规范
- [ ] 代码有适当的注释
- [ ] 没有未使用的代码和导入
- [ ] 没有 console.log 等调试代码
- [ ] 类型定义完整，没有 any
- [ ] 测试用例已添加
- [ ] 测试全部通过
- [ ] ESLint 检查通过
- [ ] Prettier 格式化完成

---

**文档版本**: 1.0  
**最后更新**: 2026年3月10日
