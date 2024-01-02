# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

一些公共的验证
"""
from enum import Enum
from typing import Any

from pydantic import BaseModel

from src.utils.passwd import encrypted_text


class DBEnum(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"


class DataBaseValidate(BaseModel):
    db_host: str
    db_port: int
    db_type: DBEnum = "mysql"
    db_name: str
    username: str
    password: str
    use_status: bool = True

    def __str__(self):
        return self.db_host

    def model_dump(self, **kwargs) -> dict[str, Any]:
        m = super().model_dump()
        if self.password and self.password != "":
            m.update({"password": encrypted_text(self.password)})
        m.pop("update_time") if "update_time" in m else None
        return m
