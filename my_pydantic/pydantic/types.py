"""Pydantic types in my_pydantic app.

References:
    https://docs.pydantic.dev/latest/concepts/types
    https://docs.pydantic.dev/latest/concepts/serialization/
    https://docs.pydantic.dev/latest/concepts/validators/
"""

from ipaddress import IPv4Address, IPv6Address, ip_address

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
