from dependency_injector.wiring import inject, Provide
from bounded_contexts.social.domain.entities import OrganizationMember
from bounded_contexts.social.domain.messages import (
    CreateOrganizationMember,
    ProfileCreated,
    OrganizationMemberCreated,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import SocialDependencyKind


@inject
async def create_organization_member_handler(
    command: CreateOrganizationMember,
    uow: UnitOfWork,
    organization_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    async with uow:
        organization = await organization_repository.get_organization_by_id(
            uow=uow, entity_id=command.organization_member_data.organization_id
        )

        if not organization:
            raise Exception("Organization does not exist")

        member = OrganizationMember(
            entity_id=command.profile_data.entity_id,
            email=command.account_data.email,
            full_name=command.profile_data.full_name,
            government_id=command.profile_data.government_id,
            phone_number=command.profile_data.phone_number,
            organization_role=command.organization_member_data.organization_role,
            organization_id=command.organization_member_data.organization_id,
            approved=False,
        )

        organization.join_organization(
            member=member,
        )

    uow.publish_messages(
        [
            ProfileCreated(
                entity_id=member.entity_id,
                account_data=command.account_data,
                profile_data=command.profile_data,
                profile_type=member.profile_type,
            ),
            OrganizationMemberCreated(
                entity_id=member.entity_id,
                profile_data=command.profile_data,
                organization_member_data=command.organization_member_data,
            ),
        ],
    )
