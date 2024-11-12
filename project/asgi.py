"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/

Query and Mutation: print(info.context["request"].consumer.scope["user"])
Subscription: print(info.context["request"].scope["user"])

References:
    https://strawberry.rocks/docs/general/subscriptions#django--channels
    https://strawberry.rocks/docs/integrations/channels
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path
from strawberry.channels import (
    GraphQLHTTPConsumer,
    GraphQLWSConsumer,
)

from .settings import DEBUG

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Import your Strawberry schema after creating the django ASGI application
# This ensures django.setup() has been called before any ORM models are imported
# for the schema.
from .schema import schema  # noqa: E402

# Consumers
gql_http_consumer = AuthMiddlewareStack(GraphQLHTTPConsumer.as_asgi(schema=schema))
gql_ws_consumer = GraphQLWSConsumer.as_asgi(schema=schema, debug=DEBUG)

# Patterns
graphql_url_pattern = "^graphql"
http_url_patterns = [
    re_path(graphql_url_pattern, gql_http_consumer),
    re_path("^", django_asgi_app),
]
websocket_url_patterns = [
    re_path(graphql_url_pattern, gql_ws_consumer),
]

application = ProtocolTypeRouter(
    {
        "http": URLRouter(http_url_patterns),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_url_patterns))
        ),
    },
)
