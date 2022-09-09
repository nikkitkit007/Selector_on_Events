import requests
from datetime import datetime, timedelta

import config

address = "http://" + config.HOST_ADDRESS + ":" + config.HOST_PORT


# ------------------------------TEST_USER------------------------------
def test_user_add_correct():
    method = "/api/user/add"
    phone_num = '9117252325'
    mail_box = 'nikkitkit0707@mail.ru'
    vk_link = 'https://vk.com/n.sulimenko12'

    test_user = {'user_isu_number': 288888,
                 'user_name': 'Nik',
                 'user_surname': 'Sul',
                 'user_patronymic': 'Serg',
                 'phone': phone_num,
                 'vk_link': vk_link,
                 'mail': mail_box,
                 'is_russian_citizenship': True}

    response = requests.post(address + method, json=test_user)
    return response.status_code == 200


def test_user_get_profile(user_id: int = 1):
    method = "/api/user/profile"

    test_user_id = {'user_id': user_id}

    response = requests.post(address + method, json=test_user_id)
    print(response.content)
    return response.status_code == 200


def test_user_update(user_id: int = 1):
    method = "/api/user/update"

    test_user_id = user_id

    phone_num = '9117252325'
    mail_box = 'nikkitkit0707@mail.ru'
    vk_link = 'https://vk.com/n.sulimenko12'

    update_name = 'Nikitos111111'
    test_data_update = {'user_id': test_user_id,
                        'user_data_to_update': {
                            'user_isu_number': 284678,
                            'user_name': update_name,
                            'user_surname': 'Sul',
                            'user_patronymic': 'Serg',
                            'phone': phone_num,
                            'vk_link': vk_link,
                            'mail': mail_box,
                            'is_russian_citizenship': True
                        }}

    response = requests.post(address + method, json=test_data_update)
    return response.status_code == 200


def test_user_delete(user_id: int = 1):
    method = "/api/user/delete"

    user_id = user_id

    test_user_id = {'user_id': user_id}

    response = requests.post(address + method, json=test_user_id)
    return response.status_code == 200


# ------------------------------TEST_EVENT------------------------------
def test_event_add():
    method = "/api/event/add"

    time_start = '09-14-2022 00:00:00'
    time_end = '09-15-2022 00:00:10'
    # time_end = 'fds'

    test_event = {'event_name': 'TEST_last... joke',
                  'time_start': time_start,
                  'time_end': time_end,
                  'description': 'Simple test',
                  'url_pdf': 'http://lol',
                  'people_count': 10,
                  'coefficient': 50,
                  'image': '/images/lol/lal.jpeg'}

    response = requests.post(address + method, json=test_event)
    return response.status_code == 200


def test_event_get(event_id: int = 1):
    method = "/api/event/get"

    test_event_id = {'event_id': event_id}

    response = requests.post(address + method, json=test_event_id)
    print(response.content)
    return response.status_code == 200


def test_event_get_all():
    method = "/api/event/get_all"

    response = requests.post(address + method)
    print(response.content)
    return response.status_code == 200


def test_event_update(event_id: int = 1):
    method = "/api/event/update"

    event_name_update = 'TEST_update_really>!'

    test_data_update = {'event_id': event_id,
                        'data_to_update':
                            {
                                'event_name': event_name_update,
                                'time_start': '09-08-2022 00:00:00',
                                'time_end': '09-10-2022 00:00:10',
                                'description': 'Simple test was update',
                                'url_pdf': 'http://lol',
                                'people_count': 10,
                                'coefficient': 50,
                                'image': '/images/lol/lal.jpeg'
                            }
                        }

    response = requests.post(address + method, json=test_data_update)
    return response.status_code == 200


def test_event_delete(event_id: int = 1):
    method = "/api/event/delete"

    test_event_id = {'event_id': event_id}

    response = requests.post(address + method, json=test_event_id)
    return response.status_code == 200


# -----------------------------TEST_NOTIFY-------------------------------
def test_notify_add(event_id: int = 1):
    method = "/api/notify/add"

    notify_data = 'You are win in event ' + str(event_id)
    # time_notify = str(datetime.now())

    notify_to_add = {'event_id': event_id,
                     'notify_header': 'Win eeeeeee!',
                     'notify_data': notify_data}

    response = requests.post(address + method, json=notify_to_add)
    return response.status_code == 200


# ------------------------TEST_EVENT_REGISTRATION------------------------
def test_event_registration(event_id: int = 1, user_id: int = 1):
    method = "/api/event/confirm/register"

    test_data_to_registration = {'event_id': event_id,
                                 'user_id': user_id}

    response = requests.post(address + method, json=test_data_to_registration)
    print(response.content)
    return response.status_code == 200


def test_event_cancel_registration(event_id: int = 1, user_id: int = 1):
    method = "/api/event/confirm/cancel_register"

    test_data_to_cancel_registration = {'event_id': event_id,
                                        'user_id': user_id}

    response = requests.post(address + method, json=test_data_to_cancel_registration)
    return response.status_code == 200


# ----------------------------TEST_EVENT_APPLY---------------------------
def test_apply_event(event_id: int = 1, user_id: int = 1):
    method = "/api/event/confirm/apply"

    test_data_to_apply_event = {'event_id': event_id,
                                'user_id': user_id}

    response = requests.post(address + method, json=test_data_to_apply_event)
    return response.status_code == 200


print(test_user_add_correct())
print(test_user_get_profile(user_id=3))
# print(test_user_update(user_id=3))
# print(test_user_get_profile(user_id=3))
# print(test_user_delete(user_id=3))

# print(test_event_add())
# print(test_event_get(event_id=1))
# print(test_event_get_all())
# print(test_event_update(event_id=1))
# print(test_event_delete(event_id=1))

# print(test_notify_add(1))

# print(test_event_registration())
# print(test_event_cancel_registration())

# print(test_apply_event())
