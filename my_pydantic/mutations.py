"""Mutations in my_pydantic app.

References:
    https://strawberry.rocks/docs/integrations/pydantic

"""

from graphql import GraphQLError
from pydantic import ValidationError
from strawberry.types import Info

from .exceptions import convert_errors
from .inputs import SharedNetworkInput
from .types import SharedNetwork


def save_shared_network(info: Info, input: SharedNetworkInput) -> SharedNetwork:
    """Resolve save_shared_network."""
    try:
        instance = input.to_pydantic()
    except ValidationError as e:
        errors = convert_errors(e)
        raise GraphQLError(f"{errors}") from e
    return SharedNetwork.from_pydantic(instance)
