import flask
from flask import request

from typing import Tuple

from configurations.logger_config import info_logger, error_logger

from data_base.base import engine, session
from data_base.tbl_workers.event_worker import EventWorker


class EventHandler:
    # ----------------------------------EVENT----------------------------------- TEST_PASSED
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
            with session(bind=engine) as local_session:
                EventWorker.update(int(request.json['event_id']), request.json['event_data_to_update'], local_session)
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
            with session(bind=engine) as local_session:
                events = EventWorker.get(local_session=local_session, event_id=int(request.args.get('event_id', 0))
                                         , all_events=False)
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
            with session(bind=engine) as local_session:
                events = EventWorker.get(local_session=local_session, event_id=0, all_events=True)
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
            with session(bind=engine) as local_session:
                EventWorker.delete(int(request.json.get('event_id')), local_session)
            info_logger.info(f"Event with id: {int(request.json.get('event_id'))} deleted.")
            return flask.make_response("Event deleted"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
