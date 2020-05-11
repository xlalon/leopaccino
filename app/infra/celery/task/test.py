# -*- coding:utf8 -*-

from ..lpc_app import lpc_app


@lpc_app.task
def add(x, y):
    return x + y
