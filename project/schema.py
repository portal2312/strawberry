"""Project Root Schema.

References:
    https://strawberry.rocks/docs/types/schema#filteringcustomising-fields
    https://strawberry.rocks/docs/general/subscriptions
"""

import asyncio
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import TYPE_CHECKING, AsyncGenerator
from uuid import uuid4

import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from app.mutations import Mutation as AppMutation
from app.queries import Query as AppQuery
from app.subscriptions import Subscription as AppSubscription
from my_pydantic.pydantic.types import IPAddress, IPNetwork
from my_pydantic.scalars import (
    IPAddressScalar,
    IPNetworkScalar,
    IPv4AddressScalar,
    IPv4NetworkScalar,
    IPv6AddressScalar,
    IPv6NetworkScalar,
)
from my_pydantic.schema import Mutation as MyPydanticMutation
from my_pydantic.schema import Query as MyPydanticQuery

if TYPE_CHECKING:
    from strawberry.types.field import StrawberryField


@strawberry.type
class Query(AppQuery, MyPydanticQuery):
    """Root query class."""


@strawberry.type
class Mutation(AppMutation, MyPydanticMutation):
    """Root mutation class."""


event_messages = {}


@strawberry.type
class Subscription(AppSubscription):
    """Root subscription class."""

    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        """Count."""
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

    @strawberry.subscription
    async def message(self) -> AsyncGenerator[int, None]:
        try:
            subscription_id = uuid4()

            event_messages[subscription_id] = []

            while True:
                if len(event_messages[subscription_id]) > 0:
                    yield event_messages[subscription_id]
                    event_messages[subscription_id].clear()

                await asyncio.sleep(1)
        except asyncio.CancelledError:
            # stop listening to events
            del event_messages[subscription_id]


def public_field_filter(field: "StrawberryField") -> bool:
    """Public field filter.

    Example:
        Refer to ``types.py``::

            from strawberry import auto
            from strawberry_django import field, type

            @type(models.Color)
            class Color:
                id: auto
                name: auto
                description: auto | None = field(metadata={"tags": ["internal"]})  # Exclude the filtered field.

        Execute `python manage.py export_schema project.schema` CLI::

            type Color {
                id: ID!
                name: String!
            }
            ...
    """
    return "internal" not in field.metadata.get("tags", [])


class PublicSchema(strawberry.Schema):
    """Override Schema class."""

    def get_fields(self, type_definition) -> list:  # type: ignore
        """Override get_fields function."""
        return list(filter(public_field_filter, type_definition.fields))


# Root Schema
schema = PublicSchema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,  # not required, but highly recommended
    ],
    scalar_overrides={
        IPAddress: IPAddressScalar,
        IPNetwork: IPNetworkScalar,
        IPv4Address: IPv4AddressScalar,
        IPv4Network: IPv4NetworkScalar,
        IPv6Address: IPv6AddressScalar,
        IPv6Network: IPv6NetworkScalar,
    },
)
