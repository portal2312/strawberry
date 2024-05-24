"""App app types."""

import strawberry_django
from strawberry import auto

from . import models


@strawberry_django.type(models.Fruit)
class Fruit:
    """Fruit model type."""

    id: auto
    name: auto
    color: "Color"


@strawberry_django.type(models.Color)
class Color:
    """Color model type."""

    id: auto
    name: auto
    # XXX: MUST change strawberry.field to strawberry_django.field.
    description: auto | None = strawberry_django.field(
        metadata={"tags": ["internal"]},  # XXX: Exclude the filtered field.
    )
    fruits: list[Fruit]
