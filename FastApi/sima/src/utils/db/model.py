# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

模型
"""

from sqlalchemy import DateTime, Column, func, BigInteger
from src.utils.log import logger


class ModelDefault:
    """
    默认的数据库变量
    """
    Logger: logger = logger

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="id")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
