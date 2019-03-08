#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
import os
from config import config
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_mail import Mail
from apscheduler.events import *
from baas.jobs.events import events_listener
from exceptions import Exception
import logging.config
import logging
from baas.models.dbs import db
from manage import app, scheduler, init_jobs

app.app_context().push()
# try to read flask design
# import flask
# flask._request_ctx_stack

# 定时任务
LISTENER_JOB = (EVENT_JOB_ADDED |
                EVENT_JOB_REMOVED |
                EVENT_JOB_MODIFIED |
                EVENT_JOB_EXECUTED |
                EVENT_JOB_ERROR |
                EVENT_JOB_MISSED)

# scheduler = APScheduler()
# scheduler.init_app(app)


from baas.models.dbs import *
from baas.models.views import *

# 后台管理
# 调整为 “/” 访问
admin = Admin(app, url='/', name=u'baas AP Server 后台管理系统', template_mode='bootstrap3')
admin.add_view(UserView(User, db.session, name=u'用户管理'))
admin.add_view(RoleView(Role, db.session, name=u'权限管理'))
admin.add_view(ShellFileView(ShellFile, db.session,name=u'Shell文件管理'))
admin.add_view(ShellParamView(ShellParam, db.session, name=u'Shell参数配置'))
admin.add_view(ApsJobView(ApsJobs, db.session, name=u'后台Job配置'))
admin.add_view(ApsJobLogsView(ApsJobLogs, db.session, name=u'后台Job运行日志'))
admin.add_view(MyLoginView(name='Login_myadmin'))
admin.add_view(MyLogoutView(name='Logout'))

# scheduler setting
# 解决gunicorn 多进程中APScheduler重复运行的问题
if os.name == 'nt':
    scheduler.add_listener(events_listener, LISTENER_JOB)
    scheduler.start()
    init_jobs()
else:
    # linux, using file lock to slove
    f = open("scheduler.lock", "wb")
    import fcntl
    import atexit

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.add_listener(events_listener, LISTENER_JOB)
        scheduler.start()
        init_jobs()
    except:
        pass

if __name__ != '__main__':
    # load logging globally
    # logging.config.fileConfig('logging.conf')
    # logging.info('logging starts')

    # [logger]root redirect to gunicorn.error
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logging.getLogger().handlers = gunicorn_logger.handlers
    logging.getLogger().setLevel(gunicorn_logger.level)
    logging.info("redirect logging to here ...")

    # [logger]app.logger redirect to gunicorn.error
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.propagate = 0
    app.logger.info("redirect app.logger to here ...")

if __name__ == '__main__':
    # Use local logging.conf for logging
    logging.config.fileConfig('logging.conf')
    logging.info('logging starts')

    flask_host = os.getenv("FLASK_HOST") if os.getenv("FLASK_HOST") else '0.0.0.0'
    flask_port = os.getenv("FLASK_PORT") if os.getenv("FLASK_PORT") else '5001'
    # flask_debug = app.config['FLASK_DEBUG']
    # application.run(host=flask_host, port=int(flask_port), debug=bool(flask_debug))
    app.run(host=flask_host, port=int(flask_port), debug=True)
    # flask_ssl_context = os.getenv("FLASK_SSL_CONTEXT") if os.getenv("FLASK_SSL_CONTEXT") else 'None'
    # app.run(ssl_context=flask_ssl_context, host=flask_host, port=int(flask_port), debug=bool(flask_debug))
    # 证书玩法
    # app.run(debug=True, ssl_context=(
    #     "server/server-cert.pem",
    #     "server/server-key.pem")
    # )


