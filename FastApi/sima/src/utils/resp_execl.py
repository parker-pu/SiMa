# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025
"""
from datetime import date, datetime

from fastapi.responses import StreamingResponse
from io import BytesIO
import xlsxwriter


def resp_execl(header, data, filename):
    """
    返回execl
    :param header:
    :param data:
    :param filename:
    :return:
    """
    output = BytesIO()  # 在内存中创建一个缓存流
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    row_index = 0

    # 设置标题
    for idx, rt in enumerate(header):
        worksheet.write(row_index, idx, rt)

    # 设置数据
    for rtd in data:
        if not isinstance(rtd, (list,)):
            continue
        row_index += 1
        for r_idx, item in enumerate(rtd):

            # 格式化数据
            if isinstance(item, datetime):
                item = item.strftime("%Y-%m-%d %H:%M:%S.%f")
            elif isinstance(item, date):
                item = item.strftime("%Y-%m-%d")

            worksheet.write(row_index, r_idx, item)

    # 结束
    workbook.close()
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="{filename}.xlsx"'.format(filename=filename)
    }
    return StreamingResponse(output, headers=headers)
