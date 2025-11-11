from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RiskAlertBase(BaseModel):
    user_id: str
    alert_type: str
    stock_code: Optional[str] = None
    sector_name: Optional[str] = None
    message: str
    severity: str
    is_read: int = 0

class RiskAlertCreate(RiskAlertBase):
    pass

class RiskAlert(RiskAlertBase):
    id: int
    triggered_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True