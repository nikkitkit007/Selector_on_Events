from time import sleep

from services.selector import Selector
from services.notify import NotifySender
from services.checker import Checker

from data_base.base import engine, session
from data_base.tbl_workers.event_worker import EventWorker

from configurations import config


delay = config.TIME_TO_CHECK


class EventController:

    @staticmethod
    async def control_event():
        """
        if event.time_start <= time to choose first applicants
        :return: sleep...
        """
        while True:
            with session(bind=engine) as local_session:
                events = EventWorker.get(all_events=True, local_session=local_session)
                for event in events:
                    event_id = int(event['event_id'])

                    if Checker.is_event_active(event_id, local_session):
                        print("Active event is: ", event_id)
                        if Checker.is_any_free_places_event(event_id, local_session):
                            users_id_go = await Selector.select_users_on_event(event_id=event_id, local_session=local_session)
                            print(users_id_go)
                            if users_id_go:
                                for user_id in users_id_go:
                                    await NotifySender.send_notifies(user_id, event_id, local_session)

            sleep(10)  # 6 hours


if __name__ == "__main__":
    EventController.control_event()
