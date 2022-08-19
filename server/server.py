import sys
# import requests
import psycopg2

import data.bd_worker as db
from flask import Flask, request
import re

DB = db.DB_PostgreSQL()


def check_mail(mail_address):
    regex_mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex_mail, mail_address):
        return True
    else:
        return False


def check_phone(phone):
    regex_phone = re.compile(r'')
    if re.fullmatch(regex_phone, phone):
        return True
    else:
        return False


app = Flask(__name__)
sys.path.append('../')


@app.route('/')
def index():
    return "User info..."


@app.route('/api/add_event', methods=["POST"])
def add_event():                            # add event in db
    """
    :return:
    """
    # name, time_start, time_end,image,pdf, cost = request.values['event_name'], request.values[]
    name = request.json["name"]
    return name[::-1]
    # bd.add_event()
    # if not request.values['token'] in accepting_tokens:
    #     return "Access denied"


@app.route('/api/update_event', methods=["POST"])
def update_event():
    """
    :return:
    """
    # name, time_start, time_end,image,pdf, cost = request.values['event_name'], request.values[]
    name = request.json["name"]
    return name[::]


@app.route('/api/add_user', methods=["POST"])
def add_user():
    # print(request.values)
    if not check_phone(request.values['phone']):
        return 'Wrong phone', 400
    if not check_mail(request.values['mail']):
        return 'Wrong mail', 400
    try:
        DB.add_user(request.values)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


if __name__ == '__main__':
    app.run()         # to see mistakes

