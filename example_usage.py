#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统使用示例脚本
展示如何使用各个模块的核心功能
"""

import os
import sys
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.database.base import get_db, init_db
from app.models import chat as chat_models, stock as stock_models, risk as risk_models
from app.schemas import chat as chat_schemas, stock as stock_schemas, risk as risk_schemas
from app.core.qwen_api import qwen_api
from app.utils.similarity import cosine_similarity

def example_chat_functionality():
    """对话功能示例"""
    print("=== 对话功能示例 ===")
    
    # 初始化数据库
    init_db()
    
    # 创建聊天会话
    from app.database.base import SessionLocal
    db = SessionLocal()
    
    try:
        # 创建新的聊天会话
        session = chat_models.ChatSession(user_id="user_123")
        db.add(session)
        db.commit()
        db.refresh(session)
        
        print(f"创建聊天会话，ID: {session.id}")
        
        # 添加用户消息
        user_message = chat_models.ChatMessage(
            session_id=session.id,
            role="user",
            content="请分析这张股票K线图，我应该买入还是卖出？"
        )
        db.add(user_message)
        db.commit()
        
        print(f"添加用户消息: {user_message.content}")
        
        # 模拟获取相关上下文
        contexts = [
            "user: 我关注的是科技股",
            "assistant: 科技股近期表现不错，但要注意风险",
            "user: 我的持仓成本是50元",
            "assistant: 建议设置止损位在45元"
        ]
        
        query = "科技股现在适合买入吗？"
        similarities = []
        for i, context in enumerate(contexts):
            similarity = cosine_similarity(query, context)
            similarities.append((i, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_context = contexts[similarities[0][0]] if similarities and similarities[0][1] > 0.1 else ""
        
        print(f"找到最相关的上下文: {top_context}")
        
        # 模拟调用大模型API（实际使用时需要有效的API密钥）
        print("调用大模型API进行分析...")
        print("分析结果: 根据当前市场情况，科技股短期有回调压力，建议观望等待合适时机再买入。")
        
        # 添加助手回复
        assistant_message = chat_models.ChatMessage(
            session_id=session.id,
            role="assistant",
            content="根据当前市场情况，科技股短期有回调压力，建议观望等待合适时机再买入。"
        )
        db.add(assistant_message)
        db.commit()
        
        print("添加助手回复成功")
        
    except Exception as e:
        print(f"对话功能示例出错: {e}")
    finally:
        db.close()

def example_stock_analysis():
    """股票分析功能示例"""
    print("\n=== 股票分析功能示例 ===")
    
    from app.database.base import SessionLocal
    db = SessionLocal()
    
    try:
        # 创建股票分析记录
        analysis = stock_models.StockAnalysis(
            stock_code="SH600000",
            stock_name="浦发银行",
            image_path="/path/to/stock_chart.png",
            analysis_result="该股处于上升通道中，技术指标显示买入信号",
            recommendation="建议在回调时买入",
            confidence=0.85
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        print(f"创建股票分析记录，ID: {analysis.id}")
        print(f"股票代码: {analysis.stock_code}")
        print(f"分析结果: {analysis.analysis_result}")
        print(f"投资建议: {analysis.recommendation}")
        
        # 创建交易规则
        trade_rule = stock_models.StockTradeRule(
            user_id="user_123",
            stock_code="SH600000",
            rule_type="stop_loss",
            condition="当股价下跌超过5%",
            action="自动卖出",
            threshold=5.0
        )
        db.add(trade_rule)
        db.commit()
        db.refresh(trade_rule)
        
        print(f"创建交易规则，ID: {trade_rule.id}")
        print(f"规则类型: {trade_rule.rule_type}")
        print(f"触发条件: {trade_rule.condition}")
        
    except Exception as e:
        print(f"股票分析功能示例出错: {e}")
    finally:
        db.close()

def example_risk_control():
    """风险控制功能示例"""
    print("\n=== 风险控制功能示例 ===")
    
    from app.database.base import SessionLocal
    db = SessionLocal()
    
    try:
        # 创建风险提醒
        risk_alert = risk_models.RiskAlert(
            user_id="user_123",
            alert_type="stop_loss",
            stock_code="SH600000",
            message="浦发银行股价已下跌5%，达到止损线",
            severity="high"
        )
        db.add(risk_alert)
        db.commit()
        db.refresh(risk_alert)
        
        print(f"创建风险提醒，ID: {risk_alert.id}")
        print(f"提醒类型: {risk_alert.alert_type}")
        print(f"提醒消息: {risk_alert.message}")
        print(f"严重程度: {risk_alert.severity}")
        
        # 检查大盘风险
        print("检查大盘风险...")
        market_trend = "down"  # 模拟大盘向下
        
        if market_trend.lower() in ["down", "downward", "下跌"]:
            market_alert = risk_models.RiskAlert(
                user_id="user_123",
                alert_type="market_down",
                message="大盘指数向下，请注意风险控制",
                severity="medium"
            )
            db.add(market_alert)
            db.commit()
            db.refresh(market_alert)
            
            print(f"创建大盘风险提醒，ID: {market_alert.id}")
            print(f"提醒消息: {market_alert.message}")
        
    except Exception as e:
        print(f"风险控制功能示例出错: {e}")
    finally:
        db.close()

def example_market_analysis():
    """市场分析功能示例"""
    print("\n=== 市场分析功能示例 ===")
    
    # 模拟市场数据分析
    market_data = {
        "date": "2023-10-01",
        "market_index": "上证指数",
        "trend": "up",
        "strong_sectors": ["科技股", "新能源", "医药生物"],
        "weak_sectors": ["银行", "房地产", "煤炭"]
    }
    
    print("今日市场分析:")
    print(f"日期: {market_data['date']}")
    print(f"大盘指数: {market_data['market_index']}")
    print(f"市场趋势: {market_data['trend']}")
    print(f"强势板块: {', '.join(market_data['strong_sectors'])}")
    print(f"弱势板块: {', '.join(market_data['weak_sectors'])}")
    
    # 模拟板块轮动分析
    print("\n板块轮动分析:")
    print("检测到从银行板块向科技板块的轮动趋势")
    print("轮动强度: 中等")
    print("建议: 适当减持银行股，增持科技股")

def main():
    """主函数"""
    print("Hello Stock 系统使用示例")
    print("=" * 30)
    
    # 运行各个功能示例
    example_chat_functionality()
    example_stock_analysis()
    example_risk_control()
    example_market_analysis()
    
    print("\n" + "=" * 30)
    print("所有示例运行完成！")

if __name__ == "__main__":
    main()