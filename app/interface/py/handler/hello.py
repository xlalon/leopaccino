# -*- coding:utf8 -*-

from .base import BaseHandler
from app.infra.celery.task.test import add


class HelloHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")


class TestHandler(BaseHandler):
    def get(self):
        x = self.get_argument('x')
        y = self.get_argument('y')
        result = add.delay(x, y)
        sum = result.get(timeout=1)
        return self.write({'x': x, 'y': y, 'sum': sum})
