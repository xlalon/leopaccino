# -*- coding:utf8 -*-

from celery import Celery
from app.infra.celery.config import celeryconfig


lpc_app = Celery('lpc_app')
lpc_app.config_from_object(celeryconfig)


if __name__ == '__main__':
    lpc_app.start()
