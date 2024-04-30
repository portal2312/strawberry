import strawberry

from .mutations import Mutation
from .queries import Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=strawberry.schema.config.StrawberryConfig(auto_camel_case=True),
)
