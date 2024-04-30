import strawberry

from app.mutations import Mutation as AppMutation
from app.queries import Query as AppQuery


@strawberry.type
class Query(AppQuery):
    """Root Query"""


@strawberry.type
class Mutation(AppMutation):
    """Root Mutation"""


# Root Schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
