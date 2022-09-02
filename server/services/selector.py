
import data.db_worker as db
import config
from datetime import datetime, timedelta

DB = db.DataBaseEvents()


def gen_users():
    users_ids = [1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1020, 1021, 1022, 1023]
    users_score = [10, 11, 12, 43, 153, 81, 93, 55, 12, 10, 8, 1022, 49]
    users_count = len(users_ids)

    for i in range(users_count):
        test_user = {'user_id': users_ids[i],
                     'user_name': 'Nik',
                     'user_surname': 'Sul',
                     'user_patronymic': 'Serg',
                     'phone': '8991',
                     'vk_link': 'http://',
                     'mail': 'nikkitkit@mail.ru',
                     'is_russian_citizenship': True,
                     'score': users_score[i]}
        DB.user_add(test_user)


def update_users_id_go():
    pass


# -------------------norm-----------------
def get_user_score(users_ids):
    users_score = {}
    for user_id in users_ids:
        users_score[user_id] = DB.user_get(int(user_id))['score']
    return users_score


def select_users_on_event(event_id: int):
    event = DB.event_get(event_id)
    users_want = event["users_id_want"]
    users_go = event["users_id_go"]

    if users_want:
        if users_go:
            people_count_to_select = event["people_count"] - event["users_is_go"].count()
            # users_id_want = [1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1020, 1021, 1022, 1023]
        else:
            people_count_to_select = event["people_count"]

        users_want_with_score = get_user_score(users_want)

        sorted_applicants = dict(sorted(users_want_with_score.items(), key=lambda x: x[1]))
        print(sorted_applicants)
        selected_users = dict(list(sorted_applicants.items())[:people_count_to_select])
        print('selected_users:', list(selected_users))
        return list(selected_users)
    return False


def user_apply_event(user_id: int, event_id: int):
    DB.event_update_add_users_id_go(event_id, user_id)
    DB.event_update_del_users_id_want(event_id, user_id)

    score = DB.event_get(event_id)['coefficient']
    DB.user_update_add_score(user_id, score)

    DB.user_update_del_timer(user_id)

    return True


def user_decline_event(user_id: int, event_id: int):
    DB.event_update_del_users_id_go(event_id, user_id)
    event = DB.event_get(event_id)
    time_now = datetime.now()

    if time_now > event['time_start'] - timedelta(config.TIME_TO_BAN):
        DB.user_update_ban_date(user_id, time_now + timedelta(config.BAN_TIME_LATE))
    return True


# gen_users()

# mass from Events
if __name__ == "__main__":
    event_id_to_go = 1                        # откуда-то берем
    notify_id = 1
    if DB.event_get(event_id_to_go)['time_start'] <= config.TIME_TO_FIRST_APPLICANTS:
        users_id_go = select_users_on_event(event_id_to_go)
        for user in users_id_go:
            DB.user_update_add_notify(user, notify_id)
            # every user get notify to accept or decline

    users_id_go = select_users_on_event(event_id_to_go)

    # user_want_to_go_score = get_user_score(users_id_want)
    # user_want_to_go_score[:10]
    # print(user_want_to_go_score)

# dict = {}
# lol = 12
# dict[lol] = 12
# print(dict)

# people_count = 10
# users_id_go = users_id_want[:people_count]
#
# print(users_id_go)
