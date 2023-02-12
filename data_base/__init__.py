from data_base.base import get_session
from configurations.default import DefaultSettings

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)

__all__ = [
    DeclarativeBase,
    get_session,
    DefaultSettings,
]

