import sys
from os import environ

from quart import Quart

from server.handlers.login_handler import login
from server.handlers.index import index
from server.handlers.health_handler import HealthHandler

from server.handlers.user_handler import UserHandler
from server.handlers.event_handler import EventHandler
from server.handlers.notify_handler import NotifyHandler
from server.handlers.news_handler import NewsHandler
from server.handlers.decision_handler import DecisionHandler


app = Quart(__name__)
sys.path.append('../')


def api_add_url():
    app.add_url_rule("/api/", view_func=index)

    # ----------------------------------HEALTH-----------------------------------
    app.add_url_rule("/api/health/app", view_func=HealthHandler.health_app)
    app.add_url_rule("/api/health/db", view_func=HealthHandler.health_db)

    # ----------------------------------LOGIN----------------------------------
    app.add_url_rule("/api/login", view_func=login)

    # ----------------------------------USER-----------------------------------
    app.add_url_rule("/api/user", view_func=UserHandler.user_add, methods=["POST"])
    app.add_url_rule("/api/user", view_func=UserHandler.user_get_profile, methods=["GET"])
    app.add_url_rule("/api/user", view_func=UserHandler.user_update, methods=["PUT"])
    app.add_url_rule("/api/user", view_func=UserHandler.user_delete, methods=["DELETE"])

    # ----------------------------------EVENT----------------------------------
    app.add_url_rule("/api/event", view_func=EventHandler.event_add, methods=["POST"])
    app.add_url_rule("/api/event", view_func=EventHandler.event_get, methods=["GET"])
    app.add_url_rule("/api/event", view_func=EventHandler.event_update, methods=["PUT"])
    app.add_url_rule("/api/event", view_func=EventHandler.event_delete, methods=["DELETE"])

    # ---------------------------------NOTIFY----------------------------------
    app.add_url_rule("/api/notify", view_func=NotifyHandler.notify_add, methods=["POST"])
    app.add_url_rule("/api/notify/send", view_func=NotifyHandler.notify_send, methods=["POST"])
    app.add_url_rule("/api/notify", view_func=NotifyHandler.notify_delete, methods=["DELETE"])

    # ----------------------------------NEWS-----------------------------------
    app.add_url_rule("/api/news", view_func=NewsHandler.news_add, methods=["POST"])
    app.add_url_rule("/api/news", view_func=NewsHandler.news_get, methods=["GET"])
    app.add_url_rule("/api/news", view_func=NewsHandler.news_update, methods=["PUT"])
    app.add_url_rule("/api/news", view_func=NewsHandler.news_delete, methods=["DELETE"])

    # --------------------------------Decision---------------------------------
    app.add_url_rule("/api/event_registration", view_func=DecisionHandler.event_registration, methods=["POST"])
    app.add_url_rule("/api/event_cancel_registration", view_func=DecisionHandler.event_cancel_registration,
                     methods=["POST"])

    app.add_url_rule("/api/apply_event", view_func=DecisionHandler.apply_event, methods=["POST"])
    app.add_url_rule("/api/decline_event", view_func=DecisionHandler.decline_event, methods=["POST"])


api_add_url()


if __name__ == '__main__':
    app.run(host=str(environ.get("APP_HOST", "127.0.0.1")),
            port=int(environ.get("APP_PORT", 8080)))
