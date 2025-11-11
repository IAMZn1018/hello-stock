#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试配置文件
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试数据库配置
TEST_DATABASE_URL = "sqlite:///./test.db"

# 测试API密钥
TEST_QWEN_API_KEY = "test_api_key"

# 测试模型名称
TEST_QWEN_MODEL = "qwen-max"