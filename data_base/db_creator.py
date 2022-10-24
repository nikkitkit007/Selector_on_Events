from sqlalchemy.schema import CreateSchema
from .base import Base, engine


#   O
# \/|\|  good luck!
#   |
#  / \
#  | |


class DataBase:

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

    # @staticmethod
    # def create_schema():
    #     engine.execute(CreateSchema(config.SCHEMA_NAME))

    @staticmethod
    def create_db():
        # if not engine.dialect.has_schema(engine, config.SCHEMA_NAME):
        # DataBase.create_schema()
        DataBase.create_all_tables()
