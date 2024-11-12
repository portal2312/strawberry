"""Tests pydantic.models in the my_pydantic app.

References:
    https://docs.pytest.org/en/stable/how-to/index.html
    https://pytest-dependency.readthedocs.io/en/stable/usage.html#using-test-classes
"""

import re

from ipaddress import IPv4Address, IPv6Address, IPv6Network
from typing import TYPE_CHECKING

from pydantic import ValidationError

from ..pydantic.models import IANA, Bind, Option, Parameter, SharedNetwork, Subnet6

if TYPE_CHECKING:
    from pydantic import BaseModel
    from pydantic.fields import FieldInfo


def get_model_field_attr(model: type["BaseModel"], field_name: str, attr_name: str):
    """Get field attribute."""
    field = model.model_fields[field_name]
    return field._attributes_set.get(attr_name)


def is_field_default_none(field: "FieldInfo") -> bool:
    """Is field default attribute value None."""
    return (
        "default" in field._attributes_set and field._attributes_set["default"] is None
    )


class TestOption:
    """Test pydantic models Option."""

    def test_dns_servers(self, dns_servers_list, domain_list_list):
        """Test dns_servers field."""
        is_dns_servers_field_default_none = is_field_default_none(
            Option.model_fields["dns_servers"]
        )
        for dns_servers in dns_servers_list:
            if dns_servers is None:
                assert is_dns_servers_field_default_none is True
            option = Option(
                dns_servers=dns_servers,
                domain_list=domain_list_list[0],
            )
            assert isinstance(option, Option)
            if option.dns_servers is not None:
                assert all(
                    isinstance(v, (IPv4Address, IPv6Address))
                    for v in option.dns_servers
                )

    def test_domain_list(self, dns_servers_list, domain_list_list):
        """Test domain_list field."""
        is_domain_list_field_default_none = is_field_default_none(
            Option.model_fields["domain_list"]
        )
        for domain_list in domain_list_list:
            if domain_list is None:
                assert is_domain_list_field_default_none is True
            option = Option(
                dns_servers=dns_servers_list[0],
                domain_list=domain_list,
            )
            assert isinstance(option, Option)
            if option.domain_list is not None:
                assert all(isinstance(v, str) for v in option.domain_list) is True


class TestParameter:
    """Test pydantic models Parameter."""

    def test_preferred_lifetime(
        self,
        preferred_lifetime_list: list[int],
        valid_lifetime_list: list[int],
    ):
        """Test preferred_lifetime field."""
        for preferred_lifetime in preferred_lifetime_list:
            parameter = Parameter(
                preferred_lifetime=preferred_lifetime,
                valid_lifetime=valid_lifetime_list[0],
            )
            assert isinstance(parameter, Parameter)
            assert parameter.preferred_lifetime == preferred_lifetime

    def test_preferred_lifetime__gt(self, valid_lifetime_list):
        """Test preferred_lifetime field, greater than."""
        preferred_lifetime__gt: int = get_model_field_attr(
            Parameter, "preferred_lifetime", "gt"
        )
        try:
            Parameter(
                preferred_lifetime=preferred_lifetime__gt,
                valid_lifetime=valid_lifetime_list[0],
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", ("preferred_lifetime",):
                        assert error["input"] <= error["ctx"]["gt"]
                    case _:
                        raise e

    def test_valid_lifetime(self, preferred_lifetime_list, valid_lifetime_list):
        """Test valid_lifetime field."""
        for valid_lifetime in valid_lifetime_list:
            parameter = Parameter(
                preferred_lifetime=preferred_lifetime_list[0],
                valid_lifetime=valid_lifetime,
            )
            assert isinstance(parameter, Parameter)
            assert parameter.valid_lifetime == valid_lifetime

    def test_valid_lifetime__gt(self, preferred_lifetime_list):
        """Test valid_lifetime field, greater than."""
        valid_lifetime__gt: int = get_model_field_attr(
            Parameter, "valid_lifetime", "gt"
        )
        try:
            Parameter(
                preferred_lifetime=preferred_lifetime_list[0],
                valid_lifetime=valid_lifetime__gt,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", ("valid_lifetime",):
                        assert error["input"] <= error["ctx"]["gt"]
                    case _:
                        raise e

    def test_check_preferred_lifetime__lte__valid_lifetime(self, valid_lifetime_list):
        """Test Parameter.check_preferred_lifetime__lte__valid_lifetime func."""
        valid_lifetime = valid_lifetime_list[0]
        preferred_lifetime = valid_lifetime + 1
        try:
            parameter = Parameter(
                preferred_lifetime=preferred_lifetime,
                valid_lifetime=valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"]:
                    case "preferred_lifetime__lte__valid_lifetime__is_greater":
                        assert preferred_lifetime > valid_lifetime
                    case "preferred_lifetime__lte__valid_lifetime__is_none":
                        assert valid_lifetime is None
                    case _:
                        raise e
        else:
            assert isinstance(parameter, Parameter)
            assert parameter.preferred_lifetime == preferred_lifetime
            assert parameter.valid_lifetime == valid_lifetime


class TestBind:
    """Test Bind."""

    def test_duid(self, duid_list, iaid_list, ip6_address_list):
        """Test duid field."""
        for duid in duid_list:
            bind = Bind(
                duid=duid,
                iaid=iaid_list[0],
                ip6_address=ip6_address_list[0],
            )
            assert isinstance(bind, Bind)

    def test_iaid(self, duid_list, iaid_list, ip6_address_list):
        """Test iaid field."""
        for iaid in iaid_list:
            bind = Bind(
                duid=duid_list[0],
                iaid=iaid,
                ip6_address=ip6_address_list[0],
            )
            assert isinstance(bind, Bind)

    def test_ip6_address(self, duid_list, iaid_list, ip6_address_list):
        """Test ip6_address field."""
        for ip6_address in ip6_address_list:
            bind = Bind(
                duid=duid_list[0],
                iaid=iaid_list[0],
                ip6_address=ip6_address,
            )
            assert isinstance(bind, Bind)


class TestIANA:
    """Test IANA."""

    def test_low_address(
        self,
        iana_low_address: IPv6Address,
        iana_high_address: IPv6Address,
        iana_klass_list: list[str],
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        duid_list,
        iaid_list,
    ):
        """Test low_address field."""
        iana = IANA(
            low_address=iana_low_address,
            high_address=iana_high_address,
            klass=iana_klass_list[0],
            option=shared_network_option_list[0],
            parameter=shared_network_parameter_list[0],
            binds=[
                Bind(
                    duid=duid_list[0],
                    iaid=iaid_list[0],
                    ip6_address=IPv6Address("::2"),
                ),
            ],
        )
        assert isinstance(iana, IANA)


class TestSubnet6:
    """Test Subnet6."""

    def test_subnet6_number(self, subnet6_number_list):
        """Test subnet6_number field."""
        for subnet6_number in subnet6_number_list:
            subnet6 = Subnet6(subnet6_number=subnet6_number)
            assert isinstance(subnet6, Subnet6)
            assert isinstance(subnet6.subnet6_number, IPv6Network)


class TestSharedNetwork:
    """Test SharedNetwork."""

    def test_name(
        self,
        shared_network_name_list,
        shared_network_description_list,
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        shared_network_subnets_list: list[list[Subnet6] | None],
    ):
        """Test name field."""
        name_min_length = get_model_field_attr(SharedNetwork, "name", "min_length")
        if name_pattern := get_model_field_attr(SharedNetwork, "name", "pattern"):
            name_pattern = re.compile(name_pattern)
        for name in shared_network_name_list:
            if name_min_length is not None:
                assert len(name) >= name_min_length
            if name_pattern is not None:
                assert name_pattern.search(name)
            shared_network = SharedNetwork(
                name=name,
                description=shared_network_description_list[0],
                option=shared_network_option_list[0],
                parameter=shared_network_parameter_list[0],
                subnets=shared_network_subnets_list[0],
            )
            assert isinstance(shared_network, SharedNetwork)
            assert shared_network.name, name

    def test_description(
        self,
        shared_network_name_list,
        shared_network_description_list,
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        shared_network_subnets_list: list[list[Subnet6] | None],
    ):
        """Test description field."""
        for description in shared_network_description_list:
            shared_network = SharedNetwork(
                name=shared_network_name_list[0],
                description=description,
                option=shared_network_option_list[0],
                parameter=shared_network_parameter_list[0],
                subnets=shared_network_subnets_list[0],
            )
            assert isinstance(shared_network, SharedNetwork)
            assert shared_network.description == description

    def test_option(
        self,
        shared_network_name_list,
        shared_network_description_list,
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        shared_network_subnets_list: list[list[Subnet6] | None],
    ):
        """Test option field."""
        for option in shared_network_option_list:
            shared_network = SharedNetwork(
                name=shared_network_name_list[0],
                description=shared_network_description_list[0],
                option=option,
                parameter=shared_network_parameter_list[0],
                subnets=shared_network_subnets_list[0],
            )
            assert isinstance(shared_network, SharedNetwork)
            assert isinstance(shared_network.option, Option)

    def test_parameter(
        self,
        shared_network_name_list,
        shared_network_description_list,
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        shared_network_subnets_list: list[list[Subnet6] | None],
    ):
        """Test parameter field."""
        for parameter in shared_network_parameter_list:
            shared_network = SharedNetwork(
                name=shared_network_name_list[0],
                description=shared_network_description_list[0],
                option=shared_network_option_list[0],
                parameter=parameter,
                subnets=shared_network_subnets_list[0],
            )
            assert isinstance(shared_network, SharedNetwork)
            assert isinstance(shared_network.parameter, Parameter)

    def test_subnets(
        self,
        shared_network_name_list,
        shared_network_description_list,
        shared_network_option_list: list[Option],
        shared_network_parameter_list: list[Parameter],
        shared_network_subnets_list: list[list[Subnet6] | None],
    ):
        """Test subnets field."""
        is_subnets_field_default_none = is_field_default_none(
            SharedNetwork.model_fields["subnets"]
        )
        for subnets in shared_network_subnets_list:
            if subnets is None:
                assert is_subnets_field_default_none is True
            shared_network = SharedNetwork(
                name=shared_network_name_list[0],
                description=shared_network_description_list[0],
                option=shared_network_option_list[0],
                parameter=shared_network_parameter_list[0],
                subnets=subnets,
            )
            assert isinstance(shared_network, SharedNetwork)
            if shared_network.subnets is not None:
                assert all(
                    isinstance(subnet, Subnet6) for subnet in shared_network.subnets
                )
