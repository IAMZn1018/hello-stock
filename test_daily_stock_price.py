#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试daily_stock_price表的创建和使用
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.base import init_db, get_db
from app.models.stock import DailyStockPrice

def test_daily_stock_price():
    """测试DailyStockPrice模型"""
    print("初始化数据库...")
    init_db()
    print("数据库初始化完成")
    
    # 获取数据库会话
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        # 创建测试数据
        test_price = DailyStockPrice(
            stock_code="SH600000",
            stock_name="浦发银行",
            price=10.50,
            timestamp=datetime.now()
        )
        
        # 添加到数据库
        db.add(test_price)
        db.commit()
        db.refresh(test_price)
        
        print(f"成功创建测试记录，ID: {test_price.id}")
        print(f"股票代码: {test_price.stock_code}")
        print(f"股票名称: {test_price.stock_name}")
        print(f"股价: {test_price.price}")
        print(f"时间戳: {test_price.timestamp}")
        print(f"创建时间: {test_price.created_at}")
        
        # 查询测试数据
        retrieved_price = db.query(DailyStockPrice).filter(
            DailyStockPrice.stock_code == "SH600000"
        ).first()
        
        if retrieved_price:
            print("\n查询验证成功:")
            print(f"ID: {retrieved_price.id}")
            print(f"股票代码: {retrieved_price.stock_code}")
            print(f"股票名称: {retrieved_price.stock_name}")
            print(f"股价: {retrieved_price.price}")
            print(f"时间戳: {retrieved_price.timestamp}")
        else:
            print("\n查询验证失败")
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        db.rollback()
    finally:
        # 清理测试数据
        try:
            if 'test_price' in locals():
                db.delete(test_price)
                db.commit()
                print("\n测试数据已清理")
        except:
            pass
        # 关闭数据库连接
        try:
            next(db_generator, None)  # 触发生成器的finally块
        except:
            pass

if __name__ == "__main__":
    test_daily_stock_price()