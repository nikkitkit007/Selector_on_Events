import flask
from flask import request

from data_base.tbl_notify import Notify
from data_base.tbl_user import User
from typing import Tuple

from _config.logger_config import info_logger, error_logger


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
            Notify.add(request.json)
            info_logger.info(f"Notify with id: {int(request.json.get('notify_id'))} added.")
            return flask.make_response("Notify added"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
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

    @staticmethod
    def notify_delete() -> Tuple[flask.Response, int]:
        """
        request.json = {"notify_id": int(notify_id)}
        :return: flask.Response("Notify deleted"), int(status_code)
        """
        try:
            Notify.delete(int(request.json.get('notify_id')))
            info_logger.info(f"Notify with id: {int(request.json.get('notify_id'))} deleted.")
            return flask.make_response("Notify deleted"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
