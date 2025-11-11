#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票综合分析工具
整合问财数据获取和DeepSeek AI分析功能
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Optional, Tuple
from utils.wencai_tool import get_stock_info, format_stock_info
from utils.deepseek_analyzer import analyze_stock_with_deepseek, format_analysis_result

def analyze_stock(stock_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    综合分析股票：先获取问财数据，再用DeepSeek进行分析
    
    Args:
        stock_name (str): 股票名称或代码
        
    Returns:
        tuple: (股票信息, DeepSeek分析结果)
    """
    print(f"正在分析股票: {stock_name}")
    
    # 1. 获取问财股票信息
    print("正在从问财接口获取股票信息...")
    stock_info_dict = get_stock_info(stock_name)
    
    if not stock_info_dict:
        return None, f"未能获取到 {stock_name} 的股票信息"
    
    # 格式化股票信息
    stock_info_str = format_stock_info(stock_info_dict)
    print(f"成功获取 {stock_name} 的股票信息")
    
    # 2. 使用DeepSeek进行分析
    print("正在使用DeepSeek AI进行分析...")
    analysis = analyze_stock_with_deepseek(stock_name, stock_info_str)
    
    if not analysis:
        return stock_info_str, f"DeepSeek AI分析失败"
    
    print(f"DeepSeek AI分析完成")
    return stock_info_str, analysis

def print_analysis_result(stock_name: str, stock_info: str, analysis: str):
    """
    打印分析结果
    
    Args:
        stock_name (str): 股票名称
        stock_info (str): 股票信息
        analysis (str): 分析结果
    """
    print("\n" + "="*60)
    print(f"股票综合分析报告 - {stock_name}")
    print("="*60)
    
    print("\n【股票基本信息】")
    # 只显示股票信息的前1000个字符，避免输出过长
    if len(stock_info) > 1000:
        print(stock_info[:1000] + "...\n(信息过长，已截取)")
    else:
        print(stock_info)
    
    print("\n【DeepSeek AI 分析结果】")
    # 只显示分析结果的前2000个字符，避免输出过长
    if len(analysis) > 2000:
        print(analysis[:2000] + "...\n(分析过长，已截取)")
    else:
        print(analysis)

# 示例用法
if __name__ == "__main__":
    if len(sys.argv) > 1:
        stock_name = sys.argv[1]
    else:
        stock_name = "三维通信"  # 默认股票
    
    print(f"开始分析股票: {stock_name}")
    
    stock_info, analysis = analyze_stock(stock_name)
    
    if stock_info and analysis:
        print_analysis_result(stock_name, stock_info, analysis)
    else:
        print(f"分析失败: {analysis}")