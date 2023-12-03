import pytest
from dependency_injector.wiring import Provide, inject
from bounded_contexts.social.domain.enums import OrganizationRole
from bounded_contexts.social.domain.messages import ApproveOrganizationMember
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_organization,
    create_test_organization_member,
    test_organization_data,
    test_organization_member_data,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, SocialDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_approve_organization_member(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    organizations_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    organization_id: str = test_organization_data.TEST_ORGANIZATION_ID
    member_id: str = test_organization_member_data.TEST_ENTITY_ID

    await create_test_organization(message_bus=testing_message_bus)

    await create_test_organization_member(
        message_bus=testing_message_bus,
        organization_id=organization_id,
        organization_role=OrganizationRole.VOLUNTEER,
    )

    async with uow:
        organization = await organizations_repository.get_organization_by_id(
            uow=uow, entity_id=organization_id
        )

        member = organization.get_member(member_id)

        assert member.approved == False

        admin_id = organization.admin.entity_id

    await testing_message_bus.handle(
        ApproveOrganizationMember(
            actor_member_id=admin_id,
            member_id=member_id,
        )
    )

    async with uow:
        organization = await organizations_repository.get_organization_by_id(
            uow=uow, entity_id=organization_id
        )

        member = organization.get_member(member_id)

        assert member.approved == True


@pytest.mark.asyncio
@inject
async def test_approve_organization_member_fails_for_non_admin(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    organizations_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    organization_id: str = test_organization_data.TEST_ORGANIZATION_ID
    member_id: str = test_organization_member_data.TEST_ENTITY_ID

    await create_test_organization(
        message_bus=testing_message_bus,
    )

    await create_test_organization_member(
        message_bus=testing_message_bus,
        organization_id=organization_id,
        organization_role=OrganizationRole.VOLUNTEER,
    )

    async with uow:
        organization = await organizations_repository.get_organization_by_id(
            uow=uow, entity_id=organization_id
        )

        member = organization.get_member(member_id)
        assert member.approved == False

    with pytest.raises(Exception):
        await testing_message_bus.handle(
            ApproveOrganizationMember(
                actor_member_id="test_random_user_id",
                member_id=member_id,
            )
        )

    async with uow:
        organization = await organizations_repository.get_organization_by_id(
            uow=uow, entity_id=organization_id
        )

        member = organization.get_member(member_id)
        assert member.approved == False
