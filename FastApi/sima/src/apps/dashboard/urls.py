# -*- coding: utf-8 -*-
from fastapi import APIRouter

from src.apps.dashboard.views import static_data

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/static")
async def is_init():
    """ Static DataBase nums. Scan table nums """
    # return static_data()
    return await static_data()
