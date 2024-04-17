import typing

import strawberry


def get_author_for_book(root) -> "Author":
    return Author(name="Michael Crichton")


def get_books_for_author(root):
    return [Book(title="Jurassic Park")]


def get_authors(root) -> typing.List["Author"]:
    return [Author(name="Michael Crichton")]


@strawberry.type
class Book:
    title: str
    author: "Author" = strawberry.field(resolver=get_author_for_book)


@strawberry.type
class Author:
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)
