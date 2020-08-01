# -*- coding: utf8 -*-

import os


class MysqlConfigMixin:
    MYSQL_USERNAME = os.getenv('TORNADO_MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('TORNADO_MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('TORNADO_MYSQL_DB', 'leo_web')
    MYSQL_HOST = os.getenv('TORNADO_MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.getenv('TORNADO_MYSQL_PORT', 3306))


class RedisConfigMixin:
    REDIS_HOST = os.getenv('TORNADO_REDIS_HOST')
    REDIS_PORT = int(os.getenv('TORNADO_REDIS_PORT', 6379))


class ConfigBase(MysqlConfigMixin, RedisConfigMixin):
    """"""
