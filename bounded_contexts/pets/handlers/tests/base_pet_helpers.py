from dependency_injector.wiring import inject, Provide

from bounded_contexts import (
    CreateIndividual,
    create_individual_handler,
    create_pet_owner_handler,
    CreatePet,
    RegisterPetLoss,
)
from bounded_contexts.pets.domain.entities import OwnerProfile, Pet
from bounded_contexts.pets.domain.value_objects import Location
from bounded_contexts.pets.repository.pet_repositories import (
    OwnersRepository,
    PetsRepository,
)
from bounded_contexts.social.domain.value_objects import AccountData, ProfileData
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    test_individual_data,
)
from common.message_bus import MessageBus
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, PetDependencyKind


# Helpers
@inject
async def get_owner_by_entity_id(
    entity_id: str,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    owners_repository: OwnersRepository = Provide[PetDependencyKind.owners_repository],
) -> OwnerProfile:
    async with uow:
        owner = await owners_repository.get_owner_by_id(uow=uow, entity_id=entity_id)
        return owner


async def create_test_pet(
    message_bus: MessageBus,
    entity_id: str,
    actor_profile_id: str,
    pet_name: str = "test_pet_name",
    lost: bool = False,
    last_sight: Location | None = None,
) -> None:
    command = CreatePet(
        entity_id=entity_id,
        actor_profile_id=actor_profile_id,
        pet_name=pet_name,
    )

    await message_bus.handle(command)

    if lost and last_sight:
        await message_bus.handle(
            RegisterPetLoss(
                pet_id=entity_id,
                actor_profile_id=actor_profile_id,
                last_sight=last_sight,
            )
        )


@inject
async def get_pet(
    uow: UnitOfWork,
    entity_id: str,
    pets_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
) -> Pet:
    return await pets_repository.get_pet_by_id(uow=uow, entity_id=entity_id)
