# -*- coding: utf-8 -*-
import uuid

from src.apps.dictionary.models import (
    ScanConnDBSettingModel,
    NewTableModel,
    SearchModel,
    HistoryTableColumnModel
)
from src.utils.rdbms_model import DBStatus, RDBMModel
from src.utils.utils import gen_md5
from src.utils.log import logger


def compared_column(new_data: list, old_data: list, compared_key: list):
    """ compared column. Based on the new field
    :param new_data:
    :param old_data:
    :param compared_key:
    :return:
    """

    def list_to_dict(list_data):
        back_dict = {}
        for _item in list_data:
            back_dict[_item.get("COLUMN_NAME")] = _item
        return back_dict

    add_data, up_data, del_data = [], [], []

    if not old_data:
        return new_data, up_data, del_data

    new_data_dict, old_data_dict = list_to_dict(new_data), list_to_dict(old_data)
    # new column
    for k in set(new_data_dict.keys()) - set(old_data_dict.keys()):
        add_data.append(new_data_dict.get(k))
    # update column
    for k in set(old_data_dict.keys()) & set(new_data_dict.keys()):
        # compared column
        n_item, o_item = new_data_dict.get(k), old_data_dict.get(k)
        up_status = False
        up_column = []
        for c in compared_key:
            if n_item.get(c) != o_item.get(c):
                up_status = True
                up_column.append(c)
        if up_status:
            n_item['compared_column'] = ",".join(up_column)
            up_data.append(n_item)
    # del column
    for k in set(old_data_dict.keys()) - set(new_data_dict.keys()):
        del_data.append(old_data_dict.get(k)) if old_data_dict.get(k) else None
    return add_data, up_data, del_data


def scan_mysql(item: ScanConnDBSettingModel):
    rdb = RDBMModel(db_conf=item)
    for one_table in rdb.show_tables():
        table_base_public = {
            "db_host": item.db_host,
            "db_port": item.db_port,
            "db_type": item.db_type,
            "db_name": item.db_name,
            "table_name": one_table
        }
        nt = NewTableModel(**table_base_public)
        nt.load()
        old_table_md5 = nt.table_md5
        # check the difference from last time
        table_data = rdb.show_create_table(table_name=one_table)
        new_table_md5 = gen_md5(table_data)

        if old_table_md5 == new_table_md5:
            continue

        nt.data = table_data
        nt.status = DBStatus.USE
        nt.table_md5 = new_table_md5
        nt.save()

        # Generate table fields
        sql = ("SELECT * FROM information_schema.COLUMNS "
               "WHERE table_schema = '{table_schema}'  AND table_name = '{table_name}'").format(
            table_schema=item.db_name,
            table_name=one_table,
        )
        schema_key = []
        schema_data = []
        for result in rdb.execute(sql=sql):
            schema_key = result.keys()
            schema_data.append(dict(zip(schema_key, result)))

        # Use old data for comparison
        table_base_public["batch_md5"] = old_table_md5
        ht = HistoryTableColumnModel(**table_base_public)
        ht.last()
        last_data: list = list(ht.all_column_data)

        # save
        add_data, up_data, del_data = compared_column(schema_data, last_data, schema_key)
        ht.batch_md5 = gen_md5(str(uuid.uuid1()))
        ht.add_column_data = add_data
        ht.up_column_data = up_data
        ht.del_column_data = del_data
        ht.all_column_data = schema_data
        # ht.delete_index()
        ht.save()


def sync_data_view():
    """ sync database data
    :return:
    """
    for item in ScanConnDBSettingModel().all_list().get("data", []):
        scan_db = ScanConnDBSettingModel(**item)
        if scan_db.db_type.mysql == "mysql":
            scan_mysql(scan_db)
    logger.info("scan success")
    return "ok"


async def search_table_list_view(dada: str = None):
    search_data = SearchModel().search(search_data=dada)
    return search_data
