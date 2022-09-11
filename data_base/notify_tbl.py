import config
import sqlalchemy as sa
from .base import Base, session, engine
import logging
from logger_config import LOGGING_CONFIG
from datetime import datetime

logging.config.dictConfig(LOGGING_CONFIG)
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


class Notify(Base):
    __tablename__ = config.TBL_NOTIFIES
    __table_args__ = {'extend_existing': True}

    notify_id = sa.Column('notify_id', sa.Integer, primary_key=True)
    event_id = sa.Column('event_id', sa.Integer, nullable=False)
    time = sa.Column('time', sa.TIMESTAMP, default=sa.func.now())
    notify_header = sa.Column('notify_header', sa.String(127))
    notify_data = sa.Column('notify_data', sa.String)

    def __init__(self, notify_data):
        self.event_id = notify_data['event_id']
        self.time = notify_data['time']
        self.notify_header = notify_data['notify_header']
        self.notify_data = notify_data['notify_data']

    def __repr__(self):
        return f"<Notify (notify_header: {self.notify_header}," \
               f"notify_id: {self.notify_id}, " \
               f"event_id: {self.event_id})>"

    def get_dict(self):
        atts_dict = {"notify_id": self.notify_id,
                     "event_id": self.event_id,
                     "time": self.time,
                     "notify_header": self.notify_header,
                     "notify_data": self.notify_data}
        return atts_dict

    @staticmethod
    def add(notify_to_add: dict):
        with session(bind=engine) as local_session:
            notify_to_add['time'] = datetime.now()
            new_notify = Notify(notify_to_add)

            local_session.add(new_notify)
            local_session.commit()

    @staticmethod
    def get(notify_id: int = 0):
        with session(bind=engine) as local_session:
            notify = local_session.query(Notify).filter(Notify.notify_id == notify_id).first()

            if notify:
                return notify.get_dict()
        return {}

    @staticmethod
    def get_for_event(event_id: int = 0):
        with session(bind=engine) as local_session:
            notifies = local_session.query(Notify).filter(Notify.event_id == event_id).all()
            all_notifies = []

            for notify in notifies:
                all_notifies.append(notify.get_dict())

        return all_notifies

    @staticmethod
    def update(notify_id: int, notify_data_to_update: dict):
        with session(bind=engine) as local_session:
            notify_to_update = local_session.query(Notify).filter(Notify.notify_id == notify_id).first()
            if notify_to_update:
                notify_to_update.time = notify_data_to_update["time"]
                notify_to_update.notify_header = notify_data_to_update["notify_header"]
                notify_to_update.notify_data = notify_data_to_update["notify_data"]

                local_session.commit()
            else:
                info_logger.error(f'Notify {notify_id} does not exist!')

    @staticmethod
    def delete(notify_id: int):
        with session(bind=engine) as local_session:
            notify_to_delete = local_session.query(Notify).filter(Notify.notify_id == notify_id).first()
            if notify_to_delete:
                local_session.delete(notify_to_delete)
                local_session.commit()
            else:
                info_logger.error(f'Notify {notify_id} does not exist!')


if __name__ == "__main__":
    pass
