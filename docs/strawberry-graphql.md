# Strawberry

Home Page: [Strawberry](https://strawberry.rocks/)

Package name: [strawberry-graphql](https://github.com/strawberry-graphql/strawberry)

Table of Contents:

- [Strawberry](#strawberry)
  - [Getting started](#getting-started)
  - [GENERAL](#general)
    - [Schema basics](#schema-basics)
    - [Queries](#queries)
    - [Mutations](#mutations)
    - [Subscriptions](#subscriptions)
    - [~~Why~~](#why)
    - [~~Breaking changes~~](#breaking-changes)
    - [~~Upgrading Strawberry~~](#upgrading-strawberry)
    - [~~FAQ~~](#faq)
  - [EDITOR INTEGRATION](#editor-integration)
    - [Mypy](#mypy)
      - [~~Visual Studio Code~~](#visual-studio-code)
  - [GUIDES](#guides)
    - [Schema export](#schema-export)
    - [~~Authentication~~](#authentication)
  - [TYPE](#type)
    - [Schema](#schema)
      - [API reference](#api-reference)
      - [Methods](#methods)
      - [Handling execution errors](#handling-execution-errors)
      - [Filtering/customising fields](#filteringcustomising-fields)
  - [INTEGRATIONS](#integrations)
    - [Django](#django)

## Getting started

Refer to [here](https://strawberry.rocks/docs/)

## GENERAL

### Schema basics

Refer to [here](https://strawberry.rocks/docs/general/schema-basics).

### Queries

Refer to [here](https://strawberry.rocks/docs/general/queries).

### Mutations

Refer to [here](https://strawberry.rocks/docs/general/mutations).

### Subscriptions

1. must support ASGI and websockets or use the AIOHTTP integration, install packages: `django`, `channels`, `daphne`
2. [Update urls.py for Django](https://strawberry.rocks/docs/integrations/django)
3. [Update asgi.py for Django + Channels](https://strawberry.rocks/docs/general/subscriptions#django--channels)

Refer to [here](https://strawberry.rocks/docs/general/subscriptions).

### ~~Why~~

### ~~Breaking changes~~

### ~~Upgrading Strawberry~~

### ~~FAQ~~

## EDITOR INTEGRATION

### Mypy

Install [django-stubs](https://github.com/typeddjango/django-stubs) to support Mypy on [Django](https://www.djangoproject.com/).

Common issues related to type and typing can be found [here](https://mypy.readthedocs.io/en/stable/common_issues.html).

Refer to [here](https://strawberry.rocks/docs/editors/mypy).

#### ~~Visual Studio Code~~

`Mypy` 를 사용하므로 무시합니다.

## GUIDES

### Schema export

For example in Django (refer to [here](https://github.com/strawberry-graphql/strawberry-django/pull/299)):

```bash
python manage.py export_schema project.schema > schema.graphql
```

Refer to [here](https://strawberry.rocks/docs/guides/schema-export).

### ~~Authentication~~

예제:

- 동기식으로 동작합니다.
- Union 활용을 하지만 결과에 대한 field 접근을 할 수 없습니다.

Refer to [Authentication](https://strawberry.rocks/docs/guides/authentication)

## TYPE

### Schema

#### API reference

#### Methods

For example in Jupyter Notebook:

```python
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django

django.setup()

from project.schema import schema

await schema.execute("query Q { colors { name} }")
```

#### Handling execution errors

#### Filtering/customising fields

Refer to [here](https://strawberry.rocks/docs/types/schema).

## INTEGRATIONS

### Django

`Django` 하위 `Extending the view` 은 동작하지 않습니다.

`Async Django` 하위 `Extending the view` 은 동작하지 않습니다.

본문의 내용은 간략하게 읽고 [여기](https://strawberry-graphql.github.io/strawberry-django/quick-start/) 참조해야 합니다.

Refer to [here](https://strawberry.rocks/docs/integrations/django).
