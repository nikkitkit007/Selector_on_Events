import requests
from starlette import status


event_id = 1


class TestEvent:
    def test_add(self, get_base_url, get_one_event):
        method = "/api/event/add"
        event = get_one_event

        response = requests.post(get_base_url + method, json=event)

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, get_base_url, get_one_event):
        method = "/api/event/get"
        # event_id = get_one_event["event_id"]
        event_id_dict = {'event_id': event_id}

        response = requests.get(get_base_url + method, params=event_id_dict)

        assert response.status_code == status.HTTP_200_OK

    def test_get_all(self, get_base_url):
        method = "/api/event/get_all"

        response = requests.get(get_base_url + method)

        assert response.status_code == status.HTTP_200_OK

    def test_update(self, get_base_url, get_update_event):
        method = "/api/event/update"
        data_update = get_update_event

        response = requests.post(get_base_url + method, json=data_update)

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, get_base_url, get_one_event):
        method = "/api/event/delete"

        # event_id = get_one_event["event_id"]
        event_id_dict = {'event_id': event_id}

        response = requests.delete(get_base_url + method, json=event_id_dict)
        assert response.status_code == status.HTTP_200_OK
