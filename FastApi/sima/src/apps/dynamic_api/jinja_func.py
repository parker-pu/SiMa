# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

jinja 处理函数
"""
import ast
import os


def ja_concat_in(st: str) -> str:
    """
    这个函数的作用是把一个字符串变成是 sql in 方式的的函数
    :param st: 字符串
    :return:
    """
    return "({})".format(",".join(["'{}'".format(r) for r in st.split(",")]))


def ja_many_to_many_like(name, like_st: str) -> str:
    """
    这个函数的作用是对一个字段进行多对多like
    :param name: 字符串
    :param like_st: 字符串
    :return:
    """
    return " OR ".join(["{} like '%{}%'".format(name, r) for r in like_st.split(",")])


# def env_include_self_recover() -> bool:
#     """
#     判断是否包含自恢复,从保存的环境变量文件读取
#     :return:
#     """
#     load_env()  # 加载env
#     return bool(ast.literal_eval(os.getenv("include_self_recover", "True")))
