
from data_base.tbl_workers import UserWorker, EventWorker
from data_base.base import session


class Selector:

    @staticmethod
    def get_user_score(users_ids: list, local_session: session):
        users_score = {}
        for user_id in users_ids:
            users_score[user_id] = UserWorker.get(user_id, local_session)['score']
        return users_score

    @staticmethod
    def select_users_on_event(event_id: int, local_session: session):
        event = EventWorker.get(local_session, event_id)
        users_want = event["users_id_want"]
        users_go = event["users_id_go"]
        selected_users = {}
        if users_want:
            if users_go:
                people_count_to_select = event["people_count"] - event["users_is_go"].count()
            else:
                people_count_to_select = event["people_count"]

            users_want_with_score = Selector.get_user_score(users_want, local_session)

            sorted_applicants = dict(sorted(users_want_with_score.items(), key=lambda x: x[1]))
            print(sorted_applicants)
            selected_users = dict(list(sorted_applicants.items())[:people_count_to_select])
            print('selected_users:', list(selected_users))
        return list(selected_users)

