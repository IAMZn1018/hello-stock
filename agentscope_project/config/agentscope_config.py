#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Qwen API配置
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "your_api_key_here")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-max")

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Cx1028.+@192.168.31.254:49176/hello-stock")

# 应用配置
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"