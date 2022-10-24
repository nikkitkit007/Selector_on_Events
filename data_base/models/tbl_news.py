import sqlalchemy as sa
from data_base.base import Base, session, settings

from server import info_logger


class News(Base):
    __tablename__ = settings.TBL_NEWS

    news_id = sa.Column('news_id', sa.Integer, primary_key=True)
    header = sa.Column('header', sa.String(127), nullable=False)
    data = sa.Column('data', sa.String)
    time = sa.Column('time', sa.TIMESTAMP)
