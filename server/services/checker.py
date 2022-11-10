from datetime import datetime, timedelta
import re

from configurations import config
from configurations.logger_config import error_logger
from data_base.tbl_workers.event_worker import EventWorker
from data_base.tbl_workers import UserWorker

from data_base.base import session


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
    def is_event_active(event_id: int, local_session: session) -> bool:
        time_now = datetime.now()
        event_time_start = datetime.strptime(EventWorker.get(local_session=local_session,
                                                             event_id=event_id)['time_start'], "%m/%d/%Y, %H:%M:%S")

        if time_now < event_time_start and (event_time_start - time_now >= timedelta(config.TIME_TO_POST_EVENT)):
            return True
        else:
            return False

    @staticmethod
    def is_user_banned(user_id: int, local_session: session) -> bool:
        # with session(bind=engine) as local_session:
        user_ban = UserWorker.get(user_id, local_session)['ban_date']

        if user_ban:
            if user_ban <= datetime.now():
                return False
            else:
                return True
        return False

    @staticmethod
    def is_event_opened_for_want(event_id: int, local_session: session) -> bool:
        """
        Check that event in period time for registration.\n
        :param local_session: session
        :param event_id: int
        :return: bool
        """

        event = EventWorker.get(local_session, event_id)
        time_now = datetime.now()
        event_time_start = datetime.strptime(dict(event)['time_start'], "%m/%d/%Y, %H:%M:%S")

        if event:
            if (event_time_start < time_now) &\
                    (time_now - event_time_start < days_finish_registration):
                return True
            return False
        else:
            error_logger.error(f"Event with id:{event_id} does not exist!")
            return False

    @staticmethod
    def is_user_can_apply_event(user_id: int, local_session: session) -> bool:
        """
        Check user has time on apply. User must have got notify.\n
        Notify gives time on make choice.\n
        When time_select_finish more than time_now, user can make choice.\n
        :param local_session: session
        :param user_id: int
        :return: bool
        """
        user_time_select_finish = UserWorker.get(user_id, local_session)['time_select_finish']
        time_now = datetime.now()
        if user_time_select_finish:
            if user_time_select_finish > time_now:
                return True
            else:
                return False
        return False

    @staticmethod
    def is_user_on_event_want(user_id: int, event_id: int, local_session: session) -> bool:
        event = EventWorker.get(local_session=local_session, event_id=event_id)

        if event:
            users_want = dict(event)['users_id_want']
            if users_want:
                if user_id in users_want:
                    return True
            return False
        else:
            return False

    @staticmethod
    def is_user_on_event_go(user_id: int, event_id: int, local_session: session) -> bool:
        """
        Check user in event field 'users_id_go'.\n
        :param local_session: session
        :param user_id: int
        :param event_id: int
        :return: bool
        """
        event = EventWorker.get(local_session=local_session, event_id=event_id)

        if event:
            users_go = dict(event)['users_id_go']
            if user_id in users_go:
                return True
            return False
        else:
            return False

    @staticmethod
    def is_any_free_places_event(event_id: int, local_session: session) -> bool:
        event = EventWorker.get(local_session=local_session, event_id=event_id, all_events=False)
        users_id_go = event['users_id_go']
        free_places = int(event['people_count']) - len(users_id_go)

        if free_places > 0:
            print("For event with ID:", event_id, "count of free places equal:", free_places)
            return True
        return False
