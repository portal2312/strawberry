"""Tests pytest contest module in my_pydantic app.

References:
    https://docs.pytest.org/en/stable/reference/fixtures.html
    https://docs.pytest.org/en/stable/explanation/fixtures.html
"""

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

import pytest

from ..pydantic.models import Option, Parameter, Subnet6


@pytest.fixture
def ipv4_address_str() -> str:
    """IPv4 address string."""
    return "8.8.8.8"


@pytest.fixture
def ipv4_network_str() -> str:
    """IPv4 network string."""
    return "8.8.8.0/24"


@pytest.fixture
def ipv4_low_address_str() -> str:
    """IPv4 low address string."""
    return "8.8.8.1"


@pytest.fixture
def ipv4_high_address_str() -> str:
    """IPv4 high address string."""
    return "8.8.8.254"


@pytest.fixture
def ipv4_address(ipv4_address_str: str) -> IPv4Address:
    """IPv4 address."""
    return IPv4Address(ipv4_address_str)


@pytest.fixture
def ipv4_network(ipv4_network_str: str) -> IPv4Network:
    """IPv4 network."""
    return IPv4Network(ipv4_network_str)


@pytest.fixture
def ipv6_address_str() -> str:
    """IPv6 address string."""
    return "2001:4860:4860::8888"


@pytest.fixture
def ipv6_network_str() -> str:
    """IPv6 network string."""
    return "2001:4860:4860::/112"


@pytest.fixture
def ipv6_low_address_str() -> str:
    """IPv6 low address string."""
    return "2001:4860:4860::1"


@pytest.fixture
def ipv6_high_address_str() -> str:
    """IPv6 high address string."""
    return "2001:4860:4860::fffe"


@pytest.fixture
def ipv6_address(ipv6_address_str: str) -> IPv6Address:
    """IPv6 address string."""
    return IPv6Address(ipv6_address_str)


@pytest.fixture
def ipv6_network(ipv6_network_str: str) -> IPv6Network:
    """IPv6Network."""
    return IPv6Network(ipv6_network_str)


@pytest.fixture
def duid_list():
    """DUID list."""
    return ["000300011A2B3C4D5E6F7A8B", "00:03:00:01:1A:2B:3C:4D:5E:6F:7A:8B"]


@pytest.fixture
def iaid_list():
    """IAID list."""
    return [
        "1A:2B:3C:4D",
        "4294967295",
    ]


@pytest.fixture
def ip6_address_list(ipv6_address_str: str, ipv6_address: IPv6Address):
    """ip6_address list."""
    return [ipv6_address, ipv6_address_str]


@pytest.fixture
def dns_servers_list(
    ipv4_address_str: str,
    ipv4_address: IPv4Address,
    ipv6_address_str: str,
    ipv6_address: IPv6Address,
):
    """Option.dns_servers list."""
    return [
        [ipv4_address, ipv6_address],
        [ipv4_address_str, ipv6_address_str],
        [ipv4_address_str, ipv6_address_str, ipv4_address, ipv6_address],
        None,
    ]


@pytest.fixture
def domain_list_list():
    """Option.domain_list list."""
    return [
        ["https://www.google.com/", "google.com"],
        "https://www.google.com/, google.com,",
        "https://www.google.com/",
        None,
    ]


@pytest.fixture
def preferred_lifetime_list() -> list[int]:
    """Parameter.preferred_lifetime list."""
    return [1]


@pytest.fixture
def valid_lifetime_list() -> list[int]:
    """Parameter.valid_lifetime list."""
    return [1]


@pytest.fixture
def subnet6_number_list(ipv6_network_str):
    """Subnet6.subnet6_number list."""
    return [
        IPv6Network(ipv6_network_str),
        ipv6_network_str,
    ]


@pytest.fixture
def shared_network_name_list():
    """SharedNetwork.name list."""
    return [
        "string_type",
        "not_string_too_short",
        "not_string_pattern_mismatch",
    ]


@pytest.fixture
def shared_network_description_list():
    """SharedNetwork.description list."""
    return [
        "description",
        "",
        None,
        "a" * 79,
    ]


@pytest.fixture
def shared_network_option_list(
    dns_servers_list,
    domain_list_list,
) -> list[Option]:
    """SharedNetwork.option list."""
    return [
        Option(
            dns_servers=dns_servers_list[0],
            domain_list=domain_list_list[0],
        )
    ]


@pytest.fixture
def shared_network_parameter_list(
    preferred_lifetime_list,
    valid_lifetime_list,
) -> list[Parameter]:
    """SharedNetwork.parameter list."""
    return [
        Parameter(
            preferred_lifetime=preferred_lifetime_list[0],
            valid_lifetime=valid_lifetime_list[0],
        )
    ]


@pytest.fixture
def shared_network_subnets_list(ipv6_network) -> list[list[Subnet6] | None]:
    """SharedNetwork.subnets list."""
    return [
        [
            Subnet6(subnet6_number=ipv6_network),
        ],
        None,
    ]


@pytest.fixture
def iana_low_address(ipv6_low_address_str: str) -> IPv6Address:
    """IANA low_address."""
    return IPv6Address(ipv6_low_address_str)


@pytest.fixture
def iana_high_address(ipv6_high_address_str: str) -> IPv6Address:
    """IANA high address."""
    return IPv6Address(ipv6_high_address_str)


@pytest.fixture
def iana_klass_list() -> list[str]:
    """IANA klass."""
    return ["default"]
