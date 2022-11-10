
import flask
from flask import request

from data_base.tbl_workers import UserWorker
from typing import Tuple

from server.services.checker import Checker

from configurations.logger_config import info_logger, error_logger

from data_base.base import engine, session


class UserHandler:
    @staticmethod
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

        if not Checker.is_correct_phone(request.json['phone']):
            error_logger.error("User add incorrect phone number")
            return flask.make_response({"error": "Wrong phone"}), 400
        if not Checker.is_correct_mail(request.json['mail']):
            error_logger.error("User add incorrect mail")
            return flask.make_response({"error": "Wrong mail"}), 400
        try:
            with session(bind=engine) as local_session:
                UserWorker.add(request.json, local_session)
            info_logger.info(f'User {request.json["user_name"]} added')
            return flask.make_response("User added"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def user_get_profile() -> Tuple[flask.Response, int]:
        """
        request.json = {"user_id": int(user_id)}
        :return: flask.Response({"user": dict(user)}), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                user = UserWorker.get(int(request.args.get('user_isu_number')), local_session)
            return flask.make_response({"user": user}), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def user_get_history():         # feature
        user_id = request.json.args()

        try:
            pass
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def user_update() -> Tuple[flask.Response, int]:
        """
        request.json = {"user_isu_number": int(user_isu_number),
                        'user_data_to_update': {
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
            with session(bind=engine) as local_session:
                UserWorker.update(int(request.json.get('user_isu_number')), request.json.get('user_data_to_update'),
                                  local_session)
            info_logger.info(f"User with isu:{int(request.json['user_isu_number'])} updated!")
            return flask.make_response("User data updated"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def user_delete() -> Tuple[flask.Response, int]:
        """
        request.json = {"user_id": int(user_id)}
        :return: flask.Response("User deleted"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                UserWorker.delete(int(request.json.get('user_isu_number')), local_session)
            info_logger.info(f"User with isu: {int(request.json.get('user_isu_number'))} deleted.")
            return flask.make_response("OK"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
