import quart
from quart import request
from typing import Tuple
from starlette import status

from configurations.config import LEN_ERR_MSG

from data_base.tbl_workers import UserWorker
from data_base.base import get_session

from server import info_logger, error_logger
from server.services.checker import Checker
from server.services.sso.auth import check_auth


class UserHandler:

    @check_auth
    @staticmethod
    async def user_add() -> Tuple[quart.Response, int]:
        """
        request.json = {'user_isu_number': 288888,
                        'user_name': str(127),
                        'user_surname': str(127),
                        'user_patronymic': str(127),
                        'phone': str(127),
                        'vk_link': str(127),
                        'mail': str(127),
                        'is_russian_citizenship': bool}
        :return: quart.Response("User added"), int(status_code)
        """
        session = await get_session()

        data = await request.json

        if not await Checker.is_correct_phone(data.get('phone')):
            error_logger.error("User add incorrect phone number")
            return await quart.make_response({"error": "Wrong phone"}), status.HTTP_400_BAD_REQUEST
        if not await Checker.is_correct_mail(data.get('mail')):
            error_logger.error("User add incorrect mail")
            return await quart.make_response({"error": "Wrong mail"}), status.HTTP_400_BAD_REQUEST
        try:
            async with session() as local_session:
                await UserWorker.add(data, local_session)
                await local_session.commit()
            info_logger.info(f"User {data.get('user_name')} added")
            return await quart.make_response("User added"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def user_get_profile() -> Tuple[quart.Response, int]:
        """
        request.json = {"user_isu_number": int(user_isu_number)}
        :return: quart.Response({"user": dict(user)}), int(status_code)
        """
        session = await get_session()
        try:
            async with session() as local_session:
                user = await UserWorker.get(int(request.args.get('user_isu_number')), local_session)
                await local_session.commit()
            return await quart.make_response({"user": user}), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def user_get_history():  # feature
        user_id = request.json

        try:
            pass
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def user_update() -> Tuple[quart.Response, int]:
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
        :return: quart.Response("User data updated"), int(status_code)
        """
        session = await get_session()

        data = await request.json
        try:
            async with session() as local_session:
                await UserWorker.update(int(data.get('user_isu_number')), data.get('user_data_to_update'),
                                        local_session)
                await local_session.commit()

            info_logger.info(f"User with isu:{int(data.get('user_isu_number'))} updated!")
            return await quart.make_response("User data updated"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_auth
    @staticmethod
    async def user_delete() -> Tuple[quart.Response, int]:
        """
        request.json = {"user_isu_number": int(user_isu_number)}
        :return: quart.Response("User deleted"), int(status_code)
        """
        session = await get_session()

        data = await request.json
        try:
            async with session() as local_session:
                await UserWorker.delete(int(data.get('user_isu_number')), local_session)
                await local_session.commit()

            info_logger.info(f"User with isu: {int(data.get('user_isu_number'))} deleted.")
            return await quart.make_response("OK"), status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return await quart.make_response(
                {"error": str(E)[:LEN_ERR_MSG] + " ..."}), status.HTTP_500_INTERNAL_SERVER_ERROR
