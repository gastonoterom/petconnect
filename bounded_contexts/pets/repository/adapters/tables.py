from sqlalchemy import Table, Column, String, ForeignKey, Enum, Integer, Boolean, Float
from sqlalchemy.orm import relationship

from bounded_contexts.pets.domain.entities import OwnerProfile, Pet, PetSight
from bounded_contexts.social.domain.enums import ProfileType
from infrastructure import metadata, orm_registry


async def create_pets_tables() -> None:
    owner_profiles_table = Table(
        "owner_profiles",
        metadata,
        Column("entity_id", String, ForeignKey("profiles.entity_id"), primary_key=True),
        Column("profile_type", Enum(ProfileType), nullable=False),
    )

    orm_registry.map_imperatively(
        OwnerProfile,
        owner_profiles_table,
    )

    pets_table = Table(
        "pets",
        metadata,
        Column("entity_id", String, primary_key=True),
        Column("pet_name", String, nullable=False),
        Column(
            "owner_profile_id",
            String,
            ForeignKey(owner_profiles_table.c.entity_id),
            nullable=False,
        ),
        Column("lost", Boolean, nullable=False),
        Column("version", Integer, nullable=False),
    )

    pet_sights_table = Table(
        "pet_sights",
        metadata,
        Column("entity_id", String, primary_key=True),
        Column("pet_id", String, ForeignKey(pets_table.c.entity_id), nullable=True),
        Column("latitude", Float, nullable=False),
        Column("longitude", Float, nullable=False),
        Column(
            "spotter_profile_id",
            String,
            ForeignKey(owner_profiles_table.c.entity_id),
            nullable=True,
        ),
    )

    orm_registry.map_imperatively(
        PetSight,
        pet_sights_table,
    )

    orm_registry.map_imperatively(
        Pet,
        pets_table,
        properties={
            "sights": relationship(
                PetSight, lazy="joined", cascade="all, delete-orphan"
            ),
        },
    )
