# -*- coding:utf8 -*-

import os


class MysqlConfig:
    mysql_username = os.environ.get('TORNADO_MYSQL_USERNAME')
    mysql_password = os.environ.get('TORNADO_MYSQL_PASSWORD')
    mysql_database = os.environ.get('mysql_database', 'leo_web')
    mysql_host = os.environ.get('mysql_host', '10.99.87.27')
    mysql_port = os.environ.get('mysql_port', 3306)
