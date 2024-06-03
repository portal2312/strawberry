"""App app scalars.

Examples:
    Use `strawberry.Schema.scalar_overrides`, ``schema.py``::

        from .queries import Query
        from .scalars import SlugScalar, UnixTimeStampScalar

        schema = strawberry.Schema(
            query=Query,
            scalar_overrides={
                slug: SlugScalar,
                datetime: UnixTimeStampScalar
            },
        )

    OR, Use `strawberry_django.fields.types.field_type_map.update`, ``types.py``::

        from django.db import models
        from strawberry_django.fields.types import field_type_map

        from .scalars import SlugScalar, UnixTimeStampScalar

        field_type_map.update(
            {
                models.SlugField: SlugScalar,
                models.DateTimeField: UnixTimeStampScalar,
            }
        )
        ...

References:
    https://strawberry.rocks/docs/types/scalars
    https://strawberry-graphql.github.io/strawberry-django/guide/fields/#defining-types-for-auto-fields
"""

from datetime import datetime, timezone
from typing import NewType

import strawberry

SlugScalar = strawberry.scalar(
    NewType("Slug", str),
    serialize=lambda v: v,
    parse_value=lambda v: v,
)

UnixTimeStampScalar = strawberry.scalar(
    NewType("UnixTimeStamp", datetime),
    serialize=lambda value: int(value.timestamp()),
    parse_value=lambda value: datetime.fromtimestamp(int(value), timezone.utc),
)
# @strawberry_django.type
# class MyCustomFileType:
#     ...
