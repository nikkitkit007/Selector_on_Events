import os
import config
from sqlalchemy.schema import CreateSchema
from .base import Base, engine

#   O
# \/|\| this import need to create tables
#   |
#  / \
#  | |
from .event_tbl import Event
from .user_tbl import User
from .notify_tbl import Notify
from .news_tbl import News


def create_all_tables():
    Base.metadata.create_all(engine)


def create_schema():
    engine.execute(CreateSchema(config.SCHEMA_NAME))


def create_db():
    if not engine.dialect.has_schema(engine, config.SCHEMA_NAME):
        create_schema()
    create_all_tables()
    # print(dir(Base))
    pass


if __name__ == "__main__":
    create_db()
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    # time_start = '09-14-2022 00:00:00'
    # time_end = '09-15-2022 00:00:10'
    #
    # test_event = {'event_name': '2jnfs2222222',
    #               'time_start': time_start,
    #               'time_end': time_end,
    #               'description': 'Simple test',
    #               'url_pdf': 'http://lol',
    #               'people_count': 10,
    #               'coefficient': 50,
    #               'image': '/images/lol/lal.jpeg'}

    # event.event_add(test_event)

    # event_got = event.event_get(3)
    # print(event_got)

    # data_to_upd = {'event_name': 'event_name_update',
    #                'time_start': '09-08-2022 00:00:00',
    #                'time_end': '09-10-2022 00:00:10',
    #                'description': 'Simple test was update',
    #                'url_pdf': 'http://lol',
    #                'people_count': 10,
    #                'coefficient': 50,
    #                'image': '/images/lol/lal.jpeg'}

    # event_tbl.event_update(3, data_to_upd)

    # event_tbl.event_delete(22)

    # event_tbl.event_update_add_users_id_go(13, 13)
    # event_tbl.event_update_add_users_id_want(1, 12)
    # event_tbl.event_update_del_users_id_want(12, 12)
