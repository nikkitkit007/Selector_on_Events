
from services.selector import Selector
from services.checker import Checker
import services.notify as notify
from datetime import datetime, timedelta
import config
from time import sleep

import data_base.tbl_event as event_tbl
import data_base.tbl_user as user_tbl
import data_base.tbl_notify as notify_tbl
import data_base.tbl_news as news_tbl


delay = config.TIME_TO_CHECK


def is_any_free_places_event(event_id: int) -> bool:
    event = event_tbl.Event.get(event_id)
    users_id_go = event['users_id_go']
    if users_id_go:
        free_places = int(event['people_count']) - users_id_go.count()
    else:
        free_places = int(event['people_count'])
    if free_places > 0:
        print("For event with ID:", event_id, "count of free places equal:", free_places)
        win_selection_users = Selector.select_users_on_event(event_id)
        if win_selection_users:
            for user in win_selection_users:
                notify.send_notifies(user, event_id)
    return True


if __name__ == "__main__":
    while True:
        events = event_tbl.Event.get_all()
        for event_i in events:
            if Checker.is_event_active(int(event_i['event_id'])):
                print("Active event is: ", int(event_i['event_id']))
                is_any_free_places_event(int(event_i['event_id']))

        sleep(delay)    # 6 hours
