from dependency_injector.wiring import inject, Provide
from bounded_contexts.auth.domain.entities import Account
from bounded_contexts.auth.repository.auth_repositories import AccountsRepository
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, AuthDependencyKind


@inject
async def get_account_by_id(
    entity_id: str,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    accounts_repository: AccountsRepository = Provide[
        AuthDependencyKind.accounts_repository
    ],
) -> Account:
    async with uow:
        account = await accounts_repository.get_account_by_id(
            uow=uow, entity_id=entity_id
        )
        return account
