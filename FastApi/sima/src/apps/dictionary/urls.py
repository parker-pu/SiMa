# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends

from src.apps.dictionary.models import ScanConnDBSetting
from src.apps.dictionary.views import (
    sync_data_view,
    del_conn_view,
    patch_conn_view, get_conn_view
)
from src.apps.user.models import User
from src.apps.user.views import get_current_active_user
from src.settings import SUCCESS_DATA

router = APIRouter(
    prefix="/dictionary",
    tags=["dictionary"],
    responses={404: {"description": "Not found"}},
)


@router.get("/sync-table")
async def sync_data():
    return await sync_data_view()


@router.put("/db-conn")
async def put_conn(conn: ScanConnDBSetting):
    conn.save()
    return SUCCESS_DATA


@router.get("/db-conn")
async def get_conn():
    return list(ScanConnDBSetting().all_list())


@router.delete("/db-conn")
async def del_conn(conn: ScanConnDBSetting):
    return await del_conn_view()
