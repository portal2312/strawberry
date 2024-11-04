"""Pydantic types in my_pydantic app.

References:
    https://docs.pydantic.dev/latest/concepts/types
    https://docs.pydantic.dev/latest/concepts/serialization/
    https://docs.pydantic.dev/latest/concepts/validators/
    https://docs.python.org/3/library/ipaddress.html#ipaddress.ip_address
    https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address
    https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv6Address
    https://docs.python.org/3/library/ipaddress.html#ipaddress.ip_network
    https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network
    https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv6Network
"""

from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    ip_address,
    ip_network,
)

from pydantic import (
    AfterValidator,
    PlainSerializer,
)
from typing_extensions import Annotated, TypeAliasType

IPAddress = TypeAliasType(
    "IPAddress",
    Annotated[
        IPv4Address | IPv6Address,
        AfterValidator(lambda v: ip_address(v)),
        PlainSerializer(str, return_type=str),
    ],
)

IPNetwork = TypeAliasType(
    "IPNetwork",
    Annotated[
        IPv4Network | IPv6Network,
        AfterValidator(lambda v: ip_network(v)),
        PlainSerializer(str, return_type=str),
    ],
)
