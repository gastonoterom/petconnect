from abc import abstractmethod, ABC
from dataclasses import dataclass
from common.unit_of_work import UnitOfWork


@dataclass
class ProfileView:
    entity_id: str
    profile_type: str
    full_name: str
    phone_number: str
    government_id: str


@dataclass
class IndividualView(ProfileView):
    pass


@dataclass
class OrganizationMemberView(ProfileView):
    organization_id: str
    organization_role: str
    approved: bool


class ProfileViewFactory(ABC):
    @abstractmethod
    async def crete_profile_view(self, profile_id: str, uow: UnitOfWork) -> ProfileView:
        pass

    @abstractmethod
    async def creat_individual_view(
        self, profile_id: str, uow: UnitOfWork
    ) -> IndividualView:
        pass

    @abstractmethod
    async def create_organization_member_view(
        self, profile_id: str, uow: UnitOfWork
    ) -> OrganizationMemberView:
        pass
