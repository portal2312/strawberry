# Strawberry

## Documents

[Getting started](https://strawberry.rocks/docs)

GENERAL:

- [Schema basics](https://strawberry.rocks/docs/general/schema-basics)
- [Queries](https://strawberry.rocks/docs/general/queries)
- [Mutations](https://strawberry.rocks/docs/general/mutations)
- [Subscriptions](https://strawberry.rocks/docs/general/subscriptions)
  1. must support ASGI and websockets or use the AIOHTTP integration, install packages: `django`, `channels`, `daphne`
  2. [Update urls.py for Django](https://strawberry.rocks/docs/integrations/django)
  3. [Update asgi.py for Django + Channels](https://strawberry.rocks/docs/general/subscriptions#django--channels)
- ~~Why~~
- ~~Breaking changes~~
- ~~Upgrading Strawberry~~
- ~~FAQ~~

EDITOR INTEGRATION:

- [Mypy](https://strawberry.rocks/docs/editors/mypy)
  - Install [django-stubs](https://github.com/typeddjango/django-stubs)
  - See [Common Issue](https://mypy.readthedocs.io/en/stable/common_issues.html)
- ~~Visual Studio Code~~: `Mypy` 를 사용하므로 무시

INTEGRATIONS:

- [Django](https://strawberry.rocks/docs/integrations/django)
  - Setup [strawberry-django](https://github.com/strawberry-graphql/strawberry-django)
