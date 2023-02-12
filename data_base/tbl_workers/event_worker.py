from sqlalchemy import select, insert, and_, update, delete

from data_base.base import get_session
from server import info_logger, error_logger
from data_base.models.tbl_event import Event


class EventWorker(Event):
    # def __init__(self, event_data):
    #     self.event_name = event_data['event_name']
    #     self.time_start = event_data['time_start']
    #     self.time_end = event_data['time_end']
    #     self.description = event_data['description']
    #     self.url_pdf = event_data['url_pdf']
    #     self.people_count = event_data['people_count']
    #     self.coefficient = event_data['coefficient']
    #     self.image = event_data['image']
    #     self.users_id_want = []
    #     self.users_id_go = []

    def __repr__(self):
        return f"<Event(event_name: {self.event_name})>"

    def get_dict(self):
        atts_dict = {"event_id": self.event_id,
                     "event_name": self.event_name,
                     "time_start": self.time_start.strftime("%m/%d/%Y, %H:%M:%S"),
                     "time_end": self.time_end.strftime("%m/%d/%Y, %H:%M:%S"),
                     "description": self.description,
                     "url_pdf": self.url_pdf,
                     "people_count": self.people_count,
                     "coefficient": self.coefficient,
                     "users_id_want": self.users_id_want,
                     "users_id_go": self.users_id_go,
                     "image": self.image}
        return atts_dict

    @staticmethod
    async def add(event_to_add: dict, local_session):
        query = insert(Event).values(event_to_add)
        await local_session.execute(query)

    @staticmethod
    async def get(local_session: get_session, event_id: int = None, all_events: bool = None):
        if all_events:
            query = select(Event).where()
            events = await local_session.execute(query)
            events = events.scalars().all()

            if events:
                all_news_list = []
                for event in events:
                    all_news_list.append(EventWorker.get_dict(event))
                return all_news_list
            else:
                return {}
        else:
            query = select(Event).where(Event.event_id == int(event_id)).limit(1)
            event = await local_session.execute(query)
            event = event.scalars().first()

            if event:
                return EventWorker.get_dict(event)
            else:
                return {}

    @staticmethod
    async def update(event_id: int, event_data_to_update: dict, local_session: get_session):
        query = update(Event).where(Event.event_id == event_id).values(event_data_to_update)

        await local_session.execute(query)
        # event_to_update = await local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        # if event_to_update:
        #     event_to_update.event_name = event_data_to_update["event_name"]
        #     event_to_update.time_start = event_data_to_update["time_start"]
        #     event_to_update.time_end = event_data_to_update["time_end"]
        #     event_to_update.description = event_data_to_update["description"]
        #     event_to_update.url_pdf = event_data_to_update["url_pdf"]
        #     event_to_update.people_count = int(event_data_to_update["people_count"])
        #     event_to_update.coefficient = int(event_data_to_update["coefficient"])
        #     event_to_update.image = event_data_to_update['image']
        #
        # else:
        #     info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    async def delete(event_id: int, local_session: get_session):
        query = delete(Event).where(Event.event_id == event_id)
        await local_session.execute(query)

    @staticmethod
    async def update_add_users_id_want(event_id: int, user_id_want: int, local_session: get_session):
        event_data_to_update = {"users_id_want": Event.users_id_want + [user_id_want]}
        query = update(Event).where(Event.event_id == event_id).values(event_data_to_update)

        await local_session.execute(query)

    @staticmethod
    async def update_add_users_id_go(event_id: int, user_id_go: int, local_session: get_session):
        event_data_to_update = {"users_id_go": Event.users_id_go + [user_id_go]}
        query = update(Event).where(Event.event_id == event_id).values(event_data_to_update)

        await local_session.execute(query)

    @staticmethod
    async def update_del_users_id_want(event_id: int, user_id_del: int, local_session: get_session):
        event = await EventWorker.get(local_session=local_session, event_id=event_id, all_events=False)
        users_id_want = event.get("users_id_want")
        users_id_want.remove(user_id_del)

        event_data_to_update = {"users_id_want": users_id_want}
        query = update(Event).where(Event.event_id == event_id).values(event_data_to_update)

        await local_session.execute(query)
        # event_to_update = await local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        # if event_to_update:
        #     cur_users_id_want_list = list(event_to_update.users_id_want)
        #
        #     try:
        #         cur_users_id_want_list.remove(user_id_del)
        #     except Exception as E:
        #         error_logger.error(E)
        #         info_logger.error(f'User {user_id_del} does not exist in want_list on event {event_id}!')
        #
        #     if cur_users_id_want_list:
        #         new_users_id_want_list = set(cur_users_id_want_list)
        #     else:
        #         new_users_id_want_list = []
        #
        #     event_to_update.users_id_want = new_users_id_want_list
        # else:
        #     info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    async def update_del_users_id_go(event_id: int, user_id_del: int, local_session: get_session):
        event = await EventWorker.get(local_session=local_session, event_id=event_id, all_events=False)
        users_id_go = event.get("users_id_go")
        users_id_go.remove(user_id_del)

        event_data_to_update = {"users_id_go": users_id_go}
        query = update(Event).where(Event.event_id == event_id).values(event_data_to_update)

        await local_session.execute(query)
        #
        # event_to_update = await local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        # if event_to_update:
        #     cur_users_id_go_list = event_to_update.users_id_go
        #
        #     try:
        #         cur_users_id_go_list.remove(user_id_del)
        #     except Exception as E:
        #         error_logger.error(E)
        #         info_logger.error(f'User {user_id_del} does not exist in want_list on event {event_id}!')
        #
        #     if cur_users_id_go_list:
        #         new_users_id_go_list = cur_users_id_go_list
        #     else:
        #         new_users_id_go_list = {}
        #
        #     event_to_update.users_id_go = new_users_id_go_list
        #
        # else:
        #     info_logger.error(f'Event {event_id} does not exist!')