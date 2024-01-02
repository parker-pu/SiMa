# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

缓存key
"""
import hashlib
from typing import Callable, Optional

from starlette.requests import Request
from starlette.responses import Response

from src.apps.dynamic_api.validate import DynamicApiValidate


def my_default_key_builder(
        func: Callable,
        namespace: Optional[str] = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None
) -> str:
    from fastapi_cache import FastAPICache

    for k in ["db_session"]:
        kwargs.pop(k) if k in kwargs else None

    synamic_api_model = kwargs.get("synamic_api_model")
    if synamic_api_model and isinstance(synamic_api_model, (DynamicApiValidate,)):
        namespace = "{subject_name}:{api_name}".format(subject_name=synamic_api_model.subject_name,
                                                       api_name=synamic_api_model.api_name)
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = (
            prefix
            + hashlib.md5(f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()).hexdigest()
    )
    # print(cache_key)
    return cache_key
