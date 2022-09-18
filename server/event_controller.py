from services.checker import Checker
import services.notify as notify
from _config import config
from time import sleep

from data_base.tbl_event import Event

# from datetime import datetime
from services.selector import Selector
from services.notify import Notify

delay = config.TIME_TO_CHECK


class EventController:

    @staticmethod
    def control_event():
        """
        if event.time_start <= time to choose first applicants.\n
        :return: sleep...
        """
        while True:
            events = Event.get(all_events=True)
            for event in events:
                event_id = int(event['event_id'])

                if Checker.is_event_active(event_id):
                    print("Active event is: ", event_id)
                    if Checker.is_any_free_places_event(event_id):
                        users_id_go = Selector.select_users_on_event(event_id)
                        print(users_id_go)
                        if users_id_go:
                            for user_id in users_id_go:
                                Notify.send_notifies(user_id, event_id)

            sleep(delay)  # 6 hours


if __name__ == "__main__":
    EventController.control_event()
    pass
