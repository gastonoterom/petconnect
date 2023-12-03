from dependency_injector.wiring import Provide, inject

from bounded_contexts.auth.domain.messages import (
    AccountCreated,
)
from bounded_contexts.auth.domain.entities import Account
from bounded_contexts.auth.repository.auth_repositories import AccountsRepository
from bounded_contexts.social.domain.messages import (
    ProfileCreated,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import AuthDependencyKind
from infrastructure.crypto import CryptoUtils


@inject
async def create_account_handler(
    event: ProfileCreated,
    uow: UnitOfWork,
    accounts_repository: AccountsRepository = Provide[
        AuthDependencyKind.accounts_repository
    ],
) -> None:
    account = Account(
        entity_id=event.entity_id,
        email=event.account_data.email,
        password_hash=await CryptoUtils.hash_string(event.account_data.password),
    )

    async with uow:
        await accounts_repository.add_account(uow=uow, account=account)

    uow.publish_message(AccountCreated(account_id=account.entity_id))
