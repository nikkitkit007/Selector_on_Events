#!/bin/sh
gunicorn --chdir server server_run:app -w 2 --worker-class gevent --threads 2 -b 0.0.0.0:80
