#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web API服务 - 为Agent提供HTTP接口
"""

import os
import json
from flask import Flask, request, jsonify
import agentscope
from agents.orchestrator import get_orchestrator
from utils.database import init_db

# 初始化数据库
init_db()

# 初始化AgentScope
agentscope.init(
    project="HelloStock",
    name="StockAssistant-API",
    save_dir="./runs",
    save_log=True,
)

# 初始化Agent协调器
orchestrator = get_orchestrator()

# 创建Flask应用
app = Flask(__name__)

@app.route('/')
def home():
    """首页"""
    return jsonify({
        "message": "Hello Stock AgentScope API服务",
        "version": "1.0.0",
        "endpoints": {
            "stock_analysis": "/api/analyze/stock",
            "chat": "/api/chat",
            "risk_assessment": "/api/risk/assess",
            "market_analysis": "/api/market/analysis",
            "daily_report": "/api/market/daily"
        }
    })

@app.route('/api/analyze/stock', methods=['POST'])
def stock_analysis():
    """股票分析接口"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        text_query = data.get('text_query')
        
        result = orchestrator.handle_stock_analysis(
            image_path=image_path,
            text_query=text_query
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"股票分析失败: {str(e)}"
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_interaction():
    """对话交互接口"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        query = data.get('query')
        image_path = data.get('image_path')
        
        if not user_id or not query:
            return jsonify({
                "success": False,
                "error": "缺少必需参数: user_id 和 query"
            }), 400
        
        result = orchestrator.handle_chat_interaction(
            user_id=user_id,
            query=query,
            image_path=image_path
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"对话交互失败: {str(e)}"
        }), 500

@app.route('/api/risk/assess', methods=['POST'])
def risk_assessment():
    """风险评估接口"""
    try:
        data = request.get_json()
        
        result = orchestrator.handle_risk_assessment(data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"风险评估失败: {str(e)}"
        }), 500

@app.route('/api/market/analysis', methods=['POST'])
def market_analysis():
    """市场分析接口"""
    try:
        data = request.get_json()
        action = data.get('action', 'generate_report')
        
        result = orchestrator.handle_market_analysis(action, **data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"市场分析失败: {str(e)}"
        }), 500

@app.route('/api/market/daily', methods=['GET'])
def daily_market_report():
    """每日市场报告接口"""
    try:
        result = orchestrator.handle_market_analysis('daily_analysis')
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"生成每日市场报告失败: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({
        "success": False,
        "error": "接口不存在"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """处理500错误"""
    return jsonify({
        "success": False,
        "error": "服务器内部错误"
    }), 500

if __name__ == '__main__':
    # 从环境变量获取配置
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"Hello Stock AgentScope API服务启动中...")
    print(f"访问地址: http://{host}:{port}")
    
    # 启动Flask应用
    app.run(host=host, port=port, debug=debug)