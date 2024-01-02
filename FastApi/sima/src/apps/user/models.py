# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, BOOLEAN

from src.utils.db.aiodb import Base
from src.utils.db.model import ModelDefault


class UserModel(ModelDefault, Base):
    """
    用户
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
