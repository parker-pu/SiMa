# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

一些公共的验证
"""
import json
from enum import Enum
from typing import Union, Dict, List, Tuple, Optional, Any

from pydantic import BaseModel, Field

from src.utils.passwd import gen_password_hash


class TokenDataValidate(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class ChangeUserValidate(BaseModel):
    # username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    superuser: Optional[bool] = True

    def __str__(self):
        return self.username

    def model_dump(self, **kwargs) -> dict[str, Any]:
        m = super().model_dump()
        if self.password and self.password != "":
            m.update({"password": gen_password_hash(self.password)})
        return m


class UserValidate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    # email: Optional[EmailStr] = 'admin@admin.com'
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    superuser: Optional[bool] = True

    def __str__(self):
        return self.username


class UserInfoValidate(UserValidate):
    password: Optional[str] = None

    def model_dump(self, **kwargs) -> dict[str, Any]:
        m = super().model_dump()
        if self.password and self.password != "":
            m.update({"password": gen_password_hash(self.password)})
        m.pop("update_time") if "update_time" in m else None
        return m

    def __str__(self):
        return self.username
