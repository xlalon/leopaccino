# -*- coding:utf8 -*-

from redis import Redis

from app.infra.celery.task.test import add

from .base import BaseHandler

redis = Redis(host='redis', port=6379)


class HelloHandler(BaseHandler):
    def get(self):
        count = redis.incr('hits')
        self.write('Hello World! 该页面已被访问 {} 次。\n'.format(count))


class TestHandler(BaseHandler):
    def get(self):
        x = self.get_argument('x')
        y = self.get_argument('y')
        result = add.delay(x, y)
        sum_x_y = result.get(timeout=1)
        return self.write({'x': x, 'y': y, 'sum': sum_x_y})
