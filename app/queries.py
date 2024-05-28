"""App app queries."""

import strawberry
import strawberry_django

from .types import Berry, Color, Fruit, User


@strawberry.type
class Query:
    """App app root query class."""

    berries: list[Berry] = strawberry_django.field()
    color: Color = strawberry_django.field()
    colors: list[Color] = strawberry_django.field()
    fruit: Fruit = strawberry_django.field()
    fruits: list[Fruit] = strawberry_django.field()
    user: User = strawberry_django.field()
    users: list[User] = strawberry_django.field()

    @strawberry.field
    def hello(self, info: strawberry.Info) -> str:
        """Hello world."""
        return "world"
