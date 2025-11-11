#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试DeepSeek分析功能
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.deepseek_analyzer_debug import analyze_stock_with_deepseek, format_analysis_result

# 测试数据
test_stock_name = "三维通信"
test_stock_info = """
【简介和看点】
三维通信股份有限公司是一家专注于无线通信设备制造的公司，主要产品包括移动通信网络优化覆盖设备、系统集成服务等。公司为国家高新技术企业，拥有强大的研发实力和技术积累。

【财务指标】
- 营业收入：稳步增长
- 净利润：持续改善
- 毛利率：保持稳定
- 资产负债率：合理水平

【市场表现】
近期股价表现活跃，受到资金关注。
"""

print("开始直接测试DeepSeek分析功能...")
print(f"股票名称: {test_stock_name}")
print(f"股票信息长度: {len(test_stock_info)} 字符")

# 调用分析函数
analysis = analyze_stock_with_deepseek(test_stock_name, test_stock_info)

if analysis:
    print("分析成功!")
    formatted_result = format_analysis_result(analysis)
    print(formatted_result)
else:
    print("分析失败!")

print("测试完成。")