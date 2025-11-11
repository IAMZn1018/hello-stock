#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

print(f"API Key: {DEEPSEEK_API_KEY}")
print(f"API URL: {DEEPSEEK_API_URL}")

# 简单的测试提示词
prompt = "请用一句话回答：你好世界"

# 准备请求数据
payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "stream": False
}

# 设置请求头
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

print("Sending request to DeepSeek API...")

try:
    # 发送POST请求到DeepSeek API
    response = httpx.post(DEEPSEEK_API_URL, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")