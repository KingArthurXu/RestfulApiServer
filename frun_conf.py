#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import os
from gunicorn.workers.base import Worker

bind = '0.0.0.0:5000'
workers = 4
backlog = 2048
worker_class = "sync"
debug = False
proc_name = 'frun'
pidfile = 'frun.pid'
errorlog = 'frun.log'
# errorlog = '-'
loglevel = 'debug'
daemon = True
raw_env = ["FLASK_CONFIG=production"]
accesslog = 'frun.access.log'
# accesslog = '-'
access_log_format= '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
timeout = 300


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    server.log.info("Worker pre spawned (pid: %s)", worker.pid)


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    # ## get traceback info
    # import threading, sys, traceback
    # id2name = {th.ident: th.name for th in threading.enumerate()}
    # code = []
    # for threadId, stack in sys._current_frames().items():
    #     code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
    #         threadId))
    #     for filename, lineno, name, line in traceback.extract_stack(stack):
    #         code.append('File: "%s", line %d, in %s' % (filename,
    #             lineno, name))
    #         if line:
    #             code.append("  %s" % (line.strip()))
    # worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("【in-worker】received SIGABRT signal")

