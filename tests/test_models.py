#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库模型单元测试
"""

import unittest
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import stock as stock_models
from app.models import chat as chat_models
from app.models import risk as risk_models
from app.models import market as market_models

class TestStockModels(unittest.TestCase):
    """股票相关模型测试用例"""
    
    def test_stock_analysis_model(self):
        """测试股票分析模型"""
        # 创建股票分析实例
        analysis = stock_models.StockAnalysis(
            stock_code="SH600000",
            stock_name="浦发银行",
            image_path="/path/to/chart.png",
            analysis_result="上升趋势",
            recommendation="建议买入",
            confidence=0.85
        )
        
        # 验证属性
        self.assertEqual(analysis.stock_code, "SH600000")
        self.assertEqual(analysis.stock_name, "浦发银行")
        self.assertEqual(analysis.image_path, "/path/to/chart.png")
        self.assertEqual(analysis.analysis_result, "上升趋势")
        self.assertEqual(analysis.recommendation, "建议买入")
        self.assertEqual(analysis.confidence, 0.85)
        self.assertIsNotNone(analysis.created_at)
    
    def test_stock_trade_rule_model(self):
        """测试股票交易规则模型"""
        # 创建交易规则实例
        rule = stock_models.StockTradeRule(
            user_id="user_123",
            stock_code="SH600000",
            rule_type="stop_loss",
            condition="当股价下跌超过5%",
            action="自动卖出",
            threshold=5.0,
            enabled=1
        )
        
        # 验证属性
        self.assertEqual(rule.user_id, "user_123")
        self.assertEqual(rule.stock_code, "SH600000")
        self.assertEqual(rule.rule_type, "stop_loss")
        self.assertEqual(rule.condition, "当股价下跌超过5%")
        self.assertEqual(rule.action, "自动卖出")
        self.assertEqual(rule.threshold, 5.0)
        self.assertEqual(rule.enabled, 1)
        self.assertIsNotNone(rule.created_at)

class TestChatModels(unittest.TestCase):
    """聊天相关模型测试用例"""
    
    def test_chat_session_model(self):
        """测试聊天会话模型"""
        # 创建聊天会话实例
        session = chat_models.ChatSession(
            user_id="user_123"
        )
        
        # 验证属性
        self.assertEqual(session.user_id, "user_123")
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.updated_at)
    
    def test_chat_message_model(self):
        """测试聊天消息模型"""
        # 创建聊天消息实例
        message = chat_models.ChatMessage(
            session_id=1,
            role="user",
            content="你好，请帮我分析一下这只股票",
            image_path="/path/to/stock_chart.png"
        )
        
        # 验证属性
        self.assertEqual(message.session_id, 1)
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "你好，请帮我分析一下这只股票")
        self.assertEqual(message.image_path, "/path/to/stock_chart.png")
        self.assertIsNotNone(message.created_at)

class TestRiskModels(unittest.TestCase):
    """风险控制相关模型测试用例"""
    
    def test_risk_alert_model(self):
        """测试风险提醒模型"""
        # 创建风险提醒实例
        alert = risk_models.RiskAlert(
            user_id="user_123",
            alert_type="stop_loss",
            stock_code="SH600000",
            sector_name="银行板块",
            message="股价已跌破止损线",
            severity="high",
            is_read=0
        )
        
        # 验证属性
        self.assertEqual(alert.user_id, "user_123")
        self.assertEqual(alert.alert_type, "stop_loss")
        self.assertEqual(alert.stock_code, "SH600000")
        self.assertEqual(alert.sector_name, "银行板块")
        self.assertEqual(alert.message, "股价已跌破止损线")
        self.assertEqual(alert.severity, "high")
        self.assertEqual(alert.is_read, 0)
        self.assertIsNotNone(alert.triggered_at)
        self.assertIsNotNone(alert.created_at)

class TestMarketModels(unittest.TestCase):
    """市场相关模型测试用例"""
    
    def test_market_analysis_model(self):
        """测试市场分析模型"""
        # 创建市场分析实例
        analysis = market_models.MarketAnalysis(
            analysis_date=datetime.now().date(),
            market_index="上证指数",
            trend="up",
            strong_sectors='["金融", "科技"]',
            weak_sectors='["消费", "医药"]',
            analysis_summary="市场整体呈现上涨趋势",
            next_day_plan="关注金融和科技板块的持续性"
        )
        
        # 验证属性
        self.assertIsNotNone(analysis.analysis_date)
        self.assertEqual(analysis.market_index, "上证指数")
        self.assertEqual(analysis.trend, "up")
        self.assertEqual(analysis.strong_sectors, '["金融", "科技"]')
        self.assertEqual(analysis.weak_sectors, '["消费", "医药"]')
        self.assertEqual(analysis.analysis_summary, "市场整体呈现上涨趋势")
        self.assertEqual(analysis.next_day_plan, "关注金融和科技板块的持续性")
        self.assertIsNotNone(analysis.created_at)
    
    def test_sector_rotation_model(self):
        """测试板块轮动模型"""
        # 创建板块轮动实例
        rotation = market_models.SectorRotation(
            rotation_date=datetime.now().date(),
            from_sector="消费",
            to_sector="科技",
            strength=0.75,
            confidence=0.85,
            notes="科技板块受政策利好影响"
        )
        
        # 验证属性
        self.assertIsNotNone(rotation.rotation_date)
        self.assertEqual(rotation.from_sector, "消费")
        self.assertEqual(rotation.to_sector, "科技")
        self.assertEqual(rotation.strength, 0.75)
        self.assertEqual(rotation.confidence, 0.85)
        self.assertEqual(rotation.notes, "科技板块受政策利好影响")
        self.assertIsNotNone(rotation.created_at)

if __name__ == '__main__':
    unittest.main()