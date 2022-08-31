import data.db_worker as db
import selector
from datetime import datetime, timedelta
import config
from time import sleep

DB = db.DataBaseEvents()

days_before_event = timedelta(config.TIME_TO_POST_EVENT)
days_finish_registration = timedelta(config.TIME_TO_END_TAKE_PART)

delay = config.TIME_TO_CHECK


# def check_active_events_for_participation():
#     events = DB.event_get_all()
#     # print(dict(events[0]))
#     time_now = datetime.now()
#     for event in events:
#         # print('time before event:', dict(event)['time_start'] - time_now)
#         if (dict(event)['time_start'] - time_now < days_before_event) &\
#                 (dict(event)['time_start'] - time_now > days_finish_registration):
#             event_id = dict(event)['event_id']
#             users_id_want_on_event = dict(event)['users_id_want']
#             for user_id in users_id_want_on_event:
#                 DB.event_update_add_users_id_want(event_id, user_id)
#
#             # print(dict(event)['time_start'])
#     # print(events)

def is_event_active(event_id: int) -> bool:
    time_now = datetime.now()
    event_time_start = DB.event_get()['time_start']

    if time_now < event_time_start and (time_now > event_time_start - timedelta(config.TIME_TO_POST_EVENT)):
        return True
    else:
        return False


def is_user_banned(user_id: int) -> bool:
    user_ban = DB.user_get(user_id)['ban_date']

    if user_ban:
        if user_ban <= datetime.now():
            return False
        else:
            return True                # user has ban
    return False


def is_event_opened_for_want(event_id: int) -> bool:  # return true if event open for 'want'
    event = DB.event_get(event_id)
    # print(dict(events[0]))
    time_now = datetime.now()

    if (dict(event)['time_start'] - time_now < days_before_event) & \
            (dict(event)['time_start'] - time_now > days_finish_registration):
        return True
    return False


def is_event_opened_for_go(event_id: int) -> bool:
    """return true if event open for 'go'"""
    event = DB.event_get(event_id)
    # print(dict(events[0]))
    time_now = datetime.now()

    if (dict(event)['time_start'] - time_now < days_finish_registration) & \
            (dict(event)['time_start'] - time_now > timedelta(1)):
        return True
    return False


def is_user_can_apply_event(user_id: int) -> bool:
    # check user has time on apply
    user_time_select_finish = DB.user_get(user_id)['time_select_finish']
    time_now = datetime.now()
    if user_time_select_finish:
        if user_time_select_finish > time_now:
            return False
        else:
            return True
    return False


# want, go or nothing
def is_user_on_event_want(user_id: int, event_id: int) -> bool:         # want
    event = DB.event_get(event_id)
    users_want = dict(event)['users_id_want']
    if user_id in users_want:
        return True
    return False


def is_user_on_event_go(user_id: int, event_id: int) -> bool:
    event = DB.event_get(event_id)
    users_go = dict(event)['users_id_go']
    if user_id in users_go:
        return True
    return False


def send_notifies(user_id: int, event_id: int):

    time_now = datetime.now()

    notifies = DB.notify_get_for_event(event_id)
    for notify in notifies:
        notify_id = notify['notify_id']
        DB.user_update_add_notify(user_id, notify_id, time_now + timedelta(config.TIME_TO_ACCEPT))


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
            if is_event_active(int(event_i['event_id'])):
                is_any_free_places_event(int(event_i['event_id']))

        # # ---
        # event_id_test = 4
        #
        # users_id_selected_on_event = selector.select_users_on_event(event_id_test)
        # # list with selected users
        #
        # for user_id_selected in users_id_selected_on_event:
        #     send_notifies(event_id_test, user_id_selected)
        # # ---

        # if check_user_on_event(1, 4):
        #     print('lol')

        # is_user_banned(2)

        # if check_event_actuality(4):
        #     print("lol")
        sleep(delay)  # 6 hours
