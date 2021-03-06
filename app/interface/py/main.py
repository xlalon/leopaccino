# -*- coding:utf8 -*-

import tornado.ioloop
import tornado.web

from .handler import make_app

from libs.utils.logger import get_logger
server_log = get_logger('tornado_server')


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    server_log.info('Server listen on 8080...')
    tornado.ioloop.IOLoop.current().start()
