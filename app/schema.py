"""App app schema.

References:
    https://strawberry.rocks/docs/types/schema-configurations
    https://strawberry.rocks/docs/types/scalars#overriding-built-in-scalars
"""

import strawberry

from .mutations import Mutation
from .queries import Query
from .subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    config=strawberry.schema.config.StrawberryConfig(auto_camel_case=True),
    scalar_overrides={},
)
