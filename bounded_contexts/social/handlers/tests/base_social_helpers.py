from dataclasses import dataclass
from bounded_contexts.social.domain.entities import Profile
from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.domain.messages import (
    CreateOrganization,
    CreateIndividual,
    CreateOrganizationMember,
    ProfileCreated,
)
from bounded_contexts.social.domain.value_objects import (
    AccountData,
    OrganizationData,
    ProfileData,
    OrganizationMemberData,
    OrganizationRole,
)
from common.message_bus import MessageBus


# Test data:
@dataclass
class TestIndividualData:
    TEST_ENTITY_ID = "test_individual_id"
    TEST_EMAIL = "testing@test.com"
    TEST_PASSWORD = "password"
    TEST_FULL_NAME = "Test full name"
    TEST_GOVT_ID = "User"
    TEST_PHONE_NUMBER = "123456789"


@dataclass
class TestOrganizationAdminData(TestIndividualData):
    TEST_ENTITY_ID = "test_admin_id"
    TEST_EMAIL = "admin@test.com"


@dataclass
class TestOrganizationMemberData(TestIndividualData):
    TEST_ENTITY_ID = "test_member_id"
    TEST_EMAIL = "member@test.com"


@dataclass
class TestOrganizationData:
    TEST_ORGANIZATION_ID = "test_organization_id"
    TEST_ORGANIZATION_NAME = "Test organization name"


# Test data init:
test_individual_data = TestIndividualData()
test_organization_admin_data = TestOrganizationAdminData()
test_organization_member_data = TestOrganizationMemberData()
test_organization_data = TestOrganizationData()


# Test messages
def create_individual_command_generator() -> CreateIndividual:
    return CreateIndividual(
        account_data=AccountData(
            email=test_individual_data.TEST_EMAIL,
            password=test_individual_data.TEST_PASSWORD,
        ),
        profile_data=ProfileData(
            entity_id=test_individual_data.TEST_ENTITY_ID,
            full_name=test_individual_data.TEST_FULL_NAME,
            government_id=test_individual_data.TEST_GOVT_ID,
            phone_number=test_individual_data.TEST_PHONE_NUMBER,
        ),
    )


create_individual_command = create_individual_command_generator()

create_organization_command = CreateOrganization(
    account_data=AccountData(
        email=test_organization_admin_data.TEST_EMAIL,
        password=test_organization_admin_data.TEST_PASSWORD,
    ),
    profile_data=ProfileData(
        entity_id=test_organization_admin_data.TEST_ENTITY_ID,
        full_name=test_organization_admin_data.TEST_FULL_NAME,
        government_id=test_organization_admin_data.TEST_GOVT_ID,
        phone_number=test_organization_admin_data.TEST_PHONE_NUMBER,
    ),
    organization_data=OrganizationData(
        entity_id=test_organization_data.TEST_ORGANIZATION_ID,
        organization_name=test_organization_data.TEST_ORGANIZATION_NAME,
    ),
)


def create_organization_member_command_generator(
    organization_id: str,
    organization_role: OrganizationRole,
    email: str = test_organization_member_data.TEST_EMAIL,
    password: str = test_organization_member_data.TEST_PASSWORD,
    entity_id: str = test_organization_member_data.TEST_ENTITY_ID,
    full_name: str = test_organization_member_data.TEST_FULL_NAME,
    government_id: str = test_organization_member_data.TEST_GOVT_ID,
    phone_number: str = test_organization_member_data.TEST_PHONE_NUMBER,
) -> CreateOrganizationMember:
    return CreateOrganizationMember(
        account_data=AccountData(
            email=email,
            password=password,
        ),
        profile_data=ProfileData(
            entity_id=entity_id,
            full_name=full_name,
            government_id=government_id,
            phone_number=phone_number,
        ),
        organization_member_data=OrganizationMemberData(
            organization_id=organization_id,
            organization_role=organization_role,
        ),
    )


def profile_created_event_generator(
    profile_id: str, email: str = test_individual_data.TEST_EMAIL
) -> ProfileCreated:
    return ProfileCreated(
        entity_id=profile_id,
        account_data=AccountData(
            email=email,
            password=test_individual_data.TEST_PASSWORD,
        ),
        profile_data=ProfileData(
            entity_id=test_individual_data.TEST_ENTITY_ID,
            full_name=test_individual_data.TEST_FULL_NAME,
            government_id=test_individual_data.TEST_GOVT_ID,
            phone_number=test_individual_data.TEST_PHONE_NUMBER,
        ),
        profile_type=ProfileType.INDIVIDUAL,
    )


# Helper functions
async def create_test_individual(
    message_bus: MessageBus,
    entity_id: str = test_individual_data.TEST_ENTITY_ID,
    email: str | None = None,
    password: str = test_individual_data.TEST_PASSWORD,
    full_name: str = test_individual_data.TEST_FULL_NAME,
    government_id: str = test_individual_data.TEST_GOVT_ID,
    phone_number: str = test_individual_data.TEST_PHONE_NUMBER,
) -> None:
    if email is None:
        email = f"{entity_id}@test.com"

    command = CreateIndividual(
        account_data=AccountData(
            email=email,
            password=password,
        ),
        profile_data=ProfileData(
            entity_id=entity_id,
            full_name=full_name,
            government_id=government_id,
            phone_number=phone_number,
        ),
    )

    await message_bus.handle(command)


async def create_test_organization(
    message_bus: MessageBus,
    entity_id: str = test_organization_data.TEST_ORGANIZATION_ID,
    admin_profile_id: str = test_organization_admin_data.TEST_ENTITY_ID,
    organization_name: str = test_organization_data.TEST_ORGANIZATION_NAME,
) -> None:
    command = CreateOrganization(
        account_data=AccountData(
            email=test_organization_admin_data.TEST_EMAIL,
            password=test_organization_admin_data.TEST_PASSWORD,
        ),
        profile_data=ProfileData(
            entity_id=admin_profile_id,
            full_name=test_organization_admin_data.TEST_FULL_NAME,
            government_id=test_organization_admin_data.TEST_GOVT_ID,
            phone_number=test_organization_admin_data.TEST_PHONE_NUMBER,
        ),
        organization_data=OrganizationData(
            entity_id=entity_id,
            organization_name=organization_name,
        ),
    )

    await message_bus.handle(command)


async def create_test_organization_member(
    message_bus: MessageBus,
    organization_id: str,
    organization_role: OrganizationRole,
    entity_id: str = test_organization_member_data.TEST_ENTITY_ID,
) -> None:
    command = CreateOrganizationMember(
        account_data=AccountData(
            email=test_organization_member_data.TEST_EMAIL,
            password=test_organization_member_data.TEST_PASSWORD,
        ),
        profile_data=ProfileData(
            entity_id=entity_id,
            full_name=test_organization_member_data.TEST_FULL_NAME,
            government_id=test_organization_member_data.TEST_GOVT_ID,
            phone_number=test_organization_member_data.TEST_PHONE_NUMBER,
        ),
        organization_member_data=OrganizationMemberData(
            organization_id=organization_id,
            organization_role=organization_role,
        ),
    )

    await message_bus.handle(command)


# Assert functions


def assert_profile(
    profile: Profile,
    profile_type: ProfileType,
    entity_id: str = test_individual_data.TEST_ENTITY_ID,
    full_name: str = test_individual_data.TEST_FULL_NAME,
    government_id: str = test_individual_data.TEST_GOVT_ID,
    phone_number: str = test_individual_data.TEST_PHONE_NUMBER,
) -> None:
    assert profile.entity_id == entity_id
    assert profile.full_name == full_name
    assert profile.government_id == government_id
    assert profile.phone_number == phone_number
    assert profile.profile_type == profile_type
