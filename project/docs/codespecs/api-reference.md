# API参考文档 (API Reference)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | [项目名称] |
| 版本 | 1.0 |
| Base URL | https://api.example.com/v1 |

---

## 1. API概述

### 1.1 认证方式

**Bearer Token 认证**

```http
Authorization: Bearer <access_token>
```

### 1.2 通用响应格式

**成功响应**

```json
{
  "code": 200,
  "message": "Success",
  "data": {}
}
```

**错误响应**

```json
{
  "code": 400,
  "message": "Bad Request",
  "errors": []
}
```

---

## 2. 认证接口

### 2.1 用户登录

**POST** `/auth/login`

**请求参数**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 用户密码 |

**请求示例**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应示例**

```json
{
  "code": 200,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token",
    "expiresAt": "2024-01-01T00:00:00Z"
  }
}
```

---

### 2.2 用户注册

**POST** `/auth/register`

**请求参数**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 用户密码 |
| name | string | 是 | 用户名称 |

---

## 3. 用户接口

### 3.1 获取当前用户

**GET** `/users/me`

**请求头**: Authorization: Bearer Token

**响应示例**

```json
{
  "code": 200,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "status": "active"
  }
}
```

---

### 3.2 更新用户信息

**PUT** `/users/me`

**请求参数**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| name | string | 否 | 用户名称 |
| avatar | string | 否 | 头像URL |

---

### 3.3 获取用户列表

**GET** `/users`

**查询参数**

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| limit | integer | 否 | 10 | 每页数量 |
| search | string | 否 | - | 搜索关键词 |

---

## 4. HTTP状态码

| 状态码 | 描述 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 修订历史

| 版本 | 日期 | 作者 | 修改内容 |
|------|------|------|----------|
| 1.0 | [日期] | [作者] | 初始版本 |
