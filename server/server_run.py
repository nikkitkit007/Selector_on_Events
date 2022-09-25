from _config import config
import sys
from flask import Flask, json

from data_base.db_creator import DataBase

from handlers.user_handler import UserHandler
from handlers.event_handler import EventHandler
from handlers.notify_handler import NotifyHandler
from handlers.news_handler import NewsHandler
from handlers.decision_handler import DecisionHandler


app = Flask(__name__)
sys.path.append('../')


@app.route('/')
def index():
    return "Hi"


def api_add_url():
    # ----------------------------------USER-----------------------------------
    app.add_url_rule("/api/user/add", view_func=UserHandler.user_add, methods=["POST"])
    app.add_url_rule("/api/user/get_profile", view_func=UserHandler.user_get_profile, methods=["GET"])
    app.add_url_rule("/api/user/update", view_func=UserHandler.user_update, methods=["POST"])
    app.add_url_rule("/api/user/delete", view_func=UserHandler.user_delete, methods=["DELETE"])

    # ----------------------------------EVENT----------------------------------
    app.add_url_rule("/api/event/add", view_func=EventHandler.event_add, methods=["POST"])
    app.add_url_rule("/api/event/get", view_func=EventHandler.event_get, methods=["GET"])
    app.add_url_rule("/api/event/get_all", view_func=EventHandler.event_get_all, methods=["GET"])
    app.add_url_rule("/api/event/update", view_func=EventHandler.event_update, methods=["POST"])
    app.add_url_rule("/api/event/delete", view_func=EventHandler.event_delete, methods=["DELETE"])

    # ---------------------------------NOTIFY----------------------------------
    app.add_url_rule("/api/notify/add", view_func=NotifyHandler.notify_add, methods=["POST"])
    app.add_url_rule("/api/notify/send", view_func=NotifyHandler.notify_send, methods=["POST"])
    app.add_url_rule("/api/notify/delete", view_func=NotifyHandler.notify_delete, methods=["DELETE"])

    # ----------------------------------NEWS-----------------------------------
    app.add_url_rule("/api/news/add", view_func=NewsHandler.news_add, methods=["POST"])
    app.add_url_rule("/api/news/get", view_func=NewsHandler.news_get, methods=["GET"])
    app.add_url_rule("/api/news/get_all", view_func=NewsHandler.news_get_all, methods=["GET"])
    app.add_url_rule("/api/news/update", view_func=NewsHandler.news_update, methods=["POST"])
    app.add_url_rule("/api/news/delete", view_func=NewsHandler.news_delete, methods=["DELETE"])

    # --------------------------------Decision---------------------------------
    app.add_url_rule("/api/event_registration", view_func=DecisionHandler.event_registration, methods=["POST"])
    app.add_url_rule("/api/event_cancel_registration", view_func=DecisionHandler.event_cancel_registration,
                     methods=["POST"])

    app.add_url_rule("/api/apply_event", view_func=DecisionHandler.apply_event, methods=["POST"])
    app.add_url_rule("/api/decline_event", view_func=DecisionHandler.decline_event, methods=["POST"])


if __name__ == '__main__':
    DataBase.create_db()

    api_add_url()

    app.run(host=config.HOST_ADDRESS, port=config.HOST_PORT)
    # TODO: ADD DEMON TREAD WITH event_controller

# CRUD
# 1) Create POST
# 2) Read - GET
# 3) Update - Patch Put
# 4) Delete - DELETE
