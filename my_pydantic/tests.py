"""Tests in the my_pydantic app."""

from django.test import TestCase
from pydantic import ValidationError

from .models import Parameter, SharedNetwork


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
        self.descriptions = ["description", "", None, "a" * 79]
        self.parameters = [Parameter(preferred_lifetime=1, valid_lifetime=1)]

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
                parameter=self.parameters[0],
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertEqual(shared_network.description, description)

    def test_parameter(self):
        """Test parameter field."""
        for parameter in self.parameters:
            shared_network = SharedNetwork(
                name=self.names[0],
                description=self.descriptions[0],
                parameter=parameter,
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertIsInstance(shared_network.parameter, Parameter)
