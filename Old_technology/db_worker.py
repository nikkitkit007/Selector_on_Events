#!/usr/bin/python3

# https://metanit.com/sql/postgresql/5.1.php
# https://postgrespro.ru/docs/postgresql/9.6/plpython-database

# https://questu.ru/questions/31796332/ - really cool

import config
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


def open_close_connection(func):
    def the_wrapper_around_the_original_function(*args, **kwargs):
        self = args[0]
        self.open_connection()
        result = func(*args, **kwargs)
        self.close_connection()
        return result

    return the_wrapper_around_the_original_function


class DataBaseEvents(object):
    def __init__(self):
        self.connection = ''
        self.cur = ''

        self.schema_name = config.SCHEMA_NAME

        self.tbl_events = config.TBL_EVENTS
        self.tbl_users = config.TBL_USERS
        self.tbl_notifies = config.TBL_NOTIFIES
        self.tbl_news = config.TBL_NEWS

        self.database = config.DATABASE
        self.user = config.USERNAME
        self.password = config.PASSWORD
        self.host = config.HOST
        self.port = config.PORT

    def open_connection(self):
        self.connection = psycopg2.connect(database=self.database,
                                           user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           port=self.port)  # create connection
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

            info_logger.info("Schema ITMO_Events created!")
        except Exception as E:
            error_logger.error(E)

    def create_tables(self):
        self.create_table_events()
        self.create_table_notifies()
        self.create_table_users()
        self.create_table_news()

    # ---------------------------------------TABLES----------------------------------
    def create_table_events(self):
        try:
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
                users_id_go integer[],
                image varchar(127)
                );""" % (self.schema_name, self.tbl_events))
            self.connection.commit()
            print("Table Events created!")
        except Exception as E:
            print("Some errors with tables creation with error: {}".format(E))

    def create_table_users(self):
        try:
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                user_id serial primary key not null,
                user_isu_number integer UNIQUE,
                user_name varchar(255),
                user_surname varchar(255),
                user_patronymic varchar(255),
                phone varchar(127),
                vk_link varchar(255),
                mail varchar(255),
                is_russian_citizenship bool,
                score integer DEFAULT 0,
                ban_date TIMESTAMP,
                notify_id integer[],
                time_select_finish TIMESTAMP
                );""" % (self.schema_name, self.tbl_users))
            self.connection.commit()
            print("Table Users created!")
        except Exception as E:
            print("Some errors with tables creation with error: {}".format(E))

    def create_table_notifies(self):
        try:
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                notify_id serial primary key not null,
                event_id integer,
                time TIMESTAMP,
                notify_header varchar(255),
                notify_data text
                );""" % (self.schema_name, self.tbl_notifies))
            self.connection.commit()
            print("Table Notifies created!")
        except Exception as E:
            print("Some errors with tables creation with error: {}".format(E))

    def create_table_news(self):
        try:
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
                news_id serial primary key not null,
                header varchar(127),
                data_base text,
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
            user_isu_number = int(user_to_add['user_isu_number'])
            user_name = user_to_add['user_name']
            user_surname = user_to_add['user_surname']
            user_patronymic = user_to_add['user_patronymic']
            phone = user_to_add['phone']
            vk_link = user_to_add['vk_link']
            mail = user_to_add['mail']
            is_russian_citizenship = user_to_add['is_russian_citizenship']
            # score = 0  # after all tests make = 0   user_to_add['score']

            self.cur.execute(
                """INSERT INTO %s.%s(user_isu_number, user_name, user_surname, user_patronymic, 
                phone, vk_link, mail, is_russian_citizenship) 
                VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s');"""
                % (self.schema_name, self.tbl_users, user_isu_number, user_name, user_surname,
                    user_patronymic, phone, vk_link, mail, is_russian_citizenship))
            self.connection.commit()

            print("User with id \"%s\" " % user_isu_number + "added in table %s" % self.tbl_users)
        except Exception as E:
            return E

    def _user_get(self, user_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE user_id=%d""" % (
                self.schema_name, self.tbl_users, user_id))
        self.connection.commit()
        data = self.cur.fetchone()
        return data

    @open_close_connection
    def user_get(self, user_id):
        return self._user_get(user_id)

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
    def user_update_add_notify(self, user_id: int, notify_id: int, time_now):
        try:
            cur_user_notify_id = self._user_get(user_id)['notify_id']
            # self.open_connection()

            if cur_user_notify_id:
                cur_user_notify_id.append(notify_id)
                new_user_notify_id = str(set(cur_user_notify_id))
            else:
                new_user_notify_id = str({notify_id})

            self.cur.execute(
                """UPDATE %s.%s
                SET notify_id = '%s',
                time_select_finish = '%s'
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, new_user_notify_id, time_now, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_del_notify(self, user_id, notify_id):
        try:
            cur_user_notify_id = DB._user_get(user_id)['notify_id']
            # self.open_connection()

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
    def user_update_add_score(self, user_id, score):
        try:
            user_score = self._user_get(user_id)['score']
            # self.open_connection()

            user_score += score

            self.cur.execute(
                """UPDATE %s.%s
                SET score = %d
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, user_score, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_update_del_timer(self, user_id):
        try:
            self.cur.execute(
                """UPDATE %s.%s
                SET time_select_finish = Null
                WHERE user_id = %d;
                """
                % (self.schema_name, self.tbl_users, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def user_delete(self, user_id):
        self.cur.execute(
            """DELETE FROM %s.%s
            WHERE user_id = %s
            """ % (self.schema_name, self.tbl_users, user_id))
        self.connection.commit()

    # ------DONE----------------------------EVENT-----------------------------------
    @open_close_connection
    def event_add(self, event_to_add):
        event_name = event_to_add['event_name']  # varchar
        time_start = event_to_add['time_start']  # TIMESTAMP
        time_end = event_to_add['time_end']  # TIMESTAMP
        description = event_to_add['description']  # text
        url_pdf = event_to_add['url_pdf']  # varchar
        people_count = event_to_add['people_count']
        coefficient = event_to_add['coefficient']
        image = event_to_add['image']

        self.cur.execute(
            """INSERT INTO %s.%s(event_name, time_start, time_end, description, url_pdf, people_count, coefficient, image) 
            VALUES ('%s', '%s', '%s', '%s', '%s', %d, %d, '%s');"""
            % (self.schema_name, self.tbl_events, event_name, time_start, time_end,
               description, url_pdf, people_count, coefficient, image))
        self.connection.commit()

        print("Event \"%s\" " % event_name + "added")

    def _event_get(self, event_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE event_id=%d"""
            % (self.schema_name, self.tbl_events, event_id))
        self.connection.commit()
        data = self.cur.fetchone()
        if data:
            return data
        return False

    @open_close_connection
    def event_get(self, event_id):
        return self._event_get(event_id)

    @open_close_connection
    def event_get_all(self):
        self.cur.execute(
            """SELECT * FROM %s.%s"""
            % (self.schema_name, self.tbl_events))
        self.connection.commit()
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def event_update(self, event_id, event_data_to_update):
        try:
            event_name = event_data_to_update["event_name"]
            time_start = event_data_to_update["time_start"]
            time_end = event_data_to_update["time_end"]
            description = event_data_to_update["description"]
            url_pdf = event_data_to_update["url_pdf"]
            people_count = int(event_data_to_update["people_count"])
            coefficient = int(event_data_to_update["coefficient"])
            image = event_data_to_update['image']

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
                image = '%s'         
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, event_name, time_start, time_end, description,
                       url_pdf, people_count, coefficient, image, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_update_add_users_id_want(self, event_id, user_id_want):
        try:
            cur_users_id_want_list = self._event_get(event_id)["users_id_want"]
            # self.open_connection()

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
            cur_users_id_go_list = self._event_get(event_id)["users_id_go"]
            # self.open_connection()

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
            cur_users_id_want_list = self._event_get(event_id)["users_id_want"]
            # self.open_connection()

            cur_users_id_want_list.remove(user_id)
            if cur_users_id_want_list:
                new_users_id_want_list = str(set(cur_users_id_want_list))
            else:
                new_users_id_want_list = {}

            self.cur.execute(
                """UPDATE %s.%s
                SET users_id_want = '%s'
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, new_users_id_want_list, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_update_del_users_id_go(self, event_id, user_id):
        try:
            cur_users_id_go_list = DB._event_get(event_id)["users_id_go"]
            # DB.open_connection()

            cur_users_id_go_list.remove(user_id)
            new_users_id_go_list = cur_users_id_go_list
            new_users_id_go_list = str(set(new_users_id_go_list))

            self.cur.execute(
                """UPDATE %s.%s
                SET users_id_go = '%s'
                where event_id = %d;
                """ % (self.schema_name, self.tbl_events, new_users_id_go_list, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    @open_close_connection
    def event_delete(self, event_id):
        self.cur.execute(
            """DELETE FROM %s.%s
            WHERE event_id = %s;
            """ % (self.schema_name, self.tbl_events, event_id))
        self.connection.commit()

    # -------------------------------NOTIFIES--------------------------------
    @open_close_connection
    def notify_add(self, notify_to_add):
        try:
            event_id = notify_to_add['event_id']
            # time = notify_to_add['time']  # TIMESTAMP
            time = datetime.now()
            notify_header = notify_to_add['notify_header']  # varchar
            notify_data = notify_to_add['notify_data']  # text

            self.cur.execute(
                """INSERT INTO %s.%s(event_id, time, notify_header, notify_data) 
                VALUES (%d, '%s', '%s', '%s');"""
                % (self.schema_name, self.tbl_notifies, event_id, time, notify_header, notify_data))
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
    def notify_get_for_event(self, event_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE event_id=%d;""" % (
                self.schema_name, self.tbl_notifies, event_id))
        self.connection.commit()
        data = self.cur.fetchall()
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
        self.cur.execute(
            """DELETE FROM %s.%s
            WHERE notify_id = %d;
            """ % (self.schema_name, self.tbl_notifies, notify_id))
        self.connection.commit()

    # -------------------------------NEWS--------------------------------
    @open_close_connection
    def news_add(self, news_to_add):
        # header varchar
        # data_base text
        # time TIMESTAMP
        try:
            header = news_to_add['header']  # varchar
            data = news_to_add['data_base']  # text
            time = news_to_add['time']  # TIMESTAMP

            self.cur.execute(
                """INSERT INTO %s.%s(header, data_base, time) 
                VALUES ('%s', '%s', '%s');"""
                % (self.schema_name, self.tbl_news, header, data, time))
            self.connection.commit()

            print("News \"%s\" " % header + "added")
        except Exception as E:
            print(E)

    @open_close_connection
    def news_get(self, news_id):
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
        self.cur.execute(
            """DELETE FROM %s.%s
            WHERE news_id = %d;
            """ % (self.schema_name, self.tbl_news, news_id))
        self.connection.commit()


# done
def user_test():
    # ---------------USER-test------------------
    test_user = {'user_isu_number': 284678,
                 'user_name': 'LOL',
                 'user_surname': 'Sul',
                 'user_patronymic': 'Serg',
                 'phone': '8918',
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

    DB.user_add(test_user)

    user_id_test = 2

    # user1 = DB.get(user_id_test)
    # print(dict(user1))
    # # print(user1['user_id'])

    # DB.update(user_id_test, upd_test_user1)
    # user1 = DB.get(user_id_test)
    # print(dict(user1))

    # # add notify -----------------------------------
    # DB.update_add_notify(user_id_test, 1, datetime.now())
    # user1 = DB.get(user_id_test)
    # print(dict(user1))

    # # delete notify -----------------------------------
    # DB.update_del_notify(user_id_test, 1)
    # user1 = DB.get(user_id_test)
    # print(dict(user1))

    # # add ban_date -----------------------------------
    # ban = datetime.now() + timedelta(10)
    # print(ban)
    # DB.update_ban_date(user_id_test, ban)
    # user1 = DB.get(user_id_test)
    # print(dict(user1))

    # # add score -----------------------------------
    # scr = 100
    # DB.update_add_score(user_id_test, scr)
    # user1 = DB.get(user_id_test)
    # print(dict(user1))

    # DB.delete(user_id_test)
    # user1 = DB.get(user_id_test)
    # print(dict(user1))            # !ERROR because it's none


# done
def event_test():
    # ---------------EVENT-test------------------

    test_event = {'event_name': 'TEST',
                  'time_start': '09-08-2022 00:00:00',
                  'time_end': '09-10-2022 00:00:10',
                  'description': 'Simple test',
                  'url_pdf': 'http://lol',
                  'people_count': 10,
                  'coefficient': 50,
                  'image': '/images/lol/lal.jpeg'}
    upd_test_event1 = {'event_name': 'TEST_upd',
                       'time_start': '01-01-2022 00:00:00',
                       'time_end': '01-01-2022 00:00:10',
                       'description': 'Simple test',
                       'url_pdf': 'http://lol',
                       'people_count': 10,
                       'coefficient': 50,
                       'image': '/images/lol/lal.jpeg'}
    upd_test_event2 = {'event_name': 'TEST_lol',
                       'time_start': '01-01-2022 00:00:00',
                       'time_end': '01-01-2022 00:00:10',
                       'description': 'Simple test',
                       'url_pdf': 'http://lol',
                       'people_count': 10,
                       'coefficient': 50,
                       'image': '/images/lol/lal.jpeg'}

    event_id = 1
    # DB.add(test_event)
    # event1 = DB.get(event_id)
    # print(dict(event1))
    #
    DB.event_update(event_id, upd_test_event2)
    #
    event1 = DB.event_get(event_id)
    print(dict(event1))

    # DB.update_add_users_id_want(event_id, 99)
    # event1 = DB.get(event_id)
    # print(dict(event1))

    # DB.update_del_users_id_want(event_id, 101)
    # event1 = DB.get(event_id)
    # print(dict(event1))

    # DB.update_add_users_id_go(event_id, 99)
    # event1 = DB.get(event_id)
    # print(dict(event1))

    # DB.update_del_users_id_go(event_id, 101)
    # event1 = DB.get(event_id)
    # print(dict(event1))

    # DB.event_delete(1)


# done
def notify_test():
    test_notify = {'event_id': 4,
                   'time': '01-01-2022 00:00:00',
                   'notify_header': 'I am test notify',
                   'notify_data': 'Cool notify'}

    upd_test_notify = {'time': '01-01-2022 00:00:00',
                       'notify_header': 'I updated test notify!!!!!',
                       'notify_data': 'WOW'}
    notify_id = 1

    DB.notify_add(test_notify)
    notify = DB.notify_get(notify_id)
    print(dict(notify))

    DB.notify_update(notify_id, upd_test_notify)
    notify = DB.notify_get(notify_id)
    print(dict(notify))
    # DB.delete(1)


def news_test():
    test_news = {'header': 'I am test news',
                 'data_base': 'Lets go!',
                 'time': '01-01-2022 00:00:00'}

    DB.news_add(test_news)
    news1 = DB.news_get(1)
    print(dict(news1))

    DB.news_delete(1)


if __name__ == "__main__":
    DB = DataBaseEvents()
    # DB.create_db()

    # user_test()

    # DB.update_add_users_id_want(4, 1)

    # event_test()

    # news_test()
    # notify_test()
