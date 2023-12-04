from sqlalchemy import text
from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.views.factories.profile_view_factory import (
    ProfileViewFactory,
    ProfileView,
    IndividualView,
    OrganizationMemberView,
)
from common.unit_of_work import UnitOfWork


class AlchemyProfileViewFactory(ProfileViewFactory):
    async def crete_profile_view(self, profile_id: str, uow: UnitOfWork) -> ProfileView:
        profile_dict = await self.__get_profile_row(profile_id, uow)
        profile_type = ProfileType(profile_dict["profile_type"])

        if profile_type == ProfileType.INDIVIDUAL:
            return self.__create_individual_view(profile_dict)

        if profile_type == ProfileType.ORGANIZATIONAL:
            return self.__create_organization_member_view(profile_dict)

        raise ValueError(f"Invalid profile type {profile_dict['profile_type']}")

    async def creat_individual_view(
        self, profile_id: str, uow: UnitOfWork
    ) -> IndividualView:
        profile_dict = await self.__get_profile_row(profile_id, uow)
        profile_type = ProfileType(profile_dict["profile_type"])

        if profile_type != ProfileType.INDIVIDUAL:
            raise ValueError(
                f"Tried to create individual profile view for profile type: {profile_type}"
            )

        return self.__create_individual_view(profile_dict)

    async def create_organization_member_view(
        self, profile_id: str, uow: UnitOfWork
    ) -> OrganizationMemberView:
        profile_dict = await self.__get_profile_row(profile_id, uow)
        profile_type = ProfileType(profile_dict["profile_type"])

        if profile_type != ProfileType.ORGANIZATIONAL:
            raise ValueError(
                f"Tried to create organization member profile view for profile type: {profile_type}"
            )

        return self.__create_organization_member_view(profile_dict)

    async def __get_profile_row(self, profile_id: str, uow: UnitOfWork) -> dict:
        query = text(
            """
            SELECT 
                p.entity_id,
                p.profile_type,
                p.full_name,
                p.phone_number,
                p.government_id ,
                op.organization_id, 
                op.organization_role, 
                op.approved
            FROM profiles p 
            LEFT JOIN organizational_profiles op ON p.entity_id = op.entity_id
            WHERE p.entity_id = :entity_id
            """
        )

        result = await uow.session.execute(query, {"entity_id": profile_id})

        row = result.first()

        if row is None:
            raise Exception("Profile not found")

        return dict(row._mapping)

    def __create_individual_view(self, profile_dict: dict) -> IndividualView:
        return IndividualView(
            entity_id=profile_dict["entity_id"],
            profile_type=profile_dict["profile_type"],
            full_name=profile_dict["full_name"],
            phone_number=profile_dict["phone_number"],
            government_id=profile_dict["government_id"],
        )

    def __create_organization_member_view(
        self, profile_dict: dict
    ) -> OrganizationMemberView:
        return OrganizationMemberView(
            entity_id=profile_dict["entity_id"],
            profile_type=profile_dict["profile_type"],
            full_name=profile_dict["full_name"],
            phone_number=profile_dict["phone_number"],
            government_id=profile_dict["government_id"],
            approved=profile_dict["approved"],
            organization_id=profile_dict["organization_id"],
            organization_role=profile_dict["organization_role"],
        )
