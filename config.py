#!/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler.auth import HTTPBasicAuth
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 默认配置
class Config:
    #
    # for oslo config
    # MQ config
    mq_url = 'rabbit://:@192.168.92.135:5672/'

    NBAgent_namespace = 'nb_api'
    NBAgent_version = '1.0'

    NBAgentOracle_namespace = 'nb_api_oracle'
    NBAgentOracle_version = '1.0'

    NBAgentOracle_topic = 'rpc'
    executor = 'threading'


    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YYYYYYYYYYYYYYmy_secret_keyXXXXXXXXXX'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    WTF_CSRF_ENABLED = False
    # Default Token expired in 24 hours
    SECURITY_TOKEN_MAX_AGE = 86400
    SECURITY_UNAUTHORIZED_VIEW = '/'
    #
    UPLOAD_DIR = 'static/uploads'
    ERROR_404_HELP = False

    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'baas.jobs.jobs:job1',
    #         'args': (1, 2),
    #         'trigger': 'interval',
    #         'seconds': 2
    #     },
    #     # {
    #     #     'id': 'job2',
    #     #     'func': 'baas.jobs.jobs:execute_shell_script_with_params',
    #     #     'args': (1, 2),
    #     #     'trigger': 'interval',
    #     #     'seconds': 2
    #     # },
    # ]
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI, tablename='jobs')
    # }
    SCHEDULER_ALLOWED_HOSTS = ['*']
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }

    SCHEDULER_API_ENABLED = False
    # SCHEDULER_AUTH = HTTPBasicAuth()

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/db/sql.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    INIT_DB = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = '3540710@qq.com'
    MAIL_PASSWORD = 'ilmnlxjsqbdtbhgh'
    MAIL_DEFAULT_SENDER = '3540710@qq.com'

    DEBUG = False

    # SWAGGER_UI
    # https://flask-restplus.readthedocs.io/en/0.8.5/swaggerui.html
    SWAGGER_UI_DOC_EXPANSION = 'list'
    # SWAGGER_VALIDATOR_URL = 'http://domain.com/validator'

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
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': './log/baas.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
            },
            'jobs_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': './log/baas_jobs.log',
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
            'jobs': {
                'handlers': ['default', 'jobs_file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    @staticmethod
    def init_app(app):
        pass

    def __init__(self):
        pass



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
