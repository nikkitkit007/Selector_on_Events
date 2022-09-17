import flask
from flask import request

from data_base.tbl_event import Event
from data_base.tbl_user import User
from typing import Tuple

from server.services.checker import Checker

from _config.logger_config import info_logger, error_logger


class EventHandler:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
            if Checker.is_user_can_apply_event(user_id):
                User.apply_event(user_id, event_id)
                info_logger.info(f'User with id: {user_id} applied event {event_id}.')
                return flask.make_response("User applied event"), 200
            else:
                info_logger.error(f'User with id: {user_id} can not apply event: {event_id}.')
                return flask.make_response("User can not apply event"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def decline_event() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: flask.Response("User applied event"), int(status_code)
        """
        try:
            event_id = int(request.json['event_id'])
            user_id = int(request.json['user_id'])

            if Checker.is_user_on_event_go(user_id, event_id):
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

    @staticmethod
    def registration(event_id: int, user_id: int, cancel: bool = False) -> Tuple[flask.Response, int]:
        try:
            if not event_id or not user_id:
                return flask.make_response({"API-error": "invalid user_id or/and event_id"}), 200
            if Checker.is_user_banned(user_id):
                return flask.make_response({"error": "You have been banned"}), 200
            if not Checker.is_event_opened_for_want(event_id):
                return flask.make_response({"error": "Event close for registration"}), 200
            if not (Checker.is_user_on_event_want(user_id, event_id) == cancel and
                    not Checker.is_user_on_event_go(user_id, event_id)):
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

    @staticmethod
    def event_registration() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: flask.Response("User registered on event"), int(status_code)
        """
        event_id = int(request.json.get('event_id'))
        user_id = int(request.json.get('user_id'))
        return EventHandler.registration(user_id, event_id)

    @staticmethod
    def event_cancel_registration():
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: flask.Response("User cancel registered event"), int(status_code)
        """
        event_id = int(request.json['event_id'])
        user_id = int(request.json['user_id'])
        return EventHandler.registration(user_id, event_id, cancel=True)
