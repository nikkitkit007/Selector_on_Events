import pytest
from random import randint
from datetime import datetime, timedelta


@pytest.fixture
def get_one_news():
    time = str(datetime.now())

    news = {'header': 'Hi Everyone!',
            'data': 'Good job!',
            'time': time}

    return news


@pytest.fixture
def get_update_news():
    update_header = "Hi Hi Hi!!!"
    time = str(datetime.now())

    news_id = 1
    data_update = {'news_id': news_id,
                   'news_data_to_update': {
                       'header': update_header,
                       'data': 'Good job!',
                       'time': time
                   }}

    return data_update
