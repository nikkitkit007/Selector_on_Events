from datetime import datetime, timedelta
from _config import config
# import data_base.db_worker as db

import data_base.tbl_user as user_tbl
import data_base.tbl_notify as notify_tbl


def send_notifies(user_id: int, event_id: int):
    notifies = notify_tbl.Notify.get_for_event(event_id)
    for notify in notifies:
        notify_id = notify['notify_id']
        user_tbl.User.update_add_notify(user_id, notify_id)
