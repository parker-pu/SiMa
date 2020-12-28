# -*- coding: utf-8 -*-
from src.apps.first.models import InitEsConnModel
from src.apps.user.models import UserInDBMode
from src.utils.log import logger


async def init_superuser(init_data: InitEsConnModel, user: UserInDBMode):
    revoke_data: dict = {
        "es_conn": False,
        "add_user": False
    }
    try:
        if init_data.conn().ping() and not init_data.save():
            revoke_data["es_conn"] = True

        if not user.create_index() and not user.save():
            revoke_data["add_user"] = True

        if len(revoke_data.values()) != sum(revoke_data.values()):
            init_data.delete()
    except Exception as e:
        logger.info(e)
    return revoke_data
