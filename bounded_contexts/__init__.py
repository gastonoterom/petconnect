# TODO: Get rid of this eyesore
from bounded_contexts.auth.handlers.events.create_account import create_account_handler
from bounded_contexts.pets.handlers.commands.create_pet import create_pet_handler
from bounded_contexts.pets.handlers.commands.register_pet_finding import (
    register_pet_finding_handler,
)
from bounded_contexts.pets.handlers.commands.register_pet_loss import (
    register_pet_as_lost_handler,
)
from bounded_contexts.pets.handlers.commands.register_pet_sight import (
    register_pet_sight_handler,
)
from bounded_contexts.pets.handlers.events.create_pet_owner import (
    create_pet_owner_handler,
)
from bounded_contexts.social.domain.messages import (
    CreateIndividual,
    CreateOrganization,
    CreateOrganizationMember,
    ApproveOrganizationMember,
    ProfileCreated,
)
from bounded_contexts.social.handlers.commands.approve_member import (
    approve_organization_member_handler,
)
from bounded_contexts.social.handlers.commands.create_individual import (
    create_individual_handler,
)
from bounded_contexts.social.handlers.commands.create_organization import (
    create_organization_handler,
)
from bounded_contexts.social.handlers.commands.create_organization_member import (
    create_organization_member_handler,
)
from bounded_contexts.pets.domain.messages import (
    CreatePet,
    RegisterPetLoss,
    RegisterPetFinding,
    RegisterPetSight,
    PetSightRegistered,
)
