import quart
from quart import request

from starlette import status
from typing import Tuple

from server.services.checker import Checker
from server.services.sso.auth import check_auth

from configurations.logger_config import info_logger, error_logger
from configurations.config import LEN_ERR_MSG

from data_base.base import get_session
from data_base.tbl_workers.event_worker import EventWorker
from data_base.tbl_workers import UserWorker


class DecisionHandler:
    # -------------------------EVENT_want/not_want------------------------------ TEST_PASSED
    @check_auth
    @staticmethod
    async def registration(event_id: int, user_isu_number: int, cancel: bool = False) -> Tuple[quart.Response, int]:
        session = await get_session()

        try:
            async with session() as local_session:
                if not event_id or not user_isu_number:
                    return await quart.make_response(
                        {"API-error": "invalid user_id or/and event_id"}), status.HTTP_400_BAD_REQUEST
                if not await UserWorker.get(user_isu_number=user_isu_number, local_session=local_session):
                    info_logger.error(f"User: {user_isu_number} does not exist")
                    return await quart.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not await EventWorker.get(event_id=event_id, all_events=False, local_session=local_session):
                    info_logger.error(f"Event: {event_id} does not exist")
                    return await quart.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST
                if await Checker.is_user_banned(user_isu_number=user_isu_number, local_session=local_session):
                    info_logger.error(f"User: {user_isu_number} have been banned")
                    return await quart.make_response({"error": "User have been banned"}), status.HTTP_400_BAD_REQUEST
                if not await Checker.is_event_opened_for_want(event_id=event_id, local_session=local_session):
                    info_logger.error(f"Event: {event_id} close for registration")
                    return await quart.make_response(
                        {"error": "Event close for registration"}), status.HTTP_400_BAD_REQUEST
                if not await Checker.is_user_on_event_want(user_isu_number, event_id, local_session) == cancel:
                    info_logger.error(f"User: {user_isu_number} made not available request")
                    return await quart.make_response(
                        {"error": "Not available request for this user"}), status.HTTP_400_BAD_REQUEST

                if cancel:
                    await EventWorker.update_del_users_id_want(event_id, user_isu_number, local_session)
                    info_logger.info(f"User: {user_isu_number} cancel registered on event: {event_id}")
                else:
                    await EventWorker.update_add_users_id_want(event_id, user_isu_number, local_session)
                    info_logger.info(f"User: {user_isu_number} registered on event: {event_id}")

                await local_session.commit()

            return await quart.make_response("OK"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def event_registration() -> Tuple[quart.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: quart.Response("User registered on event"), int(status_code)
        """
        data = await request.json

        event_id = int(data.get('event_id'))
        user_isu_number = int(data.get('user_isu_number'))
        return await DecisionHandler.registration(event_id=event_id, user_isu_number=user_isu_number)

    @check_auth
    @staticmethod
    async def event_cancel_registration():
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: quart.Response("User cancel registered event"), int(status_code)
        """
        data = await request.json

        event_id = int(data['event_id'])
        user_isu_number = int(data['user_isu_number'])
        return await DecisionHandler.registration(event_id=event_id, user_isu_number=user_isu_number, cancel=True)

    # -------------------------EVENT_apply/decline------------------------------
    @check_auth
    @staticmethod
    async def apply_event() -> Tuple[quart.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_isu_number": int(user_isu_number)}
        :return: quart.Response("User applied event"), int(status_code)
        """
        data = await request.json
        session = await get_session()

        try:
            event_id = int(data.get('event_id'))
            user_isu_number = int(data.get('user_isu_number'))

            if not event_id or not user_isu_number:
                return await quart.make_response({"API-error": "invalid user_id or/and event_id"}), \
                       status.HTTP_400_BAD_REQUEST

            async with session() as local_session:
                if not await UserWorker.get(user_isu_number=user_isu_number, local_session=local_session):
                    info_logger.error(f"User: {user_isu_number} does not exist")
                    return await quart.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not await EventWorker.get(event_id=event_id, local_session=local_session):
                    info_logger.error(f"Event: {event_id} does not exist")
                    return await quart.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST

                if await Checker.is_user_can_apply_event(user_isu_number, local_session):
                    await UserWorker.apply_event(user_isu_number, event_id, local_session)
                    await local_session.commit()

                    info_logger.info(f'User with id: {user_isu_number} applied event {event_id}.')
                    return await quart.make_response("User applied event"), status.HTTP_200_OK
                else:
                    info_logger.error(f'User with id: {user_isu_number} can not apply event: {event_id}.')
                    return await quart.make_response("User can not apply event"), status.HTTP_200_OK

        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def decline_event() -> Tuple[quart.Response, int]:
        """
        request.json = {"event_id": int(event_id),
                        "user_id": int(user_id)}
        :return: quart.Response("User applied event"), int(status_code)
        """
        session = await get_session()
        data = await request.json

        try:
            event_id = int(data['event_id'])
            user_isu_number = int(data['user_isu_number'])
            async with session() as local_session:

                if not event_id or not user_isu_number:
                    return await quart.make_response(
                        {"API-error": "invalid user_id or/and event_id"}), status.HTTP_400_BAD_REQUEST
                if not await UserWorker.get(user_isu_number=user_isu_number, local_session=local_session):
                    info_logger.error(f"User: {user_isu_number} does not exist")
                    return await quart.make_response({"error": "User does not exist"}), status.HTTP_400_BAD_REQUEST
                if not await EventWorker.get(event_id=event_id, local_session=local_session):
                    info_logger.error(f"Event: {event_id} does not exist")
                    return await quart.make_response({"error": "Event does not exist"}), status.HTTP_400_BAD_REQUEST

                if await Checker.is_user_on_event_go(user_isu_number, event_id, local_session):
                    await UserWorker.decline_event(user_isu_number, event_id, local_session)
                    await local_session.commit()

                    info_logger.info(f'User with id: {user_isu_number} decline event: {event_id}.')
                    return await quart.make_response("User decline event"), status.HTTP_200_OK
                else:
                    info_logger.error(f'User with id: {user_isu_number} not in list event_go on event: {event_id}.')
                    return await quart.make_response({"error": "User decline event"}), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
