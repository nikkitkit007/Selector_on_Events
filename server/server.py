
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
    return "Nice day..."


# ----------------------------------EVENT-----------------------------------


@app.route('/api/event/add', methods=["POST"])
def event_add() -> Tuple[flask.Response, int]:
    """
    request.json = {'event_name': str(127),
                    'time_start': str(timestamp),
                    'time_end': str(timestamp),
                    'description': str,
                    'url_pdf': str,
                    'people_count': int,
                    'coefficient': int,
                    'image': str(127)
    :return: flask.Response, int(status_code)
    """
    try:
        Event.add(request.json)

        info_logger.info(f"Event \"{request.json['event_name']}\" added!")
        return flask.make_response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/event/update', methods=["POST"])
def event_update() -> Tuple[flask.Response, int]:
    """
        request.json = {"event_id": int(event_id),
                        "data_to_update": {'event_name': str(127),
                                            'time_start': str(timestamp),
                                            'time_end': str(timestamp),
                                            'description': str,
                                            'url_pdf': str,
                                            'people_count': int,
                                            'coefficient': int,
                                            'image': str(127)}
                        }
        :return: flask.Response, status_code: int
        """
    try:
        Event.update(int(request.json['event_id']), request.json['data_to_update'])
        info_logger.info(f"Event with id:{int(request.json['event_id'])} updated!")
        return flask.make_response("200"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/event/get', methods=["GET"])
def event_get() -> Tuple[flask.Response, int]:
    """
    request.json = {"event_id": int(event_id)}
    :return: flask.Response({"event": event: dict}), status_code: int
    """
    try:
        events = Event.get(int(request.json.get('event_id', 0)), all_events=False)
        return (flask.make_response({"event": events}), 200) if events \
            else (flask.make_response({"error": "Not events"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/event/get_all', methods=["GET"])
def event_get_all() -> Tuple[flask.Response, int]:
    """
    request.json = {}
    :return: flask.Response({"events": list(dict(events))}), status_code: int
    """
    try:
        events = Event.get(0, all_events=True)
        return (flask.make_response({'events': events}), 200) if events \
            else (flask.make_response({"error": "Not events"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/event/delete', methods=["DELETE"])
def event_delete() -> Tuple[flask.Response, int]:
    """
    request.json = {"event_id": int(event_id)}
    :return: flask.Response("Event deleted"), int(status_code)
    """
    try:
        Event.delete(int(request.json.get('event_id')))
        info_logger.info(f"Event with id: {int(request.json.get('event_id'))} deleted.")
        return flask.make_response("Event deleted"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500

# -------------------------EVENT_apply/decline------------------------------


@app.route('/api/apply_event', methods=["POST"])
def apply_event() -> Tuple[flask.Response, int]:
    """
    request.json = {"event_id": int(event_id),
                    "user_id": int(user_id)}
    :return: flask.Response("User applied event"), int(status_code)
    """
    try:
        event_id = int(request.json.get('event_id'))
        user_id = int(request.json.get('user_id'))
        # check he has time to apply
        if checker.is_user_can_apply_event(user_id):
            User.apply_event(user_id, event_id)
            info_logger.info(f'User with id: {user_id} applied event {event_id}.')
            return flask.make_response("User applied event"), 200
        else:
            info_logger.error(f'User with id: {user_id} can not apply event: {event_id}.')
            return flask.make_response("User can not apply event"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/decline_event', methods=["POST"])
def decline_event() -> Tuple[flask.Response, int]:
    """
    request.json = {"event_id": int(event_id),
                    "user_id": int(user_id)}
    :return: flask.Response("User applied event"), int(status_code)
    """
    try:
        event_id = int(request.json['event_id'])
        user_id = int(request.json['user_id'])

        if checker.is_user_on_event_go(user_id, event_id):
            User.decline_event(user_id, event_id)
            info_logger.info(f'User with id: {user_id} decline event: {event_id}.')
            return flask.make_response("User decline event"), 200
        else:
            info_logger.error(f'User with id: {user_id} not in list event_go on event: {event_id}.')
            return flask.make_response({"error": "User decline event"}), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


# -------------------------EVENT_want/not_want------------------------------

def registration(event_id: int, user_id: int, cancel: bool = False) -> Tuple[flask.Response, int]:
    try:
        if not event_id or not user_id:
            return flask.make_response({"API-error": "invalid user_id or/and event_id"}), 200
        if checker.is_user_banned(user_id):
            return flask.make_response({"error": "You have been banned"}), 200
        if not checker.is_event_opened_for_want(event_id):
            return flask.make_response({"error": "Event close for registration"}), 200
        if not (checker.is_user_on_event_want(user_id, event_id) == cancel and
                not checker.is_user_on_event_go(user_id, event_id)):
            return flask.make_response({"error": "Not accepted to event"}), 200

        if cancel:
            Event.update_del_users_id_want(event_id, user_id)
            info_logger.info(f"User: {user_id} cancel registered on event: {event_id}")
        else:
            Event.update_add_users_id_want(event_id, user_id)
            info_logger.info(f"User: {user_id} registered on event: {event_id}")
        return flask.make_response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/event_registration', methods=["POST"])
def event_registration() -> Tuple[flask.Response, int]:
    """
    request.json = {"event_id": int(event_id),
                    "user_id": int(user_id)}
    :return: flask.Response("User registered on event"), int(status_code)
    """
    event_id = int(request.json.get('event_id'))
    user_id = int(request.json.get('user_id'))
    return registration(user_id, event_id)


@app.route('/api/event_cancel_registration', methods=["POST"])
def event_cancel_registration():
    """
    request.json = {"event_id": int(event_id),
                    "user_id": int(user_id)}
    :return: flask.Response("User cancel registered event"), int(status_code)
    """
    event_id = int(request.json['event_id'])
    user_id = int(request.json['user_id'])
    return registration(user_id, event_id, cancel=True)


# ----------------------------------USER------------------------------------


@app.route('/api/user/add', methods=["POST"])
def user_add() -> Tuple[flask.Response, int]:
    """
    request.json = {'user_isu_number': 288888,
                    'user_name': str(127),
                    'user_surname': str(127),
                    'user_patronymic': str(127),
                    'phone': str(127),
                    'vk_link': str(127),
                    'mail': str(127),
                    'is_russian_citizenship': bool}
    :return: flask.Response("User added"), int(status_code)
    """
    user_to_add = request.json

    if not checker.is_correct_phone(request.json['phone']):
        error_logger.error("User add incorrect phone number")
        return flask.make_response({"error": "Wrong phone"}), 400
    if not checker.is_correct_mail(request.json['mail']):
        error_logger.error("User add incorrect mail")
        return flask.make_response({"error": "Wrong mail"}), 400
    try:
        User.add(user_to_add)
        info_logger.info(f'User {request.json["user_name"]} added')
        return flask.make_response("User added"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/user/get_profile', methods=["GET"])
def user_get_profile() -> Tuple[flask.Response, int]:
    """
    request.json = {"user_id": int(user_id)}
    :return: flask.Response({"user": dict(user)}), int(status_code)
    """
    try:
        user = User.get(request.json.get('user_id'))
        return flask.make_response({"user": user}), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/user/get_history', methods=["GET"])  # feature
def user_get_history():
    user_id = request.json

    try:
        pass
    except psycopg2.Error as E:
        return 'Error with db {}'.format(E), 400
    except Exception as E:
        return str(E), 400


@app.route('/api/user/update', methods=["POST"])
def user_update() -> Tuple[flask.Response, int]:
    """
    request.json = {"user_id": int(user_id),
                    'user_data_to_update': {
                            'user_isu_number': int,
                            'user_name': str(127),
                            'user_surname': str(127),
                            'user_patronymic': str(127),
                            'phone': str(127),
                            'vk_link': str(127),
                            'mail': str(127),
                            'is_russian_citizenship': bool
                        }}
    :return: flask.Response("User data updated"), int(status_code)
    """
    try:
        User.update(int(request.json.get('user_id')), request.json.get('user_data_to_update'))
        info_logger.info(f"User with id:{int(request.json['user_id'])} updated!")
        return flask.make_response("User data updated"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/user/delete', methods=["DELETE"])
def user_delete() -> Tuple[flask.Response, int]:
    """
    request.json = {"user_id": int(user_id)}
    :return: flask.Response("User deleted"), int(status_code)
    """
    try:
        User.delete(int(request.json.get('user_id')))
        info_logger.info(f"User with id: {int(request.json.get('user_id'))} deleted.")
        return flask.make_response("OK"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


# -------------------------NOTIFIES--------------------------------

@app.route('/api/notify/add', methods=["POST"])
def notify_add() -> Tuple[flask.Response, int]:
    """
    request.json = {'event_id': int,
                    'notify_header': str(127),
                    'notify_data': str
    :return: flask.Response("Notify added"), int(status_code)
    """
    try:
        Notify.add(request.json)
        info_logger.info(f"Notify with id: {int(request.json.get('notify_id'))} added.")
        return flask.make_response("Notify added"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/notify/send', methods=["POST"])
def notify_send():
    # maybe I delete this API ! # TODO
    notifies = []
    try:
        notifies_id = User.get(request.json.get('user_id'))['notify_id']  # user's notifies

        for notify_id in notifies_id:
            notifies.append(Notify.get(notify_id))  # list with notifies json

        return notifies
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


# ----------------------------News---------------------------------
@app.route('/api/news/add', methods=["POST"])
def news_add() -> Tuple[flask.Response, int]:
    """
    request.json = {'header': str(127),
                    'data': str,
                    'time': str(timestamp)}
    :return: flask.Response("News added"), int(status_code)
    """
    try:
        News.add(request.json)
        info_logger.info(f"News with id: {request.json.get('header')} added.")
        return flask.make_response("News added"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/news/get', methods=["GET"])
def news_get() -> Tuple[flask.Response, int]:
    """
    request.json = {"news_id": int(news_id)}
    :return: flask.Response({"news": dict(news)}), int(status_code)
    """
    try:
        news = News.get(int(request.json.get('news_id', 0)), all_news=False)
        return (flask.make_response({"news": news}), 200) if news \
            else (flask.make_response({"error": "Not news"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/news/get_all', methods=["GET"])
def news_get_all() -> Tuple[flask.Response, int]:
    """
    request.json = {}
    :return: flask.Response({"news": list(dict(news))}), status_code: int
    """
    try:
        news = News.get(0, all_news=True)
        return (flask.make_response({'news': news}), 200) if news \
            else (flask.make_response({"error": "Not news"}), 400)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/news/update', methods=["POST"])
def news_update() -> Tuple[flask.Response, int]:
    """
    request.json = {'news_id': news_id,
                    'news_data_to_update': {
                        'header': str(127),
                        'data': str,
                        'time': str(timestamp)}
                    }
    :return: flask.Response("News updated"), int(status_code)
    """
    try:
        News.update(int(request.json.get('news_id')), request.json.get('news_data_to_update'))
        info_logger.info(f"News with id:{int(request.json['news_id'])} updated!")
        return flask.make_response("News updated"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


@app.route('/api/news/delete', methods=["DELETE"])
def news_delete() -> Tuple[flask.Response, int]:
    """
    request.json = {"news_id": int(news_id)}
    :return: flask.Response("News deleted"), int(status_code)
    """
    try:
        News.delete(int(request.json.get('news_id')))
        info_logger.info(f"News with id: {int(request.json.get('news_id'))} deleted.")
        return flask.make_response("News deleted"), 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.make_response({"error": str(E)}), 500


if __name__ == '__main__':
    app.run(host=config.HOST_ADDRESS, port=config.HOST_PORT)  # to see mistakes

# CRUD
# 1) Create POST
# 2) Read - GET
# 3) Update - Patch Put
# 4) Delete - DELETE
