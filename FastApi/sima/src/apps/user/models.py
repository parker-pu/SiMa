# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, BOOLEAN

from src.utils.db.aiodb import Base
from src.utils.db.model import ModelDefault
from src.utils.es_model import EsModel
from src.utils.passwd import gen_password_hash


# class UserModel(EsModel):
#     _index_name = "users"
#     _pk_no_arr = ["username"]
#     username: Optional[str] = "admin"
#     email: Optional[str] = 'admin@admin.com'
#     # email: Optional[EmailStr] = 'admin@admin.com'
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = False
#     is_superuser: Optional[bool] = True
#
#
# class UserInDBMode(UserModel):
#     hashed_password: Optional[str] = Field("admin", alias="password")
#
#     def save(self) -> True:
#         self.hashed_password = gen_password_hash(self.hashed_password)
#         super().save()

class UserModel(ModelDefault, Base):
    """
    API 接口数据
    """
    __tablename__ = "users"

    username = Column(String(255), index=True, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(255), comment="邮件名称")
    full_name = Column(String(255), comment="用户全名")
    disabled = Column(BOOLEAN, default=False, comment="是否失效")
    superuser = Column(BOOLEAN, default=True, comment="是否是超级用户")

    def __str__(self):
        return self.username

    def to_dict(self, **kwargs):
        d = super().to_dict()
        d.pop("password")
        return d
