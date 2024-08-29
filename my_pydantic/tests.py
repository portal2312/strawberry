"""Tests in the my_pydantic app."""

from django.test import TestCase
from pydantic import ValidationError

from .models import Parameter


class ParameterTestCase(TestCase):
    """Parameter TestCase."""

    def setUp(self):
        """Set up."""
        self.preferred_lifetime = 1
        self.preferred_lifetimes = (self.preferred_lifetime, None)
        self.invalid_preferred_lifetime = "a"
        self.invalid_preferred_lifetime__gt = 0
        self.valid_lifetime = 1
        self.valid_lifetimes = (self.valid_lifetime, None)
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
