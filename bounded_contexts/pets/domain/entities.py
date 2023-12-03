from bounded_contexts.social.domain.enums import ProfileType
from common.base_utils import Entity


# Owner profile aggregate


class OwnerProfile(Entity):
    def __init__(self, entity_id: str, profile_type: ProfileType) -> None:
        super().__init__(entity_id=entity_id)

        self.entity_id = entity_id
        self.profile_type = profile_type


# Pet aggregate


class PetSight(Entity):
    def __init__(
        self,
        entity_id: str,
        spotter_profile_id: str | None,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(entity_id=entity_id)
        self.latitude = latitude
        self.longitude = longitude
        self.spotter_profile_id = spotter_profile_id


class Pet(Entity):
    def __init__(
        self,
        entity_id: str,
        pet_name: str,
        owner_profile_id: str,
        lost: bool = False,
        sights: list[PetSight] | None = None,
        version: int = 0,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self.pet_name: str = pet_name
        self.owner_profile_id: str = owner_profile_id
        self.lost: bool = lost

        if sights is None:
            sights = []

        self.sights: list[PetSight] = sights
        self.version: int = version

    async def register_sight(self, pet_sight: PetSight) -> None:
        if not self.lost:
            # Maybe the owner is at work, and someone finds the pet in the street, so
            # if someone scans the collar, it should automatically mark the pet as lost
            self.lost = True

        self.sights.append(pet_sight)

        self.version += 1

    async def mark_as_found(self, actor_profile_id: str) -> None:
        if self.owner_profile_id != actor_profile_id:
            raise Exception("Only the owner can mark the pet as found")

        self.lost = False
        # We don't care about the previous sights, if we ever need it we need to create a history aggregate
        self.sights.clear()
        self.version += 1

    async def mark_as_lost(self, actor_profile_id: str, last_sight: PetSight) -> None:
        if self.owner_profile_id != actor_profile_id:
            raise Exception("Only the owner can mark the pet as lost")

        self.lost = True
        # The owner should always know where they saw the pet for the last time
        self.sights = [last_sight]
        self.version += 1
