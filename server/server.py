import json

import flask

import config
import sys
import psycopg2
import services.checker as checker

from flask import Flask, request

from logger_config import info_logger, error_logger

from data_base.db_controller import create_db
from data_base.event_tbl import Event
from data_base.user_tbl import User
from data_base.notify_tbl import Notify
from data_base.news_tbl import News

from typing import Tuple

app = Flask(__name__)
sys.path.append('../')

create_db()


@app.route('/')
def index():
    return "User info..."


# ----------------------------------EVENT-----------------------------------


@app.route('/api/event/add', methods=["POST"])
def event_add() -> Tuple[flask.Response, int]:
    try:
        Event.add(request.json)

        info_logger.info(f"Event \"{request.json['event_name']}\" added!")
        return flask.Response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/event/update', methods=["POST"])
def event_update() -> Tuple[flask.Response, int]:
    try:
        Event.update(int(request.json['event_id']), request.json['data_to_update'])
        info_logger.info(f"Event with id:{int(request.json['event_id'])} updated!")
        return flask.Response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/event/get', methods=["GET"])
def event_get() -> Tuple[flask.Response, int]:
    try:
        events = Event.get(int(request.json.get('event_id', 0)), all_events=False)
        return (flask.Response(events), 200) if events else (flask.Response({"error": "Not events"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/event/get_all', methods=["GET"])
def event_get_all() -> Tuple[flask.Response, int]:
    try:
        events = Event.get(0, all_events=True)
        return (flask.Response({'events': events}), 200) if events else (flask.Response({"error": "Not events"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/event/delete', methods=["DELETE"])
def event_delete() -> Tuple[flask.Response, int]:
    try:
        Event.delete(int(request.json.get('event_id')))
        info_logger.info(f"Event with id: {int(request.json.get('event_id'))} deleted.")
        return flask.Response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500

# -------------------------EVENT_apply/decline------------------------------


@app.route('/api/apply_event', methods=["POST"])
def apply_event():
    try:
        event_id = int(request.json.get('event_id'))
        user_id = int(request.json.get('user_id'))
        # check he has time to apply
        if checker.is_user_can_apply_event(user_id):
            User.apply_event(user_id, event_id)
            info_logger.info(f'User with id: {user_id} applied event {event_id}.')
        return flask.Response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/decline_event', methods=["POST"])
def decline_event():
    try:
        event_id = int(request.json['event_id'])
        user_id = int(request.json['user_id'])

        if checker.is_user_on_event_go(user_id, event_id):
            User.decline_event(user_id, event_id)
        # check, maybe he will take ban
        info_logger.info(f'User with id: {user_id} decline event {event_id}.')

        return True
    except psycopg2.Error as E:
        error_logger.error(E)
        return '', 400


# -------------------------EVENT_want/not_want------------------------------

def registration(event_id: int, user_id: int, cancel: bool = False) -> Tuple[flask.Response, int]:
    try:
        if not event_id or not user_id:
            return flask.Response({"API-error": "invalid user_id or/and event_id"}), 200
        if checker.is_user_banned(user_id):
            return flask.Response({"error": "You have been banned"}), 200
        if not checker.is_event_opened_for_want(event_id):
            return flask.Response({"error": "Event close for registration"}), 200
        if not (checker.is_user_on_event_want(user_id, event_id) == cancel and
                not checker.is_user_on_event_go(user_id, event_id)):
            return flask.Response({"error": "Not accepted to event"}), 200

        if cancel:
            Event.update_del_users_id_want(event_id, user_id)
        else:
            Event.update_add_users_id_want(event_id, user_id)
        return flask.Response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/event_registration', methods=["POST"])
def event_registration():
    event_id = int(request.json.get('event_id'))
    user_id = int(request.json.get('user_id'))
    return registration(user_id, event_id)


@app.route('/api/event_cancel_registration', methods=["POST"])
def event_cancel_registration():
    event_id = int(request.json['event_id'])
    user_id = int(request.json['user_id'])
    return registration(user_id, event_id, cancel=True)


# ----------------------------------USER------------------------------------


@app.route('/api/user/add', methods=["POST"])
def user_add() -> Tuple[flask.Response, int]:
    user_to_add = request.json

    if not checker.is_correct_phone(request.json['phone']):
        error_logger.error("User add incorrect phone number")
        return flask.Response({"error": "Wrong phone"}), 400
    if not checker.is_correct_mail(request.json['mail']):
        error_logger.error("User add incorrect mail")
        return flask.Response({"error": "Wrong mail"}), 400
    try:
        User.add(user_to_add)
        info_logger.info(f'User {request.json["user_name"]} added')
        return flask.Response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/user/get_profile', methods=["GET"])
def user_get_profile() -> Tuple[flask.Response, int]:
    user_id = request.json['user_id']
    try:
        user = User.get(user_id)
        return flask.Response(user), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/user/get_history', methods=["GET"])  # feature
def user_get_history():
    user_id = request.json

    try:
        pass
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/update', methods=["POST"])
def user_update() -> Tuple[flask.Response, int]:
    user_id = int(request.json['user_id'])
    user_data_to_update = request.json['user_data_to_update']

    try:
        User.update(user_id, user_data_to_update)
        return flask.Response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


@app.route('/api/delete', methods=["DELETE"])
def user_delete() -> Tuple[flask.Response, int]:
    user_id = int(request.json['user_id'])
    try:
        User.delete(user_id)
        return flask.Response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


# -------------------------NOTIFIES--------------------------------

@app.route('/api/notify/add', methods=["POST"])
def notify_add():
    notify_to_add = request.json
    try:
        Notify.add(notify_to_add)
        return "OK", 200
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/notify/send', methods=["POST"])
def notify_send():
    user_id = request.json['user_id']
    notifies = []
    try:
        notifies_id = User.get(user_id)['notify_id']  # user's notifies

        for notify_id in notifies_id:
            notifies.append(Notify.get(notify_id))  # list with notifies json

        return notifies
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


if __name__ == '__main__':
    app.run(host=config.HOST_ADDRESS, port=config.HOST_PORT)  # to see mistakes

# CRUD
# 1) Create POST
# 2) Read - GET
# 3) Update - Patch Put
# 4) Delete - DELETE
