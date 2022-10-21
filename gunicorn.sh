#!/bin/sh
gunicorn --bind 0.0.0.0:8080 wsgi:app
#gunicorn --chdir server '__main__':app -w 2 --worker-class gevent --threads 2 -b 0.0.0.0:8080
