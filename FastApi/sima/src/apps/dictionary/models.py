# -*- coding: utf-8 -*-
import json
from typing import Optional, Sequence, Any
from pydantic import IPvAnyAddress, BaseModel
from sqlalchemy import Column, String, BOOLEAN, TEXT, insert

from src.utils.db.aiodb import Base
from src.utils.db.model import ModelDefault
from src.utils.es_model import EsModel
from src.utils.rdbms_model import DBEnum, DBStatus


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

    @property
    def index_name(self):
        return self._index_name


class TableBaseModel(BaseModel):
    db_host: Optional[IPvAnyAddress] = '127.0.0.1'
    db_port: Optional[int] = 3306
    db_type: Optional[DBEnum] = 'mysql'
    db_name: Optional[str]
    table_name: Optional[str]


class NewTableModel(TableBaseModel, EsModel):
    _index_name = "new_table"
    _pk_no_arr = ["db_host", "db_port", "db_type", "db_name", "table_name"]
    _data_ignore = ["db_conf"]

    data: Optional[str] = None
    table_md5: Optional[str] = None
    status: Optional[DBStatus] = DBStatus.USE


class SearchModel(EsModel):
    _index_name = "new_table"

    def search(self, search_data, page: int = 0, size: int = 10) -> True:
        try:
            back_data = self.conn().search(
                index=self._index_name,
                body={"query": {"match_phrase": {'data': search_data}}},
                ignore=[400, 404],
                size=size,
                from_=page * size
            )
            return self.list_package(data=back_data, page=page, size=size)
        except Exception as e:
            self._Logger.error(e)
            return False


class HistoryTableColumnModel(TableBaseModel, EsModel):
    _index_name = "history_table_column"
    _pk_no_arr = ["db_host", "db_port", "db_type", "db_name", "table_name", "batch_md5"]
    batch_md5: str = None

    add_column_data: Sequence[Any] = []
    up_column_data: Sequence[Any] = []
    del_column_data: Sequence[Any] = []

    all_column_data: Sequence[Any] = []

    def last(self) -> True:
        try:
            d = json.loads(self.json())
            select_body = {
                "size": 1,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"db_host": d.get("db_host")}},
                            {"match": {"db_name": d.get("db_name")}},
                            {"match": {"db_type": d.get("db_type")}},
                            {"match": {"table_name": d.get("table_name")}},

                        ]
                    }
                },
                "sort": {"update_time.keyword": {"order": "desc"}}
            }
            back_data = self.conn().search(
                index=self._index_name,
                body=select_body,
                ignore=[400, 404]
            )
            if 'error' in back_data:
                return False
            one_line: dict = {}
            for his in back_data.get("hits", {}).get("hits", []):
                one_line = his.get("_source", {})
            self.crawl(**one_line)
        except Exception as e:
            self._Logger.error(e)
            return False


class ScanDBHistoryModel(ModelDefault, Base):
    """
    扫描数据库历史记录
    """
    __tablename__ = "scan_db_history"

    db_id = Column(String(255), index=True, comment="数据库ID")
    db_name = Column(String(255), index=True, comment="数据库名称")
    add_table = Column(TEXT, comment="新增表")
    up_table = Column(TEXT, comment="更新表")
    del_table = Column(TEXT, comment="删除表")
    other = Column(TEXT, comment="其他")


class ScanTBModel(ModelDefault, Base):
    """
    扫描数据表历史记录
    """
    __tablename__ = "scan_table"

    db_id = Column(String(255), index=True, comment="数据库ID")
    db_name = Column(String(255), index=True, comment="数据库名称")
    table_name = Column(String(255), index=True, comment="表名称")
    table_desc = Column(TEXT, comment="表描述")
    table_md5 = Column(String(255), comment="表md5")
    table_status = Column(BOOLEAN, default=True, nullable=True, comment="表状态")
    other = Column(String(255), comment="其他")

    def insert_or_update_sql(self, db_type="mysql"):
        stmt, new_insert = None, None
        if db_type == "mysql":
            from sqlalchemy.dialects.mysql import insert
            new_insert = insert

        stmt = new_insert(ScanTBModel).values(
            db_id=self.db_id,
            db_name=self.db_name,
            table_name=self.table_name,
            table_desc=self.table_desc,
            table_md5=self.table_md5,
            table_status=self.table_status,
            other=self.other
        )
        if db_type == "mysql":
            stmt = stmt.on_duplicate_key_update(table_md5=self.table_md5)

        return stmt


class ScanTBHistoryModel(ModelDefault, Base):
    """
    扫描数据表历史记录
    """
    __tablename__ = "scan_table_history"

    db_id = Column(String(255), index=True, comment="数据库ID")
    db_name = Column(String(255), index=True, comment="数据库名称")
    table_name = Column(String(255), index=True, comment="表名称")
    last_data = Column(TEXT, comment="上次扫描的数据")
    add_column = Column(TEXT, comment="新增字段")
    up_column = Column(TEXT, comment="更新字段")
    del_column = Column(TEXT, comment="删除字段")
    other = Column(TEXT, comment="其他")
