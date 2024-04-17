import typing

import strawberry

from library.types import (
    Author,
    Book,
    get_authors,
    get_books_for_author,
)


@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


schema = strawberry.Schema(
    query=Query,
    config=strawberry.schema.config.StrawberryConfig(auto_camel_case=True),
)
