import flask
from flask import request

from typing import Tuple
from starlette import status

from configurations.config import LEN_ERR_MSG
from server import info_logger, error_logger

from data_base.base import engine, session
from data_base.tbl_workers.event_worker import EventWorker
from server.services.sso.auth import check_auth


class EventHandler:
    @check_auth
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
            with session(bind=engine) as local_session:
                EventWorker.add(request.json, local_session)
            info_logger.info(f"Event \"{request.json['event_name']}\" added!")
            return flask.make_response("200"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
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
            with session(bind=engine) as local_session:
                EventWorker.update(int(request.json['event_id']), request.json['event_data_to_update'], local_session)
            info_logger.info(f"Event with id:{int(request.json['event_id'])} updated!")
            return flask.make_response("200"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    def event_get() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id)}
        :return: flask.Response({"event": event: dict}), status_code: int
        """
        try:
            with session(bind=engine) as local_session:
                events = EventWorker.get(local_session=local_session, event_id=int(request.args.get('event_id', 0))
                                         , all_events=False)
            return (flask.make_response({"event": events}), status.HTTP_200_OK) if events \
                else (flask.make_response({"error": "Not events"}), status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    def event_get_all() -> Tuple[flask.Response, int]:
        """
        request.json = {}
        :return: flask.Response({"events": list(dict(events))}), status_code: int
        """

        try:
            with session(bind=engine) as local_session:
                events = EventWorker.get(local_session=local_session, all_events=True)
            return (flask.make_response({'events': events}), status.HTTP_200_OK) if events \
                else (flask.make_response({"info": "Not events"}), status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    def event_delete() -> Tuple[flask.Response, int]:
        """
        request.json = {"event_id": int(event_id)}
        :return: flask.Response("Event deleted"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                EventWorker.delete(int(request.json.get('event_id')), local_session)
            info_logger.info(f"Event with id: {int(request.json.get('event_id'))} deleted.")
            return flask.make_response("Event deleted"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return flask.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
