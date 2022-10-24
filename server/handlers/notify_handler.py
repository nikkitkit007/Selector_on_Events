import flask
from flask import request

from data_base.tbl_workers import NotifyWorker
from data_base.tbl_workers import UserWorker
from typing import Tuple

from configurations.logger_config import info_logger, error_logger

from data_base.base import Base, engine, session


class NotifyHandler:
    @staticmethod
    def notify_add() -> Tuple[flask.Response, int]:
        """
        request.json = {'event_id': int,
                        'notify_header': str(127),
                        'notify_data': str
        :return: flask.Response("Notify added"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                NotifyWorker.add(request.json, local_session)
            info_logger.info(f"Notify for event {request.json['event_id']} added.")
            return flask.make_response("Notify added"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def notify_send():
        # maybe I delete this API ! # TODO
        notifies = []
        try:
            with session(bind=engine) as local_session:
                notifies_id = UserWorker.get(request.json.get('user_id'), local_session)['notify_id']  # user's notifies

                for notify_id in notifies_id:
                    notifies.append(NotifyWorker.get(notify_id, local_session))  # list with notifies json

            return notifies
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def notify_delete() -> Tuple[flask.Response, int]:
        """
        request.json = {"notify_id": int(notify_id)}
        :return: flask.Response("Notify deleted"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                NotifyWorker.delete(int(request.json.get('notify_id')), local_session)
            info_logger.info(f"Notify with id: {int(request.json.get('notify_id'))} deleted.")
            return flask.make_response("Notify deleted"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
