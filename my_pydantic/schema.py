"""Schema in my_pydantic app."""

import strawberry


@strawberry.type
class Query:
    """Root query in my_pydantic app."""

    my_pydantic: bool = strawberry.field(resolver=lambda: True)


@strawberry.type
class Mutation:
    """Root mutation in my_pydantic app."""

    is_my_pydantic: bool = strawberry.field(resolver=lambda: True)


schema = strawberry.Schema(query=Query, mutation=Mutation)
