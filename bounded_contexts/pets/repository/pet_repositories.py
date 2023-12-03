from abc import ABC, abstractmethod
from bounded_contexts.pets.domain.entities import OwnerProfile, Pet
from common.unit_of_work import UnitOfWork


class OwnersRepository(ABC):
    @abstractmethod
    async def get_owner_by_id(self, uow: UnitOfWork, entity_id: str) -> OwnerProfile:
        pass

    @abstractmethod
    async def add_owner_profile(
        self, uow: UnitOfWork, owner_profile: OwnerProfile
    ) -> None:
        pass


class PetsRepository(ABC):
    @abstractmethod
    async def add_pet(self, uow: UnitOfWork, pet: Pet) -> None:
        pass

    @abstractmethod
    async def get_pet_by_id(self, uow: UnitOfWork, entity_id: str) -> Pet:
        pass
