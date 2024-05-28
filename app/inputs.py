"""App app input types.

References:
    https://strawberry-graphql.github.io/strawberry-django/guide/types/
"""

import strawberry_django
from strawberry import auto

from . import models


@strawberry_django.input(models.Color)
class ColorInput:
    """Color model input type."""

    id: auto
    name: auto
    description: auto
    fruits: list["FruitInput"]


@strawberry_django.input(models.Color, partial=True)
class ColorPartialInput:
    """Color model partial input type."""

    id: auto
    name: auto
    description: auto
    fruits: list["FruitPartialInput"]


@strawberry_django.input(models.Color, partial=True)
class ColorNameRequiredPartialInput:
    """Color model partial input type."""

    id: auto
    name: str  # Is required.
    description: auto
    fruits: list["FruitPartialInput"]


@strawberry_django.input(models.Fruit)
class FruitInput:
    """Fruit model input type."""

    id: auto
    name: auto
    color: "ColorInput"


@strawberry_django.input(models.Fruit, partial=True)
class FruitPartialInput(FruitInput):
    """Fruit model partial input type."""

    # Override.
    color: "ColorPartialInput"  # type: ignore[assignment]
