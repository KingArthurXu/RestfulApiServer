#!/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler.auth import HTTPBasicAuth
import os
import platform

basedir = os.path.abspath(os.path.dirname(__file__))

# 默认配置
class Config:
    def __init__(self):
        pass
    # MQ config
    mq_url = 'rabbit://:@192.168.92.135:5672/'

    NBAgent_namespace = 'nb_api'
    NBAgent_version = '1.0'

    NBAgentOracle_namespace = 'nb_api_oracle'
    NBAgentOracle_version = '1.0'

    # different server name from Linux and Windows
    osName = platform.system()
    if osName == 'Windows':
        rpc_server_name = 'win1'
    elif osName == 'Linux':
        rpc_server_name = 'lnx1'
    else:
        rpc_server_name = 'oth1'

    NBAgentOracle_topic = 'rpc'
    executor= 'threading'

    log_conf = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(threadName)s %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': 'INFO',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',  # Default is stderr
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': 'db_agent.log',
                    'mode': 'a',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            }
        }

# 开发配置
class DevelopmentConfig(Config):
    DEBUG = True
    SCHEDULER_API_ENABLED = True
    SCHEDULER_AUTH = HTTPBasicAuth()

    @staticmethod
    def init_app(app):
        print("DevelopmentConfig init_app")


# 生产配置
class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
