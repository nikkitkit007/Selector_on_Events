import pytest
import requests
from datetime import datetime, timedelta
from random import randint

from tests.conftest import cookies

get_base_url = "http://127.0.0.1:8080"


def create_user(user_isu_number: int = 2):
    method = "/api/user"
    user = {'user_isu_number': user_isu_number,
            'user_name': 'test',
            'user_surname': 'test',
            'user_patronymic': 'test',
            'phone': "9117252323",
            'vk_link': "https://vk.myvk",
            'mail': "lol@mail.ru",
            'is_russian_citizenship': True}

    requests.post(get_base_url + method, json=user, cookies=cookies)


def create_event(time: dict):
    method = "/api/event"

    time_start = time["time_start"]
    time_end = time["time_end"]

    event = {'event_name': 'TEST_last... joke',
             'time_start': time_start,
             'time_end': time_end,
             'description': 'Simple test',
             'url_pdf': 'lol/lol1',
             'people_count': 10,
             'coefficient': randint(10, 30),
             'image': '/images/lol/lal.jpeg'}

    requests.post(get_base_url + method, json=event, cookies=cookies)


@pytest.fixture(scope='session')
def gen_users(count: int = 11) -> list:
    isu_list = [int(i) for i in range(1000, 1000+count)]

    for _ in range(count):
        create_user(user_isu_number=isu_list[_])

    return isu_list


@pytest.fixture(scope='session')
def gen_events(count: int = 11) -> list:
    id_events_list = [int(x) for x in range(count)]

    for _ in range(count):
        time_start = datetime.now() - timedelta(0+id_events_list[_])
        time_end = datetime.now() + timedelta(11-id_events_list[_])
        time = {"time_start": str(time_start),
                "time_end": str(time_end)}

        create_event(time=time)

    return id_events_list
