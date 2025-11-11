#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境变量加载
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

print("环境变量测试:")
print(f"DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY}")
print(f"DEEPSEEK_API_URL: {DEEPSEEK_API_URL}")

# 检查API密钥是否配置
if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_actual_deepseek_api_key_here":
    print("警告: 未配置有效的DeepSeek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
else:
    print("DeepSeek API密钥已正确配置")