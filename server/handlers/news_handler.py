import flask
from flask import request

from data_base.tbl_news import News
from typing import Tuple

from _config.logger_config import info_logger, error_logger

from data_base.base import Base, engine, session


class NewsHandler:
    @staticmethod
    def news_add() -> Tuple[flask.Response, int]:
        """
        request.json = {'header': str(127),
                        'data': str,
                        'time': str(timestamp)}
        :return: flask.Response("News added"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                News.add(request.json, local_session)
            info_logger.info(f"News with id: {request.json.get('header')} added.")
            return flask.make_response("News added"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def news_get() -> Tuple[flask.Response, int]:
        """
        request.json = {"news_id": int(news_id)}
        :return: flask.Response({"news": dict(news)}), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                news = News.get(local_session, news_id=(request.json.get('news_id', 0)), all_news=False)
            return (flask.make_response({"news": news}), 200) if news \
                else (flask.make_response({"error": "Not news"}), 400)
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def news_get_all() -> Tuple[flask.Response, int]:
        """
        request.json = {}
        :return: flask.Response({"news": list(dict(news))}), status_code: int
        """
        try:
            with session(bind=engine) as local_session:
                news = News.get(local_session, news_id=0, all_news=True)
            return (flask.make_response({'news': news}), 200) if news \
                else (flask.make_response({"error": "Not news"}), 400)
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
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
            with session(bind=engine) as local_session:
                News.update(int(request.json.get('news_id')), request.json.get('news_data_to_update'), local_session)
            info_logger.info(f"News with id:{int(request.json['news_id'])} updated!")
            return flask.make_response("News updated"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500

    @staticmethod
    def news_delete() -> Tuple[flask.Response, int]:
        """
        request.json = {"news_id": int(news_id)}
        :return: flask.Response("News deleted"), int(status_code)
        """
        try:
            with session(bind=engine) as local_session:
                News.delete(int(request.json.get('news_id')), local_session)
            info_logger.info(f"News with id: {int(request.json.get('news_id'))} deleted.")
            return flask.make_response("News deleted"), 200
        except Exception as E:
            error_logger.error(E, request.json)
            return flask.make_response({"error": str(E)}), 500
