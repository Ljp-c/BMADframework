# 组件规范文档 (Component Specs)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | [项目名称] |
| 版本 | 1.0 |
| 作者 | [作者] |
| 创建日期 | [日期] |

---

## 1. 组件设计原则

- **单一职责**: 每个组件只负责一个功能
- **可复用性**: 组件应该可以在不同场景复用
- **可组合性**: 小组件组合成大组件
- **可测试性**: 组件应该易于测试
- **可访问性**: 组件应该支持无障碍访问

---

## 2. 原子组件规范

### 2.1 Button (按钮)

**Props定义**

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
```

**使用示例**

```tsx
<Button variant="primary">主要按钮</Button>
<Button variant="secondary">次要按钮</Button>
<Button size="lg" loading>加载中</Button>
```

**设计规范**

| 变体 | 背景色 | 文字色 |
|------|--------|--------|
| primary | primary-600 | white |
| secondary | gray-100 | gray-900 |
| outline | transparent | primary-600 |
| ghost | transparent | gray-700 |
| danger | error-600 | white |

---

### 2.2 Input (输入框)

**Props定义**

```typescript
interface InputProps {
  type?: 'text' | 'password' | 'email' | 'number';
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  prefix?: React.ReactNode;
  suffix?: React.ReactNode;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}
```

**使用示例**

```tsx
<Input placeholder="请输入内容" />
<Input error="不能为空" />
<Input prefix={<UserIcon />} />
```

---

### 2.3 Select (选择器)

**Props定义**

```typescript
interface SelectProps {
  options: Array<{ value: string; label: string }>;
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  multiple?: boolean;
  searchable?: boolean;
  onChange?: (value: string | string[]) => void;
}
```

---

### 2.4 Checkbox (复选框)

**Props定义**

```typescript
interface CheckboxProps {
  checked?: boolean;
  disabled?: boolean;
  indeterminate?: boolean;
  label?: string;
  onChange?: (checked: boolean) => void;
}
```

---

### 2.5 Switch (开关)

**Props定义**

```typescript
interface SwitchProps {
  checked?: boolean;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
  onChange?: (checked: boolean) => void;
}
```

---

## 3. 分子组件规范

### 3.1 FormField (表单字段)

**Props定义**

```typescript
interface FormFieldProps {
  label?: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  children: React.ReactNode;
}
```

**使用示例**

```tsx
<FormField label="用户名" required error="不能为空">
  <Input placeholder="请输入用户名" />
</FormField>
```

---

### 3.2 Card (卡片)

**Props定义**

```typescript
interface CardProps {
  title?: string;
  bordered?: boolean;
  hoverable?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
}
```

---

## 4. 有机体组件规范

### 4.1 DataTable (数据表格)

**Props定义**

```typescript
interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  rowKey: string;
  loading?: boolean;
  pagination?: { current: number; pageSize: number; total: number };
  onChange?: (pagination: any, filters: any, sorter: any) => void;
}
```

---

### 4.2 Modal (对话框)

**Props定义**

```typescript
interface ModalProps {
  open: boolean;
  title?: string;
  width?: number | string;
  closable?: boolean;
  onClose?: () => void;
  children?: React.ReactNode;
}
```

---

## 5. 组件开发规范

### 5.1 文件结构

```
ComponentName/
├── ComponentName.tsx      # 组件实现
├── ComponentName.test.tsx # 组件测试
├── index.ts               # 导出
```

### 5.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | Button |
| Props接口 | 组件名 + Props | ButtonProps |
| 文件名 | PascalCase | Button.tsx |

---

## 附录: 组件清单

| 组件 | 类型 | 状态 |
|------|------|------|
| Button | Atom | 完成 |
| Input | Atom | 完成 |
| Select | Atom | 完成 |
| Checkbox | Atom | 完成 |
| Switch | Atom | 完成 |
| FormField | Molecule | 完成 |
| Card | Molecule | 完成 |
| DataTable | Organism | 完成 |
| Modal | Organism | 完成 |

---

## 修订历史

| 版本 | 日期 | 作者 | 修改内容 |
|------|------|------|----------|
| 1.0 | [日期] | [作者] | 初始版本 |
