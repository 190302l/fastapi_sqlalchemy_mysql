#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI

from backend.app.common.sys_redis import redis_client
from backend.app.core.conf import settings
from backend.app.api.v1 import v1
from backend.app.middleware import register_middleware


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL
    )

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 初始化连接
    register_init(app)

    return app


def register_router(app):
    """
    路由
    :param app: FastAPI
    :return:
    """
    app.include_router(
        v1,
    )


def register_init(app):
    """
    初始化连接
    :param app: FastAPI
    :return:
    """

    @app.on_event("startup")
    async def startup_event():
        # 连接redis
        await redis_client.init_redis_connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await redis_client.init_redis_connect().close()
