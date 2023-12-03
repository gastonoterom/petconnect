from abc import ABC, abstractmethod
from bounded_contexts.social.domain.entities import Individual, Organization
from common.unit_of_work import UnitOfWork


class IndividualsRepository(ABC):
    @abstractmethod
    async def get_individual_by_id(self, uow: UnitOfWork, entity_id: str) -> Individual:
        pass

    @abstractmethod
    async def add_individual(self, uow: UnitOfWork, individual: Individual) -> None:
        pass


class OrganizationsRepository(ABC):
    @abstractmethod
    async def get_organization_by_id(
        self, uow: UnitOfWork, entity_id: str
    ) -> Organization:
        pass

    @abstractmethod
    async def add_organization(
        self, uow: UnitOfWork, organization: Organization
    ) -> None:
        pass

    @abstractmethod
    async def get_organization_by_member_id(
        self, uow: UnitOfWork, member_id: str
    ) -> Organization:
        pass
