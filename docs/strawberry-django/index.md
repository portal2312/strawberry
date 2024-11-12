# Strawberry Django

Home Page: [Strawberry Django](https://strawberry-graphql.github.io/strawberry-django/)

Package name: [strawberry-graphql-django](https://github.com/strawberry-graphql/strawberry-django)

Table of Contents:

- [Strawberry Django](#strawberry-django)
  - [Quick Start](#quick-start)
  - [Guide](#guide)
    - [Serving the API](#serving-the-api)
      - [Serving as ASGI (async)](#serving-as-asgi-async)
    - [Defining Types](#defining-types)
    - [Defining Fields](#defining-fields)
  - [Integration](#integration)
    - [Channels](#channels)
    - [django-debug-toolbar](#django-debug-toolbar)

## Quick Start

Refer to [Quick Start](https://strawberry.rocks/docs).

## Guide

### Serving the API

#### Serving as ASGI (async)

```python
from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path('graphql', AsyncGraphQLView.as_view(schema=schema)),
]
```

### Defining Types

Refer to [Defining Types](https://strawberry-graphql.github.io/strawberry-django/guide/types/).

### Defining Fields

Refer to [Defining Fields](https://strawberry-graphql.github.io/strawberry-django/guide/fields/).

## Integration

### Channels

`Channels` 는 `Django` 를 필수 설치로 하지만, 사용은 없어도 할 수 있습니다.
그러나 가장 일반적인 사용 사례는 GraphQL 구독 지원을 사용하여 일반적인 `Django` 프로젝트를 실행하는 것이며, 일반적으로 `Strawberry` 통합을 통해 노출되는 채널 계층 기능을 활용합니다.

### django-debug-toolbar

Refer to [django-debug-toolbar](https://strawberry-graphql.github.io/strawberry-django/integrations/debug-toolbar/).
