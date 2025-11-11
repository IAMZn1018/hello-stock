#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析Agent
"""

import os
import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
from utils.database import get_db_session, close_db_session
import sys
sys.path.append('../app')
from core.qwen_api import qwen_api
from models.stock import StockAnalysis

class StockAnalysisAgent(AgentBase):
    """股票分析Agent，负责分析股票图片并给出投资建议"""
    
    def __init__(self, name: str = "StockAnalysisAgent") -> None:
        """初始化股票分析Agent"""
        super().__init__(name=name)
        
    def analyze_stock_image(self, image_path: str, query: str = "") -> dict:
        """
        分析股票日线图片并给出建议
        
        Args:
            image_path (str): 股票图片路径
            query (str): 用户查询
            
        Returns:
            dict: 分析结果
        """
        # 检查图片文件是否存在
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": "图片文件未找到"
            }
        
        # 调用Qwen API分析图片
        result = qwen_api.analyze_stock_image(image_path, query)
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"图片分析失败: {result['error']}"
            }
        
        # 保存分析结果到数据库
        db = get_db_session()
        try:
            db_analysis = StockAnalysis(
                stock_code="UNKNOWN",  # 实际应用中应从图片或用户输入中提取
                stock_name="未知股票",
                image_path=image_path,
                analysis_result=result["data"],
                recommendation="根据分析结果生成的建议",
                confidence=0.85  # 示例置信度
            )
            db.add(db_analysis)
            db.commit()
            db.refresh(db_analysis)
            
            return {
                "success": True,
                "data": {
                    "analysis_id": db_analysis.id,
                    "result": result["data"]
                }
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"数据库保存失败: {str(e)}"
            }
        finally:
            close_db_session(db)
    
    def reply(self, x: dict = None) -> dict:
        """
        Agent回复方法
        
        Args:
            x (dict): 输入消息
            
        Returns:
            dict: 回复消息
        """
        if x is None:
            return Msg(self.name, "请提供股票图片进行分析", "assistant")
        
        # 解析输入消息
        if isinstance(x, Msg):
            content = x.content
        else:
            content = x
            
        # 如果内容包含图片路径，则进行分析
        if isinstance(content, dict) and "image_path" in content:
            result = self.analyze_stock_image(
                content["image_path"], 
                content.get("query", "")
            )
            return Msg(self.name, result, "assistant")
        else:
            return Msg(self.name, "请提供有效的股票图片路径", "assistant")