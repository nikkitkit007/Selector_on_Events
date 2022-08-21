import sys
# import requests
import psycopg2

import data.db_worker as db
import server.services.selector as selector
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

# ----------------------------------EVENT-----------------------------------


@app.route('/api/add_event', methods=["POST"])
def add_event():
    event_to_add = request.values
    try:
        DB.add_event(event_to_add)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/update_event', methods=["POST"])       # !!!!!!!
def update_event():
    """
    :return:
    """
    # name, time_start, time_end,image,pdf, cost = request.values['event_name'], request.values[]
    name = request.json["name"]
    return name[::]


@app.route('/api/get_event', methods=["POST"])
def get_event():
    event_id = request.values
    try:
        DB.get_event(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/get_events')                       # !!!!!!!
def get_events():
    try:
        # DB.get_events()
        pass
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/delete_event', methods=["POST"])
def delete_event():
    event_id = request.values
    try:
        DB.delete_event(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400

# -------------------------EVENT_apply/decline------------------------------


@app.route('/api/apply_event', methods=["POST"])        # !!!!!!!
def apply_event():
    event_id = request.values['event_id']
    user_id = request.values['user_id']
    try:
        DB.get_event(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/decline_event', methods=["POST"])      # !!!!!!!
def decline_event():
    event_id = request.values['event_id']
    user_id = request.values['user_id']
    try:
        DB.get_event(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
# ----------------------------------USER------------------------------------


@app.route('/api/add_user', methods=["POST"])
def add_user():
    user_to_add = request.values
    # control mail and phone

    if not check_phone(user_to_add['phone']):
        return 'Wrong phone', 400
    if not check_mail(user_to_add['mail']):
        return 'Wrong mail', 400
    try:
        DB.add_user(user_to_add)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/get_user_profile', methods=["POST"])
def get_user_profile():
    user_id = request.values
    # control mail and phone
    try:
        user = DB.get_user(user_id)
        # print(user)
        return user
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/get_user_history', methods=["POST"])       # !!!!!!
def get_user_history():
    user_id = request.values

    try:
        DB.add_user(user_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/update_user', methods=["POST"])       # !!!!!!
def update_user():
    user_data_to_update = request.values

    try:
        DB.update_user(user_data_to_update)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


if __name__ == '__main__':
    app.run()         # to see mistakes

