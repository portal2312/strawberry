"""Project Root Schema."""

import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from app.queries import Query as AppQuery
from app.subscriptions import Subscription as AppSubscription


@strawberry.type
class Query(AppQuery):
    """Root query class."""


@strawberry.type
class Subscription(AppSubscription):
    """Root subscription class."""


# Root Schema
schema = strawberry.Schema(
    query=Query,
    subscription=Subscription,
    extensions=[
        DjangoOptimizerExtension,  # not required, but highly recommended
    ],
)
