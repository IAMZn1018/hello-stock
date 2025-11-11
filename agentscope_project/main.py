#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hello Stock - 基于AgentScope的AI股票分析助手
"""

import os
import agentscope
from dotenv import load_dotenv
from agents.orchestrator import get_orchestrator
from utils.database import init_db

# 加载环境变量
load_dotenv()

def main():
    """主函数"""
    # 初始化数据库
    init_db()
    
    # 初始化AgentScope
    agentscope.init(
        project="HelloStock",
        name="StockAssistant",
        save_dir="./runs",
        save_log=True,
    )
    
    # 初始化Agent协调器
    orchestrator = get_orchestrator()
    
    # 启动服务
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Hello Stock AgentScope版本启动成功！")
    print(f"服务地址: http://{host}:{port}")
    print("支持的API端点:")
    print("  /analyze/stock - 股票分析")
    print("  /chat - 对话交互")
    print("  /risk/assess - 风险评估")
    print("  /market/analysis - 市场分析")
    print("  /market/daily - 每日市场报告")
    print("\n按Ctrl+C停止服务")
    
    # 这里可以添加Web服务器启动逻辑
    # 例如使用Flask或FastAPI来提供RESTful API接口
    # 暂时以简单方式运行，后续可以扩展为完整的Web服务

if __name__ == "__main__":
    main()