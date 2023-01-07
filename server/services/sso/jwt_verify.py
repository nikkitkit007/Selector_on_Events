import jwt
from jose import jwk
from jose.utils import base64url_decode
import json
import binascii
import datetime

from data_base.base import engine, session

from server.services.sso.env_params import client_id
from server.services.sso.itmo_id import ItmoId
from data_base.tbl_workers.sso_pub_key_worker import SsoPubKeyWorker


def get_key(header):
    # берём хэдер, расшифровываем и смотрим есть ли в бд открытый ключ
    try:
        decoded_header_bytes = base64url_decode(header + '=' * (4 - len(header) % 4))
    except binascii.Error:
        return {'status': 'Invalid token'}

    try:
        decoded_header = json.loads(decoded_header_bytes.decode('utf-8'))
    except UnicodeDecodeError:
        return {'status': 'Invalid token'}

    kid = decoded_header['kid']

    with session(bind=engine) as local_session:
        db_key = SsoPubKeyWorker.get(kid=kid, local_session=local_session)

    if len(db_key) == 0 or datetime.datetime.now() - db_key["expires"] > datetime.timedelta(hours=10):
        with session(bind=engine) as local_session:
            SsoPubKeyWorker.delete(kid=kid, local_session=local_session)

        ItmoId.add_pub_keys()

        with session(bind=engine) as local_session:
            db_key = SsoPubKeyWorker.get(kid=kid, local_session=local_session)
    if len(db_key) == 0:
        return {'status': 'false'}
    return {'status': 'ok', 'rsa_key': db_key}


def verify(access_token: str):
    # расшифровать первую чаcть токена, сверить kid и затем осуществить проверку JWS с данным ключем (kid) если все
    # успешно отдать ок и пэйлоад

    if access_token.count('.') != 2:
        return {"status": "Invalid token"}

    message, encoded_sig = access_token.rsplit('.', 1)
    encoded_header = access_token.split('.', 1)[0]

    get_key_result = get_key(encoded_header)
    if get_key_result['status'] == 'false':
        return {"status": "Server does not have this token key id (kid) in the cache"}
    elif get_key_result['status'] == 'Invalid token':
        return {'status': 'Invalid token'}
    else:
        rsa_key = get_key_result['rsa_key']
        key = jwk.construct(rsa_key)

    decoded_sig = base64url_decode(encoded_sig + '=' * (4 - len(encoded_sig) % 4))
    res = key.verify(bytes(message, "UTF-8"), decoded_sig)
    if res:
        try:
            payload = jwt.decode(jwt=access_token, key=key.to_pem().decode(), algorithms='RS256', audience=client_id)  # with PEM key
            return {"status": "ok", "payload": payload}

        except jwt.exceptions.ExpiredSignatureError:
            return {"status": "Signature has expired"}
        except:
            return {"status": "Something goes wrong with verifying itmo id JWT in jwt_verify.py"}
    else:
        return {"status": "Not verified"}


