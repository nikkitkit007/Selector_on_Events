#!/usr/bin/python3

# https://metanit.com/sql/postgresql/5.1.php
# https://postgrespro.ru/docs/postgresql/9.6/plpython-database

# https://questu.ru/questions/31796332/ - really cool

import config
import psycopg2
import psycopg2.extras
from datetime import datetime


def open_close_connection(func):
    def the_wrapper_around_the_original_function(*args, **kwargs):
        self = args[0]
        self.open_connection()
        result = func(*args, **kwargs)
        self.close_connection()
        return result

    return the_wrapper_around_the_original_function


class DB_PostgreSQL(object):
    def __init__(self):
        try:
            self.connection = ''
            self.cur = ''
            # self.open_connection()

            self.schema_name = config.SCHEMA_NAME
            self.tbl_events = config.TBL_EVENTS
            self.tbl_images = config.TBL_IMAGES
            self.tbl_users = config.TBL_USERS
            self.tbl_notifies = config.TBL_NOTIFIES
            self.tbl_news = config.TBL_NEWS

        except Exception as E:
            print(E)

    def open_connection(self):
        self.connection = psycopg2.connect(database=config.DATABASE, user=config.USERNAME, password=config.PASSWORD,
                                           host=config.HOST,
                                           port=config.PORT)  # create connection
        self.cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)  # create cursor - object to manipulation with db
        # print("Successfully connection to database: \"%s\" for user \"%s\"" % (config.DATABASE, config.USERNAME))

    def close_connection(self):
        self.connection.close()

    @open_close_connection
    def create_db(self):
        self.create_schema()
        self.create_tables()

    def create_schema(self):  # creation schema 'Itmo_Events'
        try:
            self.cur.execute("""CREATE SCHEMA IF NOT EXISTS %s;""" % self.schema_name)
            self.connection.commit()

            print("Schema ITMO_Events created!")
        except Exception as E:
            print(E)

    def create_tables(self):
        try:
            # -------------------------Events-----------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                event_id serial primary key not null,
                event_name varchar(127),
                time_start TIMESTAMP,
                time_end TIMESTAMP,
                description text,
                url_pdf varchar(255),
                people_count integer,
                coefficient integer,
                users_id_want integer[],
                users_id_go integer[]
                );""" % (self.schema_name, self.tbl_events))
            self.connection.commit()
            print("Table Events created!")

            # -------------------------Images-----------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                image_id serial primary key not null,
                event_id integer references %s.%s(event_id),
                image varchar(127)
                );""" % (self.schema_name, self.tbl_images, self.schema_name, self.tbl_events))
            self.connection.commit()
            print("Table Images created!")

            # -------------------------Users-------------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                user_id integer primary key not null,
                user_name varchar(255),
                user_surname varchar(255),
                user_patronymic varchar(255),
                phone varchar(127),
                vk_link varchar(255),
                mail varchar(255),
                is_russian_citizenship bool,
                score integer DEFAULT 0,
                ban_date TIMESTAMP,
                notify_id integer[]
                );""" % (self.schema_name, self.tbl_users))
            self.connection.commit()
            print("Table Users created!")

            # -----------------------Notifies------------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                notify_id serial primary key not null,
                time TIMESTAMP,
                notify_header varchar(255),
                notify_data text
                );""" % (self.schema_name, self.tbl_notifies))
            self.connection.commit()
            print("Table Notifies created!")

            # -------------------------News--------------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                news_id serial primary key not null,
                header varchar(127),
                data text,
                time TIMESTAMP
                );""" % (self.schema_name, self.tbl_news))
            self.connection.commit()
            print("Table News created!")

        except Exception as E:
            print("Some errors with tables creation with error: {}".format(E))

    # -----DONE------------------------------USER-----------------------------------
    @open_close_connection
    def user_add(self, user_to_add):
        try:
            user_id = int(user_to_add['user_id'])
            user_name = user_to_add['user_name']
            user_surname = user_to_add['user_surname']
            user_patronymic = user_to_add['user_patronymic']
            phone = user_to_add['phone']
            vk_link = user_to_add['vk_link']
            mail = user_to_add['mail']
            is_russian_citizenship = user_to_add['is_russian_citizenship']
            # score = 0  # after all tests make = 0   user_to_add['score']

            self.cur.execute(
                """INSERT INTO %s.%s(user_id, user_name, user_surname, user_patronymic, phone, vk_link, mail, 
                is_russian_citizenship, score) 
                VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (
                    self.schema_name, self.tbl_users, user_id, user_name, user_surname,
                    user_patronymic, phone, vk_link, mail, is_russian_citizenship))
            self.connection.commit()

            print("User with id \"%s\" " % user_id + "added in table %s" % self.tbl_users)
        except Exception as E:
            print(E)

    @open_close_connection
    def user_get(self, user_id):
        # type(self.cur.fetchone())
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE user_id=%d""" % (
                self.schema_name, self.tbl_users, user_id))
        self.connection.commit()
        data = self.cur.fetchone()
        return data

    @open_close_connection
    def user_update(self, user_id, user_data_to_update):
        try:
            user_name = user_data_to_update['user_name']
            user_surname = user_data_to_update['user_surname']
            user_patronymic = user_data_to_update['user_patronymic']
            phone = user_data_to_update['phone']
            vk_link = user_data_to_update['vk_link']
            mail = user_data_to_update['mail']
            is_russian_citizenship = user_data_to_update['is_russian_citizenship']
            # notify_id = user_data_to_update['notify_id']

            self.cur.execute(
                """UPDATE %s.%s
                SET user_name = '%s',
                user_surname = '%s',
                user_patronymic = '%s',
                phone = '%s',
                vk_link = '%s',
                mail = '%s',
                is_russian_citizenship = '%s'
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, user_name, user_surname, user_patronymic,
                   phone, vk_link, mail, is_russian_citizenship, user_id))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_add_notify(self, user_id, notify_id):
        try:
            cur_user_notify_id = DB.user_get(user_id)['notify_id']
            self.open_connection()

            if cur_user_notify_id:
                cur_user_notify_id.append(notify_id)
                new_user_notify_id = str(set(cur_user_notify_id))
            else:
                new_user_notify_id = str({notify_id})

            self.cur.execute(
                """UPDATE %s.%s
                SET notify_id = '%s'
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, new_user_notify_id, user_id))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_del_notify(self, user_id, notify_id):
        try:
            cur_user_notify_id = DB.user_get(user_id)['notify_id']
            self.open_connection()

            cur_user_notify_id.remove(notify_id)
            new_user_notify_id = cur_user_notify_id
            new_user_notify_id = str(set(new_user_notify_id))

            self.cur.execute(
                """UPDATE %s.%s
                SET notify_id = '%s'
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, new_user_notify_id, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_ban_date(self, user_id, ban_date):
        try:
            self.cur.execute(
                """UPDATE %s.%s
                SET ban_date = '%s'
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, ban_date, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_score(self, user_id, score):
        try:
            self.cur.execute(
                """UPDATE %s.%s
                SET score = %d
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, score, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_delete(self, user_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE user_id = %s
                """ % (self.schema_name, self.tbl_users, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # ------DONE----------------------------EVENT-----------------------------------
    @open_close_connection
    def event_add(self, event_to_add):
        try:
            event_name = event_to_add['event_name']  # varchar
            time_start = event_to_add['time_start']  # TIMESTAMP
            time_end = event_to_add['time_end']  # TIMESTAMP
            description = event_to_add['description']  # text
            url_pdf = event_to_add['url_pdf']  # varchar
            people_count = event_to_add['people_count']
            coefficient = event_to_add['coefficient']

            self.cur.execute(
                """INSERT INTO %s.%s(event_name, time_start, time_end, description, url_pdf, people_count, coefficient) 
                VALUES ('%s', '%s', '%s', '%s', '%s', %d, %d);"""
                % (self.schema_name, self.tbl_events, event_name, time_start, time_end,
                   description, url_pdf, people_count, coefficient))
            self.connection.commit()

            print("Event \"%s\" " % event_name + "added")
        except Exception as E:
            print(E)

    @open_close_connection
    def event_get(self, event_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE event_id=%d"""
            % (self.schema_name, self.tbl_events, event_id))
        self.connection.commit()
        data = self.cur.fetchone()
        return data

    @open_close_connection
    def event_update(self, event_id, event_data_to_update):
        try:
            event_name = event_data_to_update["event_name"]
            time_start = event_data_to_update["time_start"]
            time_end = event_data_to_update["time_end"]
            description = event_data_to_update["description"]
            url_pdf = event_data_to_update["url_pdf"]
            people_count = event_data_to_update["people_count"]
            coefficient = event_data_to_update["coefficient"]
            users_id_want = event_data_to_update["users_id_want"]
            users_id_go = event_data_to_update["users_id_go"]

            if users_id_want:
                users_id_want = str(set(users_id_want))
            else:
                users_id_want = '{}'

            if users_id_go:
                users_id_go = str(set(users_id_go))
            else:
                users_id_go = '{}'

            self.cur.execute(
                """UPDATE %s.%s
                SET
                event_name = '%s',
                time_start = '%s',
                time_end = '%s',
                description = '%s',
                url_pdf = '%s',
                people_count = %d,
                coefficient = %d,
                users_id_want = '%s',
                users_id_go = '%s'         
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, event_name, time_start, time_end, description,
                       url_pdf, people_count, coefficient, users_id_want, users_id_go, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_update_add_users_id_want(self, event_id, user_id_want):
        try:
            cur_users_id_want_list = DB.event_get(event_id)["users_id_want"]
            self.open_connection()

            if cur_users_id_want_list:
                cur_users_id_want_list.append(user_id_want)
                # new_users_id_want_list = str(cur_users_id_want_list).replace('[', '{').replace(']', '}')
                new_users_id_want_list = str(set(cur_users_id_want_list))
            else:
                new_users_id_want_list = str({user_id_want})

            self.cur.execute(
                """UPDATE %s.%s
                SET users_id_want = '%s'
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, new_users_id_want_list, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_update_add_users_id_go(self, event_id, user_id_go):
        try:
            cur_users_id_go_list = DB.event_get(event_id)["users_id_go"]
            self.open_connection()

            if cur_users_id_go_list:
                cur_users_id_go_list.append(user_id_go)
                new_users_id_go_list = str(set(cur_users_id_go_list))
            else:
                new_users_id_go_list = str({user_id_go})

            self.cur.execute(
                """UPDATE %s.%s
                SET users_id_go = '%s'
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, new_users_id_go_list, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_update_del_users_id_want(self, event_id, user_id):
        try:
            cur_users_id_want_list = DB.event_get(event_id)["users_id_want"]
            DB.open_connection()

            cur_users_id_want_list.remove(user_id)
            new_users_id_want_list = cur_users_id_want_list
            new_users_id_want_list = str(set(new_users_id_want_list))

            self.cur.execute(
                """UPDATE %s.%s
                SET users_id_want = '%s'
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, new_users_id_want_list, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_delete(self, event_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE event_id = %s
                """ % (self.schema_name, self.tbl_events, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # -------------------------------IMAGE--------------------------------
    @open_close_connection
    def image_add(self, image_to_add):
        try:
            event_id = 0
            image = image_to_add['image']  # varchar

            self.cur.execute(
                """INSERT INTO %s.%s(event_id, image) 
                VALUES (%d, '%s');"""
                % (self.schema_name, self.tbl_images, event_id, image))
            self.connection.commit()

            print("Image for event with ID = \"%s\" " % event_id + "added")
        except Exception as E:
            print(E)

    @open_close_connection
    def image_get_by_id(self, image_id, event_id=False):
        if event_id:
            insert_query = """SELECT * FROM %s.%s WHERE event_id=%d;"""
        else:
            insert_query = """SELECT * FROM %s.%s WHERE image_id=%d;"""

        item_tuple = (self.schema_name, self.tbl_images, image_id)
        self.cur.execute(insert_query, item_tuple)
        self.connection.commit()
        data = self.cur.fetchall()
        all_data = []
        for row in data:
            all_data.append(dict(row))
        return all_data

    @open_close_connection
    def image_update(self, image_data_to_update, event_id):
        try:
            self.cur.execute(
                """UPDATE %s.%s
                SET image = %s
                WHERE event_id = %d;
                """ % (self.schema_name, self.tbl_images, image_data_to_update, event_id))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def image_delete(self, id_to_delete, event_id=False):
        if event_id:
            insert_query = """DELETE FROM %s.%s WHERE event_id = %d;"""
        else:
            insert_query = """DELETE FROM %s.%s WHERE image_id = %d;"""

        item_tuple = (self.schema_name, self.tbl_images, id_to_delete)

        try:
            self.cur.execute(insert_query, item_tuple)
            self.connection.commit()
        except Exception as E:
            print(E)

    # -------------------------------NOTIFIES--------------------------------
    @open_close_connection
    def notify_add(self, notify_to_add):
        try:
            time = notify_to_add['time']  # TIMESTAMP
            notify_header = notify_to_add['notify_header']  # varchar
            notify_data = notify_to_add['notify_data']  # text

            self.cur.execute(
                """INSERT INTO %s.%s(time, notify_header, notify_data) 
                VALUES ('%s', '%s', '%s');"""
                % (self.schema_name, self.tbl_notifies, time, notify_header, notify_data))
            self.connection.commit()

            print("Notify with header \"%s\" " % notify_header + "added")
        except Exception as E:
            print(E)

    @open_close_connection
    def notify_get(self, notify_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE notify_id=%d;""" % (
                self.schema_name, self.tbl_notifies, notify_id))
        self.connection.commit()
        data = self.cur.fetchone()
        return data

    @open_close_connection
    def notify_update(self, notify_id, notify_data_to_update):
        try:
            time = notify_data_to_update['time']
            notify_header = notify_data_to_update['notify_header']
            notify_data = notify_data_to_update['notify_data']

            self.cur.execute(
                """UPDATE %s.%s
                SET time = '%s',
                notify_header = '%s',
                notify_data = '%s'
                WHERE notify_id = %d;
                """
                % (self.schema_name, self.tbl_notifies, time, notify_header, notify_data, notify_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def notify_delete(self, notify_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE notify_id = %d;
                """ % (self.schema_name, self.tbl_notifies, notify_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # -------------------------------NEWS--------------------------------
    @open_close_connection
    def news_add(self, news_to_add):
        # header varchar
        # data text
        # time TIMESTAMP
        try:
            header = news_to_add['header']  # varchar
            data = news_to_add['data']  # text
            time = news_to_add['time']  # TIMESTAMP

            self.cur.execute(
                """INSERT INTO %s.%s(header, data, time) 
                VALUES ('%s', '%s', '%s');"""
                % (self.schema_name, self.tbl_news, header, data, time))
            self.connection.commit()

            print("News \"%s\" " % header + "added")
        except Exception as E:
            print(E)

    @open_close_connection
    def get_news(self, news_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE news_id=%d;""" % (
                self.schema_name, self.tbl_news, news_id))
        self.connection.commit()
        data = self.cur.fetchone()
        return data

    @open_close_connection
    def news_update(self, news_data_to_update):
        try:
            event_SOMETHING = news_data_to_update
            self.cur.execute(
                """UPDATE %s.%s
                SET att_name = %s;
                """ % (self.schema_name, self.tbl_news, event_SOMETHING))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def news_delete(self, news_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE news_id = %d;
                """ % (self.schema_name, self.tbl_news, news_id))
            self.connection.commit()
        except Exception as E:
            print(E)


# done
def user_test():
    # ---------------USER-test------------------
    test_user = {'user_id': 1,
                 'user_name': 'Nik',
                 'user_surname': 'Sul',
                 'user_patronymic': 'Serg',
                 'phone': '8991',
                 'vk_link': 'http://',
                 'mail': 'nikkitkit@mail.ru',
                 'is_russian_citizenship': True}

    upd_test_user1 = {'user_id': 1,
                      'user_name': 'Nik',
                      'user_surname': 'Sul',
                      'user_patronymic': 'Serg',
                      'phone': '11111111111111111',
                      'vk_link': 'http://',
                      'mail': 'nikkitkit@mail.ru',
                      'is_russian_citizenship': False}

    upd_test_user2 = {'user_id': 1,
                      'user_name': 'Nik',
                      'user_surname': 'Sul',
                      'user_patronymic': 'Serg',
                      'phone': '222222222222',
                      'vk_link': 'http://',
                      'mail': 'nikkitkit@mail.ru',
                      'is_russian_citizenship': True, }

    # DB.add_user(test_user)

    user_id_test = 1

    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))
    # # print(user1['user_id'])
    #
    # DB.user_update(user_id_test, upd_test_user1)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))

    # # add notify -----------------------------------
    # DB.user_update_add_notify(user_id_test, 1)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))

    # # delete notify -----------------------------------
    # DB.user_update_del_notify(user_id_test, 1)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))

    # # add ban_date -----------------------------------
    # ban = datetime.now()
    # print(ban)
    # DB.user_update_ban_date(user_id_test, ban)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))

    # # add score -----------------------------------
    # scr = 100
    # DB.user_update_score(user_id_test, scr)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))

    # DB.user_delete(user_id_test)
    # user1 = DB.user_get(user_id_test)
    # print(dict(user1))            # !ERROR because it's none


# done
def event_test():
    # ---------------EVENT-test------------------
    test_event = {'event_name': 'TEST',
                  'time_start': '01-01-2022 00:00:00',
                  'time_end': '01-01-2022 00:00:10',
                  'description': 'Simple test',
                  'url_pdf': 'http://lol',
                  'people_count': 10,
                  'coefficient': 50}
    upd_test_event1 = {'event_name': 'TEST_upd',
                       'time_start': '01-01-2022 00:00:00',
                       'time_end': '01-01-2022 00:00:10',
                       'description': 'Simple test',
                       'url_pdf': 'http://lol',
                       'people_count': 10,
                       'coefficient': 50,
                       'users_id_want': [10, 12, 45],
                       'users_id_go': []}
    upd_test_event2 = {'event_name': 'TEST_lol',
                       'time_start': '01-01-2022 00:00:00',
                       'time_end': '01-01-2022 00:00:10',
                       'description': 'Simple test',
                       'url_pdf': 'http://lol',
                       'people_count': 10,
                       'coefficient': 50,
                       'users_id_want': [11, 12, 10, 100, 1000],
                       'users_id_go': []}

    event_id = 1
    # DB.event_add(test_event)
    event1 = DB.event_get(event_id)
    print(dict(event1))

    DB.event_update(event_id, upd_test_event2)

    event1 = DB.event_get(event_id)
    print(dict(event1))

    # DB.event_update_add_users_id_want(event_id, 99)
    # event1 = DB.event_get(event_id)
    # print(dict(event1))

    # DB.event_update_del_users_id_want(event_id, 101)
    # event1 = DB.event_get(event_id)
    # print(dict(event1))
    # DB.event_delete(1)


def image_test():
    pass


# done
def notify_test():
    test_notify = {'time': '01-01-2022 00:00:00',
                   'notify_header': 'I am test notify',
                   'notify_data': 'Cool notify'}

    upd_test_notify = {'time': '01-01-2022 00:00:00',
                       'notify_header': 'I updated test notify!!!!!',
                       'notify_data': 'WOW'}
    notify_id = 1
    DB.notify_add(test_notify)
    notify = DB.notify_get(notify_id)
    print(dict(notify))

    DB.notify_update(1, upd_test_notify)
    notify = DB.notify_get(notify_id)
    print(dict(notify))
    # DB.notify_delete(1)


def news_test():
    test_news = {'header': 'I am test news', 'data': 'Lets go!', 'time': '01-01-2022 00:00:00'}

    DB.news_add(test_news)
    news1 = DB.get_news(1)
    try:
        print(dict(news1))
    except:
        print("Not found")
    DB.news_delete(1)


if __name__ == "__main__":
    DB = DB_PostgreSQL()
    # DB.create_db()

    # user_test()
    # event_test()

    # image_test()
    # news_test()
    # notify_test()
