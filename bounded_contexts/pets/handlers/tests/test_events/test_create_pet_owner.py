import pytest
from dependency_injector.wiring import inject, Provide
from bounded_contexts.pets.repository.pet_repositories import OwnersRepository
from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, PetDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_owner_creation(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    owner_repository: OwnersRepository = Provide[PetDependencyKind.owners_repository],
) -> None:
    profile_id = "test_profile_id"

    await create_test_individual(message_bus=testing_message_bus, entity_id=profile_id)

    async with uow:
        owner = await owner_repository.get_owner_by_id(uow=uow, entity_id=profile_id)

        assert owner is not None
        assert owner.entity_id == profile_id
        assert owner.profile_type == ProfileType.INDIVIDUAL
