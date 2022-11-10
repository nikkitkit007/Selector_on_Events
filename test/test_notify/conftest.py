import pytest
# from datetime import datetime, timedelta

event_id = 1


@pytest.fixture
def get_one_notify():
    notify_data = 'You are win in event ' + str(event_id)

    notify = {'event_id': event_id,
              'notify_header': 'Win eeeeeee!',
              'notify_data': notify_data}
    return notify
