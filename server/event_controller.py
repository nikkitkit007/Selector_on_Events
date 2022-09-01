import data.db_worker as db
import services.selector as selector
import services.checker as checker
from datetime import datetime, timedelta
import config
from time import sleep

DB = db.DataBaseEvents()
delay = config.TIME_TO_CHECK


def is_any_free_places_event(event_id: int) -> bool:
    event = DB.event_get(event_id)
    free_places = int(event['people_count']) - event['user_id_go'].count()

    if free_places > 0:
        selector.select_users_on_event(event_id)
    return True


if __name__ == "__main__":
    while True:
        events = DB.event_get_all()
        for event_i in events:
            if checker.is_event_active(int(event_i['event_id'])):
                is_any_free_places_event(int(event_i['event_id']))

        sleep(delay)    # 6 hours
