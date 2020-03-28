# -*- coding:utf8 -*-

from .base import BaseHandler


class HelloHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")
