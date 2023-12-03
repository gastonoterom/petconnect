from typing import Type

from sqlalchemy import select

from bounded_contexts.auth.domain.entities import Account
from bounded_contexts.auth.repository.auth_repositories import AccountsRepository
from common.unit_of_work import UnitOfWork


class AlchemyAccountsRepository(AccountsRepository):
    def __init__(self) -> None:
        self.model: Type = Account

    async def get_account_by_id(self, uow: UnitOfWork, entity_id: str) -> Account:
        statement = select(self.model).filter_by(entity_id=entity_id)

        result = await uow.session.execute(statement)

        account = result.scalars().unique().first()

        if account is None:
            raise ValueError(f"Account does not exist")

        return account

    async def add_account(self, uow: UnitOfWork, account: Account) -> None:
        uow.session.add(account)
        await uow.session.flush()

    async def get_account_by_email(self, uow: UnitOfWork, email: str) -> Account:
        statement = select(self.model).filter_by(email=email)

        result = await uow.session.execute(statement)

        account = result.scalars().unique().first()

        if account is None:
            raise ValueError(f"Account does not exist")

        return account
