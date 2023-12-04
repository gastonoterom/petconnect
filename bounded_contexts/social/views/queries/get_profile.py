from dependency_injector.wiring import Provide, inject
from bounded_contexts.social.views.factories.profile_view_factory import (
    ProfileView,
    ProfileViewFactory,
)
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind, SocialDependencyKind


@inject
async def get_profile(
    profile_id: str,
    profile_view_factory: ProfileViewFactory = Provide[
        SocialDependencyKind.profile_view_factory
    ],
    uow: UnitOfWork = Provide[CommonDependencyKind.uow],
) -> ProfileView:
    async with uow:
        view = await profile_view_factory.crete_profile_view(
            uow=uow,
            profile_id=profile_id,
        )

    return view
