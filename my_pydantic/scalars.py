"""Scalars in my_pydantic app.

References:
    https://strawberry.rocks/docs/types/scalars
    https://strawberry.rocks/docs/integrations/pydantic#classes-with-__get_validators__
"""

from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import NewType

import strawberry

from .pydantic.types import IPAddress

IPv4AddressScalar = strawberry.scalar(
    NewType("IPv4Address", IPv4Address),
    serialize=str,
    parse_value=lambda address: IPv4Address(address),
    description="The IPv4Address scalar type represents `IPv4Address`.",
)

IPv6AddressScalar = strawberry.scalar(
    NewType("IPv6Address", IPv6Address),
    serialize=str,
    parse_value=lambda address: IPv6Address(address),
    description="The IPv6Address scalar type represents `IPv6Address`.",
)

IPAddressScalar = strawberry.scalar(
    IPAddress,
    serialize=str,
    parse_value=lambda x: ip_address(x),
    description="The IPAddress scalar type represents `IPv4Address` or `IPv6Address`.",
)
