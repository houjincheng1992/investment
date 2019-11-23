# -*- coding: UTF-8 -*-

'''
    拉取基础的股票列表
    todo:增量更新
'''

import tushare as ts
from config import basic_data_config
from redis_pool import pool_redis
from redis_pool import get_redis_conn
import json
import time
# from sqlalchemy import create_engine


class StockCompanyData(object):
    """
        股票公司基本信息
    """
    def __init__(self, data):
        """
            init
        """
        self.ts_code = data.get("ts_code", "")
        self.symbol = data.get("symbol", "")
        self.name = data.get("name", "")
        self.area = data.get("area", "")
        self.industry = data.get("industry", "")
        self.fullname = data.get("fullname", "")
        self.enname = data.get("enname", "")
        self.market = data.get("market", "")
        self.exchange = data.get("exchange", "")
        self.curr_type = data.get("curr_type", "")
        self.list_status = data.get("list_status", "")
        self.list_date = data.get("list_date", "")
        self.delist_date = data.get("delist_date", "")
        self.is_hs = data.get("is_hs", "")
        return

    @staticmethod
    def get_fields():
        """
            获取fields
        """
        fields = [
            "ts_code",
            "symbol",
            "name",
            "area",
            "industry",
            "fullname",
            "enname",
            "market",
            "exchange",
            "curr_type",
            "list_status",
            "list_date",
            "delist_date",
            "is_hs"
        ]
        return fields


ts.set_token('ed705fdae931aa5ccd28ffbbf0f678ff8bf9c007c0081135971e6d56')
# engine = create_engine('mysql://root:12345Ssdlh@127.0.0.1/investment?charset=utf8')
engine = None

def stock_list_data(pro, engine):
    """
        获取股票列表数据
    """
    data = pro.stock_basic(fields = ",".join(StockCompanyData.get_fields()))
    size = len(data)

    all_list = []
    for index in range(0, size):
        basic_data = ["" if data.iloc[index][field] == None else data.iloc[index][field] for field in StockCompanyData.get_fields()]
        all_list.append(basic_data)
    redis_conn = get_redis_conn(pool_redis)
    for basic_data in all_list:
        update_basic_data = "\t".join(basic_data)
        pre_basic_data = redis_conn.hget("stock_basic", basic_data[0])
        if pre_basic_data == update_basic_data:
            continue
        redis_conn.hset("stock_basic", basic_data[0], update_basic_data)

    basic_data_path = "%s/stock_basic_%s.log" %(basic_data_config["stock_basic_path"], time.strftime('%Y-%m-%d', time.localtime(time.time())))
    with open(basic_data_config["stock_basic_path"], "w+") as f:
        for basic_data in all_list:
            f.write("\t".join(basic_data))
    return

    

def stock_on_charge_date(pro, engine):
    """
        股票交易日期
    """
    data = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
    data.to_sql('trade_cal', engine)

def stock_daily(pro, engine):
    """
        日线行情
    """
    return
    

if __name__ == '__main__':
    process_name = "stock_basic_data"
    pro = ts.pro_api()

    if process_name == "stock_basic_data":
        stock_list_data(pro, engine)
    elif process_name == "on_charge_date":
        stock_on_charge_date(pro, engine)

