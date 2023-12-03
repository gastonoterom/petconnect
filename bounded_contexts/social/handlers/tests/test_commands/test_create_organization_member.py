import pytest
from dependency_injector.wiring import Provide, inject
from bounded_contexts.auth.handlers.tests.base_auth_helpers import get_account_by_id
from bounded_contexts.pets.handlers.tests.base_pet_helpers import get_owner_by_entity_id
from bounded_contexts.social.domain.enums import ProfileType, OrganizationRole
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    assert_profile,
    create_test_organization,
    create_organization_member_command_generator,
    test_organization_member_data,
    test_organization_data,
)
from bounded_contexts.social.repository.social_repositories import (
    OrganizationsRepository,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, SocialDependencyKind
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
@inject
async def test_create_organization_member(
    testing_message_bus,
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
    organizations_repository: OrganizationsRepository = Provide[
        SocialDependencyKind.organizations_repository
    ],
) -> None:
    organization_id = test_organization_data.TEST_ORGANIZATION_ID

    await create_test_organization(
        message_bus=testing_message_bus,
    )

    for i, role in enumerate([OrganizationRole.MANAGER, OrganizationRole.VOLUNTEER]):
        profile_id = f"test_profile_id-{i + 1}"
        email = f"{i + 1}-{test_organization_member_data.TEST_EMAIL}"

        create_organization_member_command = (
            create_organization_member_command_generator(
                entity_id=profile_id,
                email=email,
                organization_id=organization_id,
                organization_role=role,
            )
        )

        await testing_message_bus.handle(create_organization_member_command)

        async with uow:
            organization = await organizations_repository.get_organization_by_id(
                uow=uow, entity_id=organization_id
            )

            assert organization is not None

            assert organization.entity_id == organization_id
            assert len(organization.members) == i + 2

            member = organization.get_member(profile_id)

            assert_profile(
                entity_id=profile_id,
                profile=member,
                profile_type=ProfileType.ORGANIZATIONAL,
            )

            assert member.profile_type == ProfileType.ORGANIZATIONAL
            assert member.organization_id == organization_id
            assert member.organization_role == role
            assert member.approved == False

        # Assert event propagation
        account = await get_account_by_id(entity_id=profile_id)

        assert account
        assert account.entity_id == profile_id
        assert account.email == member.email

        owner = await get_owner_by_entity_id(entity_id=profile_id)
        assert owner and owner.entity_id == profile_id
        assert owner.profile_type == ProfileType.ORGANIZATIONAL
