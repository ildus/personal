#!/usr/bin/env bash

cd /root/personal
. env/bin/activate
cd pro
exec python manage.py runfcgi method=threaded host=127.0.0.1 port=8081 pidfile=ildusorg.pid minspare=4 maxspare=30 daemonize=false
