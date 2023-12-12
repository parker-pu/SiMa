# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

一些公共的验证
"""
from enum import Enum
from typing import Union, Dict, List, Tuple

from pydantic import BaseModel, Field


class DynamicApiCustomValidate(BaseModel):
    class CustomValidateTypeEnum(str, Enum):
        str = "str"
        int = "int"
        list = "list"
        dict = "dict"

    v_key: str = Field(title="验证key", description="自定义验证器")
    v_type: CustomValidateTypeEnum = Field(title="验证类型", description="自定义验证器类型")
    v_desc: str = Field(title="名称描述", description="名称描述")
    v_default: str = Field(default=None, title="默认值", description="默认值")


class TargetDescValidate(BaseModel):
    """
    指标描述
    """

    class TargetInfo(BaseModel):
        target_key: str = Field(title="指标key", description="指标key")
        name: str = Field(title="指标名称", description="指标名称")
        desc: Union[Dict, str] = Field(None, title="指标描述", description="指标描述")

    zh: List[TargetInfo] = Field(title="中文", description="中文")
    en: List[TargetInfo] = Field(title="英文", description="英文")


class DynamicApiValidate(BaseModel):
    """
    动态接口的模型
    """

    class DynamicApiInnerValidateEnum(str, Enum):
        time = "time"
        paginator = "paginator"
        order = "order"
        export = "export"

    subject_name: str = Field(title="主题", description="接口所属主题域")
    api_name: str = Field(title="接口名称", description="接口名称")
    api_desc: str = Field(title="接口描述", description="用于生成接口描述文档")
    api_version: str = Field(title="接口版本", description="接口版本")
    methods: Union[List, Tuple] = Field(["POST"], title="请求方式", description="接口请求方式")
    jinja_content: str = Field(title="接口内容", description="jinja2格式的内容")
    inner_validate: List[DynamicApiInnerValidateEnum] = Field(title="内部验证器", description="内部保留的验证器")
    custom_validate: List[DynamicApiCustomValidate] = Field(title="自定义验证器", description="自定义的验证器")
    target_desc: TargetDescValidate = Field(title="指标描述", description="指标描述")
