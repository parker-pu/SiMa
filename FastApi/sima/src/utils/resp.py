# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

处理返回的 Response
"""
import decimal
import json
from _decimal import Decimal
from datetime import date, datetime

from sqlalchemy.engine.row import RowMapping
import orjson
from fastapi import status
from fastapi.responses import ORJSONResponse
from orjson.orjson import JSONEncodeError
from pydantic import BaseModel, Field
from typing import Union, Optional, Any

from src.utils.error_code import ErrorBase
from src.utils.utils import f_data


class MyORJSONResponse(ORJSONResponse):

    @staticmethod
    def f_default(field):
        """
        格式化数据
        :param field:
        :return:
        """

        if isinstance(field, RowMapping):
            srt = {}
            for k, v in field.items():
                srt[k] = f_data(v)
            return srt
        else:
            return f_data(field)

    def render(self, content: Any) -> bytes:
        """
        编码
        :param content: 内容
        :return:
        """
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content,
            default=self.f_default,
            option=orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )


class RespJsonBase(BaseModel):
    code: int = Field(title="错误编码", description="没错误的时候是0")
    msg: str = Field(title="错误消息", description="错误的时候显示错误消息")
    data: Union[dict, list] = Field(title="数据", description="数据")


def resp_success_json(data: Union[list, dict, str] = None, msg: str = "success"):
    """ 接口成功返回 """
    return MyORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 0,
            "msg": msg,
            "data": data or {}
        }
    )


def resp_error_json(error: ErrorBase, *, msg: Optional[str] = None, msg_append: str = "",
                    data: Union[list, dict, str] = None, status_code: int = status.HTTP_200_OK):
    """ 错误接口返回 """
    return MyORJSONResponse(
        status_code=status_code,
        content={
            "code": error.code,
            "msg": (msg or error.msg) + ((",[" + msg_append + "]") if msg_append else ""),
            "data": data or {}
        }
    )
