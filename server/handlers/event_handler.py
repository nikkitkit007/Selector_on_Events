import quart
from quart import request
import dateutil.parser

from typing import Tuple
from starlette import status

from configurations.config import LEN_ERR_MSG
from server import info_logger, error_logger

from data_base.base import get_session
from data_base.tbl_workers.event_worker import EventWorker
from server.services.sso.auth import check_auth


class EventHandler:
    @check_auth
    @staticmethod
    async def event_add() -> Tuple[quart.Response, int]:
        """
        request.json = {'event_name': str(127),
                        'time_start': str(timestamp),
                        'time_end': str(timestamp),
                        'description': str,
                        'url_pdf': str,
                        'people_count': int,
                        'coefficient': int,
                        'image': str(127)
        :return: quart.Response, int(status_code)
        """
        data = await request.json
        session = await get_session()
        data["time_start"] = dateutil.parser.isoparse(data.get("time_start"))
        data["time_end"] = dateutil.parser.isoparse(data.get("time_end"))

        try:
            async with session() as local_session:
                await EventWorker.add(data, local_session)
                await local_session.commit()

            info_logger.info(f"Event \"{data.get('event_name')}\" added!")
            return await quart.make_response("200"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def event_update() -> Tuple[quart.Response, int]:
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
            :return: quart.Response, status_code: int
            """
        session = await get_session()
        data = await request.json
        data["event_data_to_update"]["time_start"] = dateutil.parser.isoparse(
            data.get("event_data_to_update").get("time_start"))
        data["event_data_to_update"]["time_end"] = dateutil.parser.isoparse(
            data.get("event_data_to_update").get("time_end"))

        try:
            async with session() as local_session:
                await EventWorker.update(int(data['event_id']), data['event_data_to_update'], local_session)
                await local_session.commit()

            info_logger.info(f"Event with id:{int(data['event_id'])} updated!")
            return await quart.make_response("200"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def event_get() -> Tuple[quart.Response, int]:
        session = await get_session()
        data = request.args

        event_id = data.get("event_id", None)
        is_all = data.get("all", None)

        try:
            async with session() as local_session:
                events = await EventWorker.get(local_session=local_session, event_id=event_id, all_events=is_all)

                await local_session.commit()

            return (await quart.make_response({"Result": events}), status.HTTP_200_OK) if events \
                else (await quart.make_response({"Result": "Not events"}), status.HTTP_200_OK)

        except Exception as E:
            error_logger.error(E)
            return await quart.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), \
                   status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def event_delete() -> Tuple[quart.Response, int]:
        """
        request.json = {"event_id": int(event_id)}
        :return: quart.Response("Event deleted"), int(status_code)
        """
        session = await get_session()
        data = await request.json
        try:
            async with session() as local_session:
                await EventWorker.delete(int(data.get('event_id')), local_session)
                await local_session.commit()
            info_logger.info(f"Event with id: {int(data.get('event_id'))} deleted.")
            return await quart.make_response("Event deleted"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
