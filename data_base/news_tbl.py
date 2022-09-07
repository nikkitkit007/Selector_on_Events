import config
import sqlalchemy as sa
from .base import Base, Session, engine

import logging
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


class News(Base):
    __tablename__ = config.TBL_NEWS
    __table_args__ = {'extend_existing': True}

    news_id = sa.Column('news_id', sa.Integer, primary_key=True)
    header = sa.Column('header', sa.String(127), nullable=False)
    data = sa.Column('data', sa.String)
    time = sa.Column('time', sa.TIMESTAMP)

    def __init__(self, news_data):
        self.header = news_data['header']
        self.data = news_data['data']
        self.time = news_data['time']

    def __repr__(self):
        return f"<News(news_name: {self.header})>"

    def get_dict(self):
        atts_dict = {"header": self.header,
                     "data": self.data,
                     "time": self.time}
        return atts_dict


def news_add(news_to_add: dict):
    with Session(bind=engine) as local_session:
        new_news = News(news_to_add)

        local_session.add(new_news)
        local_session.commit()


def news_get(news_id: int = 0, all_news: bool = False):
    with Session(bind=engine) as local_session:
        if all_news:
            news_all = local_session.query(News).all()
            if news_all:
                all_news_data = []
                for news in news_all:
                    all_news_data.append(news.get_dict())
                return all_news_data
        else:
            news = local_session.query(News).filter(News.news_id == news_id).first()
            if news:
                return news.get_dict()

    return {}


def news_update(news_id: int, news_data_to_update: dict):
    with Session(bind=engine) as local_session:
        news_to_update = local_session.query(News).filter(News.news_id == news_id).first()
        if news_to_update:
            news_to_update.header = news_data_to_update["header"]
            news_to_update.data = news_data_to_update["data"]
            news_to_update.time = news_data_to_update["time"]

            local_session.commit()
        else:
            info_logger.error(f'News {news_id} does not exist!')


def news_delete(news_id: int):
    with Session(bind=engine) as local_session:
        news_to_delete = local_session.query(News).filter(News.news_id == news_id).first()
        if news_to_delete:
            local_session.delete(news_to_delete)
            local_session.commit()
        else:
            info_logger.error(f'News {news_id} does not exist!')


if __name__ == "__main__":
    pass
