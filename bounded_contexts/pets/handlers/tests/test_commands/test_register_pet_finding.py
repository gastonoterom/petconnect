import pytest
from dependency_injector.wiring import inject, Provide

from bounded_contexts import RegisterPetFinding
from bounded_contexts.pets.domain.value_objects import Location
from bounded_contexts.pets.handlers.tests.base_pet_helpers import (
    create_test_pet,
    get_pet,
)
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_register_pet_as_found(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
) -> None:
    profile_id = "test_profile_id"
    pet_id = "test_pet_id"
    last_sight = Location(
        latitude=1.0,
        longitude=2.0,
    )

    await create_test_individual(message_bus=testing_message_bus, entity_id=profile_id)

    await create_test_pet(
        message_bus=testing_message_bus,
        entity_id=pet_id,
        actor_profile_id=profile_id,
        lost=True,
        last_sight=last_sight,
    )

    async with uow:
        pet = await get_pet(uow=uow, entity_id=pet_id)

        assert pet.lost == True
        assert pet.sights[0].latitude == 1.0
        assert pet.sights[0].longitude == 2.0

    await testing_message_bus.handle(
        RegisterPetFinding(
            pet_id=pet_id,
            actor_profile_id=profile_id,
        )
    )

    async with uow:
        pet = await get_pet(uow=uow, entity_id=pet_id)

        assert pet.lost == False
        assert len(pet.sights) == 0
