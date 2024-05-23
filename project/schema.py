"""Project Root Schema.

References:
    https://strawberry.rocks/docs/types/schema#filteringcustomising-fields
"""

import strawberry
from strawberry.types.types import StrawberryObjectDefinition
from strawberry_django.optimizer import DjangoOptimizerExtension

from app.queries import Query as AppQuery
from app.subscriptions import Subscription as AppSubscription


@strawberry.type
class Query(AppQuery):
    """Root query class."""


@strawberry.type
class Subscription(AppSubscription):
    """Root subscription class."""


def public_field_filter(field) -> bool:
    """Public field filter.

    Example:
        Refer to ``types.py``::

            from strawberry import auto
            from strawberry_django import field, type

            @type(models.Color)
            class Color:
                id: auto
                name: auto
                description: auto | None = field(metadata={"tags": ["internal"]})  # Exclude the filtered field.

        Execute `python manage.py export_schema project.schema` CLI::

            type Color {
                id: ID!
                name: String!
            }
            ...
    """
    return "internal" not in field.metadata.get("tags", [])


class PublicSchema(strawberry.Schema):
    """Override Schema class."""

    def get_fields(self, type_definition: StrawberryObjectDefinition) -> list:
        """Override get_fields function."""
        return list(filter(public_field_filter, type_definition.fields))


# Root Schema
schema = PublicSchema(
    query=Query,
    subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,  # not required, but highly recommended
    ],
)
