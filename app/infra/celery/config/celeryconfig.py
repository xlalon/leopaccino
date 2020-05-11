# -*- coding:utf8 -*-

broker_url = 'pyamqp://'
result_backend = 'redis://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
include = ['app.infra.celery.task.test']
