import os
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import registry


connection_url: str | None = os.environ.get("DB_CONNECTION_URL")

if not connection_url:
    raise Exception("DB_CONNECTION_URL environment variable is not set")

engine = create_async_engine(
    url=connection_url,
    echo=False,
    # We'll use optimistic concurrency control
    isolation_level="REPEATABLE READ",
)

postgres_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


metadata = MetaData()
orm_registry = registry()
