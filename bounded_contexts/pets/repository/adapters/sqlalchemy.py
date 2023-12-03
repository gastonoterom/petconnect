from typing import Type

from sqlalchemy import select

from bounded_contexts.pets.domain.entities import Pet, OwnerProfile
from bounded_contexts.pets.repository.pet_repositories import (
    OwnersRepository,
    PetsRepository,
)
from common.unit_of_work import UnitOfWork


class AlchemyOwnersRepository(OwnersRepository):
    def __init__(self) -> None:
        self.model: Type = OwnerProfile

    async def get_owner_by_id(self, uow: UnitOfWork, entity_id: str) -> OwnerProfile:
        statement = select(self.model).filter_by(entity_id=entity_id)

        result = await uow.session.execute(statement)

        owner = result.scalars().unique().first()

        if owner is None:
            raise ValueError("Owner does not exist")

        return owner

    async def add_owner_profile(
        self, uow: UnitOfWork, owner_profile: OwnerProfile
    ) -> None:
        uow.session.add(owner_profile)
        await uow.session.flush()


class AlchemyPetsRepository(PetsRepository):
    def __init__(self) -> None:
        self.model: Type = Pet

    async def add_pet(self, uow: UnitOfWork, pet: Pet) -> None:
        uow.session.add(pet)
        await uow.session.flush()

    async def get_pet_by_id(self, uow: UnitOfWork, entity_id: str) -> Pet:
        statement = select(self.model).filter_by(entity_id=entity_id)

        result = await uow.session.execute(statement)

        pet = result.scalars().unique().first()

        if pet is None:
            raise ValueError("Pet does not exist")

        return pet
