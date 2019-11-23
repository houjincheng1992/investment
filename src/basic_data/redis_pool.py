# -*- coding: UTF-8 -*-

import redis
from config import redis_config

pool_redis = redis.ConnectionPool(
                host = redis_config["host"],
                port = redis_config["port"],
                db = redis_config["db"],
                max_connections=redis_config["max_connections"],
                decode_responses=True)

def get_redis_conn(pool_redis):
    """
        获取redis连接
    """
    conn = redis.Redis(connection_pool=pool_redis)
    return conn