import pytest
from dependency_injector.wiring import Provide, inject

from bounded_contexts.auth.handlers.tests.base_auth_helpers import get_account_by_id
from bounded_contexts.pets.handlers.tests.base_pet_helpers import get_owner_by_entity_id
from bounded_contexts.social.domain.enums import ProfileType, OrganizationRole
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    test_organization_data,
    test_organization_admin_data,
    assert_profile,
    create_organization_command,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, SocialDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_create_organization_with_admin(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    organizations_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    organization_id: str = test_organization_data.TEST_ORGANIZATION_ID
    profile_id: str = test_organization_admin_data.TEST_ENTITY_ID

    await testing_message_bus.handle(create_organization_command)

    async with uow:
        organization = await organizations_repository.get_organization_by_id(
            uow=uow, entity_id=organization_id
        )

        assert organization is not None

        assert (
            organization.organization_name
            == test_organization_data.TEST_ORGANIZATION_NAME
        )

        assert organization.admin

        assert_profile(
            profile=organization.admin,
            profile_type=ProfileType.ORGANIZATIONAL,
            entity_id=profile_id,
        )

        assert organization.admin.organization_id == organization.entity_id
        assert organization.admin.organization_role == OrganizationRole.ADMIN
        assert organization.admin.approved == True

        assert len(organization.members) == 1
        assert organization.members[0].entity_id == organization.admin.entity_id

    # Assert event propagation
    account = await get_account_by_id(entity_id=profile_id)

    assert account
    assert account.entity_id == profile_id
    assert account.email == organization.admin.email

    owner = await get_owner_by_entity_id(entity_id=profile_id)
    assert owner and owner.entity_id == profile_id
    assert owner.profile_type == ProfileType.ORGANIZATIONAL
