#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库工具模块
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.agentscope_config import DATABASE_URL

# 创建Base类
Base = declarative_base()

# 创建数据库引擎
# 根据数据库类型设置不同的连接参数
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """获取数据库会话"""
    return SessionLocal()

def close_db_session(db):
    """关闭数据库会话"""
    db.close()

def init_db():
    """初始化数据库"""
    # 导入所有模型
    from models import stock, chat, risk, market
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)