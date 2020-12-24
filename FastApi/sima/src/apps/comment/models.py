# -*- coding: utf-8 -*-
from typing import Optional, Sequence, Any
from pydantic import BaseModel

from src.utils.es_model import EsModel
from src.utils.rdbms_model import (
    TableBaseModel
)


class CommentInfoModel(BaseModel):
    actions: Sequence[Any] = ['Reply to']
    author: Optional[str] = 'Admin'
    avatar: Optional[str] = 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png'
    content: Optional[str] = ''


class CommentModel(TableBaseModel, EsModel):
    _index_name = "comment"
    _pk_no_arr = ["db_host", "db_port", "db_type", "db_name", "table_name", "batch_md5"]
    batch_md5: str = None

    comment_main: Optional[CommentInfoModel] = None
    # comment_child: Sequence[Any] = []
