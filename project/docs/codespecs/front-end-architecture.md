# 前端架构文档 (Front-end Architecture)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | [项目名称] |
| 版本 | 1.0 |
| 架构师 | [姓名] |
| 创建日期 | [日期] |

---

## 1. 架构概述

### 1.1 设计目标

- **高性能**: 首屏加载 < 3秒
- **可维护性**: 清晰的代码结构
- **可扩展性**: 支持功能扩展
- **用户体验**: 流畅的交互

### 1.2 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 框架 | React 18 | 团队熟悉，生态丰富 |
| 语言 | TypeScript | 类型安全 |
| 状态管理 | Zustand + React Query | 轻量，分离关注点 |
| 样式方案 | Tailwind CSS | 原子化，快速开发 |

---

## 2. 项目结构

```
src/
├── assets/                    # 静态资源
├── components/               # 组件
│   ├── atoms/               # 原子组件
│   ├── molecules/           # 分子组件
│   ├── organisms/           # 有机体组件
│   └── templates/           # 页面模板
├── pages/                    # 页面组件
├── hooks/                    # 自定义Hooks
├── services/                 # API服务
├── stores/                   # 状态管理
├── types/                    # 类型定义
├── utils/                    # 工具函数
└── styles/                   # 全局样式
```

---

## 3. 组件架构

### 3.1 组件层次

```
Pages → Templates → Organisms → Molecules → Atoms
```

### 3.2 原子组件

| 组件 | 描述 |
|------|------|
| Button | 按钮 |
| Input | 输入框 |
| Text | 文本 |
| Icon | 图标 |
| Badge | 徽章 |
| Avatar | 头像 |

### 3.3 分子组件

| 组件 | 描述 | 组成 |
|------|------|------|
| FormField | 表单字段 | Label + Input + Error |
| SearchBar | 搜索栏 | Input + Button |
| UserCard | 用户卡片 | Avatar + Text |

### 3.4 有机体组件

| 组件 | 描述 |
|------|------|
| Header | 页头 |
| Sidebar | 侧边栏 |
| DataTable | 数据表格 |
| Form | 表单 |

---

## 4. 状态管理

### 4.1 状态分类

```
┌─────────────────────────────────────┐
│  服务端状态 (React Query)            │
│  - 用户数据, 列表数据, 缓存数据        │
├─────────────────────────────────────┤
│  全局状态 (Zustand)                  │
│  - 认证状态, UI状态, 用户偏好         │
├─────────────────────────────────────┤
│  组件状态 (useState)                 │
│  - 表单状态, UI交互状态               │
└─────────────────────────────────────┘
```

### 4.2 Zustand Store示例

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
);
```

---

## 5. API层设计

### 5.1 API客户端

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 5.2 服务层

```typescript
export const userService = {
  getCurrentUser: () => api.get<User>('/users/me'),
  updateUser: (id: string, data: UpdateUserInput) =>
    api.put<User>(`/users/${id}`, data),
};
```

---

## 6. 性能优化

### 6.1 代码分割

```typescript
const Dashboard = lazy(() => import('@/pages/Dashboard'));
```

### 6.2 虚拟列表

使用 @tanstack/react-virtual 处理大列表

### 6.3 图片优化

- 懒加载
- 响应式图片
- WebP格式

---

## 修订历史

| 版本 | 日期 | 作者 | 修改内容 |
|------|------|------|----------|
| 1.0 | [日期] | [作者] | 初始版本 |
