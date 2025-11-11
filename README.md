# Hello Stock - AI股票分析助手

基于大模型的股票分析和交易助手系统，具有以下核心功能：

1. 股票日线图片识别与买卖建议
2. 对话记录持久化与上下文检索
3. 风险控制与止损提醒
4. 每日市场分析与次日预案
5. 板块轮动监控与提醒

## 功能模块

- **图像识别模块**: 使用Qwen-Max识别股票日线图片
- **对话管理模块**: 管理用户对话历史和上下文
- **风险控制模块**: 实现止损和风险提示功能
- **市场分析模块**: 分析强势板块和制定投资预案
- **轮动监控模块**: 监控板块轮动并提供提醒

## 技术栈

- Python 3.8+
- FastAPI (Web框架)
- SQLite (数据存储)
- Qwen-Max (大模型API)

## 项目结构

```
hello-stock/
├── app/                  # 主应用目录
│   ├── core/             # 核心模块
│   ├── database/         # 数据库相关
│   ├── models/           # 数据模型
│   ├── routers/          # API路由
│   ├── schemas/          # 数据验证模型
│   └── utils/            # 工具函数
├── .env                  # 环境变量配置
├── app.py                # 应用入口
├── requirements.txt      # 依赖包列表
└── README.md             # 项目说明文档
```

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入你的 Qwen API Key
   ```

3. 启动应用：
   ```bash
   python app.py
   ```

4. 访问 API 文档：
   ```
   http://localhost:8000/docs
   ```

## API 接口说明

### 股票分析接口
- `POST /api/stock/analyze-image` - 分析股票日线图片
- `POST /api/stock/rules/` - 创建交易规则
- `GET /api/stock/rules/{user_id}` - 获取用户交易规则

### 对话管理接口
- `POST /api/chat/sessions/` - 创建聊天会话
- `POST /api/chat/messages/` - 发送聊天消息
- `POST /api/chat/query/` - 智能对话
- `GET /api/chat/sessions/{user_id}/history` - 获取聊天历史

### 风险控制接口
- `POST /api/risk/alerts/` - 创建风险提醒
- `GET /api/risk/alerts/{user_id}` - 获取用户风险提醒
- `POST /api/risk/check-stop-loss` - 检查止损条件
- `POST /api/risk/check-market-risk` - 检查市场风险

### 市场分析接口
- `POST /api/market/analysis/` - 创建市场分析报告
- `GET /api/market/analysis/latest` - 获取最新市场分析
- `POST /api/market/daily-analysis` - 执行每日市场分析
- `POST /api/market/check-sector-rotation` - 检查板块轮动
```

### 爬虫列表
- `https://yuanchuang.10jqka.com.cn/djsjdp_list/` - 每日早中收复盘+龙虎榜复盘
- `https://yuanchuang.10jqka.com.cn/mrnxgg_list/` - 涨停雷达
- `https://news.10jqka.com.cn/realtimenews.html` - 快讯

### mysql配置
ip: 192.168.31.254
port: 49176
user: root
password: Cx1028.+
database: hello-stock