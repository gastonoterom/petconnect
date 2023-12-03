from sqlalchemy import Table, Column, String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from bounded_contexts.social.domain.entities import (
    Profile,
    OrganizationMember,
    Individual,
    Organization,
)
from bounded_contexts.social.domain.enums import ProfileType
from bounded_contexts.social.domain.value_objects import OrganizationRole
from infrastructure import metadata, orm_registry


async def create_social_tables() -> None:
    # Profiles

    profiles_table = Table(
        "profiles",
        metadata,
        # Shared attributes
        Column("entity_id", String, primary_key=True),
        Column("email", String, nullable=False, unique=True),
        Column(
            "full_name",
            String,
            nullable=False,
        ),
        Column("phone_number", String, nullable=False),
        Column("government_id", String, nullable=False),
        # Discriminator
        Column("profile_type", Enum(ProfileType), nullable=False),
    )

    individual_profiles_table = Table(
        "individual_profiles",
        metadata,
        Column(
            "entity_id",
            String,
            ForeignKey(profiles_table.c.entity_id),
            primary_key=True,
        ),
    )

    organizational_profiles_table = Table(
        "organizational_profiles",
        metadata,
        Column(
            "entity_id",
            String,
            ForeignKey(profiles_table.c.entity_id),
            primary_key=True,
        ),
        Column(
            "organization_id",
            String,
            ForeignKey("organizations.entity_id"),
            nullable=False,
        ),
        Column("organization_role", Enum(OrganizationRole), nullable=False),
        Column("approved", Boolean, nullable=False),
    )

    base = orm_registry.map_imperatively(
        Profile,
        profiles_table,
        with_polymorphic=("*", profiles_table),
        polymorphic_on=profiles_table.c.profile_type,
    )

    orm_registry.map_imperatively(
        Individual,
        individual_profiles_table,
        inherits=base,
        polymorphic_identity=ProfileType.INDIVIDUAL,
    )

    orm_registry.map_imperatively(
        OrganizationMember,
        organizational_profiles_table,
        inherits=base,
        polymorphic_identity=ProfileType.ORGANIZATIONAL,
    )

    # Organizations

    organization_table = Table(
        "organizations",
        metadata,
        # Shared attributes
        Column("entity_id", String, primary_key=True),
        Column("organization_name", String, unique=True, nullable=False),
        Column("version", Integer, nullable=False),
    )

    orm_registry.map_imperatively(
        Organization,
        organization_table,
        properties={
            "members": relationship(
                OrganizationMember,
                lazy="joined",
            ),
        },
    )
