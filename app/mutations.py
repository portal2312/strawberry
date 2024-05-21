"""App app mutations."""

# import strawberry

# from .types import Color

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


# @strawberry.type
# class Mutation:
#     """App app root mutation class."""

#     def save_color(self, name: str) -> Color:
#         """Create 색상."""
#         return Color(name=name)

# @strawberry.field
# def fruit(self) -> FruitMutations:
#     return FruitMutations()
