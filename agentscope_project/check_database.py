#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import engine
from sqlalchemy import text

def check_database():
    """检查数据库表结构"""
    print("检查数据库表结构...")
    
    try:
        # 获取所有表名
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"数据库中的表: {tables}")
            
            # 检查daily_stock_price表结构
            if 'daily_stock_price' in tables:
                print("\ndaily_stock_price表存在")
                result = conn.execute(text("DESCRIBE daily_stock_price"))
                columns = [(row[0], row[1]) for row in result]
                print("表结构:")
                for col_name, col_type in columns:
                    print(f"  {col_name}: {col_type}")
            else:
                print("\ndaily_stock_price表不存在")
            
    except Exception as e:
        print(f"检查过程中出现错误: {e}")

if __name__ == "__main__":
    check_database()