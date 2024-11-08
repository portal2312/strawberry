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
        assert fieldname in response.data
        assert response.data[fieldname]

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
        assert "sharedNetwork" in response.data


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
        input = {
            "name": "MySharedNetwork",
            "description": "This is my shared network.",
            "option": {
                "dnsServers": ["8.8.8.8", "2001:4860:4860::8888"],
                "domainList": ["google.com"],
            },
            "parameter": {"preferredLifetime": 2, "validLifetime": 2},
            "subnets": [{"subnet6Number": "2001:4860:4860::/64"}],
        }
        resp = schema.execute_sync(
            query,
            variable_values={"input": input},
        )
        assert resp.errors is None
        root = to_camel_case("save_shared_network")
        assert root in resp.data
        assert resp.data[root]["name"] == input["name"]
        assert resp.data[root]["description"] == input["description"]
        assert resp.data[root]["option"] == input["option"]
        assert resp.data[root]["parameter"] == input["parameter"]
        assert resp.data[root]["subnets"] == input["subnets"]
