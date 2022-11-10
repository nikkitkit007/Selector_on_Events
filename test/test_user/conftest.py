import pytest


@pytest.fixture
def get_one_user():
    user_isu_number = 284679

    phone_num = '9117252325'
    mail_box = 'nikkitkit0707@mail.ru'
    vk_link = 'https://vk.com/n.sulimenko12'

    user = {'user_isu_number': user_isu_number,
            'user_name': 'Nik',
            'user_surname': 'Sul',
            'user_patronymic': 'Serg',
            'phone': phone_num,
            'vk_link': vk_link,
            'mail': mail_box,
            'is_russian_citizenship': True}

    return user


@pytest.fixture
def get_update_user():
    user_isu_number = 284679

    phone_num = '9117252325'
    mail_box = 'nikkitkit0707@mail.ru'
    vk_link = 'https://vk.com/n.sulimenko12'

    update_user = {'user_isu_number': user_isu_number,
                   "user_data_to_update":
                       {
                           'user_name': 'Nik',
                           'user_surname': 'Sul',
                           'user_patronymic': 'Serg',
                           'phone': phone_num,
                           'vk_link': vk_link,
                           'mail': mail_box,
                           'is_russian_citizenship': True
                       }
                   }

    return update_user
