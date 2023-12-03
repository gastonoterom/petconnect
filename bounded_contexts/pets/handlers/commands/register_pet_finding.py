from dependency_injector.wiring import inject, Provide

from bounded_contexts.pets.domain.messages import (
    RegisterPetFinding,
)
from bounded_contexts.pets.repository.pet_repositories import (
    PetsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import PetDependencyKind


@inject
async def register_pet_finding_handler(
    command: RegisterPetFinding,
    uow: UnitOfWork,
    pets_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
):
    async with uow:
        pet = await pets_repository.get_pet_by_id(uow=uow, entity_id=command.pet_id)

        await pet.mark_as_found(
            actor_profile_id=command.actor_profile_id,
        )
