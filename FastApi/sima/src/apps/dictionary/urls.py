# -*- coding: utf-8 -*-
import json

from fastapi import APIRouter
from src.apps.dictionary.models import (
    ScanConnDBSettingModel,
    TableBaseModel,
    HistoryTableColumnModel,
    NewTableModel
)
from src.apps.dictionary.views import (
    sync_data_view,
    search_table_list_view
)
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
async def search_table_list(data: str):
    return await search_table_list_view(data)


@router.post("/search-table")
async def search_table_list(new_table: NewTableModel):
    new_table.load()
    return new_table


@router.put("/db-conn")
async def put_conn(conn: ScanConnDBSettingModel):
    conn.save()
    return SUCCESS_DATA


@router.get("/db-conn")
async def get_conn():
    return ScanConnDBSettingModel().all_list()


@router.delete("/db-conn")
async def del_conn(conn: ScanConnDBSettingModel):
    conn.delete()
    return SUCCESS_DATA


@router.post("/table-column")
async def table_column_list(table: TableBaseModel):
    h = HistoryTableColumnModel(**json.loads(table.json()))
    return h.table_list()
