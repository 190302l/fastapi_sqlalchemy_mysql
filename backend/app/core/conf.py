#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import secrets
from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ 配置类 """
    # FastAPI
    TITLE: str = '博客系统API'
    VERSION: str = 'v0.0.1'
    DESCRIPTION: str = """
    > demo：
    """
    DOCS_URL: str = '/v1/docs'
    REDOCS_URL: bool = False
    OPENAPI_URL: str = '/v1/openapi'

    # Uvicorn
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    RELOAD: bool = True

    # DB
    DB_ECHO: bool = False
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'fm'
    DB_CHARSET: str = 'utf8mb4'

    # redis
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 5

    # Token
    ALGORITHM: str = 'HS256'  # 算法
    SECRET_KEY: str = '1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk'  # 密钥 (py生成方法：print(secrets.token_urlsafe(32)))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

    # Email
    DEFAULT_FROM_EMAIL: str = 'fastapi-mysql-demo'  # 默认发件说明
    EMAIL_SERVER: str = 'smtp.qq.com'
    EMAIL_USER: str = 'xxxx-nav@qq.com'
    EMAIL_PASSWORD: str = 'cvszjyenrlvfkeaef'  # 授权密码，非邮箱密码

    # 密码重置 cookies 过期时间
    MAX_AGE: int = 60 * 5  # cookies 时效 60 * 5 = 5 分钟

    # 中间件
    CORS: bool = True
    GZIP: bool = True


@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
