import quart
from quart import request

from typing import Tuple
from starlette import status

from configurations.config import LEN_ERR_MSG

from server import info_logger, error_logger
from server.services.sso.auth import check_auth

from data_base.base import get_session
from data_base.tbl_workers import NotifyWorker
from data_base.tbl_workers import UserWorker


class NotifyHandler:
    @check_auth
    @staticmethod
    async def notify_add() -> Tuple[quart.Response, int]:
        """
        request.json = {'event_id': int,
                        'notify_header': str(127),
                        'notify_data': str
        :return: quart.Response("Notify added"), int(status_code)
        """
        session = await get_session()
        data = await request.json
        try:
            async with session() as local_session:
                await NotifyWorker.add(data, local_session)
            info_logger.info(f"Notify for event {data.get('event_id')} added.")
            return await quart.make_response("Notify added"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def notify_send():
        # maybe I delete this API ! # TODO
        notifies = []
        session = await get_session()
        data = await request.json
        try:
            async with session() as local_session:
                user = await UserWorker.get(data.get('user_id'), local_session)
                await local_session.commit()

            notifies_id = user.get('notify_id')  # user's notifies

            for notify_id in notifies_id:
                notifies.append(await NotifyWorker.get(notify_id, local_session))  # list with notifies json

            return notifies
        except Exception as E:
            error_logger.error(E)
            return quart.make_response({"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def notify_delete() -> Tuple[quart.Response, int]:
        """
        request.json = {"notify_id": int(notify_id)}
        :return: quart.Response("Notify deleted"), int(status_code)
        """
        session = await get_session()
        data = await request.json
        try:
            async with session() as local_session:
                await NotifyWorker.delete(int(data.get('notify_id')), local_session)
                await local_session.commit()

            info_logger.info(f"Notify with id: {int(data.get('notify_id'))} deleted.")
            return await quart.make_response("Notify deleted"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
