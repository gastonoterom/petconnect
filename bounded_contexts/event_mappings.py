from dataclasses import dataclass
from typing import Type, Callable

# TODO: this can be better
from bounded_contexts import (
    create_individual_handler,
    create_organization_handler,
    create_organization_member_handler,
    approve_organization_member_handler,
    create_pet_handler,
    register_pet_as_lost_handler,
    register_pet_finding_handler,
    register_pet_sight_handler,
    CreateIndividual,
    CreateOrganization,
    CreateOrganizationMember,
    ApproveOrganizationMember,
    CreatePet,
    RegisterPetLoss,
    RegisterPetFinding,
    RegisterPetSight,
    ProfileCreated,
    create_account_handler,
    PetSightRegistered,
    create_pet_owner_handler,
)
from common.base_utils import Event, Command


@dataclass
class Dispatcher:
    event_handlers: dict[Type[Event], list[Callable]]
    command_handlers: dict[Type[Command], Callable]


command_handlers: dict[Type[Command], Callable] = {
    # Social commands handlers
    CreateIndividual: create_individual_handler,
    CreateOrganization: create_organization_handler,
    CreateOrganizationMember: create_organization_member_handler,
    ApproveOrganizationMember: approve_organization_member_handler,
    # Pets commands handlers
    CreatePet: create_pet_handler,
    RegisterPetLoss: register_pet_as_lost_handler,
    RegisterPetFinding: register_pet_finding_handler,
    RegisterPetSight: register_pet_sight_handler,
}


event_handlers: dict[Type[Event], list[Callable]] = {
    # Social events
    ProfileCreated: [
        create_account_handler,
        create_pet_owner_handler,
    ],
    # Pet events
    PetSightRegistered: [],
}
