# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

分页
"""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.validators import OrderBYEnum


class Page:
    def __init__(self):
        pass

    @staticmethod
    def format_sort_sql(sql, order_filed, order_by: OrderBYEnum, *args, **kwargs):
        """
        格式化排序 SQL
        :param sql:
        :param order_by:
        :param order_filed:
        :return:
        """
        ob_sql = "SELECT * FROM ({}) _tmp_ss ORDER BY {} {}".format(sql, order_filed, order_by.value)
        return text(ob_sql)

    @staticmethod
    def format_row_count_sql(sql, *args, **kwargs):
        """
        格式化总数
        :param sql:
        :return:
        """
        rcs_sql = "SELECT count(1) as row_count FROM ({}) _tmp_rcs ".format(sql)
        return text(rcs_sql)

    @staticmethod
    def format_paginate_sql(sql, page, size, *args, **kwargs):
        """
        格式化分页
        :param sql:
        :param page:
        :param size:
        :return:
        """
        ps_sql = "SELECT * FROM ({}) _tmp_ps LIMIT {},{}".format(sql, int(page - 1) * size, size)
        return text(ps_sql)

    @staticmethod
    def format_sort_and_paginate_sql(sql, order_filed, order_by, page, size, *args, **kwargs):
        """
        排序且分页
        :param sql:
        :param order_filed:
        :param order_by:
        :param page:
        :param size:
        :return:
        """
        sps_sql = "SELECT * FROM ({}) _tmp_sps ORDER BY {} {} LIMIT {},{}".format(sql, order_filed, order_by.value,
                                                                                  int(page - 1) * size, size)
        return text(sps_sql)

    async def exec_sql(self, db_session: AsyncSession, sql: str, *args, **kwargs):
        """
        格式化执行的 SQL
        :param db_session:
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        async with db_session.begin():
            rowcount = None
            if all(k in kwargs for k in ["order_by", "order_filed", "page", "size"]):
                # 分页和排序
                row_count_rs = await db_session.execute(self.format_row_count_sql(sql))
                for row in row_count_rs.mappings():
                    rowcount = row.get("row_count")
                f_sql = self.format_sort_and_paginate_sql(sql, **kwargs)
                results = await db_session.execute(f_sql)
            elif all(k in kwargs for k in ["order_by", "order_filed"]):
                # 只有排序
                f_sql = self.format_sort_sql(sql, **kwargs)
                results = await db_session.execute(f_sql)
            elif all(k in kwargs for k in ["page", "size"]):
                # 只有分页
                row_count_rs = await db_session.execute(self.format_row_count_sql(sql))
                for row in row_count_rs.mappings():
                    rowcount = row.get("row_count")
                f_sql = self.format_paginate_sql(sql, **kwargs)
                results = await db_session.execute(f_sql)
            else:
                results = await db_session.execute(text(sql))

            return rowcount, results
