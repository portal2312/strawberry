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

from pydantic import AfterValidator, Field, PlainSerializer
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

DUID = TypeAliasType(
    "DUID",
    Annotated[
        str,
        Field(
            pattern=r"^(?:[0-9A-Fa-f]{2}[:-]?){1,128}$",
            min_length=1,
            max_length=128,
            description=(
                "A DHCP Unique Identifier (DUID) is made up of a 2-byte code and a variable-length identifier field that can be up to 128 bytes long."
                "The DUID's actual length depends on its type."
                "\n\n"
                "The `server-duid` statement configures the server DUID."
                "You may pick either LLT (link local address plus time), EN (enterprise), or LL (link local)."
                "If you choose LLT or LL, you may specify the exact contents of the DUID. Otherwise the server will generate a DUID of the specified type."
                "If you choose EN, you must include the enterprise number and the enterprise-identifier."
                "The default `server-duid` type is LLT."
                "\n\n"
                'For example: `"000300011A2B3C4D5E6F7A8B"` or `"00:03:00:01:1A:2B:3C:4D:5E:6F:7A:8B"`',
            ),
        ),
    ],
)

IAID = TypeAliasType(
    "IAID",
    Annotated[
        str,
        Field(
            pattern=r"^((?:[0-9A-Fa-f]{2}:){3}[0-9A-Fa-f]{2})|(?:[1-9][0-9]{0,9}|0)$",
            description=(
                "The DHCP Identity Association Identifier (IAID) is typically a 4-byte identifier, often represented as either a hexadecimal number or an integer."
                "The IAID helps DHCP servers and clients uniquely identify network interfaces."
                "\n\n"
                'For example: `"1A:2B:3C:4D"` or `"4294967295"`'
            ),
        ),
    ],
)
