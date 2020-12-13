# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import IPvAnyAddress

from src.utils.es_model import EsModel


class ScanConnDBSetting(EsModel):
    _index_name = "scan_conn_db_setting"
    _pk_no_arr = ["db_host", "db_port", "db_type", "db_name"]

    db_host: Optional[IPvAnyAddress] = '127.0.0.1'
    db_port: Optional[int] = 3306
    db_type: Optional[str]
    db_name: Optional[str]


class NewTable(EsModel):
    _index_name = "new_table"


class HistoryTableColumn(EsModel):
    _index_name = "history_table_column"
