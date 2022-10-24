from data_base.base import session
from server import info_logger, error_logger
from data_base.models.tbl_event import Event


class EventWorker(Event):
    def __init__(self, event_data):
        self.event_name = event_data['event_name']
        self.time_start = event_data['time_start']
        self.time_end = event_data['time_end']
        self.description = event_data['description']
        self.url_pdf = event_data['url_pdf']
        self.people_count = event_data['people_count']
        self.coefficient = event_data['coefficient']
        self.image = event_data['image']
        self.users_id_want = []
        self.users_id_go = []

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
    def add(event_to_add: dict, local_session):
        local_session.add(EventWorker(event_to_add))

    @staticmethod
    def get(local_session: session, event_id: int = 0, all_events: bool = False):
        """
        SELECT * FROM EVENT (WHERE event_id = event_id);\n
        :param local_session: session
        :param event_id: int
        :param all_events: bool
        :return: list with event or events
        """
        if all_events:
            events = local_session.query(EventWorker).all()
            if events:
                all_events_data = []
                for event in events:
                    all_events_data.append(event.get_dict())
                return all_events_data
        else:
            event = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
            if event:
                return event.get_dict()
        return {}

    @staticmethod
    def update(event_id: int, event_data_to_update: dict, local_session: session):
        event_to_update = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_update:
            event_to_update.event_name = event_data_to_update["event_name"]
            event_to_update.time_start = event_data_to_update["time_start"]
            event_to_update.time_end = event_data_to_update["time_end"]
            event_to_update.description = event_data_to_update["description"]
            event_to_update.url_pdf = event_data_to_update["url_pdf"]
            event_to_update.people_count = int(event_data_to_update["people_count"])
            event_to_update.coefficient = int(event_data_to_update["coefficient"])
            event_to_update.image = event_data_to_update['image']

        else:
            info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    def delete(event_id: int, local_session: session):
        event_to_delete = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_delete:
            local_session.delete(event_to_delete)
        else:
            info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    def update_add_users_id_want(event_id: int, user_id_want: int, local_session: session):
        event_to_update = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_update:
            cur_users_id_want_list = list(event_to_update.users_id_want)

            if cur_users_id_want_list:
                cur_users_id_want_list.append(user_id_want)
                new_users_id_want_list = set(cur_users_id_want_list)
            else:
                new_users_id_want_list = {user_id_want}

            event_to_update.users_id_want = new_users_id_want_list
        else:
            info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    def update_add_users_id_go(event_id: int, user_id_go: int, local_session: session):
        event_to_update = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_update:
            cur_users_id_go_list = list(event_to_update.users_id_go)

            if cur_users_id_go_list:
                cur_users_id_go_list.append(user_id_go)
                new_users_id_go_list = set(cur_users_id_go_list)
            else:
                new_users_id_go_list = {user_id_go}

            event_to_update.users_id_go = new_users_id_go_list
        else:
            info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    def update_del_users_id_want(event_id: int, user_id_del: int, local_session: session):
        event_to_update = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_update:
            cur_users_id_want_list = list(event_to_update.users_id_want)

            try:
                cur_users_id_want_list.remove(user_id_del)
            except Exception as E:
                error_logger.error(E)
                info_logger.error(f'User {user_id_del} does not exist in want_list on event {event_id}!')

            if cur_users_id_want_list:
                new_users_id_want_list = set(cur_users_id_want_list)
            else:
                new_users_id_want_list = []

            event_to_update.users_id_want = new_users_id_want_list
        else:
            info_logger.error(f'Event {event_id} does not exist!')

    @staticmethod
    def update_del_users_id_go(event_id: int, user_id_del: int, local_session: session):
        event_to_update = local_session.query(EventWorker).filter(EventWorker.event_id == event_id).first()
        if event_to_update:
            cur_users_id_go_list = event_to_update.users_id_go

            try:
                cur_users_id_go_list.remove(user_id_del)
            except Exception as E:
                error_logger.error(E)
                info_logger.error(f'User {user_id_del} does not exist in want_list on event {event_id}!')

            if cur_users_id_go_list:
                new_users_id_go_list = cur_users_id_go_list
            else:
                new_users_id_go_list = {}

            event_to_update.users_id_go = new_users_id_go_list

        else:
            info_logger.error(f'Event {event_id} does not exist!')