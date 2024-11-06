"""Models in the my_pydantif app.

References:
    https://linux.die.net/man/5/dhcpd.conf
    https://docs.pydantic.dev/latest/api/base_model/
    https://docs.pydantic.dev/latest/concepts/fields/
    https://docs.pydantic.dev/latest/concepts/serialization/
    https://docs.pydantic.dev/latest/concepts/validators/
    https://docs.pydantic.dev/latest/errors/errors/
    https://docs.pydantic.dev/latest/concepts/config/
    https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_assignment
"""

import abc
from ipaddress import IPv6Address, IPv6Network
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

from .types import DUID, IAID, IPAddress


class AbstractBaseModel(BaseModel, abc.ABC):
    model_config = ConfigDict(
        validate_assignment=True,
    )


class Option(AbstractBaseModel):
    """Dynamic Host Configuration Protocol options.

    References:
        https://linux.die.net/man/5/dhcp-options
    """

    dns_servers: list[IPAddress] | None = Field(
        default=None,
        description=(
            'The `name-servers` option instructs clients about locally available recursive DNS servers. It is easiest to describe this as the "nameserver" line in /etc/resolv.conf.'
        ),
    )
    domain_list: list[str] | None = Field(
        default=None,
        description=(
            'The domain-list data type specifies a list of domain names, enclosed in double quotes and separated by commas ("example.com", "foo.example.com").'
        ),
    )

    @field_serializer("dns_servers")
    def serialize_dns_servers(self, dns_servers: list[IPAddress], info) -> str:
        """Serialize dns_servers field."""
        return ", ".join(dns_server.compressed for dns_server in dns_servers)

    @field_validator("domain_list", mode="before")
    @classmethod
    def check_domain_list(cls, value: Any) -> list[str] | Any:
        """Check and parse domain_list.

        Args:
            value (Any): Unparsed domain_list value.

        Returns:
            list[str] | Any: parsed domain_list or any.
        """
        if isinstance(value, str):
            # Split the string by commas and strip whitespace
            value = [item.strip() for item in value.split(",")]

        # Return the value as-is if it's neither string, list, nor tuple
        return value

    @field_serializer("domain_list")
    def serialize_domain_list(self, domain_list: list[str], info) -> str:
        """Serialize dns_servers field."""
        return ", ".join(domain for domain in domain_list)


class Parameter(AbstractBaseModel):
    """Dynamic Host Configuration Protocol parameters."""

    preferred_lifetime: int = Field(
        gt=0,
        description=(
            "IPv6 addresses have 'valid' and 'preferred' lifetimes. The valid lifetime determines at what point at lease might be said to have expired, and is no longer useable. A preferred lifetime is an advisory condition to help applications move off of the address and onto currently valid addresses (should there still be any open TCP sockets or similar)."
            ""
            "The preferred lifetime defaults to the renew+rebind timers, or 3/4 the default lease time if none were specified."
        ),
        # alias="preferred-lifetime",
    )
    valid_lifetime: int = Field(
        gt=0,
        description=(
            'Time should be the length in seconds that will be assigned to a lease if the client requesting the lease does not ask for a specific expiration time. This is used for both DHCPv4 and DHCPv6 leases (it is also known as the "valid lifetime" in DHCPv6).'
        ),
        # alias="default-lease-time",
    )

    @model_validator(mode="after")
    def check_preferred_lifetime__lte__valid_lifetime(self) -> Self:
        """Check preferred_lifetime less than or equal valid_lifetime."""
        if self.preferred_lifetime is None:
            return self
        if self.valid_lifetime is None:
            raise PydanticCustomError(
                "preferred_lifetime__lte__valid_lifetime__is_none",
                "Preferred Lifetime 의 값이 있는 경우, Valid Lifetime 의 값이 존재해야 합니다.",
            )
        if self.preferred_lifetime > self.valid_lifetime:
            raise PydanticCustomError(
                "preferred_lifetime__lte__valid_lifetime__greater",
                "Preferred Lifetime 이 Valid Lifetime 보다 큽니다: {preferred_lifetime} <= {valid_lifetime} 은 올바르지 않습니다.",
                {
                    "preferred_lifetime": self.preferred_lifetime,
                    "valid_lifetime": self.valid_lifetime,
                },
            )
        return self


class Bind(AbstractBaseModel):
    """Dynamic Host Configuration Protocol bind for IPv6Address."""

    duid: DUID
    iaid: IAID
    ip6_address: IPv6Address


class Subnet6(AbstractBaseModel):
    """Subnet IPv6Network.

    The `subnet6` statement is used to provide dhcpd with enough information to
    tell whether or not an IPv6 address is on that subnet6.
    It may also be used to provide subnet-specific parameters and to specify
    what addresses may be dynamically allocated to clients booting on that subnet.
    """

    subnet6_number: IPv6Network = Field(
        description=(
            "The `subnet6-number` should be an IPv6 network identifier, specified as ip6-address/bits."
        ),
        # alias="subnet6-number",
    )


class SharedNetwork(AbstractBaseModel):
    """SharedNetwork.

    The `shared-network` statement is used to inform the DHCP server that some IP subnets actually share the same physical network.
    Any subnets in a shared network should be declared within a shared-network statement.
    Parameters specified in the shared-network statement will be used when booting clients on those subnets unless parameters provided at the subnet or host level override them.
    If any subnet in a shared network has addresses available for dynamic allocation, those addresses are collected into a common pool for that shared network and assigned to clients as needed.
    There is no way to distinguish on which subnet of a shared network a client should boot.
    """

    name: str = Field(
        min_length=1,
        pattern=r"^\w*$",
        description=(
            "Name should be the name of the shared network. This name is used when printing debugging messages, so it should be descriptive for the shared network. The name may have the syntax of a valid domain name (although it will never be used as such), or it may be any arbitrary name, enclosed in quotes."
        ),
    )
    description: str | None = Field(
        default=None,
        max_length=79,
        description="Description of the shared network.",
    )
    option: Option = Field(
        description=Option.__doc__,
    )
    parameter: Parameter = Field(
        description=Parameter.__doc__,
    )
    subnets: list[Subnet6] | None = Field(
        default=None,
        description=Subnet6.__doc__,
    )
