# -*- coding:utf8 -*-

from app.infra.celery.task.test import add
from app.interface.py.dao import mysql_conn, redis_conn

from .base import BaseHandler


class HelloHandler(BaseHandler):
    def get(self):
        self.write("Hello, Leo Tornado!")


class TestRedisHandler(BaseHandler):
    def get(self):
        try:
            data = redis_conn.incr('hits')
        except Exception as e:
            data = e
        self.write('Hello Redis!\n 该页面已被访问 {} 次。'.format(str(data)))


class TestMysqlHandler(BaseHandler):
    def get(self):
        try:
            with mysql_conn.cursor() as cursor:
                sql = "SELECT value FROM test"
                cursor.execute(sql)
                data = cursor.fetchall()
        except Exception as e:
            data = e
        self.write('Hello Mysql!\n {}'.format(data))


class TestCeleryHandler(BaseHandler):
    def get(self):
        try:
            x = self.get_argument('x')
            y = self.get_argument('y')
            result = add.delay(x, y)
            data = result.get(timeout=1)
        except Exception as e:
            data = e
        return self.write({'x': x, 'y': y, 'data': data})
