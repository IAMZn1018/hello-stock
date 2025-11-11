# Hello Stock - 基于AgentScope的AI股票分析助手

这是一个使用AgentScope 1.0框架重构的股票分析助手项目。

## 项目结构

```
agentscope_project/
├── agents/              # Agent实现
│   ├── __init__.py
│   ├── stock_agent.py   # 股票分析Agent
│   ├── chat_agent.py    # 对话管理Agent
│   ├── risk_agent.py    # 风险控制Agent
│   ├── market_agent.py  # 市场分析Agent
│   └── orchestrator.py  # Agent协调器
├── config/              # 配置文件
│   ├── __init__.py
│   └── agentscope_config.py
├── utils/               # 工具模块
│   ├── __init__.py
│   ├── database.py      # 数据库工具
│   ├── wencai_tool.py   # 问财接口工具
│   ├── deepseek_analyzer.py   # DeepSeek分析工具
│   └── stock_analyzer.py      # 股票综合分析工具
├── app.py               # Web API服务
├── main.py              # 主程序入口
├── analyze_stock.py     # 股票分析命令行工具
├── test_agents.py       # Agent测试脚本
└── requirements.txt     # 依赖包列表
```

## 功能特性

- 股票分析：基于图片和文本的智能股票分析
- 对话管理：智能对话交互与上下文管理
- 风险控制：投资风险识别与评估
- 市场分析：市场趋势分析与板块轮动检测
- Agent协作：多个Agent协同工作处理复杂任务
- RESTful API：提供Web接口供外部调用
- 命令行工具：通过命令行直接分析股票

## 股票分析功能

本项目新增了一个强大的股票分析功能，可以：
1. 输入个股名称或代码
2. 自动调用问财接口获取详细的股票信息
3. 将获取的信息发送给DeepSeek AI进行专业分析
4. 返回包括短期建议、中期建议、买入风险与机会、止盈止损策略等在内的全面分析

### 使用方法

#### 方法一：命令行工具
```bash
python analyze_stock.py <股票名称或代码>
```

例如：
```bash
python analyze_stock.py 三维通信
python analyze_stock.py 002115
```

#### 方法二：作为模块导入使用
```python
from utils.stock_analyzer import analyze_stock, print_analysis_result

# 分析股票
stock_info, analysis = analyze_stock("三维通信")

# 打印结果
if stock_info and analysis:
    print_analysis_result("三维通信", stock_info, analysis)
```

## 安装和运行

### 环境准备

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   创建 `.env` 文件并配置必要的环境变量：
   ```
   DATABASE_URL=sqlite:///./stock_assistant.db
   QWEN_API_KEY=your_qwen_api_key_here
   QWEN_MODEL=qwen-max
   PORT=8000
   HOST=0.0.0.0
   ```

### 运行方式

#### 方式一：直接运行主程序
```bash
python main.py
```

#### 方式二：启动Web API服务
```bash
python app.py
```

启动后可通过以下API端点访问服务：
- `POST /api/analyze/stock` - 股票分析
- `POST /api/chat` - 对话交互
- `POST /api/risk/assess` - 风险评估
- `POST /api/market/analysis` - 市场分析
- `GET /api/market/daily` - 每日市场报告

### 测试Agent功能

运行测试脚本验证各Agent功能：
```bash
python test_agents.py
```