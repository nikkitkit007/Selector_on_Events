import requests
from configurations.default import DefaultSettings
from datetime import datetime, timedelta
# from data_base.models.tbl_user import User
import random

settings = DefaultSettings()
address = settings.host_address


# ------------------------------TEST_USER------------------------------
class TestUser:
    @staticmethod
    def user_add_correct():
        method = "/api/user/add"

        phone_num = '9117252325'
        mail_box = 'nikkitkit0707@mail.ru'
        vk_link = 'https://vk.com/n.sulimenko12'

        user = {'user_isu_number': 222,
                'user_name': 'Nik',
                'user_surname': 'Sul',
                'user_patronymic': 'Serg',
                'phone': phone_num,
                'vk_link': vk_link,
                'mail': mail_box,
                'is_russian_citizenship': True}

        response = requests.post(address + method, json=user)
        return response.status_code == 200

    # @staticmethod
    # def user_get_profile(user_id: int = 1):
    #     method = "/api/user/get"
    #
    #     user_id = {'user_id': user_id}
    #
    #     response = requests.get(address + method, params=user_id)
    #     print(response.content)
    #     return response.status_code == 200
    @staticmethod
    def user_get_profile(user_isu_number: int = 284679):
        method = "/api/user/get"

        user_id = {'user_isu_number': user_isu_number}

        response = requests.get(address + method, params=user_id)
        print(response.content)
        return response.status_code == 200

    @staticmethod
    def user_update(user_id: int = 1):
        method = "/api/user/update"

        phone_num = '9117252325'
        mail_box = 'nikkitkit0707@mail.ru'
        vk_link = 'https://vk.com/n.sulimenko12'

        update_name = 'Nikitos'
        data_update = {'user_id': user_id,
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

        response = requests.post(address + method, json=data_update)
        return response.status_code == 200

    @staticmethod
    def user_delete(user_id: int = 1):
        method = "/api/user/delete"

        user_id = {'user_id': user_id}

        response = requests.delete(address + method, json=user_id)
        return response.status_code == 200


# ------------------------------TEST_EVENT------------------------------
class TestEvent:
    @staticmethod
    def event_add(time_start: str = "09/25/2022, 00:01:10", time_end: str = "09/30/2022, 00:01:10"):
        method = "/api/event/add"

        event = {'event_name': 'TEST_last... joke',
                 'time_start': time_start,
                 'time_end': time_end,
                 'description': 'Simple test',
                 'url_pdf': 'http://lol',
                 'people_count': 10,
                 'coefficient': random.randint(10, 30),
                 'image': '/images/lol/lal.jpeg'}

        response = requests.post(address + method, json=event)
        return response.status_code == 200

    @staticmethod
    def event_get(event_id: int = 1):
        method = "/api/event/get"

        event_id = {"event_id": event_id}

        response = requests.get(address + method, params=event_id)
        print(response.content)
        return response.status_code == 200

    @staticmethod
    def event_get_all():
        method = "/api/event/get_all"

        response = requests.get(address + method)
        print(response.content, response.text)
        return response.status_code == 200

    @staticmethod
    def event_update(event_id: int = 1):
        method = "/api/event/update"

        event_name_update = 'TEST_update_really>!'
        data_update = {'event_id': event_id,
                       'event_data_to_update':
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

        response = requests.post(address + method, json=data_update)
        return response.status_code == 200

    @staticmethod
    def event_delete(event_id: int = 1):
        method = "/api/event/delete"

        event_id = {'event_id': event_id}

        response = requests.delete(address + method, json=event_id)
        return response.status_code == 200


# -----------------------------TEST_NOTIFY-------------------------------
class TestNotify:
    @staticmethod
    def notify_add(event_id: int):
        method = "/api/notify/add"

        notify_data = 'You are win in event ' + str(event_id)

        notify_to_add = {'event_id': event_id,
                         'notify_header': 'Win eeeeeee!',
                         'notify_data': notify_data}

        response = requests.post(address + method, json=notify_to_add)
        return response.status_code == 200


# ------------------------------TEST_NEWS------------------------------
class TestNews:
    @staticmethod
    def news_add():
        method = "/api/news/add"

        time = '09-15-2022 00:01:00'

        news = {'header': 'Hi Nik!',
                'data': 'Good job!',
                'time': time}

        response = requests.post(address + method, json=news)
        return response.status_code == 200

    @staticmethod
    def news_get(news_id: int = 1):
        method = "/api/news/get"

        news_id = {'news_id': news_id}

        response = requests.get(address + method, params=news_id)
        print(response.content)
        return response.status_code == 200

    @staticmethod
    def news_get_all():
        method = "/api/news/get_all"

        response = requests.get(address + method)
        print(response.content)
        return response.status_code == 200

    @staticmethod
    def news_update(news_id: int = 1):
        method = "/api/news/update"

        update_header = 'I was updated'
        time = '09-15-2022 00:01:00'

        data_update = {'news_id': news_id,
                       'news_data_to_update': {
                           'header': update_header,
                           'data': 'Good job!',
                           'time': time
                       }}

        response = requests.post(address + method, json=data_update)
        return response.status_code == 200

    @staticmethod
    def news_delete(news_id: int = 1):
        method = "/api/news/delete"

        news_id = {'news_id': news_id}

        response = requests.delete(address + method, json=news_id)
        return response.status_code == 200


# ------------------------TEST_EVENT_REGISTRATION------------------------
class TestDecision:
    @staticmethod
    def event_registration(user_id: int, event_id: int):
        method = "/api/event_registration"

        data_to_registration = {'event_id': event_id,
                                'user_id': user_id}

        response = requests.post(address + method, json=data_to_registration)
        print(response.text, response.status_code)
        return response.status_code == 200

    @staticmethod
    def event_cancel_registration(user_id: int, event_id: int):
        method = "/api/event_cancel_registration"

        data_to_cancel_registration = {'event_id': event_id,
                                       'user_id': user_id}

        response = requests.post(address + method, json=data_to_cancel_registration)
        print(response.text, response.status_code)
        return response.status_code == 200

    # ----------------------------TEST_EVENT_APPLY---------------------------
    @staticmethod
    def apply_event(event_id: int, user_id: int):
        method = "/api/apply_event"

        data_to_apply_event = {'event_id': event_id,
                               'user_id': user_id}

        response = requests.post(address + method, json=data_to_apply_event)
        return response.status_code == 200

    @staticmethod
    def decline_event(event_id: int, user_id: int):
        method = "/api/decline_event"

        data_to_apply_event = {'event_id': event_id,
                               'user_id': user_id}

        response = requests.post(address + method, json=data_to_apply_event)
        return response.status_code == 200


def _base_functions(user_id: int = 1, event_id: int = 1, news_id: int = 1, notify_id: int = 1):

    print(TestUser.user_add_correct())
    print(TestUser.user_get_profile(user_id))
    print(TestUser.user_update(user_id))
    print(TestUser.user_get_profile(user_id))
    print(TestUser.user_delete(user_id))

    print(TestEvent.event_add())
    print(TestEvent.event_get(event_id))
    print(TestEvent.event_get_all())
    print(TestEvent.event_update(event_id))
    print(TestEvent.event_delete(event_id))

    print(TestNews.news_add())
    print(TestNews.news_get(news_id))
    print(TestNews.news_get_all())
    print(TestNews.news_update(news_id))
    print(TestNews.news_delete(news_id))

    print(TestNotify.notify_add(event_id))


def generate_users(user_count: int):
    for i in range(user_count):
        TestUser.user_add_correct()


def generate_events(event_count: int):
    time_now = datetime.now()
    for i in range(event_count):
        TestNotify.notify_add(event_id=i)
        time_event_start = (time_now + timedelta(i)).strftime("%m/%d/%Y, %H:%M:%S")
        TestEvent.event_add(time_start=time_event_start)


def _registrate(user_count: int, event_id: int):
    for i in range(user_count):
        TestDecision.event_registration(user_id=i, event_id=event_id)
    TestDecision.event_cancel_registration(user_id=(user_count-1), event_id=event_id)

# print(apply_event(event_id=9, user_id=7))
# print(decline_event(event_id=9, user_id=7))


if __name__ == "__main__":
    TestUser.user_get_profile()

    # TestEvent.event_get(3)
    # test_base_functions(user_id=1, event_id=1, notify_id=1, news_id=1)
    # generate_events(15)
    # generate_users(12)
    # test_registrate(5, 11)

    # print(TestDecision.apply_event(event_id=11, user_id=2))
    # print(TestDecision.decline_event(event_id=10, user_id=2))
    # print(TestUser.user_add_correct())
    # print(TestEvent.event_add())
    # print(TestEvent.event_get(3))

    pass
