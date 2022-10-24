from data_base.base import session
from server import info_logger, error_logger
from data_base.models.tbl_news import News


class NewsWorker(News):
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

    @staticmethod
    def add(news_to_add: dict, local_session: session):
        local_session.add(NewsWorker(news_to_add))

    @staticmethod
    def get(local_session: session, news_id: int = 0, all_news: bool = False):
        if all_news:
            news_all = local_session.query(NewsWorker).all()
            if news_all:
                all_news_data = []
                for news in news_all:
                    all_news_data.append(news.get_dict())
                return all_news_data
        else:
            news = local_session.query(NewsWorker).filter(NewsWorker.news_id == news_id).first()
            if news:
                return news.get_dict()
        return {}

    @staticmethod
    def update(news_id: int, news_data_to_update: dict, local_session: session()):
        news_to_update = local_session.query(NewsWorker).filter(NewsWorker.news_id == news_id).first()
        if news_to_update:
            news_to_update.header = news_data_to_update["header"]
            news_to_update.data = news_data_to_update["data"]
            news_to_update.time = news_data_to_update["time"]

        else:
            info_logger.error(f'News {news_id} does not exist!')

    @staticmethod
    def delete(news_id: int, local_session: session()):
        news_to_delete = local_session.query(NewsWorker).filter(NewsWorker.news_id == news_id).first()
        if news_to_delete:
            local_session.delete(news_to_delete)
        else:
            info_logger.error(f'News {news_id} does not exist!')

