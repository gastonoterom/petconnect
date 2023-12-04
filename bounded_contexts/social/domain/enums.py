from enum import Enum


class OrganizationRole(Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    VOLUNTEER = "VOLUNTEER"


class ProfileType(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    ORGANIZATIONAL = "ORGANIZATIONAL"
