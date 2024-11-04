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
from ipaddress import IPv6Network
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

from .types import IPAddress


class AbstractBaseModel(BaseModel, abc.ABC):
    model_config = ConfigDict(
        validate_assignment=True,
    )


class Option(AbstractBaseModel):
    """Options."""

    dns_servers: list[IPAddress] | None = Field(default=None)
    domain_list: list[str] | None = Field(default=None)

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
    """Parameter."""

    preferred_lifetime: int = Field(
        gt=0,
        description="Preferred Lifetime",
    )
    valid_lifetime: int = Field(
        gt=0,
        description="Valid Lifetime",
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


class Subnet6(AbstractBaseModel):
    """Subnet6 IPv6Network.

    The subnet6 statement is used to provide dhcpd with enough information to
    tell whether or not an IPv6 address is on that subnet6.
    It may also be used to provide subnet-specific parameters and to specify
    what addresses may be dynamically allocated to clients booting on that subnet.
    """

    subnet6_number: IPv6Network = Field(
        description="The `subnet6-number` should be an IPv6 network identifier, specified as ip6-address/bits."
    )


class SharedNetwork(AbstractBaseModel):
    """SharedNetwork.

    The shared-network statement is used to inform the DHCP server
    that some IP subnets actually share the same physical network.
    Any subnets in a shared network should be declared within a shared-network statement.
    Parameters specified in the shared-network statement will be used when booting clients
    on those subnets unless parameters provided at the subnet or host level override them.
    If any subnet in a shared network has addresses available for dynamic allocation,
    those addresses are collected into a common pool for that shared network and assigned to clients as needed.
    There is no way to distinguish on which subnet of a shared network a client should boot.
    """

    name: str = Field(
        min_length=1,
        pattern=r"^\w*$",
        description="Name should be the `name` of the shared network."
        "This `name` is used when printing debugging messages, so it should be descriptive for the shared network."
        "The `name` may have the syntax of a valid domain name (although it will never be used as such), or it may be any arbitrary name, enclosed in quotes.",
    )
    description: str | None = Field(default=None, max_length=79)
    option: Option
    parameter: Parameter
