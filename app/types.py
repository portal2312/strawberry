"""App app types."""

from strawberry import auto
from strawberry_django import field, type

from . import models


@type(models.Fruit)
class Fruit:
    """Fruit model type."""

    id: auto
    name: auto
    color: "Color"


@type(models.Color)
class Color:
    """Color model type."""

    id: auto
    name: auto
    # XXX: MUST change strawberry.field to strawberry_django.field.
    description: auto | None = field(
        metadata={"tags": ["internal"]},  # XXX: Exclude the filtered field.
    )
