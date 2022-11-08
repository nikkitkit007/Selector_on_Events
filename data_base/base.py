import typing
from contextlib import contextmanager

from configurations.default import DefaultSettings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, Query, Mapper


def _get_query_cls(mapper, _session):
    if mapper:
        m = mapper
        if isinstance(m, tuple):
            m = mapper[0]
        if isinstance(m, Mapper):
            m = m.entity

        try:
            return m.__query_cls__(mapper, _session)
        except AttributeError:
            pass
    return Query(mapper, _session)


Session = sessionmaker(query_cls=_get_query_cls)

settings = DefaultSettings()

engine = create_engine(settings.database_uri,
                       echo=False)

metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    pass


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    """Provide a transactional scope around a series of operations."""
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()
