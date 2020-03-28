# -*- coding:utf8 -*-

from tornado.web import Application

from .hello import HelloHandler


def make_app():
    return Application([
        (r"/", HelloHandler),
    ])

