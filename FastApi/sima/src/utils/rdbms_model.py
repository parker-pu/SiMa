# -*- coding: utf-8 -*-
from enum import Enum
from typing import Optional

from pydantic import BaseModel, IPvAnyAddress
from sqlalchemy.orm import sessionmaker

from src.utils.es_model import EsModel
import re
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class DBEnum(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"


class DBStatus(str, Enum):
    use = 1
    fail = 0


class DBBase(BaseModel):
    db_host: Optional[IPvAnyAddress] = '127.0.0.1'
    db_port: Optional[int] = 3306
    db_type: Optional[DBEnum] = 'mysql'
    db_name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    status: Optional[DBStatus]


class RDBMModel(EsModel):
    """ 这个类是用来操作数据库的基类
    """
    table_name: str
    db_conf: DBBase

    @contextmanager
    def session_scope(self):
        """提供围绕一系列操作的事务范围"""
        base = "mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
        if self.db_conf.db_type == "mysql":
            base = "mysql+pymysql://{username}:{password}@{host}/{dbname}"
        engine = create_engine(
            base.format(
                username=self.db_conf.username,
                password=self.db_conf.password,
                host=self.db_conf.db_host,
                port=self.db_conf.db_port,
                dbname=self.db_conf.db_name,
            ),
            convert_unicode=True,
            pool_size=100,
            pool_recycle=3600,
            echo=False
        )
        session = sessionmaker(bind=engine)()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self._Logger.error('{}:{}'.format(type(e), e))
        finally:
            session.close()

    # EXEC SQL
    def execute(self, sql, **kwargs):
        """ exec sql
        :param sql:
        :param kwargs:
        :return:
        """
        raw_sql = text(sql)
        with self.session_scope() as session:
            temp = session.execute(raw_sql, kwargs)
            temp = temp.fetchall()
            return temp

    def show_tables(self):
        show_table_sql = "show tables"
        for batch_table in self.execute(sql=show_table_sql):
            for one_table in batch_table:
                yield one_table

    def show_create_table(self):
        desc_table_sql = "show create table {}".format(self.table_name)
        return self.execute(sql=desc_table_sql)[0][1]
