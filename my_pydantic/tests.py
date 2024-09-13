"""Tests in the my_pydantic app."""

from django.test import TestCase
from pydantic import ValidationError

from .models import Parameter, SharedNetwork


class ParameterTestCase(TestCase):
    """Parameter TestCase."""

    def setUp(self):
        """Set up."""
        self.preferred_lifetime = 1
        self.preferred_lifetimes = (self.preferred_lifetime,)
        self.invalid_preferred_lifetime = "a"
        self.invalid_preferred_lifetime__gt = 0
        self.valid_lifetime = 1
        self.valid_lifetimes = (self.valid_lifetime,)
        self.invalid_valid_lifetime = "a"
        self.invalid_valid_lifetime__gt = 0
        self.invalid_check_preferred_lifetime__lte__valid_lifetime = (
            self.valid_lifetime + 1
        )

    def test_preferred_lifetime(self):
        """Test valid preferred_lifetime value."""
        for value in self.preferred_lifetimes:
            parameter = Parameter(
                preferred_lifetime=value,
                valid_lifetime=self.valid_lifetime,
            )
            self.assertEqual(parameter.preferred_lifetime, value)

    def test_invalid_preferred_lifetime(self):
        """Test invalid preferred_lifetime."""
        try:
            Parameter(
                preferred_lifetime=self.invalid_preferred_lifetime,
                valid_lifetime=self.valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "int_parsing", ("preferred_lifetime",):
                        self.assertNotIsInstance(error["input"], int)
                    case _:
                        raise e

    def test_invalid_preferred_lifetime__gt(self):
        """Test invalid preferred_lifetime greater than."""
        try:
            Parameter(
                preferred_lifetime=self.invalid_preferred_lifetime__gt,
                valid_lifetime=self.valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", ("preferred_lifetime",):
                        self.assertGreaterEqual(error["input"], error["ctx"]["gt"])
                    case _:
                        raise e

    def test_valid_lifetime(self):
        """Test valid valid_lifetime."""
        for value in self.valid_lifetimes:
            try:
                parameter = Parameter(
                    preferred_lifetime=self.preferred_lifetime,
                    valid_lifetime=value,
                )
            except ValidationError as e:
                for error in e.errors():
                    match error["type"]:
                        case "preferred_lifetime__lte__valid_lifetime__is_none":
                            self.assertIsNone(value)
                        case _:
                            raise e
            else:
                self.assertEqual(parameter.valid_lifetime, value)

    def test_invalid_valid_lifetime(self):
        """Test invalid valid_lifetime."""
        try:
            Parameter(
                preferred_lifetime=self.preferred_lifetime,
                valid_lifetime=self.invalid_valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "int_parsing", ("valid_lifetime",):
                        self.assertNotIsInstance(error["input"], int)
                    case _:
                        raise e

    def test_invalid_valid_lifetime__gt(self):
        """Test invalid valid_lifetime greater than."""
        try:
            Parameter(
                preferred_lifetime=self.preferred_lifetime,
                valid_lifetime=self.invalid_valid_lifetime__gt,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"], error["loc"]:
                    case "greater_than", ("valid_lifetime",):
                        self.assertGreaterEqual(error["input"], error["ctx"]["gt"])
                    case _:
                        raise e

    def test_check_preferred_lifetime__lte__valid_lifetime(self):
        """Test Parameter.check_preferred_lifetime__lte__valid_lifetime func."""
        try:
            parameter = Parameter(
                preferred_lifetime=self.invalid_check_preferred_lifetime__lte__valid_lifetime,
                valid_lifetime=self.valid_lifetime,
            )
        except ValidationError as e:
            for error in e.errors():
                match error["type"]:
                    case "preferred_lifetime__lte__valid_lifetime__greater":
                        self.assertGreater(
                            self.invalid_check_preferred_lifetime__lte__valid_lifetime,
                            self.valid_lifetime,
                        )
                    case "preferred_lifetime__lte__valid_lifetime__is_none":
                        self.assertIsNone(self.valid_lifetime)
                    case _:
                        raise e
        else:
            self.assertIsInstance(parameter, Parameter)


class SharedNetworkTestCase(TestCase):
    """SharedNetwork TestCase."""

    def setUp(self):
        """Set up."""
        self.name = "My_SharedNetwork_01"
        self.names = (self.name,)
        self.invalid_names = ("", 1, True, None, "My SharedNetwork 01")
        self.description = "description"
        self.descriptions = (self.description, "", None)
        self.invalid_descriptions = (1, True, "a" * 80)
        self.parameter = Parameter(preferred_lifetime=1, valid_lifetime=1)

    def test_name(self):
        """Test name field set value."""
        for name in self.names:
            shared_network = SharedNetwork(
                name=name,
                description=self.description,
                parameter=self.parameter,
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertIsInstance(shared_network.parameter, Parameter)

    def test_invalid_name(self):
        """Test name field set invalid value."""
        for name in self.invalid_names:
            try:
                SharedNetwork(
                    name=name,
                    description=self.description,
                    parameter=self.parameter,
                )
            except ValidationError as e:
                for error in e.errors():
                    match error["type"], error["loc"]:
                        case "string_type", ("name",):
                            self.assertNotIsInstance(
                                error["input"],
                                str,
                            )
                        case "string_too_short", ("name",):
                            self.assertLess(
                                len(error["input"]),
                                error["ctx"]["min_length"],
                            )
                        case "string_pattern_mismatch", ("name",):
                            self.assertNotRegex(
                                error["input"],
                                error["ctx"]["pattern"],
                            )
                        case _:
                            raise e

    def test_description(self):
        """Test description field set value."""
        for description in self.descriptions:
            shared_network = SharedNetwork(
                name=self.name,
                description=description,
                parameter=self.parameter,
            )
            self.assertIsInstance(shared_network, SharedNetwork)
            self.assertIsInstance(shared_network.parameter, Parameter)

    def test_invalid_description(self):
        """Test description field set invalid value."""
        for description in self.invalid_descriptions:
            try:
                SharedNetwork(
                    name=self.name,
                    description=description,
                    parameter=self.parameter,
                )
            except ValidationError as e:
                for error in e.errors():
                    match error["type"], error["loc"]:
                        case "string_type", ("description",):
                            self.assertNotIsInstance(
                                error["input"],
                                str,
                            )
                        case "string_too_long", ("description",):
                            self.assertGreater(
                                len(error["input"]),
                                error["ctx"]["max_length"],
                            )
                        case _:
                            raise e

    def test_parameter(self):
        """Test parameter field set value."""
        shared_network = SharedNetwork(
            name=self.name,
            description=self.description,
            parameter=Parameter(
                preferred_lifetime=1,
                valid_lifetime=1,
            ),
        )
        self.assertIsInstance(shared_network, SharedNetwork)
        self.assertIsInstance(shared_network.parameter, Parameter)
