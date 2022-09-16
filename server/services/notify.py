from datetime import datetime, timedelta
import config
# import data_base.db_worker as db

import data_base.tbl_event as event_tbl
import data_base.tbl_user as user_tbl
import data_base.tbl_notify as notify_tbl
import data_base.tbl_news as news_tbl


def send_notifies(user_id: int, event_id: int):

    time_now = datetime.now()

    notifies = notify_tbl.Notify.get_for_event(event_id)
    for notify in notifies:
        notify_id = notify['notify_id']
        user_tbl.User.update_add_notify(user_id, notify_id, time_now + timedelta(config.TIME_TO_ACCEPT))
