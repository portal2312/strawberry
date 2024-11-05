"""Queries in the my_pydantic app."""

from ipaddress import IPv4Address, IPv6Address, IPv6Network

from strawberry.types import Info

from .pydantic.models import Parameter
from .types import Option, SharedNetwork, Subnet6


def get_shared_network(info: Info) -> SharedNetwork:
    """Resolves a shared network."""
    instance = SharedNetwork(
        name="MySharedNetwork",
        description="This is my shared network.",
        option=Option(
            dns_servers=[
                IPv4Address("8.8.8.8"),
                IPv6Address("2001:4860:4860::8888"),
            ],
            domain_list=["google.com"],
        ),
        parameter=Parameter(
            preferred_lifetime=1,
            valid_lifetime=1,
        ),
        subnets=[
            Subnet6(subnet6_number=IPv6Network("2001:4860:4860::/64")),
        ],
    )
    return instance
