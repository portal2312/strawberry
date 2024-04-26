import strawberry


@strawberry.input
class AddFruitInput:
    id: strawberry.ID
    weight: float
