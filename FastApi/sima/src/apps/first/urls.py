# # -*- coding: utf-8 -*-
# import os
#
# from fastapi import APIRouter
#
# from src.apps.first.models import InitEsConnModel
# from src.apps.first.views import init_superuser
# # from src.apps.user.models import UserInDBMode
# from src.settings import CONN_PATH, SUCCESS_DATA
#
# router = APIRouter(
#     prefix="/first",
#     tags=["first"],
#     responses={404: {"description": "Not found"}},
# )
#
#
# @router.get("/is_init")
# async def is_init():
#     """ Determine whether to initialize """
#     return os.path.exists(CONN_PATH)
#
#
# @router.post("/init-superuser")
# async def set_superuser(init_data: InitEsConnModel, user: UserInDBMode):
#     if await is_init():
#         return SUCCESS_DATA
#     return await init_superuser(init_data, user)
