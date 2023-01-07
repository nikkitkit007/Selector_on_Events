import requests
from starlette import status

from tests.conftest import cookies


class TestDecision:

    def test_event_registration(self, get_base_url, gen_events, gen_users):
        method = "/api/event_registration"

        # user_id = gen_users[1]
        user_id = gen_users[1]
        event_id = gen_events[2]

        data_to_registration = {'event_id': event_id,
                                'user_isu_number': user_id}

        response = requests.post(get_base_url + method, json=data_to_registration, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK

    def test_event_cancel_registration(self, get_base_url, gen_events, gen_users):
        method = "/api/event_cancel_registration"

        user_id = gen_users[1]
        event_id = gen_events[2]

        data_to_cancel_registration = {'event_id': event_id,
                                       'user_isu_number': user_id}

        response = requests.post(get_base_url + method, json=data_to_cancel_registration, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK

    # ----------------------------TEST_EVENT_APPLY---------------------------
    def test_apply_event(self, get_base_url, gen_events, gen_users):
        method = "/api/apply_event"

        user_id = gen_users[1]
        event_id = gen_events[2]

        data_to_apply_event = {'event_id': event_id,
                               'user_isu_number': user_id}

        response = requests.post(get_base_url + method, json=data_to_apply_event, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK

    def test_decline_event(self, get_base_url, gen_events, gen_users):
        method = "/api/decline_event"

        user_id = gen_users[1]
        event_id = gen_events[2]

        data_to_apply_event = {'event_id': event_id,
                               'user_isu_number': user_id}

        response = requests.post(get_base_url + method, json=data_to_apply_event, cookies=cookies)
        assert response.status_code == status.HTTP_200_OK
