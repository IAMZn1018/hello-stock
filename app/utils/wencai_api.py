"""
同花顺问财接口工具
用于查询个股的详细诊股信息
"""

import pywencai
import json
import pandas as pd
from typing import Dict, Any, Optional


class WenCaiAPI:
    """同花顺问财API封装类"""
    
    @staticmethod
    def _convert_nested_dataframe(obj):
        """
        递归处理嵌套在字典或列表中的DataFrame对象
        
        Args:
            obj: 需要处理的对象
            
        Returns:
            处理后的对象
        """
        if isinstance(obj, dict):
            return {key: WenCaiAPI._convert_nested_dataframe(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [WenCaiAPI._convert_nested_dataframe(item) for item in obj]
        elif isinstance(obj, pd.DataFrame):
            try:
                return obj.to_dict(orient='records')
            except:
                return str(obj)
        elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            try:
                return obj.to_dict()
            except:
                return str(obj)
        else:
            return obj
    
    @staticmethod
    def get_stock_diagnosis(stock_code: str) -> Optional[Dict[str, Any]]:
        """
        通过问财接口获取股票诊断信息
        
        Args:
            stock_code: 股票代码或名称，如 "002115" 或 "三维通信"
            
        Returns:
            股票诊断信息字典，包括：
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
            
        Example:
            >>> api = WenCaiAPI()
            >>> data = api.get_stock_diagnosis("002115")
            >>> print(data.keys())
        """
        try:
            # 调用问财接口
            res = pywencai.get(query=stock_code)
            
            if res is None:
                return None
            
            # 递归处理DataFrame
            processed_res = WenCaiAPI._convert_nested_dataframe(res)
            
            return processed_res
            
        except Exception as e:
            print(f"获取股票诊断信息失败: {e}")
            return None
    
    @staticmethod
    def format_diagnosis(diagnosis: Dict[str, Any], sections: list = None) -> str:
        """
        格式化诊断信息为易读的文本
        
        Args:
            diagnosis: 诊断信息字典
            sections: 要显示的部分列表，None表示显示所有
            
        Returns:
            格式化后的文本
        """
        if not diagnosis:
            return "未获取到诊断信息"
        
        formatted_lines = []
        formatted_lines.append("=" * 80)
        formatted_lines.append("股票诊断报告")
        formatted_lines.append("=" * 80)
        
        # 如果指定了sections，只显示这些部分
        items_to_show = diagnosis.items()
        if sections:
            items_to_show = [(k, v) for k, v in diagnosis.items() if k in sections]
        
        for key, value in items_to_show:
            formatted_lines.append(f"\n【{key}】")
            
            # 将值转换为JSON字符串（如果是字典或列表）
            if isinstance(value, (dict, list)):
                try:
                    value_str = json.dumps(value, ensure_ascii=False, indent=2)
                except:
                    value_str = str(value)
            else:
                value_str = str(value)
            
            # 限制长度
            if len(value_str) > 2000:
                formatted_lines.append(value_str[:2000] + "\n... (内容过长已截取)")
            else:
                formatted_lines.append(value_str)
        
        return "\n".join(formatted_lines)

