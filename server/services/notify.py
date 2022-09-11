from datetime import datetime, timedelta
import config
# import data_base.db_worker as db

import data_base.event_tbl as event_tbl
import data_base.user_tbl as user_tbl
import data_base.notify_tbl as notify_tbl
import data_base.news_tbl as news_tbl


def send_notifies(user_id: int, event_id: int):

    time_now = datetime.now()

    notifies = notify_tbl.notify_get_for_event(event_id)
    for notify in notifies:
        notify_id = notify['notify_id']
        user_tbl.user_update_add_notify(user_id, notify_id, time_now + timedelta(config.TIME_TO_ACCEPT))
