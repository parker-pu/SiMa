# -*- coding: utf-8 -*-
import hashlib


def gen_md5(src_byte):
    """ gen md5
    :param src_byte:
    :return:
    """
    m2 = hashlib.md5()
    m2.update(src_byte.encode("utf-8"))
    return m2.hexdigest()
