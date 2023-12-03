from dependency_injector.wiring import Provide, inject
from bounded_contexts.social.domain.entities import Individual
from bounded_contexts.social.domain.messages import CreateIndividual, ProfileCreated
from bounded_contexts.social.repository.social_repositories import IndividualsRepository
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import SocialDependencyKind


@inject
async def create_individual_handler(
    command: CreateIndividual,
    uow: UnitOfWork,
    individuals_repository: IndividualsRepository = Provide[
        SocialDependencyKind.individuals_repository
    ],
) -> None:
    async with uow:
        individual = Individual(
            entity_id=command.profile_data.entity_id,
            email=command.account_data.email,
            full_name=command.profile_data.full_name,
            government_id=command.profile_data.government_id,
            phone_number=command.profile_data.phone_number,
        )

        await individuals_repository.add_individual(uow=uow, individual=individual)

    uow.publish_message(
        ProfileCreated(
            entity_id=individual.entity_id,
            account_data=command.account_data,
            profile_data=command.profile_data,
            profile_type=individual.profile_type,
        )
    )
