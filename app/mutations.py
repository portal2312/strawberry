from typing import Annotated

import strawberry
from strawberry.field_extensions import InputMutationExtension

from .inputs import AddFruitInput
from .types import Author, Book, Fruit


@strawberry.type
class FruitMutations:
    @strawberry.mutation
    def add(self, info, input: AddFruitInput) -> Fruit:
        return Fruit(**vars(input))

    @strawberry.mutation(extensions=[InputMutationExtension()])
    def update_fruit_weight(
        self,
        info: strawberry.Info,
        id: strawberry.ID,
        weight: Annotated[
            float,
            strawberry.argument(description="The fruit's new weight in grams"),
        ],
    ) -> Fruit:
        return Fruit(id=id, weight=weight)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        return Book(title=title, author=Author(name=author))

    @strawberry.mutation
    def add_author(self, name: str) -> Author:
        return Author(name=name)

    @strawberry.mutation
    def restart() -> None:
        print("Restarting the server")

    @strawberry.field
    def fruit(self) -> FruitMutations:
        return FruitMutations()
