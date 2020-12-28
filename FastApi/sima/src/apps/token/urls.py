# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.token.models import TokenModel
from src.apps.token.views import gen_access_token

router = APIRouter(
    prefix="",
    tags=["token"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await gen_access_token(form_data=form_data)
