import os
# ------ uncomment this if local -------

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


HOST_ADDRESS = os.getenv("HOST_ADDRESS")
HOST_PORT = os.getenv("HOST_PORT")

# ------------------------
DATABASE = os.getenv("DATABASE")
# USERNAME = "postgres"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
# HOST = "127.0.0.1"
PORT = os.getenv("PORT")

# ------------------------
SCHEMA_NAME = os.getenv("SCHEMA_NAME")
TBL_EVENTS = os.getenv("TBL_EVENTS")
TBL_USERS = os.getenv("TBL_USERS")
TBL_NOTIFIES = os.getenv("TBL_NOTIFIES")
TBL_NEWS = os.getenv("TBL_NEWS")

# ------------------------
TIME_TO_POST_EVENT = 10
TIME_TO_END_TAKE_PART = 7
TIME_TO_FIRST_APPLICANTS = TIME_TO_POST_EVENT - 3
TIME_TO_ACCEPT = 1                          # 1 day
TIME_TO_BAN = 3

TIME_TO_CHECK = 60 * 60 * 6                 # minutes

BAN_TIME_LATE = 1 * 365                     # 1 year
BAN_TIME_IGNORE = 2                         # 2 year

# ----------REGEX--------------
REGEX_MAIL = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
REGEX_PHONE = r"?:\(?(\d{3})\)?)?(?:\s|-)?(\d{3})(?:\s|-)?(\d{2})(?:\s|-)?(\d{2})(?:\s*доб[.а-я]*\s*(\d{2,5}))?"

# ----------users--------------
# user_id serial primary key not null
# user_isu_number integer UNIQUE
# user_name varchar(127)
# user_surname varchar(127)
# user_patronymic varchar(127)
# phone varchar(127)
# vk_link varchar(127)
# mail varchar(127)
# is_russian_citizenship bool
# score integer
# ban_date TIMESTAMP
# notify_id integer[]
# time_select_finish TIMESTAMP


# ----------events---------------
# event_id serial primary key not null
# event_name varchar(127)
# time_start TIMESTAMP
# time_end TIMESTAMP
# description text
# url_pdf varchar(255)
# people_count integer
# coefficient integer
# users_id_want integer[]
# users_id_go integer[]
# image varchar(127)

# ----------notifies---------------
# notify_id serial primary key not null
# event_id integer
# time TIMESTAMP
# notify_header varchar(126)
# notify_data text

# ----------news---------------
# news_id serial primary key not null
# header varchar(127)
# data text
# time TIMESTAMP

# -----------------------------------
# ----------server_func--------------
# add
# update
# get
#
# apply_event
# decline_event
#
# add_user
# get_user_history
# update_user
#
