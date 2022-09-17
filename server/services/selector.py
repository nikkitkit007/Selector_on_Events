from _config import config

import data_base.tbl_event as event_tbl
import data_base.tbl_user as user_tbl
# import data_base.notify_tbl as notify_tbl
# import data_base.news_tbl as news_tbl


class Selector:

    @staticmethod
    def get_user_score(users_ids: list):
        users_score = {}
        for user_id in users_ids:
            users_score[user_id] = user_tbl.User.get(int(user_id))['score']
        return users_score

    @staticmethod
    def select_users_on_event(event_id: int):
        event = event_tbl.Event.get(event_id)
        users_want = event["users_id_want"]
        users_go = event["users_id_go"]

        if users_want:
            if users_go:
                people_count_to_select = event["people_count"] - event["users_is_go"].count()
                # users_id_want = [1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1020, 1021, 1022, 1023]
            else:
                people_count_to_select = event["people_count"]

            users_want_with_score = Selector.get_user_score(users_want)

            sorted_applicants = dict(sorted(users_want_with_score.items(), key=lambda x: x[1]))
            print(sorted_applicants)
            selected_users = dict(list(sorted_applicants.items())[:people_count_to_select])
            print('selected_users:', list(selected_users))
            return list(selected_users)
        return False


if __name__ == "__main__":
    event_id_to_go = 1                        # откуда-то берем
    notify_id = 1
    if event_tbl.Event.get(event_id_to_go)['time_start'] <= config.TIME_TO_FIRST_APPLICANTS:
        users_id_go = Selector.select_users_on_event(event_id_to_go)
        for user in users_id_go:
            user_tbl.User.update_add_notify(user, notify_id)
            # every user get notify to accept or decline

    users_id_go = Selector.select_users_on_event(event_id_to_go)
