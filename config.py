
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

# ------------------------
TIME_TO_POST_EVENT = 10
TIME_TO_FIRST_APPLICANTS = TIME_TO_POST_EVENT - 3
TIME_TO_ACCEPT = 1                  # 1 day

BAN_TIME_LATE = 1                   # 1 year
BAN_TIME_IGNORE = 2                 # 2 year

# ----------REGEX--------------
REGEX_MAIL = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
REGEX_PHONE = r"?:\(?(\d{3})\)?)?(?:\s|-)?(\d{3})(?:\s|-)?(\d{2})(?:\s|-)?(\d{2})(?:\s*доб[.а-я]*\s*(\d{2,5}))?"

# ----------users--------------
# user_id integer primary key not null
# user_name varchar(255)
# user_surname varchar(255)
# user_patronymic varchar(255)
# phone varchar(127)
# vk_link varchar(255)
# mail varchar(255)
# is_russian_citizenship bool
# score integer
# ban_date TIMESTAMP
# notify_id integer[]

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
# image_id serial primary key not null
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

# -----------------------------------
# ----------server_func--------------
# event_add
# event_update
# event_get
#
# apply_event
# decline_event
#
# add_user
# get_user_history
# update_user
#
