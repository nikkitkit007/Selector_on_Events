import config
import sqlalchemy as sa
from .base import Base, Session, engine

from datetime import datetime, timedelta
import logging
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


class User(Base):
    __tablename__ = config.TBL_USERS
    __table_args__ = {'extend_existing': True}

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
    time_select_finish = sa.Column('time_select_finish', sa.TIMESTAMP)

    def __init__(self, user_data):
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
        atts_dict = {"user_id": self.user_id,
                     "user_isu_number": self.user_isu_number,
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


def user_add(user_to_add: dict):
    with Session(bind=engine) as local_session:
        new_user = User(user_to_add)

        local_session.add(new_user)
        local_session.commit()


def user_get(user_id: int):
    with Session(bind=engine) as local_session:
        user = local_session.query(User).filter(User.user_id == user_id).first()
        if user:
            return user.get_dict()
        else:
            info_logger.error(f'User {user_id} does not exist!')
            return {}


def user_update(user_id: int, user_data_to_update):
    with Session(bind=engine) as local_session:
        user_to_update = local_session.query(User).filter(User.user_id == user_id).first()

        if user_to_update:
            user_to_update.user_name = str(user_data_to_update["user_name"])
            user_to_update.user_surname = str(user_data_to_update["user_surname"])
            user_to_update.user_patronymic = str(user_data_to_update["user_patronymic"])
            user_to_update.phone = str(user_data_to_update["phone"])
            user_to_update.vk_link = str(user_data_to_update["vk_link"])
            user_to_update.mail = str(user_data_to_update["mail"])
            user_to_update.is_russian_citizenship = bool(user_data_to_update['is_russian_citizenship'])

            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_delete(user_id: int):
    with Session(bind=engine) as local_session:
        user_to_delete = local_session.query(User).filter(User.user_id == user_id).first()
        if user_to_delete:
            local_session.delete(user_to_delete)
            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_update_add_notify(user_id: int, notify_id: int, time_now):
    with Session(bind=engine) as local_session:
        user = local_session.query(User).filter(User.user_id == user_id).first()
        if user:
            cur_user_notify_id = list(user.notify_id)

            if cur_user_notify_id:
                cur_user_notify_id.append(notify_id)
                new_user_notify_id = set(cur_user_notify_id)
            else:
                new_user_notify_id = {notify_id}

            user.time_select_finish = datetime.now() + timedelta(config.TIME_TO_ACCEPT)
            user.notify_id = new_user_notify_id
            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_update_del_notify(user_id: int, notify_id: int):
    with Session(bind=engine) as local_session:
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
            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_update_ban_date(user_id: int, ban_date):
    with Session(bind=engine) as local_session:
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.ban_date = ban_date
            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_update_add_score(user_id: int, score: int):
    with Session(bind=engine) as local_session:
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.score += score

            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


def user_update_del_timer(user_id: int):
    with Session(bind=engine) as local_session:
        user = local_session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.time_select_finish = None
            local_session.commit()
        else:
            info_logger.error(f'User {user_id} does not exist!')


if __name__ == "__main__":

    pass