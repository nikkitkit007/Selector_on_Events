from sqlalchemy import select, insert, and_, update, delete

from data_base.base import get_session
from server import info_logger, error_logger
from data_base.models.tbl_news import News


class NewsWorker(News):

    def __repr__(self):
        return f"<News(news_name: {self.header})>"

    def get_dict(self):
        atts_dict = {"header": self.header,
                     "data": self.data,
                     "time": self.time}
        return atts_dict

    @staticmethod
    async def add(news_to_add: dict, local_session: get_session):
        query = insert(News).values(news_to_add)
        await local_session.execute(query)

    @staticmethod
    async def get(local_session: get_session, news_id: int = None, all_news: bool = None):
        if all_news:
            query = select(News).where()
            all_news = await local_session.execute(query)
            all_news = all_news.scalars().all()

            if all_news:
                all_news_list = []
                for news in all_news:
                    all_news_list.append(NewsWorker.get_dict(news))
                return all_news_list
            else:
                return {}
        else:
            query = select(News).where(News.news_id == int(news_id)).limit(1)
            news = await local_session.execute(query)
            news = news.scalars().first()

            if news:
                return NewsWorker.get_dict(news)
            else:
                return {}

    @staticmethod
    async def update(news_id: int, news_data_to_update: dict, local_session: get_session):
        query = update(News).where(News.news_id == news_id).values(news_data_to_update)
        await local_session.execute(query)

        # news_to_update = await local_session.query(NewsWorker).filter(NewsWorker.news_id == news_id).first()
        # if news_to_update:
        #     news_to_update.header = news_data_to_update["header"]
        #     news_to_update.data = news_data_to_update["data"]
        #     news_to_update.time = news_data_to_update["time"]
        #
        # else:
        #     info_logger.error(f'News {news_id} does not exist!')

    @staticmethod
    async def delete(news_id: int, local_session: get_session):
        query = delete(News).where(News.news_id == news_id)
        await local_session.execute(query)

