from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.base import get_db
from app.schemas import stock as schemas
from app.models import stock as models
from app.core.qwen_api import qwen_api
import os

router = APIRouter()

@router.post("/analyze-image", response_model=dict)
async def analyze_stock_image(request: schemas.StockImageAnalysisRequest, db: Session = Depends(get_db)):
    """
    分析股票日线图片并给出建议
    """
    # 检查图片文件是否存在
    if not os.path.exists(request.image_path):
        raise HTTPException(status_code=404, detail="图片文件未找到")
    
    # 调用Qwen API分析图片
    result = qwen_api.analyze_stock_image(request.image_path, request.query)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"图片分析失败: {result['error']}")
    
    # 保存分析结果到数据库
    db_analysis = models.StockAnalysis(
        stock_code="UNKNOWN",  # 实际应用中应从图片或用户输入中提取
        stock_name="未知股票",
        image_path=request.image_path,
        analysis_result=result["data"],
        recommendation="根据分析结果生成的建议",
        confidence=0.85  # 示例置信度
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {
        "analysis_id": db_analysis.id,
        "result": result["data"]
    }

@router.post("/rules/", response_model=schemas.StockTradeRule)
async def create_trade_rule(rule: schemas.StockTradeRuleCreate, db: Session = Depends(get_db)):
    """
    创建交易规则
    """
    db_rule = models.StockTradeRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/rules/{user_id}", response_model=List[schemas.StockTradeRule])
async def get_user_trade_rules(user_id: str, db: Session = Depends(get_db)):
    """
    获取用户的所有交易规则
    """
    rules = db.query(models.StockTradeRule).filter(
        models.StockTradeRule.user_id == user_id
    ).all()
    return rules