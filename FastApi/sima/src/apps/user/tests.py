# -*- coding: utf-8 -*-
import time
import uuid

from src.apps.user.models import UserInDB

data = {
    "username": "admin",
    # "pk_no": "{}".format(uuid.uuid5(uuid.NAMESPACE_URL, 'xs')),
    "email": "123@admin.com",
    # "full_name": "string",
    # "disabled": False,
    # "is_superuser": True,
    "password": "admin"
}
s = UserInDB(
    **data
)

print(s.gen_pk_md5)
# print(s.json())
# print(s.load)
print(s.save())
print("-----------x")
print(s.load())
print(s.json())
# time.sleep(30)
# print(s.delete())
# print(s.delete_index())
