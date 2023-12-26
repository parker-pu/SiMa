# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import update, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.models import UserModel
from src.apps.user.validate import UserValidate, ChangeUserValidate
from src.apps.user.views import get_current_active_user
from src.utils.db.aiodb import get_db_session
from src.utils.resp import resp_success_json
from src.utils.utils import delete_dict_none

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=UserValidate)
async def read_users_me(current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    return current_user


@router.put("/me")
async def put_users_me(
        user: ChangeUserValidate,
        current_user: Annotated[UserModel, Depends(get_current_active_user)],
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    sql = (update(UserModel).where(UserModel.username == str(current_user.username))
           .values(**delete_dict_none(user.model_dump())))
    async with db_session.begin():
        await db_session.execute(sql)
    return resp_success_json({})


@router.get("/user-info")
async def get_users(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    sql = (select(UserModel))
    async with db_session.begin():
        r: Result = await db_session.execute(sql)
        rd = [k.to_dict() for k in r.scalars().all()]
    return resp_success_json(rd)

