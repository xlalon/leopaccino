# -*- coding:utf8 -*-

from tornado.web import Application

from .test import (
    HelloHandler,
    TestRedisHandler,
    TestMysqlHandler,
    TestCeleryHandler
)


def make_app():
    return Application([
        (r"/", HelloHandler),
        (r"/test/redis", TestRedisHandler),
        (r"/test/mysql", TestMysqlHandler),
        (r"/test/celery", TestCeleryHandler),
    ], **{'serve_traceback': True})
