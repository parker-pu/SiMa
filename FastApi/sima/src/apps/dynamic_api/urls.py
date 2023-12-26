# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

路由
"""
from typing import List, Dict

from fastapi import APIRouter, Depends, Request
from pydantic import Field, create_model
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.apps.dynamic_api.models import DynamicAPIDataModel
from src.apps.dynamic_api.validate import DynamicApiValidate
from src.apps.dynamic_api.views import (
    all_dynamic_api_view,
    get_dynamic_api_data_view,
    add_dynamic_api_data_view,
    select_dynamic_api_view,
    dynamic_api_model_view,
    update_dynamic_api_data_view,
    update_dynamic_api_status_view
)
from src.utils.db.aiodb import get_db_session, get_sync_db_session
from src.utils.resp import RespJsonBase
from src.validators import (
    ValidateTimeData,
    ValidatePaginator,
    ValidateExpFiled,
    ValidateOrderFiled
)

router = APIRouter(responses={404: {"description": "Not found"}}, )

templates = Jinja2Templates(directory="static/templates/dynamic_api")

# 映射筛选器
cls_index = {
    "time": ValidateTimeData,  # 时间
    "paginator": ValidatePaginator,  # 分页
    "order": ValidateOrderFiled,  # 排序
    "export": ValidateExpFiled,  # 导出
}

# 查询数据库,找到所有表
db = get_sync_db_session()
for row in db.query(DynamicAPIDataModel).filter(DynamicAPIDataModel.api_status == True):
    if not isinstance(row, DynamicAPIDataModel):
        continue

    api_json = row.to_dict()
    validate_cls, DynamicFoobarModel, custom_validate = [], None, {}
    # 自定义参数验证
    for custom_validate_item in api_json.get("custom_validate"):
        if not isinstance(custom_validate_item, (dict,)):
            continue
        cv = {
            "str": str,
            "int": int,
            "list": List,
            "dict": Dict,
        }

        if "v_default" not in custom_validate_item:
            custom_validate[custom_validate_item.get("v_key")] = (
                custom_validate_item.get("v_type", str),
                Field(title=custom_validate_item.get("v_desc")))
        else:
            custom_validate[custom_validate_item.get("v_key")] = (
                custom_validate_item.get("v_type", str),
                Field(default=custom_validate_item.get("v_default"), title=custom_validate_item.get("v_desc")))
    DynamicFoobarModel = create_model('DynamicFoobarModel', **custom_validate) if custom_validate else None

    # 生成基础依赖的类
    validate_cls.append(DynamicFoobarModel) if DynamicFoobarModel else None
    for validate_cls_name in api_json.get("inner_validate"):
        if cls_index.get(validate_cls_name):
            validate_cls.append(cls_index.get(validate_cls_name))

    req_methods = api_json.get("methods", ["POST"])
    if validate_cls:
        Tc = type("{subject_name}_{api_name}".format(**api_json).upper(), tuple(validate_cls), {})


        @router.api_route("/{subject_name}/{api_name}/".format(**api_json),
                          tags=[api_json.get("subject_name")],
                          description=api_json.get("api_desc"),
                          methods=req_methods,
                          name=api_json.get("api_desc"),
                          response_model=RespJsonBase)
        async def dynamic_api(request: Request, m: Tc,
                              synamic_api_model: DynamicApiValidate = dynamic_api_model_view(api_json),
                              db_session: AsyncSession = Depends(get_db_session)):

            """ 动态API接口数据 """
            return await select_dynamic_api_view(mdl=m, db_session=db_session, synamic_api_model=synamic_api_model)
    else:
        @router.api_route("/{subject_name}/{api_name}/".format(**api_json),
                          tags=[api_json.get("subject_name")],
                          description=api_json.get("api_desc"),
                          methods=req_methods,
                          name=api_json.get("api_desc"),
                          response_model=RespJsonBase)
        async def dynamic_api(request: Request, synamic_api_model=dynamic_api_model_view(api_json),
                              db_session: AsyncSession = Depends(get_db_session)):
            """ 动态API接口数据 """
            return await select_dynamic_api_view(db_session=db_session, synamic_api_model=synamic_api_model)


@router.get("/dynamic-api/all.json", tags=["dynamic_api"], description="所有动态API列表",
            name="所有动态API列表", response_model=RespJsonBase)
async def all_dynamic_api(db_session: AsyncSession = Depends(get_db_session)):
    """ Determine whether to initialize """
    return await all_dynamic_api_view(db_session=db_session)


@router.get("/dynamic-api/{subject_name}/{api_name}/", tags=["dynamic_api"],
            description="获取最新一个动态API数据", name="获取最新一个动态API数据", response_model=RespJsonBase)
async def get_current_dynamic_api_data(subject_name: str, api_name: str,
                                       db_session: AsyncSession = Depends(get_db_session)):
    """
    获取动态API数据
    :param subject_name:
    :param api_name:
    :param db_session:
    :return:
    """
    return await get_dynamic_api_data_view(db_session, subject_name, api_name)


@router.get("/dynamic-api/{subject_name}/{api_name}/{api_version}/", tags=["dynamic_api"],
            description="获取动态API数据", name="获取动态API数据", response_model=RespJsonBase)
async def get_dynamic_api_data(subject_name: str, api_name: str, api_version: str,
                               db_session: AsyncSession = Depends(get_db_session)):
    """
    获取动态API数据
    :param subject_name:
    :param api_name:
    :param api_version:
    :param db_session:
    :return:
    """
    return await get_dynamic_api_data_view(db_session, subject_name, api_name, api_version)


@router.post("/dynamic-api/add/", tags=["dynamic_api"], name="增加动态API数据",
             description="增加动态API数据", response_model=RespJsonBase)
async def add_dynamic_api_data(d: DynamicApiValidate, db_session: AsyncSession = Depends(get_db_session)):
    """
    增加动态API数据
    :param d: 数据
    :param db_session: 数据库
    :return:
    """
    return await add_dynamic_api_data_view(d, db_session)


@router.put("/dynamic-api/update/{subject_name}/{api_name}/{api_version}/", tags=["dynamic_api"],
            description="修改动态API数据", name="修改动态API数据", response_model=RespJsonBase)
async def put_dynamic_api_data(d: DynamicApiValidate, db_session: AsyncSession = Depends(get_db_session)):
    """
    修改动态API数据
    :param d: 数据
    :param db_session: 数据
    :return:
    """
    return await update_dynamic_api_data_view(d, db_session)


@router.post("/dynamic-api/update_status/{subject_name}/{api_name}/{api_version}/", tags=["dynamic_api"],
             description="修改api状态&上下线", name="修改api状态&上下线", response_model=RespJsonBase)
async def put_dynamic_api_status_data(subject_name: str, api_name: str, api_version: str, api_status: bool,
                                      db_session: AsyncSession = Depends(get_db_session)):
    """
    修改api状态&上下线
    :param subject_name:
    :param api_name:
    :param api_version: api 版本
    :param api_status: api 状态
    :param db_session: 数据
    :return:
    """
    return await update_dynamic_api_status_view(subject_name, api_name, api_version, api_status, db_session)

# @router.get("/dynamic-api/html/add/", tags=["dynamic_api"], description="html动态API",
#             name="html动态API", response_class=HTMLResponse)
# async def add_html_dynamic_api_data(request: Request, subject_name: str = None, api_name: str = None,
#                                     api_version: str = None):
#     """
#     html动态API数据
#     :param request:
#     :param subject_name:
#     :param api_name:
#     :param api_version:
#     :return:
#     """
#     jsn_data = {"request": request}
#     if api_version:
#         _file_path = f"{BASE_DIR}/dynamic_api_data/{subject_name}/{api_name}/{api_version}.json"
#     else:
#         _file_path = get_current_version_iter(Path(f"{BASE_DIR}/dynamic_api_data/{subject_name}/{api_name}/").iterdir())
#     if Path(_file_path).exists():
#         jk = ["inner_validate", "custom_validate", "target_desc", "methods"]
#         for k, v in json.load(fp=open(_file_path, "r", encoding="utf-8")).items():
#             jsn_data[k] = json.dumps(v, ensure_ascii=False) if k in jk else v
#     jsn_data["methods"] = '["POST"]' if "methods" not in jsn_data else jsn_data.get("methods")
#     return templates.TemplateResponse("add_dynamic_api.html", jsn_data)
