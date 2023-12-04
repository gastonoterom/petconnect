import pytest_asyncio
from sqlalchemy.orm import close_all_sessions
from common.bootstrap import (
    create_tables,
    initialize_db,
    delete_table_data,
    start_dependencies,
)
from common.message_bus import MessageBus
from infrastructure.database import engine


@pytest_asyncio.fixture
async def testing_message_bus() -> MessageBus:  # type: ignore
    close_all_sessions()

    await create_tables()

    await initialize_db()

    await delete_table_data()

    start_dependencies()

    message_bus = MessageBus()

    yield message_bus

    assert len(message_bus.event_exceptions) == 0

    await engine.dispose()
