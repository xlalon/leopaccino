# -*- coding:utf8 -*-

from redis import Redis
from pymysql import connect
from pymysql.cursors import DictCursor

from app.infra.celery.task.test import add
from app.interface.py.config.app_config import MysqlConfig

from .base import BaseHandler

redis = Redis(host='10.96.139.53', port=6379)
connection = connect(host=MysqlConfig.mysql_host,
                     port=MysqlConfig.mysql_port,
                     user='root',
                     password='Xiao0000',
                     database=MysqlConfig.mysql_database,
                     charset='utf8mb4',
                     cursorclass=DictCursor)


class HelloHandler(BaseHandler):
    def get(self):
        count = redis.incr('hits')
        with connection.cursor() as cursor:
            sql = "SELECT * FROM test"
            cursor.execute(sql)
            data = cursor.fetchall()
        self.write('Hello World!\n 该页面已被访问 {} 次。\n test values:{}\n'.format(count, data))


class TestHandler(BaseHandler):
    def get(self):
        x = self.get_argument('x')
        y = self.get_argument('y')
        result = add.delay(x, y)
        sum_x_y = result.get(timeout=1)
        return self.write({'x': x, 'y': y, 'sum': sum_x_y})
