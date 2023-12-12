# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from src.utils.es_model import EsModel
from src.utils.passwd import gen_password_hash


class TokenDataModel(BaseModel):
    username: Optional[str] = None


class UserModel(EsModel):
    _index_name = "users"
    _pk_no_arr = ["username"]
    username: Optional[str] = "admin"
    email: Optional[str] = 'admin@admin.com'
    # email: Optional[EmailStr] = 'admin@admin.com'
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    is_superuser: Optional[bool] = True


class UserInDBMode(UserModel):
    hashed_password: Optional[str] = Field("admin", alias="password")

    def save(self) -> True:
        self.hashed_password = gen_password_hash(self.hashed_password)
        super().save()
