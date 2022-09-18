from datetime import datetime, timedelta
from _config import config
from _config.logger_config import info_logger, error_logger
import re
from data_base.tbl_event import Event
from data_base.tbl_user import User

days_before_event = timedelta(config.TIME_TO_POST_EVENT)
days_finish_registration = timedelta(config.TIME_TO_END_TAKE_PART)
delay = config.TIME_TO_CHECK


class Checker:

    @staticmethod
    def is_correct_mail(mail_address: str) -> bool:
        regex_mail = re.compile(config.REGEX_MAIL)
        if re.fullmatch(regex_mail, mail_address):
            return True
        else:
            return False

    @staticmethod
    def is_correct_phone(phone: str) -> bool:
        # regex_phone = re.compile(config.REGEX_PHONE)
        regex_phone = re.compile(r"\d{10}")

        if re.match(regex_phone, phone):
            return True
        return False

    @staticmethod
    def is_event_active(event_id: int) -> bool:
        time_now = datetime.now()
        event_time_start = datetime.strptime(Event.get(event_id)['time_start'], "%m/%d/%Y, %H:%M:%S")

        if time_now < event_time_start and (event_time_start - time_now >= timedelta(config.TIME_TO_POST_EVENT)):
            return True
        else:
            return False

    @staticmethod
    def is_user_banned(user_id: int) -> bool:
        user_ban = User.get(user_id)['ban_date']

        if user_ban:
            if user_ban <= datetime.now():
                return False
            else:
                return True
        return False

    @staticmethod
    def is_event_opened_for_want(event_id: int) -> bool:
        """
        Check that event in period time for registration.\n
        :param event_id: int
        :return: bool
        """
        event = Event.get(event_id)
        time_now = datetime.now()
        if event:
            if (datetime.strptime(dict(event)['time_start'], "%m/%d/%Y, %H:%M:%S") - time_now < days_before_event) & \
                    (datetime.strptime(dict(event)['time_start'], "%m/%d/%Y, %H:%M:%S") - time_now > days_finish_registration):
                return True
            return False
        else:
            error_logger.error(f"Event with id:{event_id} does not exist!")
            return False

    @staticmethod
    def is_event_opened_for_go(event_id: int) -> bool:
        """
        If time before event allow ... stop!\n
        I need delete this function\n
        TODO : Delete me!\n
        :param event_id: int
        :return: bool
        """
        event = Event.get(event_id)
        # print(dict(events[0]))
        time_now = datetime.now()

        if (datetime.strptime(dict(event)['time_start'], "%m/%d/%Y, %H:%M:%S") - time_now < days_finish_registration) & \
                (datetime.strptime(dict(event)['time_start'], "%m/%d/%Y, %H:%M:%S") - time_now > timedelta(1)):
            return True
        return False

    @staticmethod
    def is_user_can_apply_event(user_id: int) -> bool:
        """
        Check user has time on apply. User must have got notify.\n
        Notify gives time on make choice.\n
        When time_select_finish more than time_now, user can make choice.\n
        :param user_id: int
        :return: bool
        """
        user_time_select_finish = User.get(user_id)['time_select_finish']
        time_now = datetime.now()
        if user_time_select_finish:
            if user_time_select_finish > time_now:
                return True
            else:
                return False
        return False

    @staticmethod
    def is_user_on_event_want(user_id: int, event_id: int) -> bool:
        event = Event.get(event_id)
        if event:
            users_want = dict(event)['users_id_want']
            if users_want:
                if user_id in users_want:
                    return True
            return False
        else:
            return False

    @staticmethod
    def is_user_on_event_go(user_id: int, event_id: int) -> bool:
        """
        Check user in event field 'users_id_go'.\n
        :param user_id: int
        :param event_id: int
        :return: bool
        """
        event = Event.get(event_id)
        if event:
            users_go = dict(event)['users_id_go']
            if user_id in users_go:
                return True
            return False
        else:
            return False

    @staticmethod
    def is_any_free_places_event(event_id: int) -> bool:
        event = Event.get(event_id)
        users_id_go = event['users_id_go']
        free_places = int(event['people_count']) - len(users_id_go)

        if free_places > 0:
            print("For event with ID:", event_id, "count of free places equal:", free_places)
            return True
        return False

