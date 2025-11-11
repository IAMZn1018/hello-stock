from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.database.base import get_db
from app.schemas import market as schemas
from app.models import market as models
from app.core.qwen_api import qwen_api

router = APIRouter()

@router.post("/analysis/", response_model=schemas.MarketAnalysis)
async def create_market_analysis(analysis: schemas.MarketAnalysisCreate, db: Session = Depends(get_db)):
    """
    创建市场分析报告
    """
    db_analysis = models.MarketAnalysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/analysis/latest", response_model=schemas.MarketAnalysis)
async def get_latest_market_analysis(db: Session = Depends(get_db)):
    """
    获取最新的市场分析报告
    """
    analysis = db.query(models.MarketAnalysis).order_by(
        models.MarketAnalysis.analysis_date.desc()
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="未找到市场分析报告")
    
    return analysis

@router.post("/sector-rotation/", response_model=schemas.SectorRotation)
async def create_sector_rotation(rotation: schemas.SectorRotationCreate, db: Session = Depends(get_db)):
    """
    记录板块轮动事件
    """
    db_rotation = models.SectorRotation(**rotation.dict())
    db.add(db_rotation)
    db.commit()
    db.refresh(db_rotation)
    return db_rotation

@router.get("/sector-rotation/today", response_model=List[schemas.SectorRotation])
async def get_today_sector_rotations(db: Session = Depends(get_db)):
    """
    获取今天的板块轮动情况
    """
    today = date.today()
    rotations = db.query(models.SectorRotation).filter(
        models.SectorRotation.rotation_date >= datetime(today.year, today.month, today.day)
    ).all()
    
    return rotations

@router.post("/daily-analysis")
async def perform_daily_market_analysis(db: Session = Depends(get_db)):
    """
    执行每日市场分析
    """
    # 这里应该集成真实的市场数据源
    # 为了演示，我们使用模拟数据
    
    # 模拟获取当日市场数据
    market_data = {
        "date": datetime.now(),
        "market_index": "上证指数",
        "trend": "up",
        "strong_sectors": '["科技股", "新能源", "医药生物"]',
        "weak_sectors": '["银行", "房地产", "煤炭"]'
    }
    
    # 调用大模型进行分析
    analysis_prompt = f"""
    请分析以下市场数据并提供投资建议：
    日期: {market_data['date']}
    大盘指数: {market_data['market_index']}
    市场趋势: {market_data['trend']}
    强势板块: {market_data['strong_sectors']}
    弱势板块: {market_data['weak_sectors']}
    
    请提供:
    1. 市场分析摘要
    2. 次日投资预案
    3. 需要关注的风险点
    """
    
    result = qwen_api.chat_with_context([{"role": "user", "content": analysis_prompt}])
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"市场分析失败: {result['error']}")
    
    # 保存分析结果
    analysis_result = result["data"]
    
    db_analysis = models.MarketAnalysis(
        analysis_date=market_data["date"],
        market_index=market_data["market_index"],
        trend=market_data["trend"],
        strong_sectors=market_data["strong_sectors"],
        weak_sectors=market_data["weak_sectors"],
        analysis_summary="市场整体呈现上涨趋势，科技股和新能源板块表现强劲。",
        next_day_plan="建议关注科技股的持续性，适当配置新能源板块，规避银行和房地产等弱势板块。"
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {
        "analysis_id": db_analysis.id,
        "result": analysis_result
    }

@router.post("/check-sector-rotation")
async def check_sector_rotation(db: Session = Depends(get_db)):
    """
    检查板块轮动情况
    """
    # 获取最新的市场分析
    latest_analysis = db.query(models.MarketAnalysis).order_by(
        models.MarketAnalysis.analysis_date.desc()
    ).first()
    
    if not latest_analysis:
        return {"message": "暂无市场分析数据"}
    
    # 调用大模型分析可能的板块轮动
    rotation_prompt = f"""
    基于以下市场信息，请分析是否存在板块轮动的可能性：
    强势板块: {latest_analysis.strong_sectors}
    弱势板块: {latest_analysis.weak_sectors}
    市场趋势: {latest_analysis.trend}
    
    请指出：
    1. 最可能发生轮动的板块对
    2. 轮动方向和强度
    3. 投资建议
    """
    
    result = qwen_api.chat_with_context([{"role": "user", "content": rotation_prompt}])
    
    if not result["success"]:
        return {"message": f"板块轮动分析失败: {result['error']}"}
    
    return {
        "analysis": result["data"]
    }