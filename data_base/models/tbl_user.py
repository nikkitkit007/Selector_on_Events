import sqlalchemy as sa
from data_base.base import Base, settings


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
