from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from utils.database import Base
from datetime import datetime

class RiskRecord(Base):
    """风险记录模型"""
    __tablename__ = "risk_records"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # 分析内容
    analysis_result = Column(Text)  # 分析结果
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskAlert(Base):
    """风险提醒记录模型"""
    __tablename__ = "risk_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    alert_type = Column(String(50))  # 提醒类型：stop_loss, market_down, sector_rotation等
    stock_code = Column(String(20), nullable=True)  # 相关股票代码
    sector_name = Column(String(100), nullable=True)  # 相关板块名称
    message = Column(Text)  # 提醒消息
    severity = Column(String(20))  # 严重程度：low, medium, high, critical
    is_read = Column(Integer, default=0)  # 是否已读
    triggered_at = Column(DateTime, default=datetime.utcnow)  # 触发时间
    created_at = Column(DateTime, default=datetime.utcnow)