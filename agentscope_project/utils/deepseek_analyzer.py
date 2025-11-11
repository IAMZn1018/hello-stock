#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI分析工具
用于将股票信息发送给DeepSeek AI进行专业分析
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# 检查API密钥是否配置
print(f"[DEBUG] DEEPSEEK_API_KEY loaded: {DEEPSEEK_API_KEY[:10] if DEEPSEEK_API_KEY else None}...{DEEPSEEK_API_KEY[-5:] if DEEPSEEK_API_KEY else ''}")
if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
    print("警告: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
    print(f"当前DEEPSEEK_API_KEY值: {DEEPSEEK_API_KEY}")
    DEEPSEEK_API_KEY = None  # 确保全局变量被正确设置
else:
    print("[DEBUG] DeepSeek API密钥已正确配置")

# HTTP客户端会话
session = requests.Session()
# 设置默认超时时间为3分钟
DEFAULT_TIMEOUT = 180.0

def analyze_stock_with_deepseek(stock_name: str, stock_info: str) -> Optional[str]:
    """
    使用DeepSeek AI分析股票信息
    
    Args:
        stock_name (str): 股票名称
        stock_info (str): 股票信息字符串
        
    Returns:
        Optional[str]: 分析结果，如果失败则返回None
    """
    print(f"[DEBUG] analyze_stock_with_deepseek called with stock: {stock_name}")
    
    # 重新加载环境变量（确保最新）
    global DEEPSEEK_API_KEY
    if not DEEPSEEK_API_KEY:
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        print(f"[DEBUG] Reloaded DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY[:10] if DEEPSEEK_API_KEY else None}...")
    
    # 检查API密钥
    print(f"[DEBUG] Checking API key: {DEEPSEEK_API_KEY[:10] if DEEPSEEK_API_KEY else None}...")
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
        print("错误: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
        print(f"当前DEEPSEEK_API_KEY值: {DEEPSEEK_API_KEY}")
        return None
    
    print("[DEBUG] API key is valid, proceeding with analysis")
    
    try:
        # 构建提示词
        prompt = f"""
你是一位专业的股票分析师，请根据以下{stock_name}的详细信息，给出专业的投资建议：

{stock_info}

请从以下几个方面进行分析并给出具体建议：

1. 短期建议（1-2周）：
   - 股价走势预测
   - 买卖时机建议
   - 需要关注的关键指标

2. 中期建议（1-3个月）：
   - 趋势判断
   - 潜在上涨或下跌空间
   - 重点关注的事件或数据

3. 投资风险：
   - 主要风险因素
   - 风险控制建议
   - 不利情况下的应对策略

4. 投资机会：
   - 主要利好因素
   - 潜在增长点
   - 可能的催化剂

5. 止盈止损策略：
   - 建议的止盈点位
   - 建议的止损点位
   - 分批操作建议（如果适用）

请用清晰、专业的语言给出具体、可操作的建议，避免使用模棱两可的表述。
"""
        
        print(f"[DEBUG] Prompt length: {len(prompt)} characters")
        
        # 准备请求数据
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一位专业的股票投资分析师，擅长根据各种股票数据给出专业的投资建议。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print("[DEBUG] Sending request to DeepSeek API...")
        print(f"[DEBUG] Request URL: {DEEPSEEK_API_URL}")
        print(f"[DEBUG] Request headers: {headers}")
        print(f"[DEBUG] Request payload size: {len(str(payload))} characters")
        
        # 发送POST请求到DeepSeek API
        try:
            response = session.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)
            print(f"[DEBUG] Received response with status code: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Network request failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
        
        # 检查响应状态码
        if response.status_code != 200:
            print(f"[ERROR] DeepSeek API returned status code: {response.status_code}")
            print(f"[ERROR] Response headers: {dict(response.headers)}")
            print(f"[ERROR] Response text: {response.text}")
            return None
        
        # 解析响应
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to decode JSON response: {str(e)}")
            print(f"[ERROR] Response text: {response.text}")
            return None
        print(f"[DEBUG] Response parsed successfully")
        analysis = result["choices"][0]["message"]["content"]
        print(f"[DEBUG] Analysis extracted, length: {len(analysis)} characters")
        
        return analysis
        
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] DeepSeek API返回HTTP状态错误 {e.response.status_code}")
        print(f"[ERROR] Response headers: {dict(e.response.headers)}")
        print(f"[ERROR] Response text: {e.response.text}")
        return None
    except KeyError as e:
        print(f"[ERROR] 解析DeepSeek API响应失败，缺少字段 {e}")
        print(f"[ERROR] Response content: {result if 'result' in locals() else 'No response data'}")
        return None
    except Exception as e:
        print(f"[ERROR] 调用DeepSeek API时发生未知错误 - {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def format_analysis_result(analysis: str) -> str:
    """
    格式化分析结果
    
    Args:
        analysis (str): DeepSeek AI的分析结果
        
    Returns:
        str: 格式化后的分析结果
    """
    if not analysis:
        return "未获取到分析结果"
    
    formatted_lines = []
    formatted_lines.append("=== DeepSeek AI 股票分析报告 ===")
    formatted_lines.append(analysis)
    
    return "\n".join(formatted_lines)

# 示例用法
if __name__ == "__main__":
    # 这里只是一个示例，实际使用时需要传入真实的股票信息
    example_stock_info = """
    【简介和看点】
    三维通信是一家专注于无线通信设备制造的公司...
    
    【支撑位压力位】
    支撑位：11.18
    压力位：12.98
    """
    
    print("正在分析股票信息...")
    analysis = analyze_stock_with_deepseek("三维通信", example_stock_info)
    if analysis:
        print(format_analysis_result(analysis))
    else:
        print("分析失败，未获取到结果")