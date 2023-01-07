import os
from os import environ
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '../../../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

scope = environ.get("SCOPE")

client_id = environ.get("CLIENT_ID")
client_secret = environ.get("CLIENT_SECRET")

redirect_uri = environ.get("REDIRECT_URI")
post_logout_redirect_uri = environ.get("POST_LOGOUT_REDIRECT_URI")

jwt_verify = bool(int(environ.get("JWT_VERIFY", 1)))
