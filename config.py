
# ------------------------
DATABASE = "postgres"
USERNAME = "postgres"
PASSWORD = "1234"
HOST = "127.0.0.1"
PORT = "5435"

# ------------------------
SCHEMA_NAME = "ITMO_Events"
TBL_EVENTS = "Events"
TBL_IMAGES = "Images"
TBL_USERS = "Users"
TBL_NOTIFIES = "Notifies"
TBL_NEWS = "News"

# ----------users--------------
# user_id
# user_name
# user_surname
# user_patronymic
# phone
# vk_link
# mail
# is_russian_citizenship
# score
# ban_date
# notify_id

# ----------events---------------
# event_id serial primary key not null
# event_name varchar
# time_start TIMESTAMP
# time_end TIMESTAMP
# description text
# url_pdf varchar
# people_count integer
# coefficient integer
# users_id_want integer[]
# users_id_go integer[]

# ----------images---------------
# event_id integer references %s.%s(event_id)
# image varchar

# ----------notifies---------------
# notify_id serial primary key not null
# time TIMESTAMP
# notify_header varchar
# notify_data text

# ----------news---------------
# news_id serial primary key not null
# header varchar
# data text
# time TIMESTAMP

