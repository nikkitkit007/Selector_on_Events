import os
import config
from sqlalchemy.schema import CreateSchema
from .base import Base, engine

#   O
# \/|\|  good luck!
#   |
#  / \
#  | |


def create_all_tables():
    Base.metadata.create_all(engine)


def create_schema():
    engine.execute(CreateSchema(config.SCHEMA_NAME))


def create_db():
    if not engine.dialect.has_schema(engine, config.SCHEMA_NAME):
        create_schema()
    create_all_tables()
    pass


if __name__ == "__main__":
    create_db()
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
