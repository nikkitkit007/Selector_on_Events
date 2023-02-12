from sqlalchemy import select
from starlette import status
from data_base.base import get_session
from configurations.default import DefaultSettings
from server import error_logger


class HealthHandler:
    @staticmethod
    async def health_db():
        settings = DefaultSettings()
        db_uri = settings.database_uri

        success_resp = {"Result": "DB live"}
        no_success_resp = {"Result": "DB not connected"}
        try:
            local_session = await get_session()
            async with local_session() as session:
                query = select(1)
                await session.execute(query)
                await session.commit()

            return success_resp, status.HTTP_200_OK
        except Exception as E:
            error_logger.error(E)
            return no_success_resp, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    async def health_app():
        success_resp = {"Result": "App live"}

        return success_resp, status.HTTP_200_OK
