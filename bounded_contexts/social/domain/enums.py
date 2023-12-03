from enum import Enum


class OrganizationRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    VOLUNTEER = "volunteer"


class ProfileType(Enum):
    INDIVIDUAL = "individual"
    ORGANIZATIONAL = "organizational"
