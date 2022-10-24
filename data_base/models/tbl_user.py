import sqlalchemy as sa
from datetime import datetime, timedelta

# from tbl_event import Event
from data_base.base import Base, engine, session, settings
from data_base.models.tbl_event import Event

from server import info_logger, error_logger


class User(Base):
    __tablename__ = settings.TBL_USERS

    user_id = sa.Column('user_id', sa.Integer, primary_key=True)
    user_isu_number = sa.Column('user_isu_number', sa.Integer)
    user_name = sa.Column('user_name', sa.String(127), nullable=False)
    user_surname = sa.Column('user_surname', sa.String(127), nullable=False)
    user_patronymic = sa.Column('user_patronymic', sa.String(127), nullable=False)
    phone = sa.Column('phone', sa.String(127))
    vk_link = sa.Column('vk_link', sa.String(127))
    mail = sa.Column('mail', sa.String(127))
    is_russian_citizenship = sa.Column('is_russian_citizenship', sa.BOOLEAN)
    score = sa.Column('score', sa.Integer)
    ban_date = sa.Column('ban_date', sa.TIMESTAMP)
    notify_id = sa.Column('notify_id', sa.ARRAY(sa.Integer), default={})
    time_select_finish = sa.Column('time_select_finish', sa.TIMESTAMP)      # TODO: Add default

    def __init__(self, user_data: dict):
        self.user_isu_number = user_data['user_isu_number']
        self.user_name = user_data['user_name']
        self.user_surname = user_data['user_surname']
        self.user_patronymic = user_data['user_patronymic']
        self.phone = user_data['phone']
        self.vk_link = user_data['vk_link']
        self.mail = user_data['mail']
        self.is_russian_citizenship = user_data['is_russian_citizenship']
        self.score = 0
        self.notify_id = {}

    def __repr__(self):
        return f"<User(User_name: {self.user_name}, User_surname: {self.user_surname})>"

    def get_dict(self):
        atts_dict = {"user_isu_number": self.user_isu_number,
                     "user_name": self.user_name,
                     "user_surname": self.user_surname,
                     "user_patronymic": self.user_patronymic,
                     "phone": self.phone,
                     "vk_link": self.vk_link,
                     "mail": self.mail,
                     "is_russian_citizenship": self.is_russian_citizenship,
                     "score": self.score,
                     "notify_id": self.notify_id,
                     "ban_date": self.ban_date,
                     "time_select_finish": self.time_select_finish}
        return atts_dict

    @staticmethod
    def add(user_to_add: dict, local_session: session):
        local_session.add(User(user_to_add))

    @staticmethod
    def get(user_id: int, local_session: session):
        """
        SELECT * from User WHERE user_id = user_id;\n
        :param local_session: session
        :param user_id: int
        :return: list with user data
        """
        user = local_session.query(User).filter(User.user_id == user_id).first()
        if user:
            return user.get_dict()
        else:
            return {}

    @staticmethod
    def update(user_id: int, user_data_to_update: dict, local_session: session):
        user_to_update = local_session.query(User).filter(User.user_id == user_id).first()

        if user_to_update:
            user_to_update.user_name = str(user_data_to_update["user_name"])
            user_to_update.user_surname = str(user_data_to_update["user_surname"])
            user_to_update.user_patronymic = str(user_data_to_update["user_patronymic"])
            user_to_update.phone = str(user_data_to_update["phone"])
            user_to_update.vk_link = str(user_data_to_update["vk_link"])
            user_to_update.mail = str(user_data_to_update["mail"])
            user_to_update.is_russian_citizenship = bool(user_data_to_update['is_russian_citizenship'])

        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def delete(user_id: int, local_session: session):
        user_to_delete = local_session.query(User).filter(User.user_id == user_id).first()
        if user_to_delete:
            local_session.delete(user_to_delete)
        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def update_add_notify(user_id: int, notify_id: int, local_session: session):
        user = local_session.query(User).filter(User.user_id == user_id).first()
        if user:
            cur_user_notify_id = list(user.notify_id)
            if notify_id not in cur_user_notify_id:
                if cur_user_notify_id:
                    cur_user_notify_id.append(notify_id)
                    new_user_notify_id = set(cur_user_notify_id)
                else:
                    new_user_notify_id = {notify_id}

                user.time_select_finish = datetime.now() + timedelta(config.TIME_TO_ACCEPT)
                user.notify_id = new_user_notify_id
        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def update_del_notify(user_id: int, notify_id: int, local_session: session):
        user = local_session.query(User).filter(User.user_id == user_id).first()
        if user:
            cur_user_notify_id = user.notify_id
            try:
                cur_user_notify_id.remove(notify_id)
            except Exception as E:
                error_logger.error(E)
                info_logger.error(f'Notify_id {notify_id} does not exist to user {user_id}!')

            if cur_user_notify_id:
                new_user_notify_id = set(cur_user_notify_id)
            else:
                new_user_notify_id = []

            user.notify_id = new_user_notify_id
        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def update_ban_date(user_id: int, ban_date: datetime, local_session: session):
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.ban_date = ban_date
            info_logger.info(f"User {user_id} get ban until {ban_date}")
        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def update_add_score(user_id: int, score: int, local_session):
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.score += score

        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def update_del_timer(user_id: int, local_session: session):
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.time_select_finish = None
        else:
            info_logger.error(f'User {user_id} does not exist!')

    @staticmethod
    def apply_event(user_id: int, event_id: int, local_session: session):
        Event.update_add_users_id_go(event_id, user_id, local_session)
        Event.update_del_users_id_want(event_id, user_id, local_session)

        User.update_add_score(user_id, Event.get(event_id)['coefficient'], local_session)

        User.update_del_timer(user_id, local_session)

    @staticmethod
    def decline_event(user_id: int, event_id: int, local_session: session):
        Event.update_del_users_id_go(event_id, user_id, local_session)
        event = Event.get(event_id, local_session)
        time_now = datetime.now()

        if time_now > (datetime.strptime(event['time_start'], "%m/%d/%Y, %H:%M:%S") - timedelta(config.TIME_TO_BAN)):
            User.update_ban_date(user_id, time_now + timedelta(config.BAN_TIME_LATE), local_session)


if __name__ == "__main__":
    pass
