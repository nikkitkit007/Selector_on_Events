
from data_base.tbl_workers import UserWorker
from data_base.models.tbl_notify import Notify
from data_base.base import session


class NotifySender:
    @staticmethod
    async def send_notifies(user_id: int, event_id: int, local_session: session):
        notifies = Notify.get_for_event(event_id, local_session)
        for notify in notifies:
            notify_id = notify['notify_id']
            UserWorker.update_add_notify(user_id, notify_id, local_session)
