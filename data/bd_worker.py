#!/usr/bin/python3

# https://metanit.com/sql/postgresql/5.1.php

import config
import psycopg2
import re


def check_mail(mail_address):
    regex_mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex_mail, mail_address):
        return True
    else:
        return False


def check_phone(phone):
    regex_phone = re.compile(r'')
    if re.fullmatch(regex_phone, phone):
        return True
    else:
        return False


class DB_PostgreSQL(object):

    def __init__(self, db, usr, passwd, host_adr, port_value):  # connect to db
        try:
            self.connection = psycopg2.connect(database=db, user=usr, password=passwd, host=host_adr,
                                               port=port_value)  # create connection
            self.cur = self.connection.cursor()  # create cursor - object to manipulation with db

            print("Successfully connection to database: \"%s\" for user \"%s\"\n" % (db, usr))

            self.schema_name = config.SCHEMA_NAME
            self.tbl_events = config.TBL_EVENTS
            self.tbl_images = config.TBL_IMAGES
            self.tbl_users = config.TBL_USERS
            self.tbl_notifies = config.TBL_NOTIFIES
            self.tbl_news = config.TBL_NEWS


        except Exception as E:
            print(E)

    def create_db(self):
        self.create_schema(self.schema_name)
        self.create_tables(self.schema_name, self.tbl_events, self.tbl_images, self.tbl_users, self.tbl_notifies, self.tbl_news)

    def create_schema(self, schema_name="ITMO_Events"):  # creation schema 'Itmo_Events'
        try:
            self.cur.execute("CREATE SCHEMA IF NOT EXISTS %s;" % schema_name)
            self.connection.commit()

            print("Schema ITMO_Events created!")
        except Exception as E:
            print(E)

    def create_tables(self, schema_name, tbl_events, tbl_images, tbl_users,
                      tbl_notifies, tbl_news):
        try:
            # -------------------------Events-----------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
    event_id serial primary key not null,
event_name char,
time_start TIMESTAMP,
time_end TIMESTAMP,
description text,
url_pdf char,
users_id_want integer[],
users_id_go integer[]
);""" % (schema_name, tbl_events))
            self.connection.commit()
            print("Table Events created!")

            # -------------------------Images-----------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
    event_id integer references %s.%s(event_id),
image char
);""" % (schema_name, tbl_images, schema_name, tbl_events))
            self.connection.commit()
            print("Table Images created!")

            # -------------------------Users-------------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
    user_id integer primary key not null,
user_name char,
user_surname char,
user_patronymic char,
phone char,
vk_link char,
mail char,
citizenship bool,
score integer,
ban_date TIMESTAMP,
notify_id integer[]
);""" % (schema_name, tbl_users))
            self.connection.commit()
            print("Table Users created!")

            # -----------------------Notifies------------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
    notify_id serial primary key not null,
time TIMESTAMP,
notify_header char,
notify_data text
);""" % (schema_name, tbl_notifies))
            self.connection.commit()
            print("Table Notifies created!")

            # --------------------News----------------------------
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS %s.%s(
    header char,
    data text,
    time TIMESTAMP
    );""" % (schema_name, tbl_news))
            self.connection.commit()
            print("Table News created!")

        except Exception as E:
            print("Some errors with tables creation with error: {}".format(E))

    def close_connection(self):
        self.connection.close()
        print("\nConnection close")

    def add_user(self, user_to_add, schema_name="ITMO_Events", tbl_users="Users"):

        user_id = user_to_add['user_id']
        user_name = user_to_add['user_name']
        user_surname = user_to_add['user_surname']
        user_patronymic = user_to_add['user_patronymic']
        phone = user_to_add['phone']
        vk_link = user_to_add['vk_link']
        mail = user_to_add['mail']
        citizenship = user_to_add['citizenship']
        # score = user_to_add['score']
        score = 0
        ban_date = user_to_add['ban_date']
        notify_id = user_to_add['notify_id']

        self.cur.execute(
            """INSERT INTO %s.%s(user_id, user_name, user_surname, user_patronymic, phone, vk_link, mail, 
            citizenship, score, ban_date, notify_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""" % (
                schema_name, tbl_users, user_id, user_name, user_surname, user_patronymic, phone, vk_link, mail,
                citizenship, score, ban_date, notify_id))
        self.connection.commit()
        print("Table Events created!")

        print("User with id \"%s\"" % user_id + "added in table %s" % tbl_users)
        pass


if __name__ == "__main__":
    database = config.DATABASE
    username = config.USERNAME
    password = config.PASSWORD
    host = config.HOST
    port = config.PORT

    DB = DB_PostgreSQL(database, username, password, host, port)
    DB.create_db()

    example_user_to_add = {"user_id": 1, "user_name": "Nik", "user_surname": "Sul", "user_patronymic": "Serg" , "phone": "8991", "vk_link": "http://", "mail": "nikkitkit@mail.ru",
            "citizenship": "1", "score": 0, "ban_date": "", "notify_id": []}
    DB.add_user(123)

    DB.close_connection()

    # DB.add_user("people", "Nik", "Sulimenko", 20,"student")
    # DB.delete_user("people", "Nik", "Sulimenko")

    # rows = DB.get_table_rows("people")

    # DB.add_user("people", "Nik", "Sulimenko", 20,"student")
