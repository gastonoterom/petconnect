from dataclasses import dataclass

from bounded_contexts.pets.domain.value_objects import Location
from common.base_utils import Command, Event


# Commands
@dataclass
class CreatePet(Command):
    entity_id: str
    actor_profile_id: str
    pet_name: str


@dataclass
class RegisterPetSight(Command):
    pet_id: str
    actor_profile_id: str | None  # Maybe an anonymous user reported the pet sight
    latitude: float
    longitude: float


@dataclass
class RegisterPetLoss(Command):
    pet_id: str
    actor_profile_id: str
    last_sight: Location


@dataclass
class RegisterPetFinding(Command):
    pet_id: str
    actor_profile_id: str


# Events
@dataclass
class PetSightRegistered(Event):
    pet_id: str
    owner_profile_id: str
    actor_profile_id: str | None  # Maybe an anonymous user reported the pet sight
