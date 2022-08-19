#!/usr/bin/python3

# https://metanit.com/sql/postgresql/5.1.php
# https://postgrespro.ru/docs/postgresql/9.6/plpython-database

import config
import psycopg2

# проверить varchar в таблицах


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
        self.cur = self.connection.cursor()  # create cursor - object to manipulation with db
        # print("Successfully connection to database: \"%s\" for user \"%s\"" % (config.DATABASE, config.USERNAME))

    def close_connection(self):
        self.connection.close()
        # print("Connection close\n")

    def open_close_connection(func):
        def the_wrapper_around_the_original_function(*args, **kwargs):
            self = args[0]
            self.open_connection()
            result = func(*args, **kwargs)
            self.close_connection()
            return result

        return the_wrapper_around_the_original_function

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
                score integer,
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

    # -----------------------------------USER-----------------------------------
    @open_close_connection
    def add_user(self, user_to_add):
        try:
            user_id = int(user_to_add['user_id'])
            user_name = user_to_add['user_name']
            user_surname = user_to_add['user_surname']
            user_patronymic = user_to_add['user_patronymic']
            phone = user_to_add['phone']
            vk_link = user_to_add['vk_link']
            mail = user_to_add['mail']
            is_russian_citizenship = user_to_add['is_russian_citizenship']
            score = 0

            self.cur.execute(
                """INSERT INTO %s.%s(user_id, user_name, user_surname, user_patronymic, phone, vk_link, mail, 
                is_russian_citizenship, score) 
                VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d);""" % (
                    self.schema_name, self.tbl_users, user_id, user_name, user_surname,
                    user_patronymic, phone, vk_link, mail, is_russian_citizenship, score))
            self.connection.commit()

            print("User with id \"%s\" " % user_id + "added in table %s" % self.tbl_users)
        except Exception as E:
            print(E)

    @open_close_connection
    def get_user(self, user_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE user_id=%d""" % (
                self.schema_name, self.tbl_users, user_id))
        self.connection.commit()
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def update_user(self, user_data_to_update):
        try:
            user_SOMETHING = user_data_to_update
            self.cur.execute(
                """UPDATE %s.%s
                SET att_name = %s
                """ % (self.schema_name, self.tbl_users, user_SOMETHING))
            self.connection.commit()            # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def delete_user(self, user_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE user_id = %s
                """ % (self.schema_name, self.tbl_users, user_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # ----------------------------------EVENT-----------------------------------
    @open_close_connection
    def add_event(self, event_to_add):
        try:
            event_name = event_to_add['event_name']  # varchar
            time_start = event_to_add['time_start']  # TIMESTAMP
            time_end = event_to_add['time_end']  # TIMESTAMP
            description = event_to_add['description']  # text
            url_pdf = event_to_add['url_pdf']  # varchar
            people_count = event_to_add['people_count']
            coefficient = event_to_add['coefficient']
            # users_id_want integer[]
            # users_id_go integer[]

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
    def get_event(self, event_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE event_id=%d""" % (
                self.schema_name, self.tbl_users, event_id))
        self.connection.commit()
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def update_event(self, event_id, event_data_to_update):
        try:
            event_SOMETHING = event_data_to_update
            self.cur.execute(
                """UPDATE %s.%s
                SET att_name = %s
                where event_id = %d
                """ % (self.schema_name, self.tbl_users, event_SOMETHING, event_id))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def delete_event(self, event_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE event_id = %s
                """ % (self.schema_name, self.tbl_users, event_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # -------------------------------IMAGE--------------------------------
    @open_close_connection
    def add_image(self, image_to_add):
        try:
            # event_id integer references % s. % s(event_id)
            # image varchar
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
    def get_image_by_id(self, id_to_get, event_id=False):
        if event_id:
            insert_query = """SELECT * FROM %s.%s WHERE event_id=%d;"""
        else:
            insert_query = """SELECT * FROM %s.%s WHERE image_id=%d;"""

        item_tuple = (self.schema_name, self.tbl_images, id_to_get)
        self.cur.execute(insert_query, item_tuple)
        self.connection.commit()
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def update_image(self, image_data_to_update, event_id):
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
    def delete_image(self, id_to_delete, event_id=False):
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
    def add_notify(self, notify_to_add):
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
    def get_notify(self, notify_id):
        self.cur.execute(
            """SELECT * FROM %s.%s WHERE notify_id=%d;""" % (
                self.schema_name, self.tbl_notifies, notify_id))
        self.connection.commit()
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def update_notify(self, notify_data_to_update):
        try:
            event_SOMETHING = notify_data_to_update
            self.cur.execute(
                """UPDATE %s.%s
                SET att_name = %s;
                """ % (self.schema_name, self.tbl_notifies, event_SOMETHING))
            self.connection.commit()  # добавить вместо att_name массив и в цикле делать апдейт
        except Exception as E:
            print(E)

    @open_close_connection
    def delete_notify(self, notify_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE notify_id = %s;
                """ % (self.schema_name, self.tbl_notifies, notify_id))
            self.connection.commit()
        except Exception as E:
            print(E)

    # -------------------------------NEWS--------------------------------
    @open_close_connection
    def add_news(self, news_to_add):
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
        data = self.cur.fetchall()
        return data

    @open_close_connection
    def update_news(self, news_data_to_update):
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
    def delete_news(self, news_id):
        try:
            self.cur.execute(
                """DELETE FROM %s.%s
                WHERE news_id = %d;
                """ % (self.schema_name, self.tbl_news, news_id))
            self.connection.commit()
        except Exception as E:
            print(E)


if __name__ == "__main__":

    DB = DB_PostgreSQL()
    DB.create_db()

    example_user_to_add = {'user_id': 1, 'user_name': 'Nik', 'user_surname': 'Sul', 'user_patronymic': 'Serg',
                           'phone': '8991', 'vk_link': 'http://', 'mail': 'nikkitkit@mail.ru',
                           'is_russian_citizenship': True}

    DB.add_user(example_user_to_add)
    user_id_test = 1

    # DB.delete_user(user_id_test)
    print(DB.get_user(user_id_test))
