from datetime import datetime, timedelta
import config
import data.db_worker as db

DB = db.DataBaseEvents()


def send_notifies(user_id: int, event_id: int):

    time_now = datetime.now()

    notifies = DB.notify_get_for_event(event_id)
    for notify in notifies:
        notify_id = notify['notify_id']
        DB.user_update_add_notify(user_id, notify_id, time_now + timedelta(config.TIME_TO_ACCEPT))
