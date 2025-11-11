#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent功能测试模块
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# 初始化数据库
from utils.database import init_db
init_db()

# 初始化AgentScope
import agentscope
agentscope.init()

from agents.orchestrator import get_orchestrator

def test_stock_analysis():
    """测试股票分析功能"""
    print("=== 测试股票分析功能 ===")
    orchestrator = get_orchestrator()
    
    # 测试文本查询分析
    result = orchestrator.handle_stock_analysis(
        text_query="请分析贵州茅台的投资价值"
    )
    print("股票文本分析结果:", json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_chat_management():
    """测试对话管理功能"""
    print("\n=== 测试对话管理功能 ===")
    orchestrator = get_orchestrator()
    
    # 创建聊天会话并发送消息
    result = orchestrator.handle_chat_interaction(
        user_id="test_user_001",
        query="你好，我想了解今天的股市情况"
    )
    print("对话管理结果:", json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_risk_assessment():
    """测试风险评估功能"""
    print("\n=== 测试风险评估功能 ===")
    orchestrator = get_orchestrator()
    
    # 测试文本风险评估
    result = orchestrator.handle_risk_assessment({
        "text": "我打算投资新能源汽车板块，请评估相关风险"
    })
    print("风险评估结果:", json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_market_analysis():
    """测试市场分析功能"""
    print("\n=== 测试市场分析功能 ===")
    orchestrator = get_orchestrator()
    
    # 生成市场分析报告
    result = orchestrator.handle_market_analysis(
        action="generate_report"
    )
    print("市场分析结果:", json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_agent_coordination():
    """测试Agent协作功能"""
    print("\n=== 测试Agent协作功能 ===")
    orchestrator = get_orchestrator()
    
    # 测试综合分析任务
    result = orchestrator.coordinate_agents({
        "task_type": "comprehensive_analysis",
        "analysis_context": "当前市场环境下，白酒板块的投资机会如何？",
        "stock_code": "600519"  # 贵州茅台
    })
    print("Agent协作结果:", json.dumps(result, ensure_ascii=False, indent=2))
    return result

def main():
    """主测试函数"""
    print("开始测试AgentScope项目功能...")
    print(f"测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 依次测试各项功能
        test_stock_analysis()
        test_chat_management()
        test_risk_assessment()
        test_market_analysis()
        test_agent_coordination()
        
        print("\n=== 所有测试完成 ===")
        print(f"测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("请检查输出结果确认各Agent功能是否正常工作")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()