from enum import Enum, unique


@unique
class CommonDependencyKind(str, Enum):
    dispatcher_factory = "dispatcher_factory"
    uow = "uow"


@unique
class AuthDependencyKind(str, Enum):
    accounts_repository = "accounts_repository"


@unique
class SocialDependencyKind(str, Enum):
    # Repositories
    individuals_repository = "individuals_repository"
    organizations_repository = "organizations_repository"

    # View factories
    profile_view_factory = "profile_view_factory"


@unique
class PetDependencyKind(str, Enum):
    owners_repository = "owners_repository"
    pets_repository = "pets_repository"
