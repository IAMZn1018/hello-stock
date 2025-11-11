from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockAnalysisBase(BaseModel):
    stock_code: str
    stock_name: str
    image_path: str
    analysis_result: str
    recommendation: str
    confidence: float

class StockAnalysisCreate(StockAnalysisBase):
    pass

class StockAnalysis(StockAnalysisBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class StockImageAnalysisRequest(BaseModel):
    image_path: str
    query: str

class StockTradeRuleBase(BaseModel):
    user_id: str
    stock_code: Optional[str] = None
    rule_type: str
    condition: str
    action: str
    threshold: float
    enabled: int = 1

class StockTradeRuleCreate(StockTradeRuleBase):
    pass

class StockTradeRule(StockTradeRuleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True