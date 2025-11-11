from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from utils.database import Base
from datetime import datetime

class StockAnalysis(Base):
    """股票分析记录模型"""
    __tablename__ = "stock_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(20), index=True)  # 股票代码
    stock_name = Column(String(100))  # 股票名称
    image_path = Column(String(255))  # 图片路径
    analysis_result = Column(Text)  # 分析结果
    recommendation = Column(Text)  # 建议操作
    confidence = Column(Float)  # 置信度
    created_at = Column(DateTime, default=datetime.utcnow)
    
class StockTradeRule(Base):
    """股票交易规则模型"""
    __tablename__ = "stock_trade_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    stock_code = Column(String(20), nullable=True)  # 可以针对特定股票，也可以是通用规则
    rule_type = Column(String(50))  # 规则类型：stop_loss(止损), take_profit(止盈), market_condition(市场条件)
    condition = Column(String(255))  # 条件描述
    action = Column(String(100))  # 执行动作
    threshold = Column(Float)  # 阈值
    enabled = Column(Integer, default=1)  # 是否启用
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyStockPrice(Base):
    """每日股票价格模型"""
    __tablename__ = "daily_stock_price"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(20), index=True)  # 股票代码
    stock_name = Column(String(100))  # 股票中文名
    price = Column(Float)  # 股价
    timestamp = Column(DateTime, default=datetime.utcnow)  # 时间
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间