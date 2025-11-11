#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent协作流程管理
"""

import agentscope
from agentscope.agents import AgentBase, DialogAgent
from agentscope.message import Msg
from agents.stock_agent import StockAnalysisAgent
from agents.chat_agent import ChatManagementAgent
from agents.risk_agent import RiskControlAgent
from agents.market_agent import MarketAnalysisAgent

class AgentOrchestrator:
    """Agent协作流程管理器"""
    
    def __init__(self) -> None:
        """初始化Agent协作管理器"""
        # 初始化各个Agent
        self.stock_agent = StockAnalysisAgent(name="StockAnalyzer")
        self.chat_agent = ChatManagementAgent(name="ChatManager")
        self.risk_agent = RiskControlAgent(name="RiskController")
        self.market_agent = MarketAnalysisAgent(name="MarketAnalyzer")
        
        # 初始化对话Agent（用于通用对话）
        self.dialog_agent = DialogAgent(
            name="GeneralAssistant",
            sys_prompt="你是一个专业的股票投资助手，可以回答用户关于股票、投资、市场等方面的问题。",
            model_config_name="qwen"
        )
        
    def handle_stock_analysis(self, image_path: str = None, text_query: str = None) -> dict:
        """
        处理股票分析请求
        
        Args:
            image_path (str): 股票图片路径(可选)
            text_query (str): 文本查询(可选)
            
        Returns:
            dict: 分析结果
        """
        try:
            if image_path:
                # 处理图片分析
                result = self.stock_agent.analyze_stock_image(image_path)
                return result
            elif text_query:
                # 处理文本查询
                # 这里可以结合风险评估
                risk_result = self.risk_agent.assess_risk_from_text(text_query)
                if risk_result["success"]:
                    # 将风险评估结果传递给股票分析Agent
                    analysis_input = {
                        "query": text_query,
                        "risk_info": risk_result["data"]
                    }
                    # 这里简化处理，实际可能需要更复杂的交互
                    return self.stock_agent.reply(analysis_input)
                else:
                    return risk_result
            else:
                return {
                    "success": False,
                    "error": "请提供图片路径或文本查询"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理股票分析请求失败: {str(e)}"
            }
    
    def handle_chat_interaction(self, user_id: str, query: str, image_path: str = None) -> dict:
        """
        处理聊天交互
        
        Args:
            user_id (str): 用户ID
            query (str): 用户查询
            image_path (str): 图片路径(可选)
            
        Returns:
            dict: 对话结果
        """
        try:
            chat_input = {
                "user_id": user_id,
                "query": query,
                "image_path": image_path
            }
            result = self.chat_agent.reply(chat_input)
            return {
                "success": True,
                "data": result.content if isinstance(result, Msg) else result
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理聊天交互失败: {str(e)}"
            }
    
    def handle_risk_assessment(self, content: dict) -> dict:
        """
        处理风险评估请求
        
        Args:
            content (dict): 评估内容，可以是text或stock_data
            
        Returns:
            dict: 评估结果
        """
        try:
            result = self.risk_agent.reply(content)
            return {
                "success": True,
                "data": result.content if isinstance(result, Msg) else result
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理风险评估请求失败: {str(e)}"
            }
    
    def handle_market_analysis(self, action: str = "generate_report", **kwargs) -> dict:
        """
        处理市场分析请求
        
        Args:
            action (str): 执行操作
            **kwargs: 其他参数
            
        Returns:
            dict: 分析结果
        """
        try:
            market_input = {
                "action": action,
                **kwargs
            }
            result = self.market_agent.reply(market_input)
            return {
                "success": True,
                "data": result.content if isinstance(result, Msg) else result
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理市场分析请求失败: {str(e)}"
            }
    
    def coordinate_agents(self, user_input: dict) -> dict:
        """
        协调多个Agent处理复杂任务
        
        Args:
            user_input (dict): 用户输入
            
        Returns:
            dict: 处理结果
        """
        try:
            task_type = user_input.get("task_type")
            
            if task_type == "comprehensive_analysis":
                # 综合分析：市场分析 + 风险评估 + 股票分析
                # 1. 获取市场分析
                market_result = self.handle_market_analysis("generate_report")
                
                # 2. 风险评估
                risk_input = {
                    "text": user_input.get("analysis_context", "")
                }
                risk_result = self.handle_risk_assessment(risk_input)
                
                # 3. 股票分析（如果有股票代码）
                stock_result = None
                stock_code = user_input.get("stock_code")
                if stock_code:
                    stock_query = f"请分析股票{stock_code}的投资价值"
                    stock_result = self.handle_stock_analysis(text_query=stock_query)
                
                return {
                    "success": True,
                    "data": {
                        "market_analysis": market_result,
                        "risk_assessment": risk_result,
                        "stock_analysis": stock_result
                    }
                }
            elif task_type == "daily_report":
                # 生成每日报告：市场分析 + 板块轮动 + 风险提示
                # 1. 执行每日市场分析
                daily_result = self.handle_market_analysis("daily_analysis")
                
                # 2. 检查风险
                risk_result = self.handle_risk_assessment({"text": "每日风险检查"})
                
                return {
                    "success": True,
                    "data": {
                        "daily_analysis": daily_result,
                        "risk_check": risk_result
                    }
                }
            else:
                # 默认使用通用对话Agent
                result = self.dialog_agent(user_input.get("query", ""))
                return {
                    "success": True,
                    "data": result.content if isinstance(result, Msg) else result
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"协调Agent处理任务失败: {str(e)}"
            }

# 创建全局实例
orchestrator = AgentOrchestrator()

def get_orchestrator():
    """获取Agent协调器实例"""
    return orchestrator