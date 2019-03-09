#!/usr/bin/bash
# 20190309 check brun.gunicorn.pid file and kill
# http://docs.gunicorn.org/en/stable/signals.html

if [ -f "brun.pid" ]; then
    # ps -ef | grep `cat brun.gunicorn.pid` | grep -v grep | awk '{ print $2 }' | xargs kill -QUIT
    # kill master
    ps -ef | awk '{ print $2 }' | grep `cat brun.gunicorn.pid` | xargs kill -QUIT
    rm brun.gunicorn.pid
fi
if [ -f "frun.pid" ]; then
    # kill master
    # ps -ef | grep `cat frun.gunicorn.pid` | grep -v grep | awk '{ print $2 }' | xargs kill -QUIT
    ps -ef | awk '{ print $2 }' | grep `cat frun.gunicorn.pid` | xargs kill -QUIT
    rm frun.gunicorn.pid
fi

sleep 1
ps -ef | grep gunicorn | grep -v grep | awk '{ print $1 }'

if [ $? -eq 0 ]
then
    ps -ef | grep gunicorn_ | grep -v grep | awk '{ print $2 }' | xargs kill -9
fi
/usr/bin/gunicorn -c gunicorn_frun.py frun:app
/usr/bin/gunicorn -c gunicorn_brun.py brun:app
/usr/bin/tail -f ./frun.error.log

