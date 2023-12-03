from dataclasses import dataclass

from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.domain.value_objects import (
    ProfileData,
    OrganizationMemberData,
    AccountData,
    OrganizationData,
)
from common.base_utils import Command, Event


# Commands
@dataclass
class CreateIndividual(Command):
    account_data: AccountData
    profile_data: ProfileData


@dataclass
class CreateOrganizationMember(Command):
    account_data: AccountData
    profile_data: ProfileData
    organization_member_data: OrganizationMemberData


@dataclass
class CreateOrganization(Command):
    account_data: AccountData
    profile_data: ProfileData
    organization_data: OrganizationData


@dataclass
class ApproveOrganizationMember(Command):
    actor_member_id: str
    member_id: str


# Events
@dataclass
class ProfileCreated(Event):
    entity_id: str
    profile_type: ProfileType
    account_data: AccountData
    profile_data: ProfileData


@dataclass
class OrganizationMemberCreated(Event):
    entity_id: str
    profile_data: ProfileData
    organization_member_data: OrganizationMemberData


@dataclass
class OrganizationMemberApproved(Event):
    member_id: str
