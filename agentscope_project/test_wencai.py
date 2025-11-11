#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺问财工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.wencai_tool import get_stock_info, format_stock_info

def test_wencai_tool():
    """测试问财工具"""
    print("测试同花顺问财工具")
    
    # 测试查询三维通信
    stock_name = "三维通信"
    print(f"\n正在查询 {stock_name} 的信息...")
    
    stock_info = get_stock_info(stock_name)
    if stock_info:
        print("查询成功！")
        print("\n=== 股票信息预览 ===")
        # 显示前几项信息
        count = 0
        for key, value in stock_info.items():
            print(f"\n【{key}】")
            # 限制显示长度
            if isinstance(value, str) and len(value) > 200:
                print(value[:200] + "..." if len(value) > 200 else value)
            else:
                print(value)
            count += 1
            if count >= 5:  # 只显示前5项
                print("\n... (省略更多内容)")
                break
        
        # 测试格式化函数
        print("\n=== 格式化输出预览 ===")
        formatted_info = format_stock_info(stock_info)
        print(formatted_info[:1000] + "..." if len(formatted_info) > 1000 else formatted_info)
    else:
        print("查询失败，未获取到相关信息")

if __name__ == "__main__":
    test_wencai_tool()