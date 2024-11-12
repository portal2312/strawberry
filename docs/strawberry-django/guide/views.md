---
title: Views
---

# Serving the API

`WSGI` 보다 장점이 많은, `ASGI` 를 권장하므로 `AsyncGraphQLView` 를 사용합니다.

## Serving as ASGI (async)

`urls.py`:

```python title="urls.py"
from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path('graphql', AsyncGraphQLView.as_view(schema=schema)),
]
```

## Serving WSGI (sync)

PASS.
