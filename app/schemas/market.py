from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class MarketAnalysisBase(BaseModel):
    analysis_date: datetime
    market_index: str
    trend: str
    strong_sectors: str
    weak_sectors: str
    analysis_summary: str
    next_day_plan: str

class MarketAnalysisCreate(MarketAnalysisBase):
    pass

class MarketAnalysis(MarketAnalysisBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SectorRotationBase(BaseModel):
    rotation_date: datetime
    from_sector: str
    to_sector: str
    strength: float
    confidence: float
    notes: Optional[str] = None

class SectorRotationCreate(SectorRotationBase):
    pass

class SectorRotation(SectorRotationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True