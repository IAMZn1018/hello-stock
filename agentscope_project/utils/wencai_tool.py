#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺问财接口工具
用于查询个股的详细信息
"""

import pywencai
import json
import pandas as pd
from typing import Dict, Any, Optional

def _convert_nested_dataframe(obj):
    """
    递归处理嵌套在字典或列表中的DataFrame对象
    
    Args:
        obj: 需要处理的对象
        
    Returns:
        处理后的对象
    """
    if isinstance(obj, dict):
        # 如果是字典，递归处理每个值
        return {key: _convert_nested_dataframe(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        # 如果是列表，递归处理每个元素
        return [_convert_nested_dataframe(item) for item in obj]
    elif isinstance(obj, pd.DataFrame):
        # 如果是DataFrame，转换为字典
        try:
            return obj.to_dict(orient='records')
        except:
            return str(obj)
    elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        # 如果有to_dict方法，尝试调用它
        try:
            return obj.to_dict()
        except:
            return str(obj)
    else:
        # 其他情况直接返回
        return obj

def _convert_to_string(value: Any) -> str:
    """
    将各种数据类型统一转换为字符串
    
    Args:
        value: 需要转换的值
        
    Returns:
        str: 转换后的字符串
    """
    try:
        # 首先处理嵌套的DataFrame
        processed_value = _convert_nested_dataframe(value)
        
        if isinstance(processed_value, dict):
            # 如果值是字典，转换为JSON字符串
            return json.dumps(processed_value, ensure_ascii=False, indent=2, default=str)
        elif isinstance(processed_value, list):
            # 如果值是列表，转换为字符串
            return json.dumps(processed_value, ensure_ascii=False, indent=2, default=str)
        elif pd.isna(processed_value):
            # 处理NaN值
            return "无数据"
        else:
            # 其他情况直接转换为字符串
            return str(processed_value)
    except Exception as e:
        # 如果转换过程中出现任何错误，返回错误信息
        return f"转换失败: {str(e)}"

def get_stock_info(stock_name: str) -> Optional[Dict[str, Any]]:
    """
    通过同花顺问财接口获取股票信息
    
    Args:
        stock_name (str): 股票名称或代码
        
    Returns:
        dict: 股票相关信息，包括：
            - 简介和看点
            - 支撑位压力位
            - 所属概念列表
            - 北向资金流向情况
            - 历史主力资金流向
            - DDE散户数量变化
            - 龙虎榜分析
            - 财务数据
            - 估值指标
            - 十大股东持股比例
            - 重要新闻
            - 投顾点评
            - 牛叉诊股
            - 历史龙虎榜
    """
    try:
        # 调用问财接口
        res = pywencai.get(query=stock_name)
        
        if res is None:
            return None
            
        # 解析返回结果并统一转换为字符串
        stock_info = {}
        
        # 提取关键信息并统一转换为字符串格式
        if isinstance(res, dict):
            # 遍历字典中的每个键值对，将值统一转换为字符串
            for key, value in res.items():
                stock_info[key] = _convert_to_string(value)
        elif isinstance(res, pd.DataFrame):
            # 如果返回的是DataFrame，将其转换为字典后再处理
            stock_info["data"] = _convert_to_string(res)
        else:
            # 如果不是字典也不是DataFrame，直接转换为字符串
            stock_info["raw_data"] = _convert_to_string(res)
            
        return stock_info
        
    except Exception as e:
        print(f"获取股票信息失败: {e}")
        return None

def format_stock_info(stock_info: Dict[str, Any]) -> str:
    """
    格式化股票信息为易读的文本
    
    Args:
        stock_info (dict): 股票信息字典
        
    Returns:
        str: 格式化后的文本
    """
    if not stock_info:
        return "未获取到股票信息"
    
    # 构建格式化的文本输出
    formatted_lines = []
    formatted_lines.append("=== 股票信息 ===")
    
    for key, value in stock_info.items():
        formatted_lines.append(f"\n【{key}】")
        # 限制长度以避免输出过长
        if isinstance(value, str) and len(value) > 1000:
            formatted_lines.append(value[:1000] + "... (内容过长已截取)")
        else:
            formatted_lines.append(str(value))
    
    return "\n".join(formatted_lines)

# 示例用法
if __name__ == "__main__":
    # 测试代码
    stock_name = "三维通信"
    print(f"正在查询 {stock_name} 的信息...")
    
    stock_info = get_stock_info(stock_name)
    if stock_info:
        print("查询成功，股票信息如下：")
        print(format_stock_info(stock_info))
    else:
        print("查询失败，未获取到相关信息")