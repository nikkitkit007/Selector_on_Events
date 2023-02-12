import sqlalchemy as sa

from data_base import DeclarativeBase, DefaultSettings


class Notify(DeclarativeBase):
    __tablename__ = DefaultSettings().TBL_NOTIFIES

    notify_id = sa.Column('notify_id', sa.Integer, primary_key=True)
    event_id = sa.Column('event_id', sa.Integer, nullable=False)
    time = sa.Column('time', sa.TIMESTAMP, default=sa.func.now())
    notify_header = sa.Column('notify_header', sa.String(127))
    notify_data = sa.Column('notify_data', sa.String)
