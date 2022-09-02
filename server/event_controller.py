import data.db_worker as db
import services.selector as selector
import services.checker as checker
import services.notify as notify
from datetime import datetime, timedelta
import config
from time import sleep

DB = db.DataBaseEvents()
delay = config.TIME_TO_CHECK


def is_any_free_places_event(event_id: int) -> bool:
    event = DB.event_get(event_id)
    users_id_go = event['users_id_go']
    if users_id_go:
        free_places = int(event['people_count']) - users_id_go.count()
    else:
        free_places = int(event['people_count'])
    if free_places > 0:
        print("For event with ID:", event_id, "count of free places equal:", free_places)
        win_selection_users = selector.select_users_on_event(event_id)
        if win_selection_users:
            for user in win_selection_users:
                notify.send_notifies(user, event_id)
    return True


if __name__ == "__main__":
    while True:
        events = DB.event_get_all()
        for event_i in events:
            if checker.is_event_active(int(event_i['event_id'])):
                print("Active event is: ", int(event_i['event_id']))
                is_any_free_places_event(int(event_i['event_id']))

        sleep(delay)    # 6 hours
