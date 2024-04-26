import strawberry

from app.mutations import Mutation
from app.queries import Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=strawberry.schema.config.StrawberryConfig(auto_camel_case=True),
)
