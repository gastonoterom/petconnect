from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.domain.value_objects import OrganizationRole
from common.base_utils import Entity

# Profile base class


class Profile(Entity):
    def __init__(
        self,
        entity_id: str,
        email: str,
        full_name: str,
        phone_number: str,
        government_id: str,
        profile_type: ProfileType,
    ) -> None:
        super().__init__(entity_id=entity_id)
        self.email = email

        self.full_name = full_name
        self.phone_number = phone_number
        self.government_id = government_id

        self.profile_type = profile_type


# Individual aggregate


class Individual(Profile):
    def __init__(
        self,
        entity_id: str,
        email: str,
        full_name: str,
        phone_number: str,
        government_id: str,
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            government_id=government_id,
            profile_type=ProfileType.INDIVIDUAL,
        )


# Organization aggregate


class OrganizationMember(Profile):
    def __init__(
        self,
        entity_id: str,
        email: str,
        full_name: str,
        phone_number: str,
        government_id: str,
        organization_id: str,
        organization_role: OrganizationRole,
        approved: bool,
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            government_id=government_id,
            profile_type=ProfileType.ORGANIZATIONAL,
        )

        # Organization data

        self.organization_id = organization_id
        self.organization_role = organization_role
        self.approved = approved

    @property
    def organization_admin(self) -> bool:
        return self.organization_role == OrganizationRole.ADMIN


class Organization:
    def __init__(
        self,
        entity_id: str,
        organization_name: str,
        members: list[OrganizationMember],
        version: int = 0,  # For consistency purposes
    ) -> None:
        self.entity_id = entity_id
        self.organization_name = organization_name

        self.members: list[OrganizationMember] = members

        self.version = version

    @property
    def admin(self) -> OrganizationMember:
        return next(
            member
            for member in self.members
            if member.organization_role == OrganizationRole.ADMIN
        )

    def join_organization(self, member: OrganizationMember) -> None:
        if member.organization_role == OrganizationRole.ADMIN:
            raise Exception("There can only be one admin in an organization")

        self.members.append(member)
        self.version += 1

    def approve_member(self, actor_member_id: str, member_id: str) -> None:
        if not self.admin.entity_id == actor_member_id:
            raise Exception("Only organization admin can approve members")

        member: OrganizationMember = self.get_member(member_id)

        member.approved = True

        self.version += 1

    def get_member(self, member_profile_id: str) -> OrganizationMember:
        member = self.find_member(member_profile_id)

        if member is None:
            raise Exception("Member not found")

        return member

    def find_member(self, member_profile_id) -> OrganizationMember | None:
        return next(
            (
                member
                for member in self.members
                if member.entity_id == member_profile_id
            ),
            None,
        )
