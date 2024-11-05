"""Tests in the my_pydantic app."""

from django.test import TestCase
from strawberry.utils.str_converters import capitalize_first, to_camel_case

from project.schema import schema  # noqa: E402


class QueryTestCase(TestCase):
    """Tests fields at the schema query in the my_pydantic app."""

    def test_my_pydantic(self):
        """Test my_pydantic field."""
        fieldname = to_camel_case("my_pydantic")
        operation_name = capitalize_first(fieldname)
        query = f"""query {operation_name} {{
          {fieldname}
        }}"""
        response = schema.execute_sync(query)
        self.assertIn(fieldname, response.data)
        self.assertTrue(response.data[fieldname])

    def test_shared_network(self):
        """Test shared_network field."""
        query = """query SharedNetwork {
          sharedNetwork {
            name
            description
            option {
              dnsServers
              domainList
            }
            parameter {
              preferredLifetime
              validLifetime
            }
            subnets {
              subnet6Number
            }
          }
        }"""
        response = schema.execute_sync(query)
        self.assertIn("sharedNetwork", response.data)


class MutationTestCase(TestCase):
    """Tests fields at the schema mutation in the my_pydantic app."""

    def test_save_shared_network(self):
        """Test save_shared_network field."""
        query = """mutation SaveSharedNetwork($input: SharedNetworkInput!) {
          saveSharedNetwork(input: $input) {
            name
            description
            option {
              dnsServers
              domainList
            }
            parameter {
              preferredLifetime
              validLifetime
            }
            subnets {
              subnet6Number
            }
          }
        }"""
        variables = {
            "input": {
                "name": "MySharedNetwork",
                "description": "This is my shared network.",
                "option": {
                    "dnsServers": ["8.8.8.8", "2001:4860:4860::8888"],
                    "domainList": ["google.com"],
                },
                "parameter": {"preferredLifetime": 2, "validLifetime": 2},
                "subnets": [{"subnet6Number": "2001:4860:4860::/64"}],
            }
        }
        response = schema.execute_sync(query, variable_values=variables)
        output_fieldname = to_camel_case("save_shared_network")
        self.assertIn(output_fieldname, response.data)
        self.assertEqual(
            response.data[output_fieldname]["name"],
            variables["input"]["name"],
        )
        self.assertEqual(
            response.data[output_fieldname]["description"],
            variables["input"]["description"],
        )
        self.assertEqual(
            response.data[output_fieldname]["option"],
            variables["input"]["option"],
        )
        self.assertEqual(
            response.data[output_fieldname]["parameter"],
            variables["input"]["parameter"],
        )
        self.assertEqual(
            response.data[output_fieldname]["subnets"],
            variables["input"]["subnets"],
        )
