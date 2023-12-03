from dataclasses import dataclass
from bounded_contexts.social.domain.enums import OrganizationRole


@dataclass
class ProfileData:
    entity_id: str
    full_name: str
    phone_number: str
    government_id: str


@dataclass
class OrganizationMemberData:
    organization_role: OrganizationRole
    organization_id: str


@dataclass
class OrganizationData:
    entity_id: str
    organization_name: str


@dataclass
class AccountData:
    email: str
    password: str
