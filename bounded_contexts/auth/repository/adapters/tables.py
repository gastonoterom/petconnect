from sqlalchemy import Table, Column, String, Boolean, ForeignKey
from bounded_contexts.auth.domain.entities import Account
from infrastructure import metadata, orm_registry


async def create_auth_tables() -> None:
    accounts_table = Table(
        "accounts",
        metadata,
        Column("entity_id", String, ForeignKey("profiles.entity_id"), primary_key=True),
        Column("email", String, unique=True, nullable=False),
        Column("password_hash", String, nullable=False),
    )

    orm_registry.map_imperatively(Account, accounts_table)
