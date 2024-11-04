"""Tests in the my_pydantic app."""

from ipaddress import IPv4Address, IPv6Address

from django.test import TestCase
from pydantic import ValidationError
from pydantic.fields import FieldInfo

from .pydantic.models import Option, Parameter, SharedNetwork


def has_attr_default(field: FieldInfo) -> bool:
    """Has attribute default at the field."""
    return hasattr(field._attributes_set, "default")


def is_default_none(field: FieldInfo) -> bool:
    """Is default value None at the field."""
    return field._attributes_set["default"] is None


class OptionTestCase(TestCase):
    def setUp(self):
        """Set up."""
        ip4_str, ip6_str = "8.8.8.8", "2001:4860:4860::8888"
        ip4, ip6 = IPv4Address(ip4_str), IPv6Address(ip6_str)
        self.dns_servers = [
            [ip4, ip6],
            [ip4_str, ip6_str],
            [ip4_str, ip6_str, ip4, ip6],
            None,
        ]
        self.domain_list = [
            ["https://www.google.com/", "google.com"],
            "https://www.google.com/, google.com,",
            "https://www.google.com/",
            None,
        ]

    def test_dns_servers(self):
        """Test dns servers field."""
        field = Option.model_fields["dns_servers"]
        is_field_default_none = has_attr_default(field) and is_default_none(field)
        for dns_servers in self.dns_servers:
            option = Option(
                dns_servers=dns_servers,
                domain_list=self.domain_list[0],
            )
            self.assertIsInstance(option, Option)
            if option.dns_servers:
                self.assertTrue(
                    all(
                        isinstance(v, (IPv4Address, IPv6Address))
                        for v in option.dns_servers
                    )
                )
            elif is_field_default_none:
                self.assertIsNone(option.dns_servers)

    def test_domain_list(self):
        """Test domain_list field."""
        field = Option.model_fields["domain_list"]
        is_field_default_none = has_attr_default(field) and is_default_none(field)
        for domain_list in self.domain_list:
            option = Option(
                dns_servers=self.dns_servers[0],
                domain_list=domain_list,
            )
            self.assertIsInstance(option, Option)
            if option.domain_list:
                self.assertTrue(all(isinstance(v, str) for v in option.domain_list))
            elif is_field_default_none:
                self.assertIsNone(option.domain_list)


class ParameterTestCase(TestCase):
    """Parameter TestCase."""

    def setUp(self):
        """Set up."""
        self.preferred_lifetimes = [1]
        self.valid_lifetimes = [1]

    def test_preferred_lifetime(self):
        """Test valid preferred_lifetime field."""
        for preferred_lifetime in self.preferred_lifetimes:
            parameter = Parameter(
                preferred_lifetime=preferred_lifetime,
                valid_lifetime=self.valid_lifetimes[0],
            )
            self.assertIsInstance(parameter, Parameter)
            self.assertEqual(parameter.preferred_lifetime, preferred_lifetime)

    def test_preferred_lifetime__gt(self):
        """Test preferred_lifetime field, greater than."""
        field_name = "preferred_lifetime"
        field = Parameter.model_fields[field_name]
        preferred_lifetime__gt = field._attributes_set["gt"]
        try:
            Parameter(
                preferred_lifetime=preferred_lifetime__gt,
                valid_lifetime=self.valid_lifetimes[0],
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", (field_name,):
                        self.assertGreaterEqual(error["input"], error["ctx"]["gt"])
                    case _:
                        raise e

    def test_valid_lifetime(self):
        """Test valid_lifetime field."""
        for valid_lifetime in self.valid_lifetimes:
            parameter = Parameter(
                preferred_lifetime=self.preferred_lifetimes[0],
                valid_lifetime=valid_lifetime,
            )
            self.assertIsInstance(parameter, Parameter)
            self.assertEqual(parameter.valid_lifetime, valid_lifetime)

    def test_valid_lifetime__gt(self):
        """Test valid_lifetime field, greater than."""
        field_name = "valid_lifetime"
        field = Parameter.model_fields[field_name]
        valid_lifetime__gt = field._attributes_set["gt"]
        try:
            Parameter(
                preferred_lifetime=self.preferred_lifetimes[0],
                valid_lifetime=valid_lifetime__gt,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", (field_name,):
                        self.assertGreaterEqual(error["input"], error["ctx"]["gt"])
                    case _:
                        raise e

    def test_check_preferred_lifetime__lte__valid_lifetime(self):
        """Test Parameter.check_preferred_lifetime__lte__valid_lifetime func."""
        valid_lifetime = self.valid_lifetimes[0]
        preferred_lifetime = valid_lifetime + 1
        try:
            parameter = Parameter(
                preferred_lifetime=preferred_lifetime,
                valid_lifetime=valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"]:
                    case "preferred_lifetime__lte__valid_lifetime__greater":
                        self.assertGreater(preferred_lifetime, valid_lifetime)
                    case "preferred_lifetime__lte__valid_lifetime__is_none":
                        self.assertIsNone(valid_lifetime)
                    case _:
                        raise e
        else:
            self.assertIsInstance(parameter, Parameter)
            self.assertEqual(parameter.preferred_lifetime, preferred_lifetime)
            self.assertEqual(parameter.valid_lifetime, valid_lifetime)


class SharedNetworkTestCase(TestCase):
    """SharedNetwork TestCase."""

    def setUp(self):
        """Set up."""
        self.names = [
            "string_type",
            "not_string_too_short",
            "not_string_pattern_mismatch",
        ]
        self.descriptions = [
            "description",
            "",
            None,
            "a" * 79,
        ]
        self.options = [
            Option(
                dns_servers=["8.8.8.8", "2001:4860:4860::8888"],
                domain_list=["google.com"],
            )
        ]
        self.parameters = [
            Parameter(preferred_lifetime=1, valid_lifetime=1),
        ]

    def test_name(self):
        """Test name field."""
        field = SharedNetwork.model_fields["name"]
        for name in self.names:
            self.assertIsInstance(name, field._attributes_set["annotation"])
            self.assertGreater(len(name), field._attributes_set["min_length"])
            self.assertRegex(name, field._attributes_set["pattern"])
            shared_network = SharedNetwork(
                name=name,
                description=self.descriptions[0],
                option=self.options[0],
                parameter=self.parameters[0],
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertEqual(shared_network.name, name)

    def test_description(self):
        """Test description field."""
        for description in self.descriptions:
            shared_network = SharedNetwork(
                name=self.names[0],
                description=description,
                option=self.options[0],
                parameter=self.parameters[0],
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertEqual(shared_network.description, description)

    def test_option(self):
        """Test parameter field."""
        for option in self.options:
            shared_network = SharedNetwork(
                name=self.names[0],
                description=self.descriptions[0],
                option=option,
                parameter=self.parameters[0],
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertIsInstance(shared_network.option, Option)

    def test_parameter(self):
        """Test parameter field."""
        for parameter in self.parameters:
            shared_network = SharedNetwork(
                name=self.names[0],
                description=self.descriptions[0],
                option=self.options[0],
                parameter=parameter,
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertIsInstance(shared_network.parameter, Parameter)
