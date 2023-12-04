from typing import cast
import pytest
from bounded_contexts.social.domain.enums import ProfileType, OrganizationRole
from bounded_contexts.social.handlers.tests.base_social_helpers import (
    create_test_individual,
    test_individual_data,
    create_test_organization,
    test_organization_admin_data,
)
from bounded_contexts.social.views.factories.profile_view_factory import (
    OrganizationMemberView,
    IndividualView,
)
from bounded_contexts.social.views.queries.get_profile import get_profile
from common.base_testing import testing_message_bus


@pytest.mark.asyncio
async def test_get_individual_profile(
    testing_message_bus,
) -> None:
    profile_id = "test_profile_id"

    await create_test_individual(
        message_bus=testing_message_bus,
        entity_id=profile_id,
    )

    view: IndividualView = cast(IndividualView, await get_profile(profile_id))

    assert view
    assert view.profile_type == ProfileType.INDIVIDUAL.value
    assert view.entity_id == profile_id
    assert view.government_id == test_individual_data.TEST_GOVT_ID
    assert view.full_name == test_individual_data.TEST_FULL_NAME
    assert view.phone_number == test_individual_data.TEST_PHONE_NUMBER


@pytest.mark.asyncio
async def test_get_non_existing_profile_fails(
    testing_message_bus,
) -> None:
    profile_id = "test_profile_id"

    with pytest.raises(Exception):
        await get_profile(profile_id)


@pytest.mark.asyncio
async def test_get_organizational_profile(
    testing_message_bus,
) -> None:
    admin_profile_id = "test_admin_profile_id"
    organization_id = "test_org_id"

    await create_test_organization(
        message_bus=testing_message_bus,
        admin_profile_id=admin_profile_id,
        entity_id=organization_id,
    )

    view: OrganizationMemberView = cast(
        OrganizationMemberView, await get_profile(admin_profile_id)
    )

    assert view
    assert view.profile_type == ProfileType.ORGANIZATIONAL.value
    assert view.entity_id == admin_profile_id
    assert view.government_id == test_organization_admin_data.TEST_GOVT_ID
    assert view.full_name == test_organization_admin_data.TEST_FULL_NAME
    assert view.phone_number == test_organization_admin_data.TEST_PHONE_NUMBER
    assert view.organization_role == OrganizationRole.ADMIN.value
    assert view.organization_id == organization_id
