import pytest
from dependency_injector.wiring import Provide, inject

from bounded_contexts.auth.handlers.tests.base_auth_helpers import get_account_by_id
from bounded_contexts.pets.handlers.tests.base_pet_helpers import get_owner_by_entity_id
from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_individual_command,
    test_individual_data,
    assert_profile,
    create_individual_command_generator,
)
from bounded_contexts.social.repository.social_repositories import IndividualsRepository
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, SocialDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_create_individual(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    individuals_repository: IndividualsRepository = Provide[
        SocialDependencyKind.individuals_repository
    ],
) -> None:
    profile_id = test_individual_data.TEST_ENTITY_ID

    await testing_message_bus.handle(create_individual_command)

    async with uow:
        profile = await individuals_repository.get_individual_by_id(
            uow=uow, entity_id=profile_id
        )

        assert_profile(profile=profile, profile_type=ProfileType.INDIVIDUAL)

    # Assert event propagation
    account = await get_account_by_id(entity_id=profile_id)

    assert account
    assert account.entity_id == profile_id
    assert account.email == profile.email

    owner = await get_owner_by_entity_id(entity_id=profile_id)
    assert owner and owner.entity_id == profile_id
    assert owner.profile_type == ProfileType.INDIVIDUAL


@pytest.mark.asyncio
@inject
async def test_create_individual_with_same_email_fails(
    testing_message_bus,
) -> None:
    email = "same_email@test.com"

    create_individual_command_1 = create_individual_command_generator()
    create_individual_command_1.profile_data.entity_id = "test_id_1"
    create_individual_command_1.account_data.email = email

    await testing_message_bus.handle(create_individual_command_1)

    with pytest.raises(Exception):
        create_individual_command_2 = create_individual_command_generator()
        create_individual_command_2.profile_data.entity_id = "test_id_2"
        create_individual_command_2.account_data.email = email

        await testing_message_bus.handle(create_individual_command_2)


@pytest.mark.asyncio
@inject
async def test_create_individual_with_same_id_fails(
    testing_message_bus,
) -> None:
    # Should not fail
    create_individual_command_1 = create_individual_command_generator()
    create_individual_command_1.profile_data.entity_id = "test_id"
    create_individual_command_1.account_data.email = "email_1@test.com"

    await testing_message_bus.handle(create_individual_command_1)

    # Should fail
    with pytest.raises(Exception):
        create_individual_command_2 = create_individual_command_generator()
        create_individual_command_2.profile_data.entity_id = "test_id"
        create_individual_command_2.account_data.email = "email_2@test.com"

        await testing_message_bus.handle(create_individual_command_2)

    # Should not fail
    create_individual_command_3 = create_individual_command_generator()
    create_individual_command_3.profile_data.entity_id = "test_id_2"
    create_individual_command_3.account_data.email = "email_3@test.com"

    await testing_message_bus.handle(create_individual_command_3)
