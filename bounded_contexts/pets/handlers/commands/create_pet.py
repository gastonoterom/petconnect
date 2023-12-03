from dependency_injector.wiring import inject, Provide
from bounded_contexts.pets.domain.entities import Pet
from bounded_contexts.pets.domain.messages import (
    CreatePet,
)
from bounded_contexts.pets.repository.pet_repositories import (
    PetsRepository,
    OwnersRepository,
)
from bounded_contexts.social.domain.enums import ProfileType
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import PetDependencyKind


@inject
async def create_pet_handler(
    command: CreatePet,
    uow: UnitOfWork,
    pets_repository: PetsRepository = Provide[PetDependencyKind.pets_repository],
    owners_repository: OwnersRepository = Provide[PetDependencyKind.owners_repository],
) -> None:
    async with uow:
        owner_profile = await owners_repository.get_owner_by_id(
            uow=uow, entity_id=command.actor_profile_id
        )

        if owner_profile.profile_type == ProfileType.ORGANIZATIONAL:
            raise Exception("Organizational profiles can't create pets!")

        pet = Pet(
            entity_id=command.entity_id,
            pet_name=command.pet_name,
            owner_profile_id=owner_profile.entity_id,
            lost=False,
        )

        await pets_repository.add_pet(uow=uow, pet=pet)
