#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析命令行工具
输入个股名，调用问财接口获取结果后将字符串发给DeepSeek进行分析
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.stock_analyzer import analyze_stock, print_analysis_result

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法: python analyze_stock.py <股票名称或代码>")
        print("例如: python analyze_stock.py 三维通信")
        print("     python analyze_stock.py 002115")
        return
    
    # 获取股票名称
    stock_name = sys.argv[1]
    
    print(f"开始分析股票: {stock_name}")
    
    # 调用分析函数
    stock_info, analysis = analyze_stock(stock_name)
    
    # 输出结果
    if stock_info and analysis:
        print_analysis_result(stock_name, stock_info, analysis)
    else:
        print(f"分析失败: {analysis}")
        if not stock_info:
            print("未能获取到股票信息，请检查股票名称是否正确")
        if not analysis:
            print("未能获取到AI分析结果，请检查DeepSeek API配置")

if __name__ == "__main__":
    main()