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
    - [django-debug-toolbar](#django-debug-toolbar)

## Quick Start

Refer to [Quick Start](https://strawberry-graphql.github.io/strawberry-django/quick-start/).

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

### django-debug-toolbar

Refer to [django-debug-toolbar](https://strawberry-graphql.github.io/strawberry-django/integrations/debug-toolbar/).
