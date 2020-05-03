# -*- coding:utf8 -*-

from tornado.web import Application

from .hello import HelloHandler, TestHandler


def make_app():
    return Application([
        (r"/", HelloHandler),
        (r"/add", TestHandler),
    ])

