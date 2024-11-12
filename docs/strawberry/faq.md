---
title: FAQ
faq: true
---

# [Frequently Asked Questions](https://strawberry.rocks/docs/faq)

## How can I hide a field from GraphQL?

숨김 필드 유형을 지원합니다, `strawberry.Private`:

```python
import strawberry


@strawberry.type
class User:
    name: str
    age: int
    password: strawberry.Private[str]


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100, password="This is fake")


schema = strawberry.Schema(query=Query)
```

Schema 결과:

```graphql
type Query {
  user: User!
}

type User {
  name: String!
  age: Int!
}
```

## How can I deal with circular imports?

`strawberry.lazy`: resolve the circular imports(순환 참조).

```python
# posts.py
from typing import TYPE_CHECKING, Annotated

import strawberry

if TYPE_CHECKING:
    from .users import User


@strawberry.type
class Post:
    title: str
    author: Annotated["User", strawberry.lazy(".users")]
```

자세한 내용은, [Lazy types](./types/lazy.md) 문서를 참조하기.

## Can I reuse Object Types with Input Objects?

불행히도, [Graphql Spec](https://spec.graphql.org/june2018/#sec-input-objects)를 지정하기 때문에 객체 유형과 입력 유형간에 차이가 있습니다:

> 위에서 정의한 GraphQL Object 유형(ObjectTypeDefinition)은 여기서 재사용하기에 적합하지 않습니다. Object 유형은 인수를 정의하는 필드를 포함하거나 인터페이스와 유니언에 대한 참조를 포함할 수 있는데, 이는 모두 입력 인수로 사용하기에 적합하지 않기 때문입니다. 이러한 이유로 입력 객체는 시스템에서 별도의 유형을 갖습니다.

이는 Input 유형의 필드에도 해당합니다: Strawberry Input types 또는 scalar 만 사용할 수 있습니다.

자세한 내용은, [Input Types](./types/input-types.md) 를 참조하기.

## Can I use asyncio with Strawberry and Django?

[Async Django](./integrations/django.md#async-django) 보기.
