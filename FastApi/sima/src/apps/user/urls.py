# -*- coding: utf-8 -*-
import os

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.user.models import Token, User, InitEsConn, UserInDB
from src.apps.user.views import get_current_active_user, init_superuser, gen_access_token
from src.settings import CONN_PATH

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/is_init")
async def is_init():
    """ Determine whether to initialize """
    return os.path.exists(CONN_PATH)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await gen_access_token(form_data=form_data)


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/init-superuser/")
async def set_superuser(init_data: InitEsConn, user: UserInDB):
    return await init_superuser(init_data, user)
