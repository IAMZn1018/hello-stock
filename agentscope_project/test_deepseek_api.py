#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试DeepSeek API调用
"""

import os
import json
import httpx
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

print("DeepSeek API配置检查:")
print(f"DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY[:10]}...{DEEPSEEK_API_KEY[-5:] if DEEPSEEK_API_KEY else 'None'}")
print(f"DEEPSEEK_API_URL: {DEEPSEEK_API_URL}")

# 检查API密钥是否配置
if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
    print("错误: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
    exit(1)

# 测试API调用
try:
    # 构建测试提示词
    prompt = "请用一句话回答：人工智能是什么？"
    
    # 准备请求数据
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的AI助手。"},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("\n正在发送请求到DeepSeek API...")
    print(f"请求URL: {DEEPSEEK_API_URL}")
    print(f"请求头: {{'Authorization': 'Bearer ***', 'Content-Type': 'application/json'}}")
    print(f"请求数据: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    # 发送POST请求到DeepSeek API
    response = httpx.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30.0)
    
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        # 解析响应
        result = response.json()
        print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        analysis = result["choices"][0]["message"]["content"]
        print(f"\nAI回答: {analysis}")
    else:
        print(f"错误：DeepSeek API返回错误 {response.status_code} - {response.text}")
        
except httpx.TimeoutException as e:
    print(f"错误：请求DeepSeek API超时 - {str(e)}")
except httpx.HTTPStatusError as e:
    print(f"错误：DeepSeek API返回错误 {e.response.status_code} - {e.response.text}")
except KeyError as e:
    print(f"错误：解析DeepSeek API响应失败，缺少字段 {e}")
    print(f"响应内容: {response.text if 'response' in locals() else '无响应'}")
except Exception as e:
    print(f"错误：调用DeepSeek API时发生未知错误 - {str(e)}")
    import traceback
    traceback.print_exc()