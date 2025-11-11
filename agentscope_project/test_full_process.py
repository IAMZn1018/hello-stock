#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.wencai_tool import get_stock_info, format_stock_info
from utils.deepseek_analyzer import analyze_stock_with_deepseek

def main():
    """主函数"""
    stock_name = "三维通信"
    
    print(f"开始分析股票: {stock_name}")
    
    # 1. 获取问财股票信息
    print("正在从问财接口获取股票信息...")
    stock_info_dict = get_stock_info(stock_name)
    
    if not stock_info_dict:
        print(f"未能获取到 {stock_name} 的股票信息")
        return
    
    print(f"成功获取 {stock_name} 的股票信息")
    
    # 格式化股票信息
    stock_info_str = format_stock_info(stock_info_dict)
    print(f"格式化后的股票信息长度: {len(stock_info_str)} 字符")
    print(f"股票信息预览: {stock_info_str[:200]}...")
    
    # 2. 使用DeepSeek进行分析
    print("正在使用DeepSeek AI进行分析...")
    analysis = analyze_stock_with_deepseek(stock_name, stock_info_str)
    
    if not analysis:
        print("DeepSeek AI分析失败")
        return
    
    print("DeepSeek AI分析完成")
    print(f"分析结果长度: {len(analysis)} 字符")
    print(f"分析结果预览: {analysis[:200]}...")

if __name__ == "__main__":
    main()