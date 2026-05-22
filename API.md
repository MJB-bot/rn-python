# 企业内部移动办公助手 — 后端 API 文档

## 基础信息

| 项目 | 值 |
|------|-----|
| Base URL | `http://localhost:5000/api` |
| 认证方式 | JWT Bearer Token（Header: `Authorization: Bearer <token>`） |
| Token 有效期 | 2 小时 |
| 默认管理员 | `admin` / `123456` |
| Content-Type | `application/json` |

---

## 统一响应格式

### 成功

```json
{
  "success": true,
  "message": "success",
  "data": {}
}
```

### 失败

```json
{
  "success": false,
  "message": "错误信息"
}
```

### HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 参数校验失败 / 业务错误 |
| 401 | 未授权（token 缺失/过期/无效） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 一、认证模块

### POST /api/auth/login — 管理员登录

> **无需认证**

**请求体：**

```json
{
  "username": "admin",
  "password": "123456"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，1~50字符 |
| password | string | 是 | 密码，1~255字符 |

**成功响应 200：**

```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "admin": {
      "id": 1,
      "username": "admin",
      "role": "admin",
      "created_at": "2026-05-22 10:00:00",
      "updated_at": "2026-05-22 10:00:00"
    }
  }
}
```

**失败响应 401：**

```json
{
  "success": false,
  "message": "用户名或密码错误"
}
```

---

## 二、员工管理模块

> 以下接口均需在 Header 中携带 `Authorization: Bearer <token>`

### GET /api/employees — 员工列表

**Query 参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码，最小 1 |
| page_size | int | 否 | 10 | 每页条数，1~100 |
| name | string | 否 | - | 按姓名模糊搜索 |

**请求示例：**

```
GET /api/employees?page=1&page_size=10&name=张
```

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "张三",
        "age": 25,
        "email": "zhangsan@test.com",
        "created_at": "2026-05-22 10:00:00",
        "updated_at": "2026-05-22 10:00:00"
      }
    ],
    "total": 100
  }
}
```

### GET /api/employees/:id — 员工详情

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": {
    "id": 1,
    "name": "张三",
    "age": 25,
    "email": "zhangsan@test.com",
    "created_at": "2026-05-22 10:00:00",
    "updated_at": "2026-05-22 10:00:00"
  }
}
```

**失败响应 404：** `{ "success": false, "message": "员工不存在" }`

### POST /api/employees — 新增员工

**请求体：**

```json
{
  "name": "张三",
  "age": 25,
  "email": "zhangsan@test.com"
}
```

| 字段 | 类型 | 必填 | 校验规则 |
|------|------|------|----------|
| name | string | 是 | 长度 1~20 |
| age | int | 是 | 范围 18~60 |
| email | string | 是 | 合法邮箱格式，唯一 |

**成功响应 201：**

```json
{
  "success": true,
  "message": "创建成功",
  "data": { "id": 1, "name": "张三", "age": 25, "email": "zhangsan@test.com", "created_at": "...", "updated_at": "..." }
}
```

**失败响应 400：** `{ "success": false, "message": "邮箱已被使用" }`

### PUT /api/employees/:id — 修改员工

请求体同新增。

**成功响应 200：** `{ "success": true, "message": "更新成功", "data": {...} }`

**失败响应：**
- 404: `{ "success": false, "message": "员工不存在" }`
- 400: `{ "success": false, "message": "邮箱已被其他员工使用" }`

### DELETE /api/employees/:id — 删除员工

**成功响应 200：** `{ "success": true, "message": "删除成功" }`

**失败响应 404：** `{ "success": false, "message": "员工不存在" }`

---

## 三、分类管理模块

### GET /api/categories — 分类列表

返回每个分类及其下的设备数量。

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "IT设备",
      "device_count": 5,
      "created_at": "2026-05-22 10:00:00",
      "updated_at": "2026-05-22 10:00:00"
    }
  ]
}
```

### GET /api/categories/:id — 分类详情

**成功响应 200：** 格式同列表单项（含 device_count）

**失败响应 404：** `{ "success": false, "message": "分类不存在" }`

### POST /api/categories — 新增分类

```json
{ "name": "IT设备" }
```

| 字段 | 类型 | 必填 | 校验 |
|------|------|------|------|
| name | string | 是 | 长度 1~20，唯一 |

**成功响应 201：** `{ "success": true, "message": "创建成功", "data": {...} }`

**失败响应 400：** `{ "success": false, "message": "分类名称已存在" }`

### PUT /api/categories/:id — 修改分类

请求体同新增。

**失败响应：**
- 404: `{ "success": false, "message": "分类不存在" }`
- 400: `{ "success": false, "message": "分类名称已存在" }`

### DELETE /api/categories/:id — 删除分类

> 分类下有设备时拒绝删除

**成功响应 200：** `{ "success": true, "message": "删除成功" }`

**失败响应：**
- 404: `{ "success": false, "message": "分类不存在" }`
- 400: `{ "success": false, "message": "分类下存在设备，无法删除" }`

### GET /api/categories/:id/devices — 分类关联设备

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": {
    "category": { "id": 1, "name": "IT设备", "created_at": "...", "updated_at": "..." },
    "devices": [
      {
        "id": 1,
        "name": "MacBook Pro",
        "model": "M3 Pro",
        "category_id": 1,
        "category_name": "IT设备",
        "created_at": "2026-05-22 10:00:00",
        "updated_at": "2026-05-22 10:00:00"
      }
    ]
  }
}
```

**失败响应 404：** `{ "success": false, "message": "分类不存在" }`

---

## 四、设备管理模块

### GET /api/devices — 设备列表

**Query 参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 10 | 每页条数 |
| category_id | int | 否 | - | 按分类筛选 |
| name | string | 否 | - | 按名称模糊搜索 |

**请求示例：** `GET /api/devices?category_id=1&name=Mac&page=1&page_size=10`

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": {
    "list": [
      { "id": 1, "name": "MacBook Pro", "model": "M3 Pro", "category_id": 1, "category_name": "IT设备", "created_at": "...", "updated_at": "..." }
    ],
    "total": 5
  }
}
```

### GET /api/devices/:id — 设备详情

**失败响应 404：** `{ "success": false, "message": "设备不存在" }`

### POST /api/devices — 新增设备

```json
{
  "name": "MacBook Pro",
  "model": "M3 Pro",
  "category_id": 1
}
```

| 字段 | 类型 | 必填 | 校验 |
|------|------|------|------|
| name | string | 是 | 长度 1~100 |
| model | string | 否 | 最大 100 字符 |
| category_id | int | 是 | 分类必须存在 |

**成功响应 201：** `{ "success": true, "message": "创建成功", "data": {...} }`

**失败响应 400：** `{ "success": false, "message": "分类不存在" }`

### PUT /api/devices/:id — 修改设备

请求体同新增。

**失败响应：**
- 404: `{ "success": false, "message": "设备不存在" }`
- 400: `{ "success": false, "message": "分类不存在" }`

### DELETE /api/devices/:id — 删除设备

**成功响应 200：** `{ "success": true, "message": "删除成功" }`

### GET /api/dashboard/stats — 仪表盘统计

**成功响应 200：**

```json
{
  "success": true,
  "message": "success",
  "data": {
    "employee_count": 48,
    "category_count": 12,
    "device_count": 156
  }
}
```

---

## 五、认证说明

### 请求头格式

除 `/api/auth/login` 外，所有接口必须携带：

```
Authorization: Bearer <token>
```

### 401 统一响应

```json
{ "success": false, "message": "未授权，请重新登录" }
```
或
```json
{ "success": false, "message": "登录已过期，请重新登录" }
```

---

## 六、前端对接参考

### TypeScript 类型

```typescript
interface Employee {
  id: number;
  name: string;
  age: number;
  email: string;
  created_at: string;
  updated_at: string;
}

interface Category {
  id: number;
  name: string;
  device_count: number;
  created_at: string;
  updated_at: string;
}

interface Device {
  id: number;
  name: string;
  model: string | null;
  category_id: number;
  category_name: string;
  created_at: string;
  updated_at: string;
}

interface PaginatedList<T> { list: T[]; total: number; }

interface LoginResult {
  token: string;
  admin: { id: number; username: string; role: string; created_at: string; updated_at: string };
}

// 统一响应格式
// 成功: { success: true, message: string, data: T }
// 失败: { success: false, message: string }
```
