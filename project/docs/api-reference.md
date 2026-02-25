# API参考文档 (API Reference) - 智能体对话记录

## 文档信息

> **Dev**: 本文档记录了API设计阶段的智能体对话交互过程。基于功能需求，我定义了API接口规范。

---

## 第一轮对话：API概述

### 话题：API设计规范

**Dev**: API设计遵循以下规范：

**Architect**: 请说明认证方式和响应格式。

**Dev**: 

**认证方式**：Bearer Token

```http
Authorization: Bearer <access_token>
```

**通用响应格式**：

**成功响应**:

```json
{
  "code": 200,
  "message": "Success",
  "data": {}
}
```

**错误响应**:

```json
{
  "code": 400,
  "message": "Bad Request",
  "errors": [
    { "field": "email", "message": "邮箱格式不正确" }
  ]
}
```

---

## 第二轮对话：认证接口

### 话题：用户登录

**Dev**: POST `/api/v1/auth/login`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 用户密码 |

**请求示例**:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "用户名称"
    },
    "token": "jwt_token",
    "expiresAt": "2026-03-01T00:00:00Z"
  }
}
```

**QA**: 错误场景如何处理？

**Dev**: 错误响应：

```json
{
  "code": 401,
  "message": "认证失败",
  "errors": [
    { "field": "password", "message": "密码错误" }
  ]
}
```

### 话题：用户注册

**Dev**: POST `/api/v1/auth/register`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 用户密码（8-64位） |
| name | string | 是 | 用户名称 |

### 话题：微信登录

**Dev**: POST `/api/v1/auth/wechat`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| code | string | 是 | 微信授权码 |

---

## 第三轮对话：收藏接口

### 话题：获取收藏列表

**Dev**: GET `/api/v1/collections`

**查询参数**:

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| limit | integer | 否 | 20 | 每页数量 |
| ip_series | string | 否 | - | IP系列筛选 |
| status | string | 否 | - | 状态筛选 |

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "uuid",
        "ipSeries": "Labubu",
        "modelName": "森林音乐会",
        "purchasePrice": 599,
        "purchaseDate": "2026-01-15",
        "status": "owned"
      }
    ],
    "pagination": {
      "current": 1,
      "pageSize": 20,
      "total": 50
    }
  }
}
```

### 话题：创建收藏

**Dev**: POST `/api/v1/collections`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ip_series | string | 是 | IP系列 |
| model_name | string | 是 | 款式名称 |
| purchase_price | number | 否 | 购买价格 |
| purchase_date | string | 否 | 购买日期 |
| notes | string | 否 | 备注 |

### 话题：更新收藏

**Dev**: PUT `/api/v1/collections/:id`

### 话题：删除收藏

**Dev**: DELETE `/api/v1/collections/:id`

---

## 第四轮对话：估价接口

### 话题：生成估价

**Dev**: POST `/api/v1/valuations`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| collection_id | string | 是 | 收藏ID |

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "id": "uuid",
    "collectionId": "uuid",
    "estimatedPrice": 899,
    "priceRangeLow": 800,
    "priceRangeHigh": 1000,
    "analysis": {
      "marketTrend": "上涨",
      "factors": ["限量款", "热门IP"],
      "recommendation": "建议持有"
    },
    "createdAt": "2026-02-25T10:00:00Z"
  }
}
```

**QA**: 估价超时如何处理？

**Dev**: 超时响应（504）：

```json
{
  "code": 504,
  "message": "估价服务响应超时，请稍后重试"
}
```

### 话题：获取估价历史

**Dev**: GET `/api/v1/valuations?collection_id=:id`

---

## 第五轮对话：用户接口

### 话题：获取当前用户

**Dev**: GET `/api/v1/users/me`

**请求头**: Authorization: Bearer Token

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "用户名称",
    "subscription": "pro",
    "collectionCount": 15,
    "totalValue": 15000
  }
}
```

### 话题：更新用户信息

**Dev**: PUT `/api/v1/users/me`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| name | string | 否 | 用户名称 |
| avatar_url | string | 否 | 头像URL |

---

## 第六轮对话：订阅接口

### 话题：获取订阅状态

**Dev**: GET `/api/v1/subscriptions`

### 话题：创建订阅

**Dev**: POST `/api/v1/subscriptions`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| plan | string | 是 | 订阅计划（pro_monthly/pro_yearly） |

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "checkoutUrl": "https://polar.sh/checkout/xxx"
  }
}
```

---

## 第七轮对话：错误码定义

### 话题：HTTP状态码

**Dev**: HTTP状态码定义：

| 状态码 | 描述 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 验证错误 |
| 429 | 请求过于频繁 |
| 500 | 服务器错误 |
| 503 | 服务不可用 |
| 504 | 网关超时 |

### 话题：业务错误码

**Dev**: 业务错误码：

| 错误码 | 描述 |
|--------|------|
| AUTH_001 | 邮箱或密码错误 |
| AUTH_002 | Token已过期 |
| AUTH_003 | 账户已被禁用 |
| COLL_001 | 收藏数量已达上限 |
| COLL_002 | 收藏不存在 |
| SUB_001 | 订阅已过期 |
| SUB_002 | 需要Pro订阅 |

---

## 对话总结

**Dev**: API参考文档完成：

1. **认证接口**：登录、注册、微信登录
2. **收藏接口**：CRUD操作
3. **估价接口**：生成估价、历史记录
4. **用户接口**：用户信息管理
5. **订阅接口**：订阅管理
6. **错误码**：HTTP状态码和业务错误码

**Architect**: API设计符合RESTful规范。

**QA**: 我会基于此文档编写API测试用例。

---

**文档版本**: 1.0  
**最后更新**: 2026年3月7日
