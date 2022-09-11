
import sys

import flask
import config
import server.services.selector as selector
import server.services.checker as checker
from flask import Flask, request, jsonify

from logger_config import info_logger, error_logger

from data_base.db_controller import create_db
import data_base.event_tbl as event_tbl
import data_base.user_tbl as user_tbl
import data_base.notify_tbl as notify_tbl
import data_base.news_tbl as news_tbl


app = Flask(__name__)
sys.path.append('../')

create_db()


@app.route('/')
def index():
    return "User info..."


# ----------------------------------USER------------------------------------
@app.route('/api/user/<method>', methods=["GET", "POST", "DELETE"])
def api_handle_user(method):
    try:
        if request.method == "POST":
            if method == "add":
                if not checker.is_correct_phone(request.json['phone']):
                    error_logger.error("User add incorrect phone number")
                    return 'Wrong phone', 400
                if not checker.is_correct_mail(request.json['mail']):
                    error_logger.error("User add incorrect mail")
                    return 'Wrong mail', 400
                user_tbl.user_add(request.json)
                info_logger.info(f'User {request.json["user_name"]} added')
            elif method == "update":
                user_tbl.user_update(int(request.json['user_id']), request.json['user_data_to_update'])
                info_logger.info(f"User with id {int(request.json['user_id'])} updated!")
            else:
                return flask.Response({"error": "Invalid method!"}), 503
        elif request.method == "GET":
            if method == "profile":
                if user_id := request.args.get("user_id") is not None:
                    user = user_tbl.user_get(user_id)
                    return user, 200
                else:
                    return flask.Response({"error": "Empty user id"}), 504
            else:
                return flask.Response({"error": "Invalid method!"}), 503
        elif request.method == "DELETE":
            if method == "delete":
                if user_id := request.args.get("user_id") is not None:
                    user_tbl.user_delete(user_id)
                else:
                    return flask.Response({"error": "Empty user id"}), 503
            else:
                return flask.Response({"error": "Invalid method"}), 504
        else:
            return flask.Response({"error": "Invalid CRUD"}), 503
        return '', 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}), 500


# ----------------------------------EVENT-----------------------------------
@app.route('/api/event/<method>', methods=["GET", "POST", "DELETE"])
def api_handle_event(method):
    try:
        if request.method == "POST":
            if method == "add":
                event_tbl.event_add(request.json)
                info_logger.info(f'Event \"{request.json["event_name"]}\" added!')
            elif method == "update":
                event_tbl.event_update(int(request.json['event_id']), request.json['data_to_update'])
                info_logger.info(f"Event with id:{int(request.json['event_id'])} updated!")
            else:
                return flask.Response({"error": "Invalid method!"}, status=503)
        elif request.method == "GET":
            if method == "get" or method == "get_all":
                events = event_tbl.event_get(int(request.json.get('event_id', 0)), all_events=method == "get_all")
                return events, 200 if events else "Not events", 400
            else:
                return flask.Response({"error": "Invalid method!"}, status=503)
        elif request.method == "DELETE":
            if method == "delete":
                event_tbl.event_delete(int(request.json['event_id']))
                info_logger.info(f"Event with id: {int(request.json['event_id'])} deleted.")
        else:
            return flask.Response({"error": "Invalid CRUD"}, status=503)
        return "", 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}, status=500)


# ----------------------------EVENT_confirm---------------------------------
@app.route('/api/event/confirm/<method>', methods=["GET", "POST"])
def api_handle_event_confirm(method):
    try:
        if request.method == "POST":
            event_id = 0
            if (user_id := request.json.get("user_id") is not None) \
                    and (event_id := request.json.get("event_id") is not None):
                if method == "apply":
                    if checker.is_user_can_apply_event(user_id):
                        selector.user_apply_event(user_id, event_id)
                        info_logger.info(f'User with id: {user_id} applied event: {event_id}.')
                    else:
                        return {"error": "User can't to apply event"}, 400
                elif method == "decline":
                    if checker.is_user_on_event_go(user_id, event_id):
                        selector.user_decline_event(user_id, event_id)
                        info_logger.info(f'User with id: {user_id} decline event {event_id}.')
                    else:
                        return {"error": "User doesn't in event list"}, 400
                elif method == "register":
                    if not checker.is_user_on_event_want(user_id, event_id) \
                            and not checker.is_user_on_event_go(user_id, event_id) \
                            and not checker.is_user_banned(user_id):
                        if checker.is_event_opened_for_want(event_id):  # проверяю, что событие доступно для записи
                            # bottom color green
                            event_tbl.event_update_add_users_id_want(event_id, user_id)
                            info_logger.info(f"User with id: {user_id} registered on event with id: {event_id}.")
                        else:
                            # bottom color gray
                            return flask.Response({"error": "Event close for registration"}, status=503)
                    else:
                        # bottom color red
                        return flask.Response({"error": "Unpredictable situation"}, status=503)
                elif method == "cancel_register":
                    if checker.is_user_on_event_want(user_id, event_id) \
                            and not checker.is_user_on_event_go(user_id, event_id):
                        # проверяю, что юзер УЖЕ записался на мероприятие
                        if checker.is_event_opened_for_want(event_id):
                            # проверяю, что событие доступно для записи
                            # bottom color red
                            event_tbl.event_update_del_users_id_want(event_id, user_id)
                            info_logger.info(
                                f"User with id: {user_id} cancel registration on event with id: {event_id}")
                            return "OK", 200
                        else:
                            # bottom color gray
                            return flask.Response({"error": "Event close for registration"}, status=503)
                    else:
                        # bottom color green
                        return flask.Response({"error": "Unpredictable situation"}, status=503)
                else:
                    return flask.Response({"error": "Invalid method"}, status=503)
                return "", 200
            else:
                info_logger.error(f'Problems with data: user_id: {user_id}, event_id: {event_id}.')
                return flask.Response({"error": "Empty user id or/and event id!"}, status=504)
        elif request.method == "GET":
            return 201
        else:
            return flask.Response({"error": "Invalid CRUD"}, status=503)
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}, status=500)


# ---------------------------------NOTIFY-----------------------------------
@app.route('/api/notify/<method>', methods=["GET", "POST", "DELETE"])
def api_handle_notify(method):
    try:
        if request.method == "POST":
            if method == "add":
                notify_tbl.notify_add(request.json)
                info_logger.info(f"Notify {request.json['notify_header']} added")
            elif method == "update":
                # event_tbl.update(int(request.json['event_id']), request.json['data_to_update'])
                # info_logger.info(f"Event with id:{int(request.json['event_id'])} updated!")
                pass
            else:
                return flask.Response({"error": "Invalid method!"}, status=503)
        elif request.method == "GET":
            if method == "get" or method == "get_all":
                # events = event_tbl.get(int(request.json.get('event_id', 0)), all_events=method == "get_all")
                # return events, 200 if events else "Not events", 400
                pass
            elif method == "get_actual":
                pass
        elif request.method == "DELETE":
            if method == "delete":
                notify_tbl.notify_delete(int(request.json['notify_id']))
                info_logger.info(f"Notify with id: {int(request.json['notify_id'])} deleted.")
        else:
            return flask.Response({"error": "Invalid CRUD"}, status=503)
        return '', 200
    except Exception as E:
        error_logger.error(E, request.json)
        return flask.Response({"error": str(E)}, status=500)

# -------------------------NOTIFIES--------------------------------


@app.route('/api/notifies_send', methods=["POST"])
def notifies_send():
    """
    send notify to user by user_id
    :return notifies
    """
    user_id = {}
    notifies = []
    try:
        user_id = request.json['user_id']
        notifies_id = user_tbl.user_get(user_id)['notify_id']         # user's notifies

        for notify_id in notifies_id:
            notifies.append(notify_tbl.notify_get(notify_id))           # list with notifies json

        return notifies
    except Exception as E:
        error_logger.error(f"Problems with sending notifies to user {user_id}. Getting error: {E}")
        return str(E), 400


if __name__ == '__main__':
    app.run(host=config.HOST_ADDRESS, port=config.HOST_PORT)  # to see mistakes

# CRUD
# 1) Create POST
# 2) Read - GET
# 3) Update - Patch Put
# 4) Delete - DELETE
