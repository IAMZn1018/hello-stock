from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from utils.database import Base
from datetime import datetime

class MarketAnalysis(Base):
    """市场分析记录模型"""
    __tablename__ = "market_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # 分析内容
    created_at = Column(DateTime, default=datetime.utcnow)

class SectorRotation(Base):
    """板块轮动记录模型"""
    __tablename__ = "sector_rotations"
    
    id = Column(Integer, primary_key=True, index=True)
    sector_name = Column(String)  # 板块名称
    rotation_type = Column(String)  # 轮动类型：in(轮入), out(轮出)
    reason = Column(Text)  # 轮动原因
    details = Column(Text)  # 详细信息
    created_at = Column(DateTime, default=datetime.utcnow)