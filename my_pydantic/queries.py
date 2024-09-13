"""Queries in the my_pydantic app."""

from strawberry.types import Info

from my_pydantic.models import Parameter

from .types import SharedNetwork


def get_shared_network(info: Info) -> SharedNetwork:
    """Resolves a shared network."""
    instance = SharedNetwork(
        name="A",
        description="D",
        parameter=Parameter(
            preferred_lifetime=1,
            valid_lifetime=1,
        ),
    )
    return instance
