import typing

import strawberry

from .types import Author, Book, get_authors, get_books_for_author

FRUITS = [
    "Strawberry",
    "Apple",
    "Orange",
]


@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)

    @strawberry.field
    def hello(self) -> str:
        return "hello"

    @strawberry.field
    def fruit(self, startswith: str) -> str | None:
        if startswith:
            for fruit in FRUITS:
                if fruit.lower().startswith(startswith.lower()):
                    return fruit

    @strawberry.field
    def fruits(
        self,
        is_tasty: typing.Annotated[
            bool | None,
            strawberry.argument(
                description="Filters out fruits by whenever they're tasty or not",
                deprecation_reason="isTasty argument is deprecated, "
                "use fruits(taste:SWEET) instead",
            ),
        ] = None,
    ) -> list[str]:
        return FRUITS
