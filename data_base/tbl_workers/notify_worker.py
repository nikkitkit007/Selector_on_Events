from datetime import datetime

from data_base.base import session
from server import info_logger, error_logger
from data_base.models.tbl_notify import Notify


class NotifyWorker(Notify):
    def __init__(self, notify_data: dict):
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
    def add(notify_to_add: dict, local_session: session):
        notify_to_add['time'] = datetime.now()
        local_session.add(NotifyWorker(notify_to_add))

    @staticmethod
    def get(notify_id: int, local_session: session):
        notify = local_session.query(NotifyWorker).filter(NotifyWorker.notify_id == notify_id).first()

        if notify:
            return notify.get_dict()
        return {}

    @staticmethod
    def get_for_event(event_id: int, local_session: session):
        notifies = local_session.query(NotifyWorker).filter(NotifyWorker.event_id == event_id).all()
        all_notifies = []

        for notify in notifies:
            all_notifies.append(notify.get_dict())

        return all_notifies

    @staticmethod
    def update(notify_id: int, notify_data_to_update: dict, local_session: session):
        notify_to_update = local_session.query(NotifyWorker).filter(NotifyWorker.notify_id == notify_id).first()
        if notify_to_update:
            notify_to_update.time = notify_data_to_update["time"]
            notify_to_update.notify_header = notify_data_to_update["notify_header"]
            notify_to_update.notify_data = notify_data_to_update["notify_data"]

        else:
            info_logger.error(f'Notify {notify_id} does not exist!')

    @staticmethod
    def delete(notify_id: int, local_session: session):
        notify_to_delete = local_session.query(NotifyWorker).filter(NotifyWorker.notify_id == notify_id).first()
        if notify_to_delete:
            local_session.delete(notify_to_delete)
        else:
            info_logger.error(f'Notify {notify_id} does not exist!')
