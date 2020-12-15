# -*- coding: utf-8 -*-

from fastapi import APIRouter
from src.apps.dictionary.models import ScanConnDBSettingModel
from src.apps.dictionary.views import sync_data_view
from src.settings import SUCCESS_DATA

router = APIRouter(
    prefix="/dictionary",
    tags=["dictionary"],
    responses={404: {"description": "Not found"}},
)


@router.get("/sync-table")
async def sync_data():
    await sync_data_view()
    return SUCCESS_DATA


@router.get("/search")
async def sync_data():
    return await sync_data_view()


@router.put("/db-conn")
async def put_conn(conn: ScanConnDBSettingModel):
    conn.save()
    return SUCCESS_DATA


@router.get("/db-conn")
async def get_conn():
    return list(ScanConnDBSettingModel().all_list())


@router.delete("/db-conn")
async def del_conn(conn: ScanConnDBSettingModel):
    conn.delete()
    return SUCCESS_DATA
