#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试运行器
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """运行所有测试"""
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    print("开始运行所有测试...")
    success = run_all_tests()
    if success:
        print("\n所有测试通过!")
        sys.exit(0)
    else:
        print("\n部分测试失败!")
        sys.exit(1)