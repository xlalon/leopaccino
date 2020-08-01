# -*- coding: utf8 -*-

from redis import Redis
from pymysql import connect
from pymysql.cursors import DictCursor

from app.interface.py.config import Config


__all__ = ['redis_conn', 'mysql_conn']


class LeoRedis(Redis):
    """"""


redis_conn = LeoRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True,
)


mysql_conn = connect(
    host=Config.MYSQL_HOST,
    port=Config.MYSQL_PORT,
    user=Config.MYSQL_USERNAME,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB,
    charset='utf8mb4',
    cursorclass=DictCursor,
)

