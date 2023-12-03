import os
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import registry


connection_url = "postgresql+asyncpg://postgres:postgres@localhost/petconnect_events_testing?port=5439"

if os.environ.get("ENVIRONMENT") == "production":
    connection_url = (
        "postgresql+asyncpg://postgres:postgres@localhost/petconnect_events?port=5439"
    )


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
