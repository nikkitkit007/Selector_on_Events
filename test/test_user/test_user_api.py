import requests
from starlette import status


class TestUser:
    def test_add(self, get_base_url, get_one_user):
        method = "/api/user/add"
        user = get_one_user

        response = requests.post(get_base_url + method, json=user)

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, get_base_url, get_one_user):
        method = "/api/user/get"
        user_isu = get_one_user["user_isu_number"]
        user_isu_dict = {'user_isu_number': user_isu}

        response = requests.get(get_base_url + method, params=user_isu_dict)

        assert response.status_code == status.HTTP_200_OK

    def test_update(self, get_base_url, get_update_user):
        method = "/api/user/update"
        data_update = get_update_user

        response = requests.post(get_base_url + method, json=data_update)

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, get_base_url, get_update_user):
        method = "/api/user/delete"

        user_isu_number = get_update_user["user_isu_number"]
        user_id = {'user_isu_number': user_isu_number}

        response = requests.delete(get_base_url + method, json=user_id)
        assert response.status_code == 200
