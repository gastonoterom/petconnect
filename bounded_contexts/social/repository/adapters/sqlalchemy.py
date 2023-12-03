from typing import Type
from sqlalchemy import select
from bounded_contexts.social.domain.entities import (
    Individual,
    Organization,
    OrganizationMember,
)
from bounded_contexts.social.repository.social_repositories import (
    IndividualsRepository,
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork


class AlchemyIndividualsRepository(IndividualsRepository):
    def __init__(self) -> None:
        self.model: Type = Individual

    async def get_individual_by_id(self, uow: UnitOfWork, entity_id: str) -> Individual:
        statement = select(self.model).filter_by(entity_id=entity_id)

        result = await uow.session.execute(statement)

        individual = result.scalars().unique().first()

        if not individual:
            raise Exception("Individual does not exist")

        return individual

    async def add_individual(self, uow: UnitOfWork, individual: Individual) -> None:
        uow.session.add(individual)
        await uow.session.flush()


class AlchemyOrganizationsRepository(OrganizationsRepository):
    def __init__(self) -> None:
        self.model: Type = Organization
        self.members_model: Type = OrganizationMember

    async def get_organization_by_id(
        self, uow: UnitOfWork, entity_id: str
    ) -> Organization:
        statement = select(self.model).filter_by(entity_id=entity_id)

        result = await uow.session.execute(statement)

        return result.scalars().unique().first()

    async def add_organization(self, uow, organization: Organization) -> None:
        uow.session.add(organization)
        await uow.session.flush()

    async def get_organization_by_member_id(
        self, uow: UnitOfWork, member_id: str
    ) -> Organization:
        statement = select(self.model).where(
            self.model.entity_id.in_(  # type: ignore
                select(self.members_model.organization_id).filter_by(  # type: ignore
                    entity_id=self.members_model.entity_id  # type: ignore
                )
            )
        )

        result = await uow.session.execute(statement)

        organization = result.scalars().unique().first()

        if not organization:
            raise Exception("Organization does not exist")

        return organization
