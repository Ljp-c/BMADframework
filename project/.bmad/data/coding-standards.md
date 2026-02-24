# Coding Standards (编码规范)

## 使用说明

本文档定义团队的编码规范，确保代码风格统一、可读性强、易于维护。所有团队成员应严格遵守本规范。

---

## 1. 通用原则

### 1.1 核心原则
- **可读性优先**: 代码首先是给人看的，其次才是给机器执行的
- **一致性**: 保持代码风格的一致性
- **简洁性**: 简单直接的解决方案优于复杂的方案
- **可维护性**: 编写易于理解和修改的代码

### 1.2 命名规范

#### 通用命名规则
| 类型 | 规范 | 示例 |
|------|------|------|
| 变量 | camelCase | `userName`, `totalCount` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_BASE_URL` |
| 函数 | camelCase | `getUserInfo`, `calculateTotal` |
| 类/组件 | PascalCase | `UserService`, `UserProfile` |
| 接口 | PascalCase (I前缀可选) | `IUser` 或 `User` |
| 类型别名 | PascalCase | `UserStatus`, `ApiResponse` |
| 枚举 | PascalCase | `UserRole`, `HttpStatus` |
| 文件名 | kebab-case | `user-service.ts`, `api-client.ts` |
| 组件文件 | PascalCase | `UserProfile.tsx`, `Button.tsx` |

#### 命名要有意义
```typescript
// ❌ 不好的命名
const d = new Date();
const arr = users.filter(u => u.a);
function process(data) { }

// ✅ 好的命名
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
function validateUserData(userData) { }
```

### 1.3 注释规范

#### 注释原则
- 代码应自解释，减少不必要的注释
- 注释说明"为什么"而不是"是什么"
- 保持注释与代码同步更新

#### 注释格式
```typescript
/**
 * 函数说明
 * @param paramName 参数说明
 * @returns 返回值说明
 */
function functionName(paramName: Type): ReturnType {
  // 单行注释
  
  /*
   * 多行注释
   * 第二行
   */
}

// TODO: 待办事项
// FIXME: 需要修复的问题
// HACK: 临时解决方案
// NOTE: 重要说明
```

---

## 2. TypeScript 规范

### 2.1 类型定义

```typescript
// ✅ 使用 interface 定义对象类型
interface User {
  id: string;
  name: string;
  email: string;
}

// ✅ 使用 type 定义联合类型、工具类型
type Status = 'active' | 'inactive' | 'pending';
type UserKeys = keyof User;

// ✅ 避免使用 any，使用 unknown 替代
function processData(data: unknown) {
  if (typeof data === 'string') {
    // ...
  }
}

// ✅ 使用严格类型
const users: User[] = [];
const userMap: Map<string, User> = new Map();
```

### 2.2 函数定义

```typescript
// ✅ 明确参数和返回类型
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ 使用箭头函数作为回调
const activeUsers = users.filter((user) => user.isActive);

// ✅ 可选参数放在最后
function createUser(name: string, email: string, role?: UserRole): User {
  // ...
}

// ✅ 使用默认参数
function greet(name: string, greeting: string = 'Hello'): string {
  return `${greeting}, ${name}!`;
}
```

### 2.3 类定义

```typescript
// ✅ 使用 class 定义
class UserService {
  private readonly apiClient: ApiClient;
  
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }
  
  async getUser(id: string): Promise<User> {
    return this.apiClient.get(`/users/${id}`);
  }
}

// ✅ 使用 private/protected/public 明确可见性
class User {
  public id: string;
  protected createdAt: Date;
  private password: string;
}
```

---

## 3. React 规范

### 3.1 组件定义

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

// ✅ 使用 React.FC (可选，团队统一即可)
export const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  // ...
};
```

### 3.2 Hooks 规范

```typescript
// ✅ Hooks 放在组件顶部
function UserProfile({ userId }: UserProfileProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
  
  // ...
}

// ✅ 自定义 Hook 以 use 开头
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // ...
  }, [userId]);
  
  return { user, loading };
}
```

### 3.3 事件处理

```typescript
// ✅ 事件处理函数以 handle 开头
function UserForm() {
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // ...
  };
  
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // ...
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleInputChange} />
    </form>
  );
}
```

---

## 4. CSS 规范

### 4.1 Tailwind CSS 规范

```tsx
// ✅ 类名按逻辑分组，用空格分隔
<button className="
  inline-flex items-center justify-center
  px-4 py-2
  bg-blue-500 hover:bg-blue-600
  text-white font-medium
  rounded-lg transition-colors
">
  Button
</button>

// ✅ 提取重复的样式为组件
const buttonVariants = {
  primary: 'bg-blue-500 hover:bg-blue-600 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
};
```

### 4.2 CSS Modules 规范

```css
/* 使用 camelCase 命名类 */
.container {
  /* ... */
}

.headerTitle {
  /* ... */
}

/* 使用 BEM 命名（可选） */
.card {}
.card__header {}
.card__title {}
.card--featured {}
```

---

## 5. 文件组织规范

### 5.1 文件结构

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx        # 组件实现
│   │   ├── Button.test.tsx   # 组件测试
│   │   ├── Button.module.css # 组件样式
│   │   └── index.ts          # 导出
│   └── ...
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

### 5.2 导入顺序

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

## 6. Git 规范

### 6.1 分支命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | feature/描述 | feature/user-authentication |
| 修复 | fix/描述 | fix/login-error |
| 重构 | refactor/描述 | refactor/user-service |
| 文档 | docs/描述 | docs/api-documentation |

### 6.2 Commit 规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型
| 类型 | 描述 |
|------|------|
| feat | 新功能 |
| fix | 修复Bug |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具相关 |

#### 示例
```
feat(auth): 添加用户登录功能

- 实现登录表单验证
- 添加JWT认证
- 添加登录状态持久化

Closes #123
```

---

## 7. 测试规范

### 7.1 测试文件命名

| 类型 | 命名 | 示例 |
|------|------|------|
| 单元测试 | *.test.ts | user.test.ts |
| 组件测试 | *.test.tsx | Button.test.tsx |
| 集成测试 | *.spec.ts | api.spec.ts |
| E2E测试 | *.cy.ts | login.cy.ts |

### 7.2 测试结构

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

## 8. 代码审查清单

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

## 更新记录

| 日期 | 更新人 | 更新内容 |
|------|--------|----------|
| [日期] | [姓名] | 初始版本 |

---

*本规范应定期审查和更新，以适应技术发展和团队需求变化。*
