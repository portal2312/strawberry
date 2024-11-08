"""Tests pydantic.types in the my_pydantic app.

References:
    https://docs.pytest.org/en/stable/how-to/index.html
"""

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from pydantic import TypeAdapter

from ..pydantic.types import DUID, IAID, IPAddress, IPNetwork


def test_ip_address_type(
    ipv4_address_str,
    ipv4_address,
    ipv6_address_str,
    ipv6_address,
):
    """Test IPAddress type."""
    ta: TypeAdapter[IPAddress] = TypeAdapter(IPAddress)
    assert isinstance(ta.validate_python(ipv4_address_str), IPv4Address)
    assert isinstance(ta.validate_python(ipv4_address), IPv4Address)
    assert ta.dump_python(ipv4_address_str) == ipv4_address_str
    assert isinstance(ta.validate_python(ipv6_address_str), IPv6Address)
    assert isinstance(ta.validate_python(ipv6_address), IPv6Address)
    assert ta.dump_python(ipv6_address_str) == ipv6_address_str


def test_ip_network_type(
    ipv4_network_str,
    ipv4_network,
    ipv6_network_str,
    ipv6_network,
):
    """Test IPNetwork type."""
    ta: TypeAdapter[IPNetwork] = TypeAdapter(IPNetwork)
    assert isinstance(ta.validate_python(ipv4_network_str), IPv4Network)
    assert isinstance(ta.validate_python(ipv4_network), IPv4Network)
    assert ta.dump_python(ipv4_network_str) == ipv4_network_str
    assert isinstance(ta.validate_python(ipv6_network_str), IPv6Network)
    assert isinstance(ta.validate_python(ipv6_network), IPv6Network)
    assert ta.dump_python(ipv6_network_str) == ipv6_network_str


def test_duid_type(duid_list):
    """Test DUID type."""
    ta: TypeAdapter[DUID] = TypeAdapter(DUID)
    for duid in duid_list:
        assert ta.validate_python(duid) == duid


def test_iaid_type(iaid_list):
    """Test DUID type."""
    ta: TypeAdapter[IAID] = TypeAdapter(IAID)
    for iaid in iaid_list:
        assert ta.validate_python(iaid) == iaid
