# -*- coding:utf8 -*-

import tornado.ioloop
import tornado.web

from .handler import make_app

from libs.utils.logger import get_logger
server_log = get_logger('tornado server')


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    server_log.info('listen on 8888')
    tornado.ioloop.IOLoop.current().start()
