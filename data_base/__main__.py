import os
from .db_creator import DataBase


if __name__ == "__main__":
    DataBase.create_db()
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
