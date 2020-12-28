# -*- coding: utf-8 -*-
from src.apps.dictionary.models import ScanConnDBSettingModel, SearchModel, NewTableModel


async def back_sum_query_data(sum_filet_column: list) -> dict:
    source_column, agg_dict = [], {}
    for item in sum_filet_column:
        # filter column
        source_column.append(item)
        source_column.append("sum_{}".format(item))

        agg_dict["sum_{}".format(item)] = {
            "terms": {
                "field": "{}.keyword".format(item),
                "size": 99999
            },
            "aggs": {
                "sum_{}".format(item): {
                    "sum": {
                        "field": "1"
                    }
                }
            }
        }
    return {
        "_source": source_column,
        "query": {
            "match_all": {}
        },
        "aggs": agg_dict
    }


async def index_static(index_name: str, data: dict, filet_column: list) -> dict:
    back_dict = {
        index_name: {}
    }

    total_nums = data.get("hits", {}).get("total", {}).get("value", 0)
    back_dict[index_name] = {
        "total_nums": total_nums
    }

    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    for item in filet_column:
        # filter column
        back_dict[index_name]["sta_{}".format(item)] = {}
        for _item in data.get("aggregations", {}).get("sum_{}".format(item), {}).get("buckets", []):
            k = None
            k_name = "key_as_string" if "key_as_string" in _item.keys() else "key"
            if str(_item.get(k_name, "")).lower() in ["yes", "true", "t", "1", "no", "false", "f", "0"]:
                k = str2bool(_item.get(k_name))
            rk = k if k is not None else _item.get(k_name)
            back_dict[index_name]["sta_{}".format(item)][rk] = _item.get("doc_count")
    return back_dict


async def static_data():
    result_dict = {}
    # Conn
    sc = ScanConnDBSettingModel()
    sum_filet_column = ["db_host"]
    sta_base = await back_sum_query_data(sum_filet_column=sum_filet_column)
    sc_data = sc.conn().search(index=sc.get_index_name, body=sta_base)
    result_dict.update(await index_static(index_name=sc.get_index_name, data=sc_data, filet_column=sum_filet_column))

    # Table
    nt = NewTableModel()
    sum_filet_column = ["db_host"]
    sta_base = await back_sum_query_data(sum_filet_column=sum_filet_column)
    nt_data = nt.conn().search(index=nt.get_index_name, body=sta_base)
    result_dict.update(await index_static(index_name=nt.get_index_name, data=nt_data, filet_column=sum_filet_column))

    return result_dict
