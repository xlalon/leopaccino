# -*- coding:utf8 -*-

from redis import Redis
from pymysql import connect
from pymysql.cursors import DictCursor

from app.infra.celery.task.test import add

from .base import BaseHandler

redis = Redis(host='leopaccino_redis', port=6379)
connection = connect(host='leopaccino_mysql',
                     user='leo',
                     password='Xiao0000',
                     database='leo_web',
                     charset='utf8mb4',
                     cursorclass=DictCursor)


class HelloHandler(BaseHandler):
    def get(self):
        count = redis.incr('hits')
        with connection.cursor() as cursor:
            # Create a new record
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
