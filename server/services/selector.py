import data.db_worker as db
# select who goes on event


"""
добавление user_id в поле users_id_want из таблицы Events
в определенный момент времени (например за 3 дня до поездки)
формруется список users_id_go из таблицы Events
рассылаются уведомления по user_id
если user подтверждает - то ему начисляется score += coefficient
если user откланяет - то ему начисляется score += coefficient и ban_date
и происходит оповещение user из списка user_id_want

"""
DB = db.DB_PostgreSQL()


def get_user_score(users_ids):
    user_score = {}
    for user_id in users_ids:
        user_score[user_id] = DB.get_user(int(user_id))['score']
    return user_score


# mass from Events
users_id_want = [1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1020, 1021, 1022, 1023]

user_want_to_go_score = get_user_score(users_id_want)
print(user_want_to_go_score)

# dict = {}
# lol = 12
# dict[lol] = 12
# print(dict)

# people_count = 10
# users_id_go = users_id_want[:people_count]
#
# print(users_id_go)
