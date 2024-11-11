"""App app types.

References:
    https://strawberry-graphql.github.io/strawberry-django/guide/types/
    https://strawberry-graphql.github.io/strawberry-django/guide/fields/#defining-types-for-auto-fields
    https://strawberry.rocks/docs/guides/accessing-parent-data
"""

# from datetime import datetime
import strawberry
import strawberry_django
from django.contrib.auth import get_user_model
from django.db.models import DateTimeField, SlugField
from strawberry import auto
from strawberry_django.fields.types import field_type_map

from utils.strawberry_django.fields.field import CustomStrawberryDjangoField

from . import models
from .scalars import SlugScalar, UnixTimeStampScalar

field_type_map.update(
    {
        SlugField: SlugScalar,
        DateTimeField: UnixTimeStampScalar,
    }
)


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
    another_name: auto = strawberry_django.field(field_name="name")
    internal_name: auto = strawberry_django.field(
        name="onlyPkByFruit",
        field_name="fruits",
        # filters=FruitFilter,
        # order=FruitOrder,
        # pagination=True,
        description="A list of fruits with this color",
    )


@strawberry_django.type(
    models.Fruit,
    description="Priority description than Fruit model description.",
)
class Fruit:
    """Fruit model type."""

    id: auto
    name: auto
    category: auto
    wiki_urls: auto
    created_at: auto
    updated_at: auto
    color: "Color"


@strawberry_django.type(models.Fruit)
class Fruit2:
    """Fruit id and name type static."""

    id: strawberry.ID
    name: str


@strawberry_django.type(models.Fruit, fields="__all__")
class FruitAllFields:
    """Fruit All Fields.

    {
        "data": {
            "fruitAllFields": {
                "id": "1",
                "name": "Apple",
                "category": "CITRUS",
                "wikiUrls": "https://en.wikipedia.org/wiki/Apple",
                "createdAt": 1717051424,
                "updatedAt": 1717051585,
                "color": {
                    "pk": "1",
                    "__typename": "DjangoModelType"
                },
                "__typename": "FruitAllFields"
            }
        }
    }
    """


@strawberry_django.type(models.Fruit, fields=["name", "color"])
class FruitEnumeratedFields:
    """Fruit Enumerated Fields.

    {
        "data": {
            "fruitEnumeratedFields": {
                "name": "Apple",
                "color": {
                    "pk": "1",
                    "__typename": "DjangoModelType"
                },
                "__typename": "FruitEnumeratedFields"
            },
        }
    }
    """


@strawberry_django.type(models.Fruit, fields=["color"])
class FruitOverrideFields:
    """Fruit Override Fields."""

    name: str


@strawberry_django.type(models.Fruit, exclude=["name"])
class FruitExcludeFields:
    """Fruit Exclude Fields."""


@strawberry_django.type(
    models.Fruit,
    exclude=[
        "id",
        "name",
        "category",
        "wiki_urls",
        "created_at",
        "updated_at",
        "color",
    ],
)
class FruitOverrideExcludeFields:
    """Fruit Override Exclude Fields."""

    # NOTE: `name` is Will not defined.
    name = auto
    # NOTE: color_id <- color, Exception: "Int cannot represent non-integer value: <Color instance>".
    color_id: int


@strawberry_django.type(get_user_model())
class User:
    """User model type."""

    id: auto
    username: auto
    email: auto
    password: auto
    first_name: str
    last_name: str

    @strawberry.field
    def full_name(self) -> str:
        """Get the full name."""
        return f"{self.first_name} {self.last_name}"


@strawberry_django.type(get_user_model(), field_cls=CustomStrawberryDjangoField)
class User2:
    """User2 model type."""

    id: auto
    username: auto
