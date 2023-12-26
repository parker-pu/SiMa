# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

模型
"""

from sqlalchemy import (
    Column,
    String,
    BOOLEAN,
    Text,
    DECIMAL
)

from src.utils.db.aiodb import Base
from src.utils.db.model import ModelDefault


class DynamicAPIDataModel(ModelDefault, Base):
    """
    API 接口数据
    """
    __tablename__ = "dynamic_api_data"

    subject_name = Column(String(255), comment="接口所属主题域")
    api_status = Column(BOOLEAN, default=True, index=False, server_default="0", comment="激活")
    api_name = Column(String(255), comment="接口名称")
    api_desc = Column(Text, comment="用于生成接口描述文档")
    api_version = Column(String(255), comment="接口版本")
    methods = Column(String(255), comment="接口请求方式")
    jinja_content = Column(Text, comment="jinja2格式的内容")
    inner_validate = Column(Text, comment="内部保留的验证器")
    custom_validate = Column(Text, comment="自定义的验证器")
    target_desc = Column(Text, comment="指标描述")

    def __str__(self):
        return self.subject_name
