import pytest
from dependency_injector.wiring import inject, Provide
from bounded_contexts.pets.domain.messages import RegisterPetSight
from bounded_contexts.pets.handlers.tests.base_pet_helpers import (
    create_test_pet,
    get_pet,
)
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
)
from common.base_testing import testing_message_bus
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind


@pytest.mark.asyncio
@inject
async def test_register_pet_sight(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
) -> None:
    pet_owner_id = "pet_owner_id"

    pet_id = "test_pet_id"

    await create_test_individual(
        message_bus=testing_message_bus,
        entity_id=pet_owner_id,
    )

    await create_test_pet(
        message_bus=testing_message_bus,
        entity_id=pet_id,
        actor_profile_id=pet_owner_id,
    )

    async with uow:
        pet = await get_pet(uow=uow, entity_id=pet_id)
        assert len(pet.sights) == 0
        assert pet.lost == False

    # We'll test using a real profile and a guest account
    spotter_profile_id = "test_spotter_id"
    await create_test_individual(
        message_bus=testing_message_bus,
        entity_id=spotter_profile_id,
    )

    for i, profile_id in enumerate((None, spotter_profile_id)):
        latitude = i + 5
        longitude = i + 6

        await testing_message_bus.handle(
            RegisterPetSight(
                pet_id=pet_id,
                actor_profile_id=profile_id,
                latitude=latitude,
                longitude=longitude,
            )
        )

        async with uow:
            pet = await get_pet(uow=uow, entity_id=pet_id)

            assert len(pet.sights) == i + 1
            assert pet.sights[i].latitude == latitude
            assert pet.sights[i].longitude == longitude
            assert (
                pet.lost
                == True  # Pet should be marked as lost after registering a sight
            )

            assert pet.sights[i].spotter_profile_id == profile_id
