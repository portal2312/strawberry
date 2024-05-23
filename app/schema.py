"""App app schema."""

import strawberry

from .queries import Query
from .subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    subscription=Subscription,
    config=strawberry.schema.config.StrawberryConfig(auto_camel_case=True),
)
