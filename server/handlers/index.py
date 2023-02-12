import quart
from starlette import status

from server.services.sso.auth import check_auth


@check_auth
async def index():

    return await quart.make_response("Hi"), status.HTTP_200_OK
