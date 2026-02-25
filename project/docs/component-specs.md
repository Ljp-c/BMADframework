# 组件规范文档 (Component Specs) - 智能体对话记录

## 文档信息

> **DesignArchitect**: 本文档记录了组件规范定义阶段的智能体对话交互过程。基于前端架构，我与开发团队讨论确定了具体组件的设计规范。

---

## 第一轮对话：组件设计原则

### 话题：核心设计原则

**DesignArchitect**: 组件设计遵循以下原则：

**Dev**: 请详细说明每个原则的具体应用。

**DesignArchitect**: 

**1. 单一职责**: 每个组件只负责一个功能
- Button组件只负责按钮渲染
- 不在Button中处理业务逻辑

**2. 可复用性**: 组件可以在不同场景复用
- 通过props控制变体
- 不耦合具体业务数据

**3. 可组合性**: 小组件组合成大组件
- FormField = Label + Input + Error
- Card = Header + Body + Footer

**4. 可测试性**: 组件应该易于测试
- 纯函数组件优先
- 隔离外部依赖

**5. 可访问性**: 组件支持无障碍访问
- 语义化HTML
- 键盘导航支持
- ARIA属性

---

## 第二轮对话：原子组件规范

### 话题：Button组件

**DesignArchitect**: Button组件规范：

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

**Dev**: 使用示例？

**DesignArchitect**: 

```tsx
<Button variant="primary">主要按钮</Button>
<Button variant="secondary">次要按钮</Button>
<Button size="lg" loading>加载中</Button>
<Button leftIcon={<PlusIcon />}>添加收藏</Button>
```

**QA**: 我需要确认各变体的视觉规范。

**DesignArchitect**: Button设计规范：

| 变体 | 背景色 | 文字色 | 边框 |
|------|--------|--------|------|
| primary | primary-600 | white | 无 |
| secondary | gray-100 | gray-900 | 无 |
| outline | transparent | primary-600 | primary-600 |
| ghost | transparent | gray-700 | 无 |
| danger | error-600 | white | 无 |

### 话题：Input组件

**DesignArchitect**: Input组件规范：

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

**使用示例**:

```tsx
<Input placeholder="请输入内容" />
<Input error="不能为空" />
<Input prefix={<UserIcon />} />
<Input type="password" suffix={<EyeIcon />} />
```

### 话题：Select组件

**DesignArchitect**: Select组件规范：

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

**Dev**: 对于收藏管理的IP系列选择，这个组件够用吗？

**DesignArchitect**: 对于IP系列选择，可以配置searchable支持搜索：

```tsx
<Select
  options={ipSeriesOptions}
  placeholder="选择IP系列"
  searchable
  onChange={handleSelect}
/>
```

---

## 第三轮对话：分子组件规范

### 话题：FormField组件

**DesignArchitect**: FormField组件是表单的核心分子组件：

```typescript
interface FormFieldProps {
  label?: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  children: React.ReactNode;
}
```

**使用示例**:

```tsx
<FormField label="用户名" required error="不能为空">
  <Input placeholder="请输入用户名" />
</FormField>
```

**Dev**: 这个组件封装了表单字段的通用布局。

### 话题：Card组件

**DesignArchitect**: Card组件用于内容展示：

```typescript
interface CardProps {
  title?: string;
  bordered?: boolean;
  hoverable?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
}
```

**QA**: 收藏卡片如何设计？

**DesignArchitect**: 收藏卡片是特定的Card变体：

```typescript
interface CollectionCardProps {
  collection: Collection;
  onEdit?: () => void;
  onDelete?: () => void;
  onValuate?: () => void;
}

// 使用
<CollectionCard 
  collection={collection}
  onValuate={handleValuate}
/>
```

---

## 第四轮对话：有机体组件规范

### 话题：DataTable组件

**DesignArchitect**: DataTable组件用于列表展示：

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

**Dev**: 收藏列表如何使用这个组件？

**DesignArchitect**: 

```tsx
const columns: Column<Collection>[] = [
  { key: 'name', title: '名称', dataIndex: 'modelName' },
  { key: 'ipSeries', title: 'IP系列', dataIndex: 'ipSeries' },
  { key: 'price', title: '购买价格', dataIndex: 'purchasePrice' },
  { key: 'actions', title: '操作', render: (record) => <Actions /> },
];

<DataTable
  columns={columns}
  data={collections}
  rowKey="id"
  loading={isLoading}
  pagination={{ current: 1, pageSize: 20, total: 100 }}
/>
```

### 话题：Modal组件

**DesignArchitect**: Modal对话框组件：

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

**使用示例**:

```tsx
<Modal open={isOpen} title="添加收藏" onClose={handleClose}>
  <CollectionForm onSubmit={handleSubmit} />
</Modal>
```

---

## 第五轮对话：组件开发规范

### 话题：文件结构与命名

**DesignArchitect**: 组件开发规范：

**文件结构**:

```
ComponentName/
├── ComponentName.tsx      # 组件实现
├── ComponentName.test.tsx # 组件测试
├── index.ts               # 导出
```

**命名规范**:

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | Button |
| Props接口 | 组件名 + Props | ButtonProps |
| 文件名 | PascalCase | Button.tsx |
| Hook名 | use + 功能 | useAuth |
| 工具函数 | camelCase | formatDate |

**Dev**: 测试如何编写？

**DesignArchitect**: 测试规范：

```typescript
// Button.test.tsx
describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('handles click', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

---

## 对话总结

**DesignArchitect**: 组件规范定义完成：

1. **原子组件**：Button, Input, Select, Checkbox, Switch
2. **分子组件**：FormField, Card, SearchBar
3. **有机体组件**：DataTable, Modal, CollectionList
4. **开发规范**：文件结构、命名规范、测试规范

**Dev**: 规范清晰，我开始实现组件库。

**QA**: 我会为每个组件编写测试用例。

---

## 附录：组件清单

| 组件 | 类型 | 状态 |
|------|------|------|
| Button | Atom | 待开发 |
| Input | Atom | 待开发 |
| Select | Atom | 待开发 |
| Checkbox | Atom | 待开发 |
| Switch | Atom | 待开发 |
| FormField | Molecule | 待开发 |
| Card | Molecule | 待开发 |
| DataTable | Organism | 待开发 |
| Modal | Organism | 待开发 |

---

**文档版本**: 1.0  
**最后更新**: 2026年3月7日
