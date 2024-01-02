# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import update, select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.databases.models import DataBasesModel
from src.apps.databases.validate import DataBaseValidate
from src.utils.db.aiodb import get_db_session
from src.utils.resp import resp_success_json
from src.utils.utils import delete_dict_none

router = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)


@router.get("/databases/")
async def get_databases(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    """
    获取所有数据库
    :param db_session:
    :return:
    """
    sql = (select(DataBasesModel))
    async with db_session.begin():
        r: Result = await db_session.execute(sql)
        rd = [k.to_dict() for k in r.scalars().all()]
    return resp_success_json(rd)


@router.post("/databases/")
async def add_databases(db: DataBaseValidate, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    """
    新增数据库
    :param db:
    :param db_session:
    :return:
    """
    print(db)
    async with db_session.begin():
        d = DataBasesModel(**db.model_dump())
        db_session.add(d)
        await db_session.flush()  # 提交
        await db_session.refresh(d)  # 刷新对象
        return resp_success_json(d.to_dict())


@router.put("/databases/{db_id}/")
async def put_users(db_id: str, db: DataBaseValidate, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    """
    修改数据库
    :param db_id:
    :param db:
    :param db_session:
    :return:
    """
    async with db_session.begin():
        sql = update(DataBasesModel).where(DataBasesModel.id == db_id).values(**delete_dict_none(db.model_dump()))
        r: Result = await db_session.execute(sql)
        return resp_success_json({})


@router.delete("/databases/{db_id}/")
async def del_users(db_id: str, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    """
    删除数据库
    :param db_id:
    :param db_session:
    :return:
    """
    async with db_session.begin():
        sql = delete(DataBasesModel).where(DataBasesModel.id == db_id)
        r: Result = await db_session.execute(sql)
        return resp_success_json({})
