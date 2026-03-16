# 数据模型文档 (Data Models)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | [项目名称] |
| 版本 | 1.0 |
| 作者 | [作者] |
| 创建日期 | [日期] |

---

## 1. 数据模型概览

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │    Role     │       │ Permission  │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │───┐   │ id          │───┐   │ id          │
│ email       │   │   │ name        │   │   │ name        │
│ password    │   │   │ code        │   │   │ resource    │
│ name        │   │   └─────────────┘   │   │ action      │
│ status      │   │         │           │   └─────────────┘
└─────────────┘   │         │           │         │
                  │         ▼           │         │
                  │   ┌─────────────┐   │         │
                  └──▶│ user_roles  │◀──┘         │
                      ├─────────────┤             │
                      │ user_id(FK) │             │
                      │ role_id(FK) │             │
                      └─────────────┘             │
                                                  │
                          ┌─────────────┐         │
                          │ role_perms  │◀────────┘
                          ├─────────────┤
                          │ role_id(FK) │
                          │ perm_id(FK) │
                          └─────────────┘
```

---

## 2. 数据表定义

### 2.1 User (用户表)

**表名**: `users`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 用户唯一标识 |
| email | VARCHAR(255) | 否 | UNIQUE | 用户邮箱 |
| password | VARCHAR(255) | 否 | - | 密码(加密) |
| name | VARCHAR(100) | 否 | - | 用户名称 |
| status | VARCHAR(20) | 否 | DEFAULT 'active' | 状态 |
| created_at | TIMESTAMP | 否 | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | 否 | DEFAULT NOW() | 更新时间 |

**Prisma Schema**:

```prisma
model User {
  id        String    @id @default(uuid())
  email     String    @unique @db.VarChar(255)
  password  String    @db.VarChar(255)
  name      String    @db.VarChar(100)
  status    UserStatus @default(ACTIVE)
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")
  
  @@map("users")
}

enum UserStatus {
  ACTIVE
  INACTIVE
  BANNED
}
```

---

### 2.2 Role (角色表)

**表名**: `roles`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 角色唯一标识 |
| name | VARCHAR(50) | 否 | UNIQUE | 角色名称 |
| code | VARCHAR(50) | 否 | UNIQUE | 角色代码 |
| description | TEXT | 是 | - | 角色描述 |

---

### 2.3 Permission (权限表)

**表名**: `permissions`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 权限唯一标识 |
| name | VARCHAR(100) | 否 | - | 权限名称 |
| code | VARCHAR(100) | 否 | UNIQUE | 权限代码 |
| resource | VARCHAR(100) | 否 | - | 资源名称 |
| action | VARCHAR(50) | 否 | - | 操作类型 |

---

## 修订历史

| 版本 | 日期 | 作者 | 修改内容 |
|------|------|------|----------|
| 1.0 | [日期] | [作者] | 初始版本 |
