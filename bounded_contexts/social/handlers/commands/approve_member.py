from dependency_injector.wiring import inject, Provide
from bounded_contexts.social.domain.messages import (
    ApproveOrganizationMember,
    OrganizationMemberApproved,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import SocialDependencyKind


@inject
async def approve_organization_member_handler(
    command: ApproveOrganizationMember,
    uow: UnitOfWork,
    organization_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    async with uow:
        organization = await organization_repository.get_organization_by_member_id(
            uow=uow, member_id=command.member_id
        )

        organization.approve_member(
            actor_member_id=command.actor_member_id,
            member_id=command.member_id,
        )

    uow.publish_message(
        OrganizationMemberApproved(
            member_id=command.member_id,
        )
    )
