
from _config import config
from datetime import datetime

from data_base.tbl_event import Event
from data_base.tbl_user import User
from selector import Selector


class EventController:

    @staticmethod
    def control_event():
        """
        if event.time_start <= time to first applicants.\n
        :return: sleep...
        """
        notify_id = 1               # i need get it below
        events_list = Event.get(all_events=True)
        for event in events_list:
            if datetime.strptime(event['time_start'], "%m/%d/%Y, %H:%M:%S") <= config.TIME_TO_FIRST_APPLICANTS:
                users_id_go = Selector.select_users_on_event(event['event_id'])
                for user in users_id_go:
                    User.update_add_notify(user_id=user, notify_id=notify_id)


if __name__ == "__main__":
    pass
