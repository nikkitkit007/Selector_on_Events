import flask
from flask import request

from starlette import status
from typing import Tuple

from server.services.checker import Checker
from server.services.sso.auth import check_auth

from configurations.logger_config import info_logger, error_logger
from configurations.config import LEN_ERR_MSG

from data_base.base import engine, session
from data_base.tbl_workers.event_worker import EventWorker
from data_base.tbl_workers import UserWorker


class DecisionHandler:
    # -------------------------EVENT_want/not_want------------------------------ TEST_PASSED
    @check_auth
    @staticmethod
    def registration(event_id: int, user_isu_number: int, cancel: bool = False) -> Tuple[flask.Response, int]:
        try:
            with session(bind=engine) as local_session:
                if not event_id or not user_isu_number:
                    return flask.make_response({"API-error": "invalid user_id or/and event_id"}), status.HTTP_400_BAD_REQUEST
                if not UserWorker.get(user_isu_number, local_session):
                    return flask.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not EventWorker.get(event_id=event_id, all_events=False, local_session=local_session):
                    return flask.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST
                if Checker.is_user_banned(user_isu_number, local_session):
                    return flask.make_response({"error": "User have been banned"}), status.HTTP_400_BAD_REQUEST
                if not Checker.is_event_opened_for_want(event_id, local_session):
                    return flask.make_response({"error": "Event close for registration"}), status.HTTP_400_BAD_REQUEST
                if not Checker.is_user_on_event_want(user_isu_number, event_id, local_session) == cancel:
                    return flask.make_response({"error": "Not available response"}), status.HTTP_400_BAD_REQUEST

                if cancel:
                    EventWorker.update_del_users_id_want(event_id, user_isu_number, local_session)
                    info_logger.info(f"User: {user_isu_number} cancel registered on event: {event_id}")
                else:
                    EventWorker.update_add_users_id_want(event_id, user_isu_number, local_session)
                    info_logger.info(f"User: {user_isu_number} registered on event: {event_id}")

            return flask.make_response("OK"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    def event_registration() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: flask.Response("User registered on event"), int(status_code)
        """
        event_id = int(request.json.get('event_id'))
        user_isu_number = int(request.json.get('user_isu_number'))
        return DecisionHandler.registration(event_id=event_id, user_isu_number=user_isu_number)

    @check_auth
    @staticmethod
    def event_cancel_registration():
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: flask.Response("User cancel registered event"), int(status_code)
        """
        event_id = int(request.json['event_id'])
        user_isu_number = int(request.json['user_isu_number'])
        return DecisionHandler.registration(event_id=event_id, user_isu_number=user_isu_number, cancel=True)

    # -------------------------EVENT_apply/decline------------------------------
    @check_auth
    @staticmethod
    def apply_event() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: flask.Response("User applied event"), int(status_code)
        """
        try:
            event_id = int(request.json.get('event_id'))
            user_isu_number = int(request.json.get('user_isu_number'))

            if not event_id or not user_isu_number:
                return flask.make_response({"API-error": "invalid user_id or/and event_id"}), \
                       status.HTTP_400_BAD_REQUEST

            with session(bind=engine) as local_session:
                if not UserWorker.get(user_isu_number=user_isu_number, local_session=local_session):
                    return flask.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not EventWorker.get(local_session=local_session, event_id=event_id):
                    return flask.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST

                if Checker.is_user_can_apply_event(user_isu_number, local_session):
                    UserWorker.apply_event(user_isu_number, event_id, local_session)
                    info_logger.info(f'User with id: {user_isu_number} applied event {event_id}.')
                    return flask.make_response("User applied event"), status.HTTP_200_OK
                else:
                    info_logger.error(f'User with id: {user_isu_number} can not apply event: {event_id}.')
                    return flask.make_response("User can not apply event"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    def decline_event() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: flask.Response("User applied event"), int(status_code)
        """
        try:
            event_id = int(request.json['event_id'])
            user_isu_number = int(request.json['user_isu_number'])
            with session(bind=engine) as local_session:

                if not event_id or not user_isu_number:
                    return flask.make_response({"API-error": "invalid user_id or/and event_id"}), status.HTTP_400_BAD_REQUEST
                if not UserWorker.get(user_isu_number=user_isu_number, local_session=local_session):
                    return flask.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not EventWorker.get(event_id=event_id, local_session=local_session):
                    return flask.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST

                if Checker.is_user_on_event_go(user_isu_number, event_id, local_session):
                    UserWorker.decline_event(user_isu_number, event_id, local_session)
                    info_logger.info(f'User with id: {user_isu_number} decline event: {event_id}.')
                    return flask.make_response("User decline event"), status.HTTP_200_OK
                else:
                    info_logger.error(f'User with id: {user_isu_number} not in list event_go on event: {event_id}.')
                    return flask.make_response({"error": "User decline event"}), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
