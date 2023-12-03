import pytest
from dependency_injector.wiring import inject, Provide

from bounded_contexts import CreatePet
from bounded_contexts.pets.repository.pet_repositories import PetsRepository
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
    create_test_organization,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, PetDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_create_pet(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    pet_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
) -> None:
    profile_id = "test_profile_id"
    pet_id = "test_pet_id"
    pet_name = "test_pet_name"

    await create_test_individual(message_bus=testing_message_bus, entity_id=profile_id)

    await testing_message_bus.handle(
        CreatePet(
            entity_id=pet_id,
            actor_profile_id=profile_id,
            pet_name=pet_name,
        )
    )

    async with uow:
        pet = await pet_repository.get_pet_by_id(uow=uow, entity_id=pet_id)

        assert pet.entity_id == pet_id
        assert pet.pet_name == pet_name
        assert pet.lost == False
        assert pet.owner_profile_id == profile_id


@pytest.mark.asyncio
async def test_organizational_profile_cant_create_pet(
    testing_message_bus,
) -> None:
    admin_id = "test_profile_id"

    await create_test_organization(
        message_bus=testing_message_bus, admin_profile_id=admin_id
    )

    with pytest.raises(Exception) as e:
        await testing_message_bus.handle(
            CreatePet(
                entity_id="pet_id",
                actor_profile_id=admin_id,
                pet_name="test_pet_name",
            )
        )
