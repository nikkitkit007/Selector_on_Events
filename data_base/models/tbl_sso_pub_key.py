import sqlalchemy as sa
import datetime

from data_base import DeclarativeBase, DefaultSettings


class SsoPubKey(DeclarativeBase):
    __tablename__ = DefaultSettings().TBL_SSO_PUB_KEY

    kid = sa.Column("kid", sa.TEXT, unique=True, primary_key=True)
    kty = sa.Column("kty", sa.TEXT)
    alg = sa.Column("alg", sa.TEXT)
    use = sa.Column("use", sa.TEXT)
    n = sa.Column("n", sa.TEXT)
    e = sa.Column("e", sa.TEXT)

    expires = sa.Column("expires", sa.DATETIME, default=datetime.datetime.now())
