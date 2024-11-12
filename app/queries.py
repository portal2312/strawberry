"""App app queries."""

import strawberry
import strawberry_django

from utils.strawberry_django.fields.field import CustomStrawberryDjangoField

from .types import (
    Berry,
    Color,
    Fruit,
    Fruit2,
    FruitAllFields,
    FruitEnumeratedFields,
    FruitExcludeFields,
    FruitOverrideExcludeFields,
    FruitOverrideFields,
    User,
    User2,
)


@strawberry.type
class Query:
    """App app root query class."""

    berries: list[Berry] = strawberry_django.field()
    color: Color = strawberry_django.field()
    colors: list[Color] = strawberry_django.field()
    fruit: Fruit = strawberry_django.field()
    fruit2: Fruit2 = strawberry_django.field()
    fruit_all_fields: FruitAllFields = strawberry_django.field()
    fruit_enumerated_fields: FruitEnumeratedFields = strawberry_django.field()
    fruit_override_fields: FruitOverrideFields = strawberry_django.field()
    fruit_exclude_fields: FruitExcludeFields = strawberry_django.field()
    fruit_override_exclude_fields: FruitOverrideExcludeFields = (
        strawberry_django.field()
    )
    fruits: list[Fruit] = strawberry_django.field()
    user: User = strawberry_django.field()
    users: list[User] = strawberry_django.field()
    # 일반 strawberry type 에 사용자 정의 필드 클래스를 직접 생성할 수 있습니다.
    user2: User2 = CustomStrawberryDjangoField()  # type: ignore

    @strawberry.field
    def hello(self, info: strawberry.Info) -> str:
        """Hello world."""
        print(info.context["request"].consumer.scope["user"])
        return "world"
