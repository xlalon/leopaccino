# -*- coding:utf8 -*-

import tornado.ioloop
import tornado.web

from .handler import make_app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
