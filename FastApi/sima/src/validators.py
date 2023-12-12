# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

一些公共的验证
"""
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ValidateTimeData(BaseModel):
    start_time: datetime = Field(title="开始时间", description="页面选择输入的开始时间")
    end_time: datetime = Field(title="结束时间", description="页面选择输入的结束时间")


class ValidatePaginator(BaseModel):
    """
    验证页面参数
    """
    page: int = Field(default=1, ge=1, title="页码", description="分页时候使用")
    size: int = Field(default=10, ge=0, le=100, title="大小", description="页面数据大小")


class OrderBYEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class ValidateOrderFiled(BaseModel):
    """
    验证页面排序字段
    """

    order_by: OrderBYEnum = Field(title="顺序", description="排序的时候使用")
    order_filed: str = Field(title="排序字段", description="排序的时候使用", min_length=1)


class ValidateExpFiled(BaseModel):
    """
    验证导出字段
    """

    class ValidateExpFiledItem(BaseModel):
        key: str = Field(title="指标名称", description="指标名称")
        name: str = Field(title="导出字段名", description="导出的时候使用在标题上")

    fields: List[ValidateExpFiledItem] = Field(title="导出字段", description="导出的时候使用")


class RespModel(BaseModel):
    """
    验证导出字段
    """
    code: str = Field(title="错误代码", description="返回的时候的错误代码")
    msg: str = Field(title="错误信息", description="出错时候返回的错误数据")
    data: str = Field(title="数据", description="返回的时候的数据")
