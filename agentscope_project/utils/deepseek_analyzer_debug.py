#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI分析工具 - 调试版本
用于将股票信息发送给DeepSeek AI进行专业分析
"""

import os
import json
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

print(f"[DEBUG] 环境变量加载完成")
print(f"[DEBUG] DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY[:10] if DEEPSEEK_API_KEY else None}...{DEEPSEEK_API_KEY[-5:] if DEEPSEEK_API_KEY else ''}")
print(f"[DEBUG] DEEPSEEK_API_URL: {DEEPSEEK_API_URL}")

# 检查API密钥是否配置
if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
    print("[ERROR] 警告: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
    print(f"[ERROR] 当前DEEPSEEK_API_KEY值: {DEEPSEEK_API_KEY}")
    DEEPSEEK_API_KEY = None  # 确保全局变量被正确设置

# HTTP客户端
client = httpx.Client(timeout=30.0)

def analyze_stock_with_deepseek(stock_name: str, stock_info: str) -> Optional[str]:
    """
    使用DeepSeek AI分析股票信息
    
    Args:
        stock_name (str): 股票名称
        stock_info (str): 股票信息字符串
        
    Returns:
        Optional[str]: 分析结果，如果失败则返回None
    """
    print(f"[DEBUG] 开始分析股票: {stock_name}")
    
    # 重新加载环境变量（确保最新）
    global DEEPSEEK_API_KEY
    if not DEEPSEEK_API_KEY:
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        print(f"[DEBUG] 重新加载DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY[:10] if DEEPSEEK_API_KEY else None}...")
    
    # 检查API密钥
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
        print("[ERROR] 错误: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
        print(f"[ERROR] 当前DEEPSEEK_API_KEY值: {DEEPSEEK_API_KEY}")
        return None
    
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
        
        print(f"[DEBUG] 构建提示词完成，长度: {len(prompt)} 字符")
        
        # 准备请求数据
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一位专业的股票投资分析师，擅长根据各种股票数据给出专业的投资建议。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        print(f"[DEBUG] 请求数据准备完成")
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"[DEBUG] 请求头设置完成")
        
        # 发送POST请求到DeepSeek API
        print(f"[DEBUG] 正在发送请求到: {DEEPSEEK_API_URL}")
        response = client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        print(f"[DEBUG] 收到响应，状态码: {response.status_code}")
        
        # 检查响应状态
        if response.status_code != 200:
            print(f"[ERROR] DeepSeek API返回错误状态码: {response.status_code}")
            print(f"[ERROR] 响应内容: {response.text}")
            return None
            
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        print(f"[DEBUG] 响应解析完成")
        
        analysis = result["choices"][0]["message"]["content"]
        print(f"[DEBUG] 提取分析结果完成，长度: {len(analysis)} 字符")
        
        return analysis
        
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] DeepSeek API返回HTTP错误 {e.response.status_code} - {e.response.text}")
        return None
    except KeyError as e:
        print(f"[ERROR] 解析DeepSeek API响应失败，缺少字段 {e}")
        print(f"[ERROR] 响应内容: {result if 'result' in locals() else '无响应数据'}")
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