# -*- coding: utf-8 -*-
import json
import os
from src.utils.log import logger
from datetime import datetime
from pydantic import BaseModel
from elasticsearch import Elasticsearch

from src.settings import CONN_PATH
from src.utils.utils import gen_md5


class EsModel(BaseModel):
    _index_name: str = None
    _pk_no_arr = []
    _data_ignore = []

    create_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time: str = None

    _time_out: int = 15
    _Logger: logger = logger

    @property
    def gen_pk_md5(self):
        data = json.loads(self.json())
        return gen_md5("##".join([str(data.get(line)) for line in self._pk_no_arr]))

    def conn(self) -> True:
        if os.path.exists(CONN_PATH):
            json_data = json.load(open(CONN_PATH, 'r'))
        else:
            json_data = json.loads(self.json())

        return Elasticsearch(
            [{
                'host': json_data.get("setting_es_host", "127.0.0.1"),
                'port': json_data.get("setting_es_port", 9200)
            }],
            timeout=self._time_out
        )

    def crawl(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def load(self) -> True:
        try:
            his: dict = self.conn().get(index=self._index_name, id=self.gen_pk_md5, ignore=[404, ])
            if not his.get("found"):
                return False
            self.crawl(**his.get("_source", {}))
        except Exception as e:
            self._Logger.error(e)
            return False

    def save(self) -> True:
        self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data: dict = json.loads(self.json())
        for item_key in list(data.keys()):
            if item_key.startswith("_"):
                data.pop(item_key)
            if item_key in self._data_ignore:
                data.pop(item_key)
        try:
            if self.conn().exists(index=self._index_name, id=self.gen_pk_md5):
                data.pop("create_time")
                self.conn().update(index=self._index_name, id=self.gen_pk_md5, body={"doc": data})
            else:
                self.conn().create(index=self._index_name, id=self.gen_pk_md5, body=data, ignore=409)
        except Exception as e:
            self._Logger.error(e)
            return False

    def check(self):
        pass

    def delete(self) -> True:
        try:
            self.conn().delete(index=self._index_name, id=self.gen_pk_md5)
        except Exception as e:
            self._Logger.error(e)
            return False

    def create_index(self) -> True:
        try:
            self.conn().indices.create(index=self._index_name, ignore=400)
        except Exception as e:
            self._Logger.error(e)
            return False

    def delete_index(self) -> True:
        try:
            self.conn().indices.delete(index=self._index_name, ignore=[400, 404])
        except Exception as e:
            self._Logger.error(e)
            return False

    def all_list(self):
        try:
            back_data = self.conn().search(index=self._index_name, ignore=[400, 404])
            if 'error' in back_data:
                return False
            for his in back_data.get("hits", {}).get("hits", []):
                yield his.get("_source", {})
        except Exception as e:
            self._Logger.error(e)
            return False
