#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统功能测试脚本
"""

import os
import sys
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_creation():
    """测试数据库表创建"""
    print("测试数据库表创建...")
    try:
        from app.database.base import init_db
        init_db()
        print("✓ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"✗ 数据库表创建失败: {e}")
        return False

def test_model_imports():
    """测试模型导入"""
    print("测试模型导入...")
    try:
        # 测试所有模型导入
        from app.models import chat, stock, risk, market
        print("✓ 所有模型导入成功")
        return True
    except Exception as e:
        print(f"✗ 模型导入失败: {e}")
        return False

def test_schema_imports():
    """测试Schema导入"""
    print("测试Schema导入...")
    try:
        # 测试所有Schema导入
        from app.schemas import chat, stock, risk, market
        print("✓ 所有Schema导入成功")
        return True
    except Exception as e:
        print(f"✗ Schema导入失败: {e}")
        return False

def test_router_imports():
    """测试路由导入"""
    print("测试路由导入...")
    try:
        # 测试所有路由导入
        from app.routers import stock, chat, risk, market
        print("✓ 所有路由导入成功")
        return True
    except Exception as e:
        print(f"✗ 路由导入失败: {e}")
        return False

def test_core_modules():
    """测试核心模块"""
    print("测试核心模块...")
    try:
        from app.core.qwen_api import QwenAPI
        from app.utils.similarity import cosine_similarity
        print("✓ 核心模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 核心模块导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始系统功能测试...\n")
    
    tests = [
        test_model_imports,
        test_schema_imports,
        test_router_imports,
        test_core_modules,
        test_database_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        return 0
    else:
        print("❌ 部分测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())