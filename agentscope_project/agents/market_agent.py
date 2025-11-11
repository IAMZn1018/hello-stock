#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场分析Agent
"""

import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
from utils.database import get_db_session, close_db_session
import sys
sys.path.append('../app')
from core.qwen_api import qwen_api
from models.market import MarketAnalysis, SectorRotation

class MarketAnalysisAgent(AgentBase):
    """市场分析Agent，负责生成市场分析报告和板块轮动分析"""
    
    def __init__(self, name: str = "MarketAnalysisAgent") -> None:
        """初始化市场分析Agent"""
        super().__init__(name=name)
        
    def generate_market_analysis(self, market_data: dict = None) -> dict:
        """
        生成市场分析报告
        
        Args:
            market_data (dict): 市场数据(可选)
            
        Returns:
            dict: 市场分析报告
        """
        try:
            # 构造提示词
            if market_data:
                prompt = f"""
                基于以下市场数据生成详细的市场分析报告：
                
                {market_data}
                
                请从以下几个方面进行分析：
                1. 大盘走势分析：主要股指表现、成交量变化、市场情绪等
                2. 热点板块分析：当前市场热点板块及其表现
                3. 资金流向分析：主力资金流入流出情况
                4. 技术面分析：关键支撑位、阻力位、技术指标信号等
                5. 消息面分析：重要政策、经济数据、国际形势等影响
                
                请给出具体的分析结论和投资建议。
                """
            else:
                prompt = """
                请生成一份最新的市场分析报告，包括以下内容：
                
                1. 大盘走势分析：主要股指表现、成交量变化、市场情绪等
                2. 热点板块分析：当前市场热点板块及其表现
                3. 资金流向分析：主力资金流入流出情况
                4. 技术面分析：关键支撑位、阻力位、技术指标信号等
                5. 消息面分析：重要政策、经济数据、国际形势等影响
                
                请给出具体的分析结论和投资建议。
                """
            
            # 调用大模型API生成市场分析
            result = qwen_api.call_qwen_api(prompt)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"生成市场分析失败: {result['error']}"
                }
            
            # 保存分析报告到数据库
            db = get_db_session()
            try:
                analysis = MarketAnalysis(
                    content=result["data"]
                )
                db.add(analysis)
                db.commit()
                db.refresh(analysis)
                
                return {
                    "success": True,
                    "data": {
                        "analysis_id": analysis.id,
                        "report": result["data"],
                        "created_at": analysis.created_at.isoformat() if analysis.created_at else None
                    }
                }
            except Exception as e:
                db.rollback()
                return {
                    "success": False,
                    "error": f"保存分析报告失败: {str(e)}"
                }
            finally:
                close_db_session(db)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"生成市场分析过程出错: {str(e)}"
            }
    
    def record_sector_rotation(self, sector_info: dict) -> dict:
        """
        记录板块轮动事件
        
        Args:
            sector_info (dict): 板块信息
            
        Returns:
            dict: 记录结果
        """
        try:
            # 验证必需字段
            required_fields = ["sector_name", "rotation_type", "reason"]
            for field in required_fields:
                if field not in sector_info:
                    return {
                        "success": False,
                        "error": f"缺少必需字段: {field}"
                    }
            
            # 保存板块轮动记录到数据库
            db = get_db_session()
            try:
                rotation = SectorRotation(
                    sector_name=sector_info["sector_name"],
                    rotation_type=sector_info["rotation_type"],  # in/out 表示轮入/轮出
                    reason=sector_info["reason"],
                    details=sector_info.get("details", "")
                )
                db.add(rotation)
                db.commit()
                db.refresh(rotation)
                
                return {
                    "success": True,
                    "data": {
                        "rotation_id": rotation.id,
                        "sector_name": rotation.sector_name,
                        "rotation_type": rotation.rotation_type,
                        "reason": rotation.reason,
                        "details": rotation.details,
                        "created_at": rotation.created_at.isoformat() if rotation.created_at else None
                    }
                }
            except Exception as e:
                db.rollback()
                return {
                    "success": False,
                    "error": f"保存板块轮动记录失败: {str(e)}"
                }
            finally:
                close_db_session(db)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"记录板块轮动过程出错: {str(e)}"
            }
    
    def get_today_sector_rotations(self) -> dict:
        """
        获取今日板块轮动情况
        
        Returns:
            dict: 今日板块轮动列表
        """
        from datetime import datetime, date
        
        db = get_db_session()
        try:
            # 查询今天的板块轮动记录
            today = date.today()
            rotations = db.query(SectorRotation).filter(
                SectorRotation.created_at >= today
            ).order_by(SectorRotation.created_at.desc()).all()
            
            rotation_list = []
            for rotation in rotations:
                rotation_list.append({
                    "id": rotation.id,
                    "sector_name": rotation.sector_name,
                    "rotation_type": rotation.rotation_type,
                    "reason": rotation.reason,
                    "details": rotation.details,
                    "created_at": rotation.created_at.isoformat() if rotation.created_at else None
                })
            
            return {
                "success": True,
                "data": rotation_list
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取今日板块轮动失败: {str(e)}"
            }
        finally:
            close_db_session(db)
    
    def daily_market_analysis(self) -> dict:
        """
        执行每日市场分析
        
        Returns:
            dict: 分析结果
        """
        try:
            # 生成市场分析报告
            analysis_result = self.generate_market_analysis()
            
            if not analysis_result["success"]:
                return {
                    "success": False,
                    "error": f"生成市场分析报告失败: {analysis_result['error']}"
                }
            
            # 分析板块轮动情况（这里简化为模拟）
            sector_prompt = """
            请分析当前市场的板块轮动情况，指出哪些板块正在轮入，哪些板块正在轮出，
            并说明轮动的原因。请以JSON格式返回结果，格式如下：
            {
                "rotations": [
                    {
                        "sector_name": "板块名称",
                        "rotation_type": "in/out",
                        "reason": "轮动原因"
                    }
                ]
            }
            """
            
            sector_result = qwen_api.call_qwen_api(sector_prompt)
            
            if not sector_result["success"]:
                return {
                    "success": False,
                    "error": f"分析板块轮动失败: {sector_result['error']}"
                }
            
            # 记录板块轮动
            rotation_records = []
            if "rotations" in sector_result["data"]:
                for rotation in sector_result["data"]["rotations"]:
                    record_result = self.record_sector_rotation(rotation)
                    if record_result["success"]:
                        rotation_records.append(record_result["data"])
            
            return {
                "success": True,
                "data": {
                    "market_analysis": analysis_result["data"],
                    "sector_rotations": rotation_records
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"执行每日市场分析过程出错: {str(e)}"
            }
    
    def check_sector_rotation(self) -> dict:
        """
        检查板块轮动情况
        
        Returns:
            dict: 轮动分析结果
        """
        try:
            prompt = """
            请分析当前A股市场的板块轮动情况，指出哪些板块正在轮入，哪些板块正在轮出，
            并说明轮动的原因和潜在影响。请关注以下方面：
            1. 近期表现强势的板块
            2. 近期表现弱势的板块
            3. 资金流入流出明显的板块
            4. 政策或消息面影响的板块
            
            请给出具体的分析和投资建议。
            """
            
            result = qwen_api.call_qwen_api(prompt)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"分析板块轮动失败: {result['error']}"
                }
            
            return {
                "success": True,
                "data": result["data"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"检查板块轮动过程出错: {str(e)}"
            }
    
    def reply(self, x: dict = None) -> dict:
        """
        Agent回复方法
        
        Args:
            x (dict): 输入消息
            
        Returns:
            dict: 回复消息
        """
        if x is None:
            return Msg(self.name, "请指定需要执行的操作", "assistant")
        
        # 解析输入消息
        if isinstance(x, Msg):
            content = x.content
        else:
            content = x
            
        # 根据输入内容执行相应操作
        if isinstance(content, dict):
            action = content.get("action")
            
            if action == "generate_report":
                market_data = content.get("market_data")
                result = self.generate_market_analysis(market_data)
                return Msg(self.name, result, "assistant")
            elif action == "record_rotation":
                sector_info = content.get("sector_info")
                result = self.record_sector_rotation(sector_info)
                return Msg(self.name, result, "assistant")
            elif action == "get_todays_rotations":
                result = self.get_today_sector_rotations()
                return Msg(self.name, result, "assistant")
            elif action == "daily_analysis":
                result = self.daily_market_analysis()
                return Msg(self.name, result, "assistant")
            elif action == "check_rotation":
                result = self.check_sector_rotation()
                return Msg(self.name, result, "assistant")
            else:
                return Msg(self.name, "不支持的操作，请指定正确的action", "assistant")
        else:
            # 默认执行市场分析
            result = self.generate_market_analysis()
            return Msg(self.name, result, "assistant")