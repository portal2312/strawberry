---
title: Django
---

[strawberry-graphql-django](https://github.com/strawberry-graphql/strawberry-django) 를 지원합니다.

제공하는 View:

- ~~`strawberry.django.views.GraphQLView`~~: PASS.
- [x] `strawberry.django.views.AsyncGraphQLView`: [Django GENERAL Views, Serving the API](https://strawberry.rocks/docs/django/guide/views) 를 읽어 보니 ASGI 를 사용하기 위해, 사용합니다.

둘 다 설치 된 경우, `import strawberry_django` 를 사용하십시오. `import strawberry.django` 와 동일하게 동작합니다.

GraphiQL interface template 을 사용하려면:

```python
INSTALLED_APPS = [
    ...,
    "strawberry_django",
]
```

PASS.

# Async Django

GraphQL 스키마를 제공하는 데 사용할 수 있는 뷰를 제공합니다:

```python
from django.urls import path

from strawberry.django.views import AsyncGraphQLView

from api.schema import schema

urlpatterns = [
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
]
```

## Options

Arguments:

- `schema`: 필수, `strawberry.Schema` 로 생성 된 schema.
- `graphql_ide`: PASS
- `allow_queries_via_get`: PASS.

## Extending the view

Methods:

- `def get_context(self, request: HttpRequest, response: HttpResponse) -> Any`
- `def get_root_value(self, request: HttpRequest) -> Any`
- `def process_result(self, request: HttpRequest, result: ExecutionResult) -> GraphQLHTTPResponse`
- `def render_graphql_ide(self, request: HttpRequest) -> HttpResponse`

### get_context

`get_context`를 사용하면 Resolver에서 사용할 수있는 사용자 정의 컨텍스트 객체를 제공 할 수 있습니다. 여기에서 무엇이든 반환 할 수 있습니다. 기본적으로 `StrawberryDjangoContext` 객체를 반환합니다.

```python
class MyGraphQLView(AsyncGraphQLView):
    async def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        return {"example": 1}


@strawberry.type
class Query:
    @strawberry.field
    def example(self, info: strawberry.Info) -> str:
        return str(info.context["example"])
```

### get_root_value

`get_root_value`를 사용하면 schema 에 맞춤 최상위 값을 제공 할 수 있습니다. 이것은 아마도 많이 사용되지 않지만 특정 상황에서는 유용 할 수 있습니다:

```python
class MyGraphQLView(GraphQLView):
    def get_root_value(self, request: HttpRequest) -> Any:
        return Query(name="Patrick")


@strawberry.type
class Query:
    name: str
```

### process_result

`process_result`는 클라이언트에게 전송되기 전에 사용자 정의 및/또는 프로세스 결과를 허용합니다. 이것은 로깅 오류 또는 숨겨지는 유용한 일일 수 있습니다 (예: 내부 예외를 숨기기 위해).

`GraphQLHTTPResponse` 의 객체를 반환하고 요청과 실행 결과를 수락해야 합니다:

```python
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult


class MyGraphQLView(AsyncGraphQLView):
    async def process_result(
        self, request: HttpRequest, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {"data": result.data}

        if result.errors:
            data["errors"] = [err.formatted for err in result.errors]

        return data
```

### encode_json

PASS.

### render_graphql_ide

PASS.

## Subscriptions

Strawberry INTEGRATIONS [Channels](https://strawberry.rocks/docs/integrations/channels) 를 참조바랍니다.
