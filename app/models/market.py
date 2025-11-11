from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database.base import Base
from datetime import datetime

class MarketAnalysis(Base):
    """市场分析记录模型"""
    __tablename__ = "market_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_date = Column(DateTime, index=True)  # 分析日期
    market_index = Column(String)  # 大盘指数
    trend = Column(String)  # 趋势：up, down, sideways
    strong_sectors = Column(Text)  # 强势板块（JSON格式存储）
    weak_sectors = Column(Text)  # 弱势板块（JSON格式存储）
    analysis_summary = Column(Text)  # 分析摘要
    next_day_plan = Column(Text)  # 次日预案
    created_at = Column(DateTime, default=datetime.utcnow)

class SectorRotation(Base):
    """板块轮动记录模型"""
    __tablename__ = "sector_rotations"
    
    id = Column(Integer, primary_key=True, index=True)
    rotation_date = Column(DateTime, index=True)  # 轮动日期
    from_sector = Column(String)  # 轮出板块
    to_sector = Column(String)  # 轮入板块
    strength = Column(Float)  # 轮动强度
    confidence = Column(Float)  # 置信度
    notes = Column(Text)  # 备注
    created_at = Column(DateTime, default=datetime.utcnow)