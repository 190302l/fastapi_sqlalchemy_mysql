#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.conf import settings
from backend.app.common.log import log

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

try:
    # 数据库引擎
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO)
    # log.success('数据库连接成功')
except Exception as e:
    log.error('数据库链接失败 {}', e)
    sys.exit()
else:
    # 创建会话（增删改查）
    db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    conn = db_session()
    try:
        yield conn
    finally:
        conn.close()


__all__ = ['SQLALCHEMY_DATABASE_URL', 'get_db']
