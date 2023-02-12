import quart
from quart import request

import dateutil.parser
from typing import Tuple
from starlette import status

from configurations.config import LEN_ERR_MSG

from data_base.base import get_session
from data_base.tbl_workers import NewsWorker

from server import info_logger, error_logger
from server.services.sso.auth import check_auth


class NewsHandler:
    @check_auth
    @staticmethod
    async def news_add() -> Tuple[quart.Response, int]:
        """
        request.json = {'header': str(127),
                        'data': str,
                        'time': str(timestamp)}
        :return: quart.Response("News added"), int(status_code)
        """
        session = await get_session()
        data = await request.json
        data["time"] = dateutil.parser.isoparse(data.get("time"))
        try:
            async with session() as local_session:
                await NewsWorker.add(data, local_session)
                await local_session.commit()

            info_logger.info(f"News with id: {data.get('header')} added.")
            return await quart.make_response("News added"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def news_get() -> Tuple[quart.Response, int]:
        session = await get_session()
        data = request.args

        news_id = data.get('news_id', None)
        is_all = data.get('all', None)

        try:
            async with session() as local_session:
                news = await NewsWorker.get(local_session, news_id=news_id, all_news=is_all)
                await local_session.commit()

            return await quart.make_response({"news": news}), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def news_update() -> Tuple[quart.Response, int]:
        """
        request.json = {'news_id': news_id,
                        'news_data_to_update': {
                            'header': str(127),
                            'data': str,
                            'time': str(timestamp)}
                        }
        :return: quart.Response("News updated"), int(status_code)
        """
        session = await get_session()

        data = await request.json
        data["news_data_to_update"]["time"] = dateutil.parser.isoparse(data.get("news_data_to_update").get("time"))

        try:
            async with session() as local_session:
                await NewsWorker.update(int(data.get('news_id')), data.get('news_data_to_update'),
                                        local_session)
                await local_session.commit()

            info_logger.info(f"News with id:{int(data.get('news_id'))} updated!")
            return await quart.make_response("News updated"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def news_delete() -> Tuple[quart.Response, int]:
        """
        request.json = {"news_id": int(news_id)}
        :return: quart.Response("News deleted"), int(status_code)
        """
        session = await get_session()
        data = await request.json
        try:
            async with session() as local_session:
                await NewsWorker.delete(int(data.get('news_id')), local_session)
                await local_session.commit()
            info_logger.info(f"News with id: {int(data.get('news_id'))} deleted.")
            return await quart.make_response("News deleted"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
