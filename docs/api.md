# Hello Stock API 文档

## 概述

Hello Stock 是一个基于人工智能的股票分析系统，提供股票图像识别、智能对话、风险控制和市场分析等功能。

## 基础URL

```
http://localhost:8000/api/v1
```

## 认证

所有API端点都需要通过API密钥进行认证。在每个请求的头部包含以下字段：

```
Authorization: Bearer YOUR_API_KEY
```

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

## 股票分析 API

### 分析股票日线图片

分析上传的股票日线图片并返回分析结果。

```
POST /stock/analyze-image
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| image | file | 是 | 股票日线图片文件 |
| stock_code | string | 否 | 股票代码 |
| stock_name | string | 否 | 股票名称 |

**响应:**

```json
{
  "id": 1,
  "stock_code": "SH600000",
  "stock_name": "浦发银行",
  "image_path": "/uploads/stock_charts/1.png",
  "analysis_result": "该股处于上升通道中，技术指标显示买入信号",
  "recommendation": "建议在回调时买入",
  "confidence": 0.85,
  "created_at": "2023-10-01T10:00:00"
}
```

### 创建交易规则

为指定股票创建交易规则。

```
POST /stock/trade-rules
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |
| stock_code | string | 是 | 股票代码 |
| rule_type | string | 是 | 规则类型 (stop_loss, take_profit等) |
| condition | string | 是 | 触发条件描述 |
| action | string | 是 | 执行动作 |
| threshold | number | 是 | 阈值 |

**响应:**

```json
{
  "id": 1,
  "user_id": "user_123",
  "stock_code": "SH600000",
  "rule_type": "stop_loss",
  "condition": "当股价下跌超过5%",
  "action": "自动卖出",
  "threshold": 5.0,
  "created_at": "2023-10-01T10:00:00"
}
```

### 获取用户交易规则

获取指定用户的所有交易规则。

```
GET /stock/trade-rules/{user_id}
```

**路径参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |

**响应:**

```json
[
  {
    "id": 1,
    "user_id": "user_123",
    "stock_code": "SH600000",
    "rule_type": "stop_loss",
    "condition": "当股价下跌超过5%",
    "action": "自动卖出",
    "threshold": 5.0,
    "created_at": "2023-10-01T10:00:00"
  }
]
```

## 对话管理 API

### 创建聊天会话

创建一个新的聊天会话。

```
POST /chat/sessions
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |

**响应:**

```json
{
  "id": 1,
  "user_id": "user_123",
  "created_at": "2023-10-01T10:00:00"
}
```

### 发送聊天消息

向指定会话发送消息。

```
POST /chat/messages
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| session_id | integer | 是 | 会话ID |
| role | string | 是 | 角色 (user, assistant) |
| content | string | 是 | 消息内容 |

**响应:**

```json
{
  "id": 1,
  "session_id": 1,
  "role": "user",
  "content": "请分析这张股票K线图",
  "created_at": "2023-10-01T10:00:00"
}
```

### 智能对话

与AI进行带上下文的智能对话。

```
POST /chat/with-context
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |
| message | string | 是 | 用户消息 |
| session_id | integer | 否 | 会话ID |

**响应:**

```json
{
  "session_id": 1,
  "response": "根据当前市场情况，科技股短期有回调压力，建议观望等待合适时机再买入。"
}
```

### 获取聊天历史

获取指定用户的聊天历史。

```
GET /chat/history/{user_id}
```

**路径参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |

**响应:**

```json
[
  {
    "session_id": 1,
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "请分析这张股票K线图",
        "created_at": "2023-10-01T10:00:00"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "根据当前市场情况，科技股短期有回调压力，建议观望等待合适时机再买入。",
        "created_at": "2023-10-01T10:01:00"
      }
    ]
  }
]
```

## 风险控制 API

### 创建风险提醒

创建风险提醒。

```
POST /risk/alerts
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |
| alert_type | string | 是 | 提醒类型 (stop_loss, market_down等) |
| stock_code | string | 否 | 股票代码 |
| message | string | 是 | 提醒消息 |
| severity | string | 是 | 严重程度 (low, medium, high) |

**响应:**

```json
{
  "id": 1,
  "user_id": "user_123",
  "alert_type": "stop_loss",
  "stock_code": "SH600000",
  "message": "浦发银行股价已下跌5%，达到止损线",
  "severity": "high",
  "is_read": false,
  "created_at": "2023-10-01T10:00:00"
}
```

### 获取用户风险提醒

获取指定用户的所有风险提醒。

```
GET /risk/alerts/{user_id}
```

**路径参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |

**查询参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| is_read | boolean | 否 | 是否已读 |

**响应:**

```json
[
  {
    "id": 1,
    "user_id": "user_123",
    "alert_type": "stop_loss",
    "stock_code": "SH600000",
    "message": "浦发银行股价已下跌5%，达到止损线",
    "severity": "high",
    "is_read": false,
    "created_at": "2023-10-01T10:00:00"
  }
]
```

### 标记风险提醒为已读

将风险提醒标记为已读。

```
PUT /risk/alerts/{alert_id}/read
```

**路径参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| alert_id | integer | 是 | 提醒ID |

**响应:**

```json
{
  "id": 1,
  "user_id": "user_123",
  "alert_type": "stop_loss",
  "stock_code": "SH600000",
  "message": "浦发银行股价已下跌5%，达到止损线",
  "severity": "high",
  "is_read": true,
  "created_at": "2023-10-01T10:00:00"
}
```

### 检查止损条件

检查用户持仓是否达到止损条件。

```
POST /risk/check-stop-loss
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |
| stock_code | string | 是 | 股票代码 |
| current_price | number | 是 | 当前价格 |
| cost_price | number | 是 | 成本价格 |

**响应:**

```json
{
  "alert_triggered": true,
  "alert_message": "当前股价已下跌5.2%，达到止损线",
  "percentage_change": -5.2
}
```

### 检查大盘风险

检查大盘风险。

```
GET /risk/check-market
```

**响应:**

```json
{
  "market_trend": "down",
  "risk_level": "medium",
  "message": "大盘指数向下，请注意风险控制"
}
```

## 市场分析 API

### 创建市场分析报告

创建市场分析报告。

```
POST /market/analysis
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| date | string | 是 | 日期 (YYYY-MM-DD) |
| market_index | string | 是 | 大盘指数名称 |
| trend | string | 是 | 市场趋势 (up, down, neutral) |
| analysis | string | 是 | 分析内容 |
| strong_sectors | array | 是 | 强势板块列表 |
| weak_sectors | array | 是 | 弱势板块列表 |

**响应:**

```json
{
  "id": 1,
  "date": "2023-10-01",
  "market_index": "上证指数",
  "trend": "up",
  "analysis": "今日市场整体呈现上涨趋势，成交量有所放大",
  "strong_sectors": ["科技股", "新能源", "医药生物"],
  "weak_sectors": ["银行", "房地产", "煤炭"],
  "created_at": "2023-10-01T10:00:00"
}
```

### 获取最新市场分析

获取最新的市场分析报告。

```
GET /market/analysis/latest
```

**响应:**

```json
{
  "id": 1,
  "date": "2023-10-01",
  "market_index": "上证指数",
  "trend": "up",
  "analysis": "今日市场整体呈现上涨趋势，成交量有所放大",
  "strong_sectors": ["科技股", "新能源", "医药生物"],
  "weak_sectors": ["银行", "房地产", "煤炭"],
  "created_at": "2023-10-01T10:00:00"
}
```

### 记录板块轮动事件

记录板块轮动事件。

```
POST /market/sector-rotation
```

**请求参数:**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| date | string | 是 | 日期 (YYYY-MM-DD) |
| from_sector | string | 是 | 流出板块 |
| to_sector | string | 是 | 流入板块 |
| strength | string | 是 | 轮动强度 (low, medium, high) |
| analysis | string | 是 | 分析内容 |

**响应:**

```json
{
  "id": 1,
  "date": "2023-10-01",
  "from_sector": "银行",
  "to_sector": "科技股",
  "strength": "medium",
  "analysis": "资金从银行板块流向科技板块",
  "created_at": "2023-10-01T10:00:00"
}
```

### 获取今日板块轮动

获取今日的板块轮动情况。

```
GET /market/sector-rotation/today
```

**响应:**

```json
[
  {
    "id": 1,
    "date": "2023-10-01",
    "from_sector": "银行",
    "to_sector": "科技股",
    "strength": "medium",
    "analysis": "资金从银行板块流向科技板块",
    "created_at": "2023-10-01T10:00:00"
  }
]
```

### 执行每日市场分析

执行每日市场分析。

```
POST /market/daily-analysis
```

**响应:**

```json
{
  "analysis_id": 1,
  "sector_rotation_id": 1,
  "message": "每日市场分析完成"
}
```

### 检查板块轮动情况

检查板块轮动情况。

```
GET /market/check-rotation
```

**响应:**

```json
{
  "rotation_detected": true,
  "from_sector": "银行",
  "to_sector": "科技股",
  "strength": "medium",
  "analysis": "检测到从银行板块向科技板块的轮动趋势"
}
```