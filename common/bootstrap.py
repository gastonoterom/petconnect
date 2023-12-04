from bounded_contexts.auth.repository.adapters.tables import create_auth_tables
from bounded_contexts.pets.repository.adapters.tables import create_pets_tables
from bounded_contexts.social.repository.adapters.tables import create_social_tables
from common.unit_of_work import UnitOfWork
from dependencies.dependencies import DependencyContainer
from infrastructure import metadata
from infrastructure.database import engine

bootstrap_state = {
    "db_initialized": False,
    "tables_created": False,
    "dependencies_initialized": False,
}


async def create_tables() -> None:
    if bootstrap_state["tables_created"]:
        return

    await create_social_tables()
    await create_auth_tables()
    await create_pets_tables()

    bootstrap_state["tables_created"] = True


async def initialize_db() -> None:
    if bootstrap_state["db_initialized"]:
        return

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    bootstrap_state["db_initialized"] = True


async def delete_table_data() -> None:
    uow = UnitOfWork()

    async with uow:
        for table in reversed(metadata.sorted_tables):
            await uow.session.execute(table.delete())


def start_dependencies() -> None:
    if bootstrap_state["dependencies_initialized"]:
        return

    DependencyContainer()

    bootstrap_state["dependencies_initialized"] = True
