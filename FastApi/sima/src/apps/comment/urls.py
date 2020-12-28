# -*- coding: utf-8 -*-
import json
import uuid

from fastapi import APIRouter, Depends

from src.apps.comment.models import (
    CommentInfoModel,
    CommentModel
)
from src.apps.dictionary.models import (
    TableBaseModel
)
from src.apps.user.models import UserModel
from src.apps.user.views import get_current_active_user
from src.settings import SUCCESS_DATA
from src.utils.utils import gen_md5

router = APIRouter(
    prefix="",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)


# comment
@router.put("/comment")
async def put_comment(content: str, table: TableBaseModel, current_user: UserModel = Depends(get_current_active_user)):
    ct = CommentModel(
        comment_main=CommentInfoModel(
            author=current_user.username,
            content=content
        ),
        batch_md5=gen_md5(str(uuid.uuid1())),
        db_host=table.db_host,
        db_port=table.db_port,
        db_type=table.db_type,
        db_name=table.db_name,
        table_name=table.table_name,
    )
    ct.save()
    return SUCCESS_DATA


@router.post("/comment")
async def get_comment(table: TableBaseModel):
    c = CommentModel(**json.loads(table.json()))
    return c.table_list()


@router.delete("/comment")
async def del_comment(comm: CommentModel):
    comm.delete()
    return SUCCESS_DATA
