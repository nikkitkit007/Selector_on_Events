from sqlalchemy import select, insert, and_, update, delete

from data_base.base import get_session
from server import info_logger, error_logger
from data_base.models.tbl_sso_pub_key import SsoPubKey


class SsoPubKeyWorker(SsoPubKey):
    # def __init__(self, sso_pub_key_data: dict):
    #     self.kid = sso_pub_key_data["kid"]
    #     self.kty = sso_pub_key_data["kty"]
    #     self.alg = sso_pub_key_data["alg"]
    #     self.use = sso_pub_key_data["use"]
    #     self.n = sso_pub_key_data["n"]
    #     self.e = sso_pub_key_data["e"]

    @staticmethod
    def get_dict(sso_pub_key):
        atts_dict = {"kid": sso_pub_key.kid,
                     "kty": sso_pub_key.kty,
                     "alg": sso_pub_key.alg,
                     "use": sso_pub_key.use,
                     "n": sso_pub_key.n,
                     "e": sso_pub_key.e,
                     "expires": sso_pub_key.expires
                     }
        return atts_dict

    @staticmethod
    async def add(sso_pub_key_to_add: dict, local_session: get_session):
        sso_pub_key = {"kid": sso_pub_key_to_add["kid"],
                       "kty": sso_pub_key_to_add["kty"],
                       "alg": sso_pub_key_to_add["alg"],
                       "use": sso_pub_key_to_add["use"],
                       "n": sso_pub_key_to_add["n"],
                       "e": sso_pub_key_to_add["e"]}
        insert_query = insert(SsoPubKey).values(sso_pub_key)
        await local_session.execute(insert_query)

    @staticmethod
    async def get(kid: str, local_session: get_session):
        query = select(SsoPubKey).where(SsoPubKey.kid == kid).limit(1)
        sso_pub_key = await local_session.execute(query)
        sso_pub_key = sso_pub_key.scalars().first()
        if sso_pub_key:
            return SsoPubKeyWorker.get_dict(sso_pub_key)
        return {}

    @staticmethod
    async def delete(kid: int, local_session: get_session):
        query = delete(SsoPubKey).where(SsoPubKey.kid == kid)
        await local_session.execute(query)

        # sso_pub_key_to_delete = await local_session.query(SsoPubKeyWorker).filter(SsoPubKeyWorker.kid == kid).first()
        # if sso_pub_key_to_delete:
        #     await local_session.delete(sso_pub_key_to_delete)
        # else:
        #     info_logger.error(f'sso_pub_key with kid: {kid} does not exist!')
