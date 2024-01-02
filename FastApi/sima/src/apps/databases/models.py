# -*- coding: utf-8 -*-
import re

from sqlalchemy import Column, String, BOOLEAN, INT, create_engine, Result, text, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from src.utils.db.aiodb import Base
from src.utils.db.model import ModelDefault
from src.utils.passwd import decrypted_text
from src.utils.utils import gen_md5


class DataBasesModel(ModelDefault, Base):
    """
    API 接口数据
    """
    __tablename__ = "databases"

    db_host = Column(String(255), index=True, comment="数据库地址")
    db_port = Column(INT, nullable=False, comment="数据库端口")
    db_type = Column(String(255), nullable=False, default="mysql", comment="数据库类型")
    db_name = Column(String(255), nullable=False, default="mysql", comment="需要扫描的数据库")
    username = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    use_status = Column(BOOLEAN, default=True, nullable=False, comment="使用状态")

    def __str__(self):
        return self.db_host

    def to_dict(self, **kwargs):
        """
        返回字典
        :param kwargs:
        :return:
        """
        d = super().to_dict()
        d.pop("password")
        return d

    def to_conn(self, *args, **kwargs):
        """
        生成数据库连接
        :param kwargs:
        :return:
        """
        _password = decrypted_text(str(self.password))
        uri = ""
        if self.db_type == "mysql":
            uri = f"mysql+pymysql://{self.username}:{_password}@{self.db_host}"

        if uri:
            sync_engine = create_engine(uri)
            sync_db_session = scoped_session(sessionmaker(bind=sync_engine))
            with sync_db_session() as session:
                return session

    @staticmethod
    def reprocess_table_desc(st: str) -> str:
        """
        去除表结构里面的一些引擎及索引信息
        :param st:
        :return:
        """
        r = re.compile(r'(^.+\)) ENGINE.+$', re.DOTALL).findall(st)
        return r[0] if len(r) > 0 else ""

    def show_dbs_table(self, databases) -> dict:
        """
        查询数据库下的表
        :param databases:
        :return:
        """
        db_session = self.to_conn()
        with db_session.begin():
            for database_name in str(databases).replace(" ", "").split(","):
                # 查询出所有表
                db_session.execute(text(f"use {database_name}"))
                sql = text("show tables")
                r: Result = db_session.execute(sql)
                for tb in r.scalars().all():
                    # 查看表结构
                    tb_desc = text(f"show create table {database_name}.{tb}")
                    tr: Result = db_session.execute(tb_desc)
                    table_desc = self.reprocess_table_desc(tr.scalars(1).one())

                    # 查询表对应的字段
                    col_sql = text(f"SELECT * FROM information_schema.COLUMNS "
                                   f"WHERE table_schema = '{database_name}'  AND table_name = '{tb}'")
                    col_data: Result = db_session.execute(col_sql)

                    yield {
                        "db_id": self.id,
                        "db_name": database_name,
                        "table_name": tb,
                        "table_desc": table_desc,
                        "table_md5": gen_md5(table_desc),
                        "table_col": list(col_data.mappings()),
                        "table_col_key": col_data.keys()
                    }

    def ping(self, *args, **kwargs):
        pass
