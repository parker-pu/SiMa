# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from src.apps.user.models import UserModel, UserInDBMode
from src.apps.user.views import get_current_active_user
from src.settings import SUCCESS_DATA

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=UserModel)
async def get_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.put("/me")
async def put_users_me(user: UserInDBMode, current_user: UserInDBMode = Depends(get_current_active_user)):
    if not user.hashed_password:
        user.hashed_password = current_user.hashed_password
    user.save()
    return SUCCESS_DATA


@router.get("/user-info")
async def get_users(user: UserModel = Depends(get_current_active_user)):
    search_data = user.all_list()
    user_list = []
    for line in search_data.get("data", []):
        if not isinstance(line, (dict,)):
            continue
        line.pop("hashed_password")
        user_list.append(line)
    search_data["data"] = user_list
    return search_data


@router.delete("/user-info")
async def del_users(user: UserModel):
    user.delete()
    return SUCCESS_DATA
