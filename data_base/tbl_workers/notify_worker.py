from sqlalchemy import select, insert, and_, update, delete
from datetime import datetime

from data_base.base import get_session
from server import info_logger, error_logger
from data_base.models.tbl_notify import Notify


class NotifyWorker(Notify):

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
    async def add(notify_to_add: dict, local_session: get_session):
        notify_to_add['time'] = datetime.now()

        query = insert(Notify).values(notify_to_add)
        await local_session.execute(query)

    @staticmethod
    async def get(notify_id: int, local_session: get_session):
        query = select(Notify).where(Notify.notify_id == notify_id).limit(1)
        notify = await local_session.execute(query)
        notify = notify.scalars().first()

        if notify:
            return Notify.get_dict(notify)
        else:
            return {}

    @staticmethod
    async def get_for_event(event_id: int, local_session: get_session):
        query = select(Notify).where(Notify.event_id == event_id)
        notifies = await local_session.execute(query)
        notifies = notifies.scalars().all

        all_notifies = []

        for notify in notifies:
            all_notifies.append(Notify.get_dict(notify))

        return all_notifies

    @staticmethod
    async def update(notify_id: int, notify_data_to_update: dict, local_session: get_session):
        query = update(Notify).where(Notify.notify_id == notify_id).values(notify_data_to_update)
        await local_session.execute(query)
        # notify_to_update = await local_session.query(NotifyWorker).filter(NotifyWorker.notify_id == notify_id).first()
        # if notify_to_update:
        #     notify_to_update.time = notify_data_to_update["time"]
        #     notify_to_update.notify_header = notify_data_to_update["notify_header"]
        #     notify_to_update.notify_data = notify_data_to_update["notify_data"]
        #
        # else:
        #     info_logger.error(f'Notify {notify_id} does not exist!')

    @staticmethod
    async def delete(notify_id: int, local_session: get_session):
        query = delete(Notify).where(Notify.notify_id == notify_id)
        await local_session.execute(query)
