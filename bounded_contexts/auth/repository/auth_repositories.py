from abc import ABC, abstractmethod
from bounded_contexts.auth.domain.entities import Account
from common.unit_of_work import UnitOfWork


class AccountsRepository(ABC):
    @abstractmethod
    async def get_account_by_id(self, uow: UnitOfWork, entity_id: str) -> Account:
        pass

    @abstractmethod
    async def get_account_by_email(self, uow: UnitOfWork, email: str) -> Account | None:
        pass

    @abstractmethod
    async def add_account(self, uow: UnitOfWork, account: Account) -> None:
        pass
