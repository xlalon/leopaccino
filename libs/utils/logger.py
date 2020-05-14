# -*- coding: utf8 -*-

import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_logger(filename,
               level='INFO',
               max_bytes=5*1024*1024,
               backup=7,
               name=None,
               datefmt='%d/%b/%Y %H:%M:%S %z',
               fmt='[%(asctime)s][%(filename)s][lineno:%(lineno)d][%(levelname)s] %(message)s'):

    if name is None:
        name = filename.rsplit('.', maxsplit=1)[0]
    logger = logging.getLogger(name)

    logger.setLevel(level.upper())
    formatter = logging.Formatter(fmt, datefmt=datefmt)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    logspath = BASEDIR + '/logs/'
    if not os.path.isdir(logspath):
        os.mkdir(logspath)
    filepath = logspath + datetime.now().strftime('%Y%m/')
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    abs_filename = filepath + filename
    if not abs_filename.endswith('.log'):
        abs_filename += '.log'

    fh = RotatingFileHandler(abs_filename, maxBytes=max_bytes, backupCount=backup)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


if __name__ == '__main__':
    logger_test = get_logger('test.log')
    try:
        logger_test.info('test info message')
        raise ValueError("test error message")
    except:
        from traceback import format_exc
        logger_test.error(format_exc())
