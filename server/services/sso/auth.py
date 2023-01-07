from flask import request, url_for, redirect
from functools import wraps

from server.services.sso.jwt_verify import verify
from server.services.sso.env_params import jwt_verify
from server.services.sso.itmo_id import ItmoId


def check_auth(handle):
    @wraps(handle)
    def handle_work(*args, **kwargs):
        if jwt_verify:
            access_token = request.cookies.get("access_token")
            if not access_token:
                return ItmoId.get_code_auth()

            stat = verify(access_token)
            if stat["status"] == "ok":
                # payload = stat["payload"]
                pass
            else:
                return stat["status"], 404

        return handle(*args, **kwargs)

    return handle_work
