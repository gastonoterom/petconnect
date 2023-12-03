from dependency_injector.wiring import inject, Provide
from bounded_contexts.pets.domain.entities import OwnerProfile
from bounded_contexts.pets.repository.pet_repositories import OwnersRepository
from bounded_contexts.social.domain.messages import (
    ProfileCreated,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import PetDependencyKind


@inject
async def create_pet_owner_handler(
    event: ProfileCreated,
    uow: UnitOfWork,
    owners_repository: OwnersRepository = Provide[PetDependencyKind.owners_repository],
) -> None:
    async with uow:
        owner_profile = OwnerProfile(
            entity_id=event.entity_id,
            profile_type=event.profile_type,
        )

        await owners_repository.add_owner_profile(uow=uow, owner_profile=owner_profile)
