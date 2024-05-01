import strawberry

from app.mutations import Mutation as AppMutation
from app.queries import Query as AppQuery
from app.subscriptions import Subscription as AppSubscription


@strawberry.type
class Query(AppQuery):
    """Root Query"""


@strawberry.type
class Mutation(AppMutation):
    """Root Mutation"""


@strawberry.type
class Subscription(AppSubscription):
    """Root Subscription"""


# Root Schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
