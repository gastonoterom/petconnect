from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from bounded_contexts.pets.domain.entities import PetSight
from bounded_contexts.pets.domain.messages import (
    RegisterPetLoss,
)
from bounded_contexts.pets.repository.pet_repositories import (
    PetsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import PetDependencyKind


@inject
async def register_pet_as_lost_handler(
    command: RegisterPetLoss,
    uow: UnitOfWork,
    pets_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
):
    async with uow:
        pet = await pets_repository.get_pet_by_id(uow=uow, entity_id=command.pet_id)

        last_sight = PetSight(
            entity_id=uuid4().hex,
            spotter_profile_id=command.actor_profile_id,
            latitude=command.last_sight.latitude,
            longitude=command.last_sight.longitude,
        )

        await pet.mark_as_lost(
            actor_profile_id=command.actor_profile_id,
            last_sight=last_sight,
        )
