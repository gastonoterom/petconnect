import pytest
from dependency_injector.wiring import inject, Provide
from bounded_contexts.auth.repository.auth_repositories import AccountsRepository
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
    test_individual_data,
)
from common.base_testing import testing_message_bus
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, AuthDependencyKind
from infrastructure.crypto import CryptoUtils


@pytest.mark.asyncio
@inject
async def test_account_creation(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    accounts_repository: AccountsRepository = Provide[
        AuthDependencyKind.accounts_repository
    ],
) -> None:
    profile_id = "test_profile_id"
    email = "test_email@test.com"

    await create_test_individual(
        message_bus=testing_message_bus, entity_id=profile_id, email=email
    )

    async with uow:
        account = await accounts_repository.get_account_by_id(
            uow=uow, entity_id=profile_id
        )

        assert account is not None
        assert account.entity_id == profile_id
        assert account.email == email

        assert await CryptoUtils.verify_hash(
            string_to_verify=test_individual_data.TEST_PASSWORD,
            hash_to_verify=account.password_hash,
        )
