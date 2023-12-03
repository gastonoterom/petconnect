from dependency_injector.wiring import inject, Provide
from bounded_contexts.social.domain.entities import OrganizationMember, Organization
from bounded_contexts.social.domain.messages import (
    CreateOrganization,
    ProfileCreated,
    OrganizationMemberCreated,
)
from bounded_contexts.social.domain.value_objects import (
    OrganizationRole,
    OrganizationMemberData,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import SocialDependencyKind


@inject
async def create_organization_handler(
    command: CreateOrganization,
    uow: UnitOfWork,
    organization_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    async with uow:
        admin = OrganizationMember(
            entity_id=command.profile_data.entity_id,
            email=command.account_data.email,
            full_name=command.profile_data.full_name,
            government_id=command.profile_data.government_id,
            phone_number=command.profile_data.phone_number,
            organization_role=OrganizationRole.ADMIN,
            organization_id=command.organization_data.entity_id,
            approved=True,
        )

        organization = Organization(
            entity_id=command.organization_data.entity_id,
            organization_name=command.organization_data.organization_name,
            members=[admin],
        )

        await organization_repository.add_organization(
            uow=uow, organization=organization
        )

    uow.publish_messages(
        [
            ProfileCreated(
                entity_id=admin.entity_id,
                account_data=command.account_data,
                profile_data=command.profile_data,
                profile_type=admin.profile_type,
            ),
            OrganizationMemberCreated(
                entity_id=admin.entity_id,
                profile_data=command.profile_data,
                organization_member_data=OrganizationMemberData(
                    organization_role=OrganizationRole.ADMIN,
                    organization_id=command.organization_data.entity_id,
                ),
            ),
        ],
    )
