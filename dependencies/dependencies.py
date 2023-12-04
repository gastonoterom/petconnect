from dependency_injector import providers, containers
from bounded_contexts.auth.repository.adapters.sqlalchemy import (
    AlchemyAccountsRepository,
)
from bounded_contexts.event_mappings import (
    Dispatcher,
    command_handlers,
    event_handlers,
)
from bounded_contexts.pets.repository.adapters.sqlalchemy import (
    AlchemyOwnersRepository,
    AlchemyPetsRepository,
)
from bounded_contexts.social.repository.adapters.sqlalchemy import (
    AlchemyIndividualsRepository,
    AlchemyOrganizationsRepository,
)
from bounded_contexts.social.views.factories.adapters.sqlalchemy_profile_view_factory import (
    AlchemyProfileViewFactory,
)
from common.unit_of_work import UnitOfWork


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "bounded_contexts",
            "common",
            "infrastructure",
        ],
    )

    # Common dependencies

    uow = providers.Factory(UnitOfWork)

    dispatcher_factory = providers.Factory(
        Dispatcher,
        command_handlers=providers.Dict(command_handlers),
        event_handlers=providers.Dict(event_handlers),
    )

    # Auth dependencies

    accounts_repository = providers.Singleton(AlchemyAccountsRepository)

    # Social dependencies

    individuals_repository = providers.Singleton(AlchemyIndividualsRepository)
    organizations_repository = providers.Singleton(AlchemyOrganizationsRepository)

    profile_view_factory = providers.Singleton(AlchemyProfileViewFactory)

    # Pet dependencies
    owners_repository = providers.Singleton(AlchemyOwnersRepository)
    pets_repository = providers.Singleton(AlchemyPetsRepository)
