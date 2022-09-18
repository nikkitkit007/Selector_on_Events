from datetime import datetime, timedelta
from _config import config
# import data_base.db_worker as db

from data_base.tbl_user import User
from data_base.tbl_notify import Notify


class NotifySender:
    @staticmethod
    def send_notifies(user_id: int, event_id: int):
        notifies = Notify.get_for_event(event_id)
        for notify in notifies:
            notify_id = notify['notify_id']
            User.update_add_notify(user_id, notify_id)
