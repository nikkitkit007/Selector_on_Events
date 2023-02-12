from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configurations.default import DefaultSettings


class SessionManager:

    def __init__(self) -> None:
        self.engine = None
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(DefaultSettings().database_uri, echo=False, future=True)


async def get_session() -> sessionmaker:
    async_session = SessionManager().get_session_maker()
    return async_session


__all__ = [
    "get_session",
]
