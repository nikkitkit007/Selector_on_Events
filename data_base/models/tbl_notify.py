import sqlalchemy as sa
from datetime import datetime

from data_base.base import Base, session, engine, settings

from server import info_logger


class Notify(Base):
    __tablename__ = settings.TBL_NOTIFIES

    notify_id = sa.Column('notify_id', sa.Integer, primary_key=True)
    event_id = sa.Column('event_id', sa.Integer, nullable=False)
    time = sa.Column('time', sa.TIMESTAMP, default=sa.func.now())
    notify_header = sa.Column('notify_header', sa.String(127))
    notify_data = sa.Column('notify_data', sa.String)
