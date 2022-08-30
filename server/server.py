# https://tokmakov.msk.ru/blog/item/41 - about regular expressions

import sys
import psycopg2
import server.services.selector as selector
import config
import data.db_worker as db
from flask import Flask, request
import re


DB = db.DB_PostgreSQL()


def check_mail(mail_address):
    regex_mail = re.compile(config.REGEX_MAIL)
    if re.fullmatch(regex_mail, mail_address):
        return True
    else:
        return False


def check_phone(phone):
    regex_phone = re.compile(config.REGEX_PHONE)
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


@app.route('/api/event_add', methods=["POST"])
def event_add():
    event_to_add = request.values
    try:
        DB.event_add(event_to_add)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_update', methods=["POST"])
def event_update():
    event_id = request.values['event_id']
    data_to_update = request.values
    try:
        DB.event_update(event_id, data_to_update)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_get', methods=["POST"])
def event_get():
    event_id = request.values
    try:
        DB.event_get(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_delete', methods=["POST"])
def event_delete():
    event_id = request.values
    try:
        DB.event_delete(event_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400

# --------------------------------------------------------------------------
# -------------------------EVENT_apply/decline------------------------------


@app.route('/api/apply_event', methods=["POST"])        # !!!!!!!
def apply_event():
    event_id = request.values['event_id']
    user_id = request.values['user_id']
    try:
        DB.event_update_add_users_id_go(event_id, user_id)
        # DB.selector.

        DB.event_update_del_users_id_want(event_id, user_id)
        # user_id add to event.users_id_go

    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/decline_event', methods=["POST"])      # !!!!!!!
def decline_event():
    event_id = request.values['event_id']
    user_id = request.values['user_id']
    try:
        DB.event_update_del_users_id_want(event_id, user_id)
        # check, maybe he will take ban
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400

# --------------------------------------------------------------------------
# -------------------------EVENT_want/not_want------------------------------


@app.route('/api/event_want', methods=["POST"])
def event_want():
    # I need to check free places (users_id_go)? (if not free places - user can't 'event_want')
    # Or I need to check that user already 'event_want' or 'event_go'?
    event_id = request.values['event_id']
    user_id = request.values['user_id']
    try:
        DB.event_update_add_users_id_want(event_id, user_id)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_not_want', methods=["POST"])      # !!!!!!!
def event_not_want():
    pass
# ----------------------------------USER------------------------------------


@app.route('/api/user_add', methods=["POST"])
def user_add():
    user_to_add = request.values

    if not check_phone(user_to_add['phone']):
        return 'Wrong phone', 400
    if not check_mail(user_to_add['mail']):
        return 'Wrong mail', 400
    try:
        DB.user_add(user_to_add)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/user_get_profile', methods=["POST"])
def user_get_profile():
    user_id = request.values
    try:
        user = DB.user_get(user_id)
        return user
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/user_get_history', methods=["POST"])       # feature
def user_get_history():
    user_id = request.values

    try:
        pass
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/user_update', methods=["POST"])
def user_update():
    user_id = request.values['user_id']
    user_data_to_update = request.values

    try:
        DB.user_update(user_id, user_data_to_update)
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


if __name__ == '__main__':
    app.run()         # to see mistakes

