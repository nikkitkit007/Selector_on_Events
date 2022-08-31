# https://tokmakov.msk.ru/blog/item/41 - about regular expressions

"""
req = requests.post('http://127.0.0.1:5000/api/user_add', json={'user_id': 1})
req.content
b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>The browser (or proxy) sent a request that this server could not understand.</p>\n'
req.status_code
400
req.text
'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>The browser (or proxy) sent a request that this server could not understand.</p>\n'
req.json()
"""

import sys
import psycopg2
import services.selector as selector
import services.checker as checker
import config
import data.db_worker as db
from flask import Flask, request
import re

DB = db.DataBaseEvents()


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
    all_data = request.values
    event_id = all_data['event_id']
    del all_data['event_id']
    data_to_update = request.values
    try:
        DB.event_update(event_id, data_to_update)
        return True
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_get', methods=["POST"])
def event_get():
    event_id = request.values['event_id']
    user_id = request.values['user_id']
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


# -------------------------EVENT_apply/decline------------------------------


@app.route('/api/apply_event', methods=["POST"])
def apply_event():
    event_id = int(request.values['event_id'])
    user_id = int(request.values['user_id'])
    try:
        # check he has time to apply
        if checker.is_user_can_apply_event(user_id):
            selector.user_apply_event(user_id, event_id)

        return True
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/decline_event', methods=["POST"])  # !!!!!!!
def decline_event():
    event_id = int(request.values['event_id'])
    user_id = int(request.values['user_id'])
    try:
        if checker.is_user_on_event_go(user_id, event_id):
            selector.user_decline_event(user_id, event_id)
        # check, maybe he will take ban
        return True
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


# -------------------------EVENT_want/not_want------------------------------


@app.route('/api/event_registration', methods=["POST"])
def event_want():
    event_id = int(request.values['event_id'])
    user_id = int(request.values['user_id'])
    try:
        if not checker.is_user_on_event_want(user_id, event_id) \
                and not checker.is_user_on_event_go(user_id, event_id)\
                and not checker.is_user_banned(user_id):
            # проверяю, что юзер еще не записался на мероприятие
            # и нет бана
            if checker.is_event_opened_for_want(event_id):  # проверяю, что событие доступно для записи
                # bottom color green
                DB.event_update_add_users_id_want(event_id, user_id)
            else:
                # bottom color gray
                pass
        else:
            # bottom color red
            pass
        return True
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


@app.route('/api/event_cancel_registration', methods=["POST"])
def event_not_want():
    event_id = int(request.values['event_id'])
    user_id = int(request.values['user_id'])
    try:
        if checker.is_user_on_event_want(user_id, event_id) \
                and not checker.is_user_on_event_go(user_id, event_id):
            # проверяю, что юзер УЖЕ записался на мероприятие
            if checker.is_event_opened_for_want(event_id):  # проверяю, что событие доступно для записи
                # bottom color red
                DB.event_update_del_users_id_want(event_id, user_id)
            else:
                # bottom color gray
                pass
        else:
            # bottom color green
            pass
        return True
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400


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


@app.route('/api/user_get_history', methods=["POST"])  # feature
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


# -------------------------NOTIFIES--------------------------------

@app.route('/api/notifies_send', methods=["POST"])
def notifies_send():
    user_id = request.values['user_id']
    notifies = []
    try:
        notifies_id = DB.user_get(user_id)['notify_id']         # user's notifies

        for notify_id in notifies_id:
            notifies.append(DB.notify_get(notify_id))           # list with notifies json

        return notifies
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


if __name__ == '__main__':
    app.run()  # to see mistakes
