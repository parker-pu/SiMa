# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime, date
from decimal import Decimal


def gen_md5(src_byte):
    """ gen md5
    :param src_byte:
    :return:
    """
    m2 = hashlib.md5()
    m2.update(src_byte.encode("utf-8"))
    return m2.hexdigest()


def f_data(field):
    """
    格式化数据
    """
    if not field:
        return field

    if isinstance(field, (bytes,)):
        return str(field, encoding="utf-8")
    elif isinstance(field, datetime):
        return field.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(field, date):
        return field.strftime("%Y-%m-%d")
    elif isinstance(field, Decimal):
        return float(field)
    elif isinstance(field, str):
        if (field.startswith("[") and field.endswith("]")) \
                or (field.startswith("{") and field.endswith("}")):
            return json.loads(field)
        return field
    else:
        return field
