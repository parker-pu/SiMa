# -*- coding: utf-8 -*-
import os
from typing import Optional

from pydantic import BaseModel, IPvAnyAddress, EmailStr, Field

from src.settings import CONN_PATH
from src.utils.es_model import EsModel
from src.utils.passwd import gen_password_hash


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenDataModel(BaseModel):
    username: Optional[str] = None


class UserModel(EsModel):
    _index_name = "users"
    _pk_no_arr = ["username"]
    username: Optional[str] = "admin"
    email: Optional[EmailStr] = 'admin@admin.com'
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    is_superuser: Optional[bool] = True


class UserInDBMode(UserModel):
    hashed_password: Optional[str] = Field("admin", alias="password")

    def save(self) -> True:
        self.hashed_password = gen_password_hash(self.hashed_password)
        super().save()


class InitEsConnModel(EsModel):
    _index_name = ""
    _time_out = 3
    _pk_no_arr = ["setting_es_host", "setting_es_port"]
    _file_path: Optional[str] = CONN_PATH
    setting_es_host: Optional[IPvAnyAddress] = '127.0.0.1'
    setting_es_port: Optional[int] = 9200

    def save(self) -> True:
        try:
            with open(self._file_path, "w") as f:
                f.write(self.json())
        except Exception as e:
            self._Logger.error(e)
            return False

    def delete(self) -> True:
        try:
            os.remove(self._file_path)
        except Exception as e:
            self._Logger.error(e)
            return False
