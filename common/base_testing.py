import pytest_asyncio
from sqlalchemy.orm import close_all_sessions
from bounded_contexts.auth.repository.adapters.tables import create_auth_tables
from bounded_contexts.pets.repository.adapters.tables import create_pets_tables
from bounded_contexts.social.repository.adapters.tables import create_social_tables
from common.message_bus import MessageBus
from common.unit_of_work import UnitOfWork
from dependencies.dependencies import DependencyContainer
from infrastructure import metadata
from infrastructure.database import engine

testing_data = {
    "db_initialized": False,
    "tables_created": False,
    "dependencies_initialized": False,
}


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


async def create_tables() -> None:
    if testing_data["tables_created"]:
        return

    await create_social_tables()
    await create_auth_tables()
    await create_pets_tables()

    testing_data["tables_created"] = True


async def initialize_db() -> None:
    if testing_data["db_initialized"]:
        return

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    testing_data["db_initialized"] = True


async def delete_table_data() -> None:
    uow = UnitOfWork()

    async with uow:
        for table in reversed(metadata.sorted_tables):
            await uow.session.execute(table.delete())


def start_dependencies() -> None:
    if testing_data["dependencies_initialized"]:
        return

    DependencyContainer()

    testing_data["dependencies_initialized"] = True
