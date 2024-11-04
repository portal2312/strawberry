"""Schema in my_pydantic app."""

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

import strawberry
import strawberry_django

from .mutations import save_shared_network
from .pydantic.types import IPAddress, IPNetwork
from .queries import get_shared_network
from .scalars import (
    IPAddressScalar,
    IPNetworkScalar,
    IPv4AddressScalar,
    IPv4NetworkScalar,
    IPv6AddressScalar,
    IPv6NetworkScalar,
)
from .types import SharedNetwork


@strawberry.type
class Query:
    """Root query in my_pydantic app."""

    my_pydantic: bool = strawberry.field(resolver=lambda: True)
    shared_network: SharedNetwork = strawberry.field(
        resolver=get_shared_network,
    )


@strawberry.type
class Mutation:
    """Root mutation in my_pydantic app."""

    is_my_pydantic: bool = strawberry.field(resolver=lambda: True)
    save_shared_network: SharedNetwork = strawberry_django.field(
        resolver=save_shared_network,
    )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    scalar_overrides={
        IPAddress: IPAddressScalar,
        IPNetwork: IPNetworkScalar,
        IPv4Address: IPv4AddressScalar,
        IPv4Network: IPv4NetworkScalar,
        IPv6Address: IPv6AddressScalar,
        IPv6Network: IPv6NetworkScalar,
    },
)
