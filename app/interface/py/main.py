# -*- coding:utf8 -*-

import tornado.ioloop
import tornado.web
import sys
from .config.app_config import BASEDIR
sys.path.insert(0, BASEDIR)

from .handler import make_app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
