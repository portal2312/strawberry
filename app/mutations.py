"""App app mutations.

References:
    https://strawberry.rocks/docs/guides/authentication
"""

import strawberry

from .types import LoginError, LoginResult, LoginSuccess, User

# @strawberry.type
# class FruitMutations:
# @strawberry.mutation
# def add(self, info, input: AddFruitInput) -> Fruit:
#     return Fruit(**vars(input))

# @strawberry.mutation(extensions=[InputMutationExtension()])
# def update_fruit_weight(
#     self,
#     info: strawberry.Info,
#     id: strawberry.ID,
#     weight: Annotated[
#         float,
#         strawberry.argument(description="The fruit's new weight in grams"),
#     ],
# ) -> Fruit:
#     return Fruit(id=id, weight=weight)


@strawberry.type
class Mutation:
    """App app root mutation class."""

    @strawberry.field
    def strawberry_login(self, username: str, password: str) -> LoginResult:
        """Login."""
        if username != password:
            return LoginError(message="Something went wrong")
        return LoginSuccess(
            user=User(
                id="1",
                username=username,
                email=f"{username}@gmail.com",
                password=password,
            )
        )
