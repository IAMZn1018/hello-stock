from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.base import get_db
from app.schemas import risk as schemas
from app.models import risk as models

router = APIRouter()

@router.post("/alerts/", response_model=schemas.RiskAlert)
async def create_risk_alert(alert: schemas.RiskAlertCreate, db: Session = Depends(get_db)):
    """
    创建风险提醒
    """
    db_alert = models.RiskAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/alerts/{user_id}", response_model=List[schemas.RiskAlert])
async def get_user_risk_alerts(user_id: str, unread_only: bool = False, db: Session = Depends(get_db)):
    """
    获取用户的风险提醒
    """
    query = db.query(models.RiskAlert).filter(
        models.RiskAlert.user_id == user_id
    )
    
    if unread_only:
        query = query.filter(models.RiskAlert.is_read == 0)
    
    alerts = query.order_by(
        models.RiskAlert.created_at.desc()
    ).all()
    
    return alerts

@router.put("/alerts/{alert_id}/mark-as-read")
async def mark_alert_as_read(alert_id: int, db: Session = Depends(get_db)):
    """
    标记风险提醒为已读
    """
    db_alert = db.query(models.RiskAlert).filter(
        models.RiskAlert.id == alert_id
    ).first()
    
    if not db_alert:
        raise HTTPException(status_code=404, detail="风险提醒未找到")
    
    db_alert.is_read = 1
    db.commit()
    
    return {"message": "标记为已读成功"}

@router.post("/check-stop-loss")
async def check_stop_loss_conditions(user_id: str, current_price: float, purchase_price: float, db: Session = Depends(get_db)):
    """
    检查是否触发止损条件
    """
    # 获取用户的止损规则
    stop_loss_rules = db.query(models.StockTradeRule).filter(
        models.StockTradeRule.user_id == user_id,
        models.StockTradeRule.rule_type == "stop_loss",
        models.StockTradeRule.enabled == 1
    ).all()
    
    alerts = []
    
    for rule in stop_loss_rules:
        # 计算跌幅百分比
        loss_percentage = (purchase_price - current_price) / purchase_price * 100
        
        # 检查是否触发止损
        if loss_percentage >= rule.threshold:
            alert = models.RiskAlert(
                user_id=user_id,
                alert_type="stop_loss",
                stock_code=rule.stock_code,
                message=f"股票{rule.stock_code}已下跌{loss_percentage:.2f}%，达到止损线{rule.threshold}%",
                severity="high"
            )
            db.add(alert)
            alerts.append(alert)
    
    if alerts:
        db.commit()
        for alert in alerts:
            db.refresh(alert)
    
    return {
        "triggered": len(alerts) > 0,
        "alerts": alerts
    }

@router.post("/check-market-risk")
async def check_market_risk(user_id: str, market_trend: str, db: Session = Depends(get_db)):
    """
    检查大盘风险
    """
    if market_trend.lower() in ["down", "downward", "下跌"]:
        alert = models.RiskAlert(
            user_id=user_id,
            alert_type="market_down",
            message="大盘指数向下，请注意风险控制",
            severity="medium"
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        
        return {
            "triggered": True,
            "alert": alert
        }
    
    return {
        "triggered": False
    }