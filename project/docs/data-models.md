# 数据模型文档 (Data Models) - 智能体对话记录

## 文档信息

> **Architect**: 本文档记录了数据模型设计阶段的智能体对话交互过程。基于PRD功能需求，我定义了数据库表结构和数据关系。

---

## 第一轮对话：数据模型概览

### 话题：实体关系设计

**Architect**: 展示数据模型整体设计：

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │ Collection  │       │  Valuation  │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │───┐   │ id          │───┐   │ id          │
│ email       │   │   │ user_id(FK) │   │   │ collection_id(FK)│
│ name        │   │   │ ip_series   │   │   │ estimated_price    │
│ subscription│   │   │ model_name  │   │   │ analysis    │
│ status      │   │   │ purchase_price  │   │ created_at  │
└─────────────┘   │   │ purchase_date   │   └─────────────┘
                  │   │ status      │
                  │   └─────────────┘
                  │
                  │       ┌─────────────┐
                  │       │  PriceData  │
                  │       ├─────────────┤
                  │       │ id          │
                  │       │ ip_series   │
                  │       │ model_name  │
                  │       │ official_price   │
                  │       │ market_price     │
                  │       │ trend       │
                  │       └─────────────┘
```

**Dev**: 数据表之间的关系需要明确。

**Architect**: 实体关系说明：
- User 1:N Collection（一个用户多个收藏）
- Collection 1:N Valuation（一个收藏多次估价）
- PriceData 独立表（预设价格数据）

---

## 第二轮对话：数据表定义

### 话题：User用户表

**Architect**: User表定义：

**表名**: `users`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 用户唯一标识 |
| email | VARCHAR(255) | 否 | UNIQUE | 用户邮箱 |
| name | VARCHAR(100) | 否 | - | 用户名称 |
| avatar_url | VARCHAR(500) | 是 | - | 头像URL |
| subscription | VARCHAR(20) | 否 | DEFAULT 'free' | 订阅状态 |
| status | VARCHAR(20) | 否 | DEFAULT 'active' | 状态 |
| created_at | TIMESTAMP | 否 | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | 否 | DEFAULT NOW() | 更新时间 |

**Dev**: Prisma Schema如何定义？

**Architect**: 

```prisma
model User {
  id           String       @id @default(uuid())
  email        String       @unique @db.VarChar(255)
  name         String       @db.VarChar(100)
  avatarUrl    String?      @map("avatar_url") @db.VarChar(500)
  subscription Subscription @default(FREE)
  status       UserStatus   @default(ACTIVE)
  createdAt    DateTime     @default(now()) @map("created_at")
  updatedAt    DateTime     @updatedAt @map("updated_at")
  collections  Collection[]
  
  @@map("users")
}

enum Subscription {
  FREE
  PRO
}

enum UserStatus {
  ACTIVE
  INACTIVE
  BANNED
}
```

### 话题：Collection收藏表

**Architect**: Collection表定义：

**表名**: `collections`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 收藏唯一标识 |
| user_id | UUID | 否 | FOREIGN KEY | 所属用户ID |
| ip_series | VARCHAR(50) | 否 | - | IP系列 |
| model_name | VARCHAR(100) | 否 | - | 款式名称 |
| purchase_price | DECIMAL(10,2) | 是 | - | 购买价格 |
| purchase_date | DATE | 是 | - | 购买日期 |
| notes | TEXT | 是 | - | 备注 |
| status | VARCHAR(20) | 否 | DEFAULT 'owned' | 状态 |
| created_at | TIMESTAMP | 否 | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | 否 | DEFAULT NOW() | 更新时间 |

```prisma
model Collection {
  id            UUID         @id @default(uuid())
  userId        String       @map("user_id")
  ipSeries      String       @map("ip_series") @db.VarChar(50)
  modelName     String       @map("model_name") @db.VarChar(100)
  purchasePrice Decimal?     @map("purchase_price") @db.Decimal(10, 2)
  purchaseDate  DateTime?    @map("purchase_date") @db.Date
  notes         String?      @db.Text
  status        CollectionStatus @default(OWNED)
  createdAt     DateTime     @default(now()) @map("created_at")
  updatedAt     DateTime     @updatedAt @map("updated_at")
  
  user          User         @relation(fields: [userId], references: [id])
  valuations    Valuation[]
  
  @@map("collections")
}

enum CollectionStatus {
  OWNED
  SOLD
  WISHLIST
}
```

### 话题：Valuation估价表

**Architect**: Valuation表定义：

**表名**: `valuations`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 估价唯一标识 |
| collection_id | UUID | 否 | FOREIGN KEY | 收藏ID |
| estimated_price | DECIMAL(10,2) | 否 | - | 估价金额 |
| price_range_low | DECIMAL(10,2) | 是 | - | 价格区间下限 |
| price_range_high | DECIMAL(10,2) | 是 | - | 价格区间上限 |
| analysis | JSONB | 是 | - | AI分析结果 |
| created_at | TIMESTAMP | 否 | DEFAULT NOW() | 创建时间 |

```prisma
model Valuation {
  id             String   @id @default(uuid())
  collectionId   String   @map("collection_id")
  estimatedPrice Decimal  @map("estimated_price") @db.Decimal(10, 2)
  priceRangeLow  Decimal? @map("price_range_low") @db.Decimal(10, 2)
  priceRangeHigh Decimal? @map("price_range_high") @db.Decimal(10, 2)
  analysis       Json?    @db.JsonB
  createdAt      DateTime @default(now()) @map("created_at")
  
  collection     Collection @relation(fields: [collectionId], references: [id])
  
  @@map("valuations")
}
```

### 话题：PriceData预设价格表

**Architect**: PriceData表定义：

**表名**: `price_data`

| 字段名 | 数据类型 | 可空 | 约束 | 描述 |
|--------|----------|------|------|------|
| id | UUID | 否 | PRIMARY KEY | 唯一标识 |
| ip_series | VARCHAR(50) | 否 | - | IP系列 |
| model_name | VARCHAR(100) | 否 | - | 款式名称 |
| official_price | DECIMAL(10,2) | 否 | - | 官方发售价 |
| market_price | DECIMAL(10,2) | 否 | - | 市场参考价 |
| trend | VARCHAR(20) | 是 | - | 价格趋势 |
| last_updated | TIMESTAMP | 否 | DEFAULT NOW() | 最后更新时间 |

```prisma
model PriceData {
  id            String   @id @default(uuid())
  ipSeries      String   @map("ip_series") @db.VarChar(50)
  modelName     String   @map("model_name") @db.VarChar(100)
  officialPrice Decimal  @map("official_price") @db.Decimal(10, 2)
  marketPrice   Decimal  @map("market_price") @db.Decimal(10, 2)
  trend         String?  @db.VarChar(20)
  lastUpdated   DateTime @default(now()) @map("last_updated")
  
  @@unique([ipSeries, modelName])
  @@map("price_data")
}
```

---

## 第三轮对话：索引与约束

### 话题：数据库索引

**Dev**: 需要哪些索引来优化查询性能？

**Architect**: 索引策略：

```sql
-- users表索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription);

-- collections表索引
CREATE INDEX idx_collections_user_id ON collections(user_id);
CREATE INDEX idx_collections_ip_series ON collections(ip_series);
CREATE INDEX idx_collections_user_created ON collections(user_id, created_at DESC);

-- valuations表索引
CREATE INDEX idx_valuations_collection_id ON valuations(collection_id);
CREATE INDEX idx_valuations_created_at ON valuations(created_at DESC);

-- price_data表索引
CREATE UNIQUE INDEX idx_price_data_series_model ON price_data(ip_series, model_name);
```

### 话题：数据约束

**QA**: 数据完整性约束如何保证？

**Architect**: 数据约束：

1. **外键约束**：确保收藏关联有效用户
2. **唯一约束**：用户邮箱唯一，价格数据(IP+款式)唯一
3. **检查约束**：价格必须为正数
4. **行级安全**：Supabase RLS确保用户只能访问自己的数据

```sql
-- RLS策略示例
ALTER TABLE collections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own collections"
  ON collections FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own collections"
  ON collections FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

---

## 对话总结

**Architect**: 数据模型设计完成：

1. **核心表**：users, collections, valuations, price_data
2. **关系**：User 1:N Collection, Collection 1:N Valuation
3. **索引**：优化查询性能
4. **安全**：行级安全策略

**Dev**: 数据模型清晰，我开始创建数据库迁移。

**QA**: 我会验证数据完整性约束。

---

**文档版本**: 1.0  
**最后更新**: 2026年3月7日
