#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险控制Agent
"""

import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
from utils.database import get_db_session, close_db_session
import sys
sys.path.append('../app')
from core.qwen_api import qwen_api
from models.risk import RiskRecord

class RiskControlAgent(AgentBase):
    """风险控制Agent，负责识别和评估投资风险"""
    
    def __init__(self, name: str = "RiskControlAgent") -> None:
        """初始化风险控制Agent"""
        super().__init__(name=name)
        
    def assess_risk_from_text(self, text: str) -> dict:
        """
        通过文本分析评估风险
        
        Args:
            text (str): 待分析的文本内容
            
        Returns:
            dict: 风险评估结果
        """
        try:
            # 构造提示词
            prompt = f"""
            请分析以下文本中的投资风险：
            
            {text}
            
            请从以下几个维度进行分析：
            1. 市场风险：整体市场波动对投资的影响
            2. 行业风险：特定行业政策变化或竞争加剧的风险
            3. 公司风险：具体公司的经营状况、财务健康度等风险
            4. 技术风险：技术变革对投资标的的影响
            5. 政策风险：政府政策调整可能带来的影响
            
            请给出每个维度的风险等级（低/中/高）和简要说明，并提供总体建议。
            请以JSON格式返回结果，格式如下：
            {{
                "market_risk": {{"level": "风险等级", "description": "详细说明"}},
                "industry_risk": {{"level": "风险等级", "description": "详细说明"}},
                "company_risk": {{"level": "风险等级", "description": "详细说明"}},
                "technology_risk": {{"level": "风险等级", "description": "详细说明"}},
                "policy_risk": {{"level": "风险等级", "description": "详细说明"}},
                "overall_advice": "总体建议"
            }}
            """
            
            # 调用大模型API进行风险分析
            result = qwen_api.call_qwen_api(prompt)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"风险分析失败: {result['error']}"
                }
            
            # 记录风险评估结果到数据库
            db = get_db_session()
            try:
                risk_record = RiskRecord(
                    content=text,
                    analysis_result=result["data"]
                )
                db.add(risk_record)
                db.commit()
                db.refresh(risk_record)
                
                return {
                    "success": True,
                    "data": {
                        "record_id": risk_record.id,
                        "analysis": result["data"]
                    }
                }
            except Exception as e:
                db.rollback()
                return {
                    "success": False,
                    "error": f"保存风险记录失败: {str(e)}"
                }
            finally:
                close_db_session(db)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"风险评估过程出错: {str(e)}"
            }
    
    def assess_risk_from_data(self, stock_data: dict) -> dict:
        """
        通过股票数据分析评估风险
        
        Args:
            stock_data (dict): 股票数据
            
        Returns:
            dict: 风险评估结果
        """
        try:
            # 构造提示词
            prompt = f"""
            请分析以下股票数据中的投资风险：
            
            {stock_data}
            
            请从以下几个维度进行分析：
            1. 价格波动风险：股价近期波动幅度和趋势
            2. 成交量风险：交易活跃度变化
            3. 财务风险：基于提供的财务数据评估
            4. 技术指标风险：各种技术指标显示的风险信号
            
            请给出每个维度的风险等级（低/中/高）和简要说明，并提供总体建议。
            请以JSON格式返回结果，格式如下：
            {{
                "price_volatility_risk": {{"level": "风险等级", "description": "详细说明"}},
                "volume_risk": {{"level": "风险等级", "description": "详细说明"}},
                "financial_risk": {{"level": "风险等级", "description": "详细说明"}},
                "technical_risk": {{"level": "风险等级", "description": "详细说明"}},
                "overall_advice": "总体建议"
            }}
            """
            
            # 调用大模型API进行风险分析
            result = qwen_api.call_qwen_api(prompt)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"风险分析失败: {result['error']}"
                }
            
            # 记录风险评估结果到数据库
            db = get_db_session()
            try:
                risk_record = RiskRecord(
                    content=str(stock_data),
                    analysis_result=result["data"]
                )
                db.add(risk_record)
                db.commit()
                db.refresh(risk_record)
                
                return {
                    "success": True,
                    "data": {
                        "record_id": risk_record.id,
                        "analysis": result["data"]
                    }
                }
            except Exception as e:
                db.rollback()
                return {
                    "success": False,
                    "error": f"保存风险记录失败: {str(e)}"
                }
            finally:
                close_db_session(db)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"风险评估过程出错: {str(e)}"
            }
    
    def get_risk_history(self, limit: int = 10) -> dict:
        """
        获取历史风险评估记录
        
        Args:
            limit (int): 返回记录数量限制
            
        Returns:
            dict: 历史风险评估记录
        """
        db = get_db_session()
        try:
            records = db.query(RiskRecord).order_by(
                RiskRecord.created_at.desc()
            ).limit(limit).all()
            
            history = []
            for record in records:
                history.append({
                    "id": record.id,
                    "content": record.content,
                    "analysis_result": record.analysis_result,
                    "created_at": record.created_at.isoformat() if record.created_at else None
                })
            
            return {
                "success": True,
                "data": history
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取风险历史记录失败: {str(e)}"
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
            return Msg(self.name, "请提供需要分析的内容", "assistant")
        
        # 解析输入消息
        if isinstance(x, Msg):
            content = x.content
        else:
            content = x
            
        # 根据输入内容类型选择相应的风险评估方法
        if isinstance(content, dict):
            if "text" in content:
                result = self.assess_risk_from_text(content["text"])
                return Msg(self.name, result, "assistant")
            elif "stock_data" in content:
                result = self.assess_risk_from_data(content["stock_data"])
                return Msg(self.name, result, "assistant")
            else:
                return Msg(self.name, "请提供有效的分析内容(text或stock_data)", "assistant")
        elif isinstance(content, str):
            result = self.assess_risk_from_text(content)
            return Msg(self.name, result, "assistant")
        else:
            return Msg(self.name, "不支持的输入格式，请提供文本或字典格式的数据", "assistant")