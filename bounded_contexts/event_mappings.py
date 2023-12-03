from dataclasses import dataclass
from typing import Type, Callable
from common.base_utils import Event, Command

# Social imports
import bounded_contexts.social.domain.messages as social_messages
import bounded_contexts.social.handlers.commands as social_command_handlers

# Pet imports
import bounded_contexts.pets.domain.messages as pet_messages
import bounded_contexts.pets.handlers.commands as pet_command_handlers
import bounded_contexts.pets.handlers.events as pet_event_handlers

# Auth imports
import bounded_contexts.auth.handlers.events as auth_event_handlers


command_handlers: dict[Type[Command], Callable] = {
    # Social commands handlers
    social_messages.CreateIndividual: social_command_handlers.create_individual_handler,
    social_messages.CreateOrganization: social_command_handlers.create_organization_handler,
    social_messages.CreateOrganizationMember: social_command_handlers.create_organization_member_handler,
    social_messages.ApproveOrganizationMember: social_command_handlers.approve_organization_member_handler,
    # Pets commands handlers
    pet_messages.CreatePet: pet_command_handlers.create_pet_handler,
    pet_messages.RegisterPetLoss: pet_command_handlers.register_pet_loss_handler,
    pet_messages.RegisterPetFinding: pet_command_handlers.register_pet_finding_handler,
    pet_messages.RegisterPetSight: pet_command_handlers.register_pet_sight_handler,
}


event_handlers: dict[Type[Event], list[Callable]] = {
    # Social events
    social_messages.ProfileCreated: [
        auth_event_handlers.create_account_handler,
        pet_event_handlers.create_pet_owner_handler,
    ],
    # Pet events
    pet_messages.PetSightRegistered: [],
}


@dataclass
class Dispatcher:
    event_handlers: dict[Type[Event], list[Callable]]
    command_handlers: dict[Type[Command], Callable]
