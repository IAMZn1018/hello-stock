#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试整合的股票分析功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.stock_analyzer import analyze_stock, print_analysis_result

def test_stock_analyzer():
    """测试股票分析功能"""
    # 测试用的股票名称
    test_stocks = ["三维通信", "宁德时代"]
    
    for stock_name in test_stocks:
        print(f"\n开始分析股票: {stock_name}")
        try:
            stock_info, analysis = analyze_stock(stock_name)
            
            if stock_info and analysis:
                print_analysis_result(stock_name, stock_info, analysis)
            else:
                print(f"分析失败: {analysis}")
                
        except Exception as e:
            print(f"分析 {stock_name} 时发生错误: {str(e)}")
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    # 如果提供了命令行参数，则使用参数中的股票名称
    if len(sys.argv) > 1:
        stock_name = sys.argv[1]
        stock_info, analysis = analyze_stock(stock_name)
        if stock_info and analysis:
            print_analysis_result(stock_name, stock_info, analysis)
        else:
            print(f"分析失败: {analysis}")
    else:
        # 运行默认测试
        test_stock_analyzer()