"""App app types.

References:
    https://strawberry-graphql.github.io/strawberry-django/guide/types/
"""

import strawberry_django
from strawberry import auto

# from strawberry_django.auth.utils import get_current_user
from . import models


@strawberry_django.type(models.Fruit)
class Berry:
    """Fruit model type."""

    id: auto
    name: auto
    category: auto
    color: "Color"

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        """Override."""
        # TODO: Does not working.
        # user = get_current_user(info)
        # if not user.is_staff:
        #     queryset = queryset.filter(color__name="Red")
        return queryset.filter(category="berry")


@strawberry_django.type(models.Color)
class Color:
    """Color model type."""

    id: auto
    name: auto
    # XXX: MUST change strawberry.field to strawberry_django.field.
    description: auto | None = strawberry_django.field(
        metadata={"tags": ["internal"]},  # XXX: Exclude the filtered field.
    )
    fruits: list["Fruit"]


@strawberry_django.type(
    models.Fruit,
    description="Priority description than Fruit model description.",
)
class Fruit:
    """Fruit model type."""

    id: auto
    name: auto
    category: auto
    color: "Color"
