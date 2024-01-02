# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

处理函数
"""
import datetime
import os
import time
from pathlib import Path

from fastapi import params
from fastapi_cache.decorator import cache
from jinja2 import Environment
from pydantic import BaseModel
from sqlalchemy import select, text, update, Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.dynamic_api.jinja_func import (
    ja_concat_in,
    ja_many_to_many_like,
)
from src.apps.dynamic_api.models import DynamicAPIDataModel
from src.settings import BASE_DIR, CACHE_TIME, CURRENT_VERSION
from src.utils import error_code
from src.utils.cache_utils import my_default_key_builder
from src.utils.error_code import SORT_COLUMN_NOT_EXISTS_ERROR
from src.utils.pagination import Page
from src.utils.resp import resp_success_json, resp_error_json
from src.apps.dynamic_api.validate import DynamicApiValidate
from src.utils.resp_execl import resp_execl

JINJA2_ENV = Environment()  # 获取执行环境

JINJA2_ENV.globals["datetime"] = datetime
# 自定义函数
JINJA2_ENV.globals["ja_concat_in"] = ja_concat_in
JINJA2_ENV.globals["ja_many_to_many_like"] = ja_many_to_many_like


def get_current_version_iter(iter_dir, *args, **kwargs):
    """
    TODO：获取最新版本的配置文件路径
    :param iter_dir:
    :param args:
    :param kwargs:
    :return:
    """
    new_iter = None
    for row in iter_dir:
        if not isinstance(row, (Path,)):
            continue

        if os.path.splitext(row.name)[0] <= CURRENT_VERSION:
            if not new_iter:
                new_iter = row
            else:
                if row.name > new_iter.name:
                    new_iter = row

    return new_iter


def dynamic_api_model_view(api_json, *args, **kwargs):
    """
    注入模型对象数据
    :param api_json:
    :param args:
    :param kwargs:
    :return:
    """
    dy = DynamicApiValidate(**api_json)

    def return_data():
        return dy

    return params.Depends(dependency=return_data, use_cache=True)


my_page = Page()


async def __select_dynamic_api_view(mdl: BaseModel = None,
                                    synamic_api_model: DynamicApiValidate = None,
                                    db_session: AsyncSession = None,
                                    *args, **kwargs):
    """
    获取数据库数据
    :param mdl:
    :param synamic_api_model:
    :param db_session:
    :param args:
    :param kwargs:
    :return:
    """
    if not mdl:
        mdl_dict = {}
    else:
        mdl_dict = mdl.dict()

    template = JINJA2_ENV.from_string(synamic_api_model.jinja_content)
    r_sql = template.render(mdl_dict)
    print(r_sql)

    result_data = {
        "target_desc": synamic_api_model.target_desc.dict()
    }
    if all(k in mdl_dict for k in ["order_by", "order_filed"]):
        # 检查排序
        sort_all_key = [k.get("target_key") for k in synamic_api_model.target_desc.dict().get("en", [])]
        if mdl_dict.get("order_filed", "") not in sort_all_key:
            return resp_error_json(SORT_COLUMN_NOT_EXISTS_ERROR, msg_append=mdl_dict.get("order_filed", ""))

    rowcount, results = await my_page.exec_sql(db_session=db_session, sql=r_sql, **mdl_dict)
    if rowcount:
        result_data.update({"page": {
            "size": mdl_dict.get("size"),
            "page": mdl_dict.get("page"),
            "next_page": True if mdl_dict.get("page") < int(rowcount / mdl_dict.get("size")) + 1 else False,
            "sum_page": int(rowcount / mdl_dict.get("size")) + 1,
            "sum_size": rowcount
        }})
    data = [dict(row) for row in results.mappings()]
    result_data.update({"rows": data})

    # 判断返回 execl
    if "fields" in mdl_dict:
        header = [k.get("name") for k in mdl_dict.get("fields", [{}])]
        name = [k.get("key") for k in mdl_dict.get("fields", [{}])]
        data = [[item.get(ik) for ik in name] for item in data]
        return resp_execl(header=header,
                          data=data,
                          filename="{}_{}".format(synamic_api_model.api_name, int(time.time())))
    return resp_success_json(data=result_data)


@cache(key_builder=my_default_key_builder, expire=CACHE_TIME)  # 缓存
async def cache_select_dynamic_api_view(mdl, synamic_api_model, db_session, *args, **kwargs):
    """
    需要缓存
    :param mdl:
    :param synamic_api_model:
    :param db_session:
    :param args:
    :param kwargs:
    :return:
    """
    return await __select_dynamic_api_view(mdl, synamic_api_model, db_session, *args, **kwargs)


async def select_dynamic_api_view(mdl: BaseModel = None,
                                  synamic_api_model: DynamicApiValidate = None,
                                  db_session: AsyncSession = None,
                                  *args, **kwargs):
    """
    获取数据库数据
    :param mdl:
    :param synamic_api_model:
    :param db_session:
    :param args:
    :param kwargs:
    :return:
    """
    # 判断需不需要走缓存
    if "export" in synamic_api_model.inner_validate:
        return await __select_dynamic_api_view(mdl, synamic_api_model, db_session, *args, **kwargs)
    return await cache_select_dynamic_api_view(mdl, synamic_api_model, db_session, *args, **kwargs)


async def all_dynamic_api_view(db_session: AsyncSession, *args, **kwargs):
    """
    获取所有动态API列表
    :param db_session:
    :param args:
    :param kwargs:
    :return:
    """
    sql = text("SELECT id,subject_name,api_name,api_version,api_status,create_time,update_time FROM dynamic_api_data")
    # sql = select(DynamicAPIDataModel)
    r: Result = await db_session.execute(sql)
    return resp_success_json(list(r.mappings()))


async def get_dynamic_api_data_view(db_session: AsyncSession, subject_name: str, api_name: str, version: str = None,
                                    *args, **kwargs):
    """
    获取某个API的数据
    :param db_session:
    :param subject_name:
    :param api_name:
    :param version:
    :param args:
    :param kwargs:
    :return:
    """
    sql = (select(DynamicAPIDataModel).filter(DynamicAPIDataModel.subject_name == subject_name).
           filter(DynamicAPIDataModel.api_name == api_name).
           order_by(DynamicAPIDataModel.update_time.desc()))

    if version:
        sql = sql.filter(DynamicAPIDataModel.api_version == version)
    else:
        sql = sql.filter(DynamicAPIDataModel.api_status == "1")

    r: Result = await db_session.execute(sql)
    rows = r.scalars().one()

    if rows and isinstance(rows, DynamicAPIDataModel):
        return resp_success_json(rows.to_dict())
    else:
        return resp_error_json(error=error_code.ERROR_NOT_FOUND)


async def reload_dynamic_api_data_func():
    """
    重新加载
    """
    with open(f"{BASE_DIR}/reload/r.py", "wb") as f:
        f.write("{}".format(time.time()).encode())


async def add_dynamic_api_data_view(d: DynamicApiValidate, db_session: AsyncSession):
    """
    新增动态接口
    :param d:
    :param db_session:
    :return:
    """
    try:
        # 获取动态的数据,映射到对应的model
        async with db_session.begin():
            dam = DynamicAPIDataModel(**d.model_dump_dict())
            db_session.add(dam)
            await db_session.flush()  # 提交
            await db_session.refresh(dam)  # 刷新对象
            await reload_dynamic_api_data_func()  # 重启
            return resp_success_json(dam.to_dict())
    except Exception as e:
        return resp_error_json(error=error_code.ERROR_NOT_FOUND, msg_append=str(e))


async def update_dynamic_api_data_view(d: DynamicApiValidate, db_session: AsyncSession):
    """
    更新接口数据
    :param d:
    :param db_session:
    :return:
    """
    try:
        # 获取动态的数据,映射到对应的model
        async with db_session.begin():
            # 先把以前的接口状态修改
            sql = (update(DynamicAPIDataModel).
                   where(DynamicAPIDataModel.subject_name == d.subject_name).
                   where(DynamicAPIDataModel.api_name == d.api_name).
                   where(DynamicAPIDataModel.api_version == d.api_version).
                   values(**d.model_dump_dict()))
            await db_session.execute(sql)

            # dam = DynamicAPIDataModel(**d.model_dump_dict())
            # db_session.add(dam)
            # await db_session.flush()  # 提交
            # await db_session.refresh(dam)  # 刷新对象
            await reload_dynamic_api_data_func()  # 重启
            return resp_success_json({})
    except Exception as e:
        return resp_error_json(error=error_code.ERROR_NOT_FOUND, msg_append=str(e))


async def update_dynamic_api_status_view(subject_name: str, api_name: str, api_version: str,
                                         api_status: bool, db_session: AsyncSession):
    """
    更新接口状态
    :param db_session:
    :param subject_name:
    :param api_version: 状态(True & False)
    :param api_name:
    :param api_status:
    :param db_session:
    :return:
    """
    try:
        # 如果是改接口状态为True，那么先把所有接口都改为False，也就是说只有一个在线使用接口
        async with db_session.begin():
            if api_status:
                up_all_sql = (update(DynamicAPIDataModel).
                              where(DynamicAPIDataModel.subject_name == subject_name).
                              where(DynamicAPIDataModel.api_name == api_name).
                              values(api_status=False))
                await db_session.execute(up_all_sql)

            sql = (update(DynamicAPIDataModel).
                   where(DynamicAPIDataModel.subject_name == subject_name).
                   where(DynamicAPIDataModel.api_name == api_name).
                   where(DynamicAPIDataModel.api_version == api_version).
                   values(api_status=api_status))
            await db_session.execute(sql)

            await reload_dynamic_api_data_func()  # 重启
            return resp_success_json({})
    except Exception as e:
        return resp_error_json(error=error_code.ERROR_NOT_FOUND, msg_append=str(e))
