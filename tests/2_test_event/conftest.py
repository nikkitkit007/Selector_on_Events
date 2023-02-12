import pytest
from random import randint
from datetime import datetime, timedelta


def generate_event_time() -> dict:
    time_start = datetime.now() - timedelta(1)
    time_end = datetime.now() + timedelta(9)
    time = {"time_start": str(time_start),
            "time_end": str(time_end)}
    return time


@pytest.fixture
def get_one_event():
    time = generate_event_time()

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
    return event


@pytest.fixture
def get_update_event():
    event_name_update = "update_name"
    event_id = 1
    time = generate_event_time()

    time_start = time["time_start"]
    time_end = time["time_end"]

    update_event = {'event_id': event_id,
                    'event_data_to_update':
                        {
                            'event_name': event_name_update,
                            'time_start': time_start,
                            'time_end': time_end,
                            'description': 'Simple test was update',
                            'url_pdf': 'lol/lol2',
                            'people_count': 10,
                            'coefficient': 50,
                            'image': '/images/lol/lal.jpeg'
                        }
                    }

    return update_event
