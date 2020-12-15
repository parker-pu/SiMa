# -*- coding: utf-8 -*-
import json

from src.apps.dictionary.models import ScanConnDBSettingModel, NewTableModel
from src.utils.rdbms_model import DBStatus
from src.utils.utils import gen_md5


async def scan_mysql(item: ScanConnDBSettingModel):
    public_data = {
        "db_conf": item,
        "db_host": item.db_host,
        "db_port": item.db_port,
        "db_type": item.db_type,
        "db_name": item.db_name,
    }
    n = NewTableModel(**public_data)
    for one_table in n.show_tables():
        public_data["table_name"] = one_table
        nt = NewTableModel(**public_data)
        table_data = nt.show_create_table()
        nt.data = table_data
        nt.status = DBStatus.use
        nt.table_md5 = gen_md5(table_data)
        nt.save()


async def sync_data_view():
    """ sync database data
    :return:
    """
    for item in ScanConnDBSettingModel().all_list():
        scan_db = ScanConnDBSettingModel(**item)
        if scan_db.db_type.mysql == "mysql":
            await scan_mysql(scan_db)
    return "ok"
