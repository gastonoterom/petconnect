from uuid import uuid4
from dependency_injector.wiring import inject, Provide
from bounded_contexts.pets.domain.entities import PetSight
from bounded_contexts.pets.domain.messages import (
    RegisterPetSight,
    PetSightRegistered,
)
from bounded_contexts.pets.repository.pet_repositories import (
    PetsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import PetDependencyKind


@inject
async def register_pet_sight_handler(
    command: RegisterPetSight,
    uow: UnitOfWork,
    pets_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
):
    async with uow:
        pet = await pets_repository.get_pet_by_id(uow=uow, entity_id=command.pet_id)

        pet_sight: PetSight = PetSight(
            entity_id=uuid4().hex,
            spotter_profile_id=command.actor_profile_id,
            latitude=command.latitude,
            longitude=command.longitude,
        )

        await pet.register_sight(pet_sight=pet_sight)

    uow.publish_message(
        PetSightRegistered(
            pet_id=command.pet_id,
            owner_profile_id=pet.owner_profile_id,
            actor_profile_id=command.actor_profile_id,
        )
    )
