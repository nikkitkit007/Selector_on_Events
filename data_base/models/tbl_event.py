import sqlalchemy as sa

from data_base import DeclarativeBase, DefaultSettings


class Event(DeclarativeBase):
    __tablename__ = DefaultSettings().TBL_EVENTS

    event_id = sa.Column('event_id', sa.Integer, primary_key=True)
    event_name = sa.Column('event_name', sa.String(127), nullable=False)
    time_start = sa.Column('time_start', sa.TIMESTAMP, nullable=False)
    time_end = sa.Column('time_end', sa.TIMESTAMP, nullable=False)
    description = sa.Column('description', sa.String)
    url_pdf = sa.Column('url_pdf', sa.String(255))
    people_count = sa.Column('people_count', sa.Integer, nullable=False)
    coefficient = sa.Column('coefficient', sa.Integer, default=1)
    users_id_want = sa.Column('users_id_want', sa.ARRAY(sa.Integer),
                              default={})
    users_id_go = sa.Column('users_id_go', sa.ARRAY(sa.Integer),
                            default={})
    image = sa.Column('image', sa.String(127))
