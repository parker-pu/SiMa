# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.token.models import TokenModel
from src.apps.token.views import gen_access_token
from src.utils.db.aiodb import get_db_session

router = APIRouter(
    prefix="",
    tags=["token"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db_session: AsyncSession = Depends(get_db_session)):
    return await gen_access_token(form_data=form_data, db_session=db_session)
