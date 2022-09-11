from datetime import datetime, timedelta
import config
import re
from data_base.event_tbl import Event
from data_base.user_tbl import User

# DB = db.DataBaseEvents()

days_before_event = timedelta(config.TIME_TO_POST_EVENT)
days_finish_registration = timedelta(config.TIME_TO_END_TAKE_PART)
delay = config.TIME_TO_CHECK


def is_correct_mail(mail_address: str) -> bool:
    regex_mail = re.compile(config.REGEX_MAIL)
    if re.fullmatch(regex_mail, mail_address):
        return True
    else:
        return False


def is_correct_phone(phone: str) -> bool:
    # regex_phone = re.compile(config.REGEX_PHONE)
    regex_phone = re.compile(r"\d{10}")

    if re.match(regex_phone, phone):
        return True
    return False


def is_event_active(event_id: int) -> bool:
    time_now = datetime.now()
    event_time_start = Event.get(event_id)['time_start']

    if time_now < event_time_start and (time_now > event_time_start - timedelta(config.TIME_TO_POST_EVENT)):
        return True
    else:
        return False


def is_user_banned(user_id: int) -> bool:
    user_ban = User.get(user_id)['ban_date']

    if user_ban:
        if user_ban <= datetime.now():
            return False
        else:
            return True                # user has ban
    return False


def is_event_opened_for_want(event_id: int) -> bool:  # return true if event open for 'want'
    event = Event.get(event_id)
    time_now = datetime.now()
    if event:
        if (dict(event)['time_start'] - time_now < days_before_event) & \
                (dict(event)['time_start'] - time_now > days_finish_registration):
            return True
        return False
    else:
        print('Event with id: ', event_id, ' does not exist!')
        return False


def is_event_opened_for_go(event_id: int) -> bool:
    """return true if event open for 'go'"""
    event = Event.get(event_id)
    # print(dict(events[0]))
    time_now = datetime.now()

    if (dict(event)['time_start'] - time_now < days_finish_registration) & \
            (dict(event)['time_start'] - time_now > timedelta(1)):
        return True
    return False


def is_user_can_apply_event(user_id: int) -> bool:
    # check user has time on apply
    user_time_select_finish = User.get(user_id)['time_select_finish']
    time_now = datetime.now()
    if user_time_select_finish:
        if user_time_select_finish > time_now:
            return True
        else:
            return False
    return False


# want, go or nothing
def is_user_on_event_want(user_id: int, event_id: int) -> bool:         # want
    event = Event.get(event_id)
    if event:
        users_want = dict(event)['users_id_want']
        if users_want:
            if user_id in users_want:
                return True
        return False
    else:
        print('Event with id: ', event_id, ' does not exist!')
        return False


def is_user_on_event_go(user_id: int, event_id: int) -> bool:
    event = Event.get(event_id)
    if event:
        users_go = dict(event)['users_id_go']
        if users_go:
            if user_id in users_go:
                return True
        return False
    else:
        print('Event with id: ', event_id, ' does not exist!')
        return False


