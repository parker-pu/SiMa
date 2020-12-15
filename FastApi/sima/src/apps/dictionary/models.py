# -*- coding: utf-8 -*-
from enum import Enum
from typing import Optional

from pydantic import IPvAnyAddress

from src.utils.es_model import EsModel
from src.utils.rdbms_model import RDBMModel, DBEnum, DBStatus, DBBase


class ScanConnDBSettingModel(EsModel):
    _index_name = "scan_conn_db_setting"
    _pk_no_arr = ["db_host", "db_port", "db_type", "db_name"]

    db_host: Optional[IPvAnyAddress] = '127.0.0.1'
    db_port: Optional[int] = 3306
    db_type: Optional[DBEnum] = 'mysql'
    db_name: Optional[str]
    username: Optional[str]
    password: Optional[str]

    status: Optional[DBStatus]


class NewTableModel(RDBMModel):
    _index_name = "new_table"
    _pk_no_arr = ["db_host"]
    _data_ignore = ["db_conf"]

    db_host: Optional[IPvAnyAddress] = '127.0.0.1'
    db_port: Optional[int] = 3306
    db_type: Optional[DBEnum] = 'mysql'
    db_name: Optional[str]

    table_name: Optional[str]
    data: Optional[str]
    table_md5: Optional[str]
    status: Optional[DBStatus]


class HistoryTableColumnModel(RDBMModel):
    _index_name = "history_table_column"
