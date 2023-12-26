# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

异步mysql
"""
import json

from sqlalchemy import create_engine
from datetime import date, datetime
from urllib.parse import quote
from _decimal import Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy_utils import (
    database_exists,
    create_database
)

from src.settings import (
    DB_HOST,
    DB_PASSWORD,
    DB_USER
)
from src.utils.utils import f_data

NEW_DB_PASSWORD = quote(DB_PASSWORD)

# 连接字符串
ASYNC_SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{NEW_DB_PASSWORD}@{DB_HOST}:3306/sima"

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


# 运用 yield 抛出session
async def get_db_session() -> AsyncSession:
    """
    异步数据库会话
    """
    async with SessionLocal() as session:
        yield session


# 非异步,用来创建数据库
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{NEW_DB_PASSWORD}@{DB_HOST}:3306/sima"
if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL)
sync_db_session = scoped_session(sessionmaker(bind=sync_engine))


def get_sync_db_session():
    """
    同步的数据库会话
    """
    with sync_db_session() as session:
        return session


Base = declarative_base()


def to_dict(self):
    """
    变为 dict
    :param self:
    :return:
    """
    return {c.name: f_data(getattr(self, c.name, None)) for c in self.__table__.columns}


def all_columns(self):
    """
    获取所有列名
    """
    return [c.name for c in self.__table__.columns]


Base.to_dict = to_dict
Base.all_columns = all_columns
