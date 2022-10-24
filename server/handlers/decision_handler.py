import flask
from flask import request

from data_base.tbl_workers.event_worker import EventWorker
from data_base.tbl_workers import UserWorker
from typing import Tuple

from server.services.checker import Checker

from configurations.logger_config import info_logger, error_logger
from data_base.base import Base, engine, session


class DecisionHandler:
    # -------------------------EVENT_want/not_want------------------------------ TEST_PASSED
    @staticmethod
    def registration(event_id: int, user_id: int, cancel: bool = False) -> Tuple[flask.Response, int]:
        try:
            with session(bind=engine) as local_session:
                if not event_id or not user_id:
                    return flask.make_response({"API-error": "invalid user_id or/and event_id"}), 400
                if not UserWorker.get(user_id, local_session):
                    return flask.make_response({"error": "User does not exist"}), 400
                if not EventWorker.get(event_id=event_id, all_events=False, local_session=local_session):
                    return flask.make_response({"error": "Event does not exist"}), 400
                if Checker.is_user_banned(user_id, local_session):
                    return flask.make_response({"error": "User have been banned"}), 400
                if not Checker.is_event_opened_for_want(event_id, local_session):
                    return flask.make_response({"error": "Event close for registration"}), 400
                if not Checker.is_user_on_event_want(user_id, event_id, local_session) == cancel:
                    return flask.make_response({"error": "Not available response"}), 400

                if cancel:
                    EventWorker.update_del_users_id_want(event_id, user_id, local_session)
                    info_logger.info(f"User: {user_id} cancel registered on event: {event_id}")
                else:
                    EventWorker.update_add_users_id_want(event_id, user_id, local_session)
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
        return DecisionHandler.registration(event_id=event_id, user_id=user_id)

    @staticmethod
    def event_cancel_registration():
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: flask.Response("User cancel registered event"), int(status_code)
        """
        event_id = int(request.json['event_id'])
        user_id = int(request.json['user_id'])
        return DecisionHandler.registration(event_id=event_id, user_id=user_id, cancel=True)

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

            if not event_id or not user_id:
                return flask.make_response({"API-error": "invalid user_id or/and event_id"}), 400

            with session(bind=engine) as local_session:
                if not UserWorker.get(user_id=user_id, local_session=local_session):
                    return flask.make_response({"error": "User does not exist"}), 400
                if not EventWorker.get(local_session=local_session, event_id=event_id):
                    return flask.make_response({"error": "Event does not exist"}), 400

                if Checker.is_user_can_apply_event(user_id, local_session):
                    UserWorker.apply_event(user_id, event_id, local_session)
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
            with session(bind=engine) as local_session:

                if not event_id or not user_id:
                    return flask.make_response({"API-error": "invalid user_id or/and event_id"}), 400
                if not UserWorker.get(user_id=user_id, local_session=local_session):
                    return flask.make_response({"error": "User does not exist"}), 400
                if not EventWorker.get(event_id=event_id, local_session=local_session):
                    return flask.make_response({"error": "Event does not exist"}), 400

                if Checker.is_user_on_event_go(user_id, event_id, local_session):
                    UserWorker.decline_event(user_id, event_id, local_session)
                    info_logger.info(f'User with id: {user_id} decline event: {event_id}.')
                    return flask.make_response("User decline event"), 200
                else:
                    info_logger.error(f'User with id: {user_id} not in list event_go on event: {event_id}.')
                    return flask.make_response({"error": "User decline event"}), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
