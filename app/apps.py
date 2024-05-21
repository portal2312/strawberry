"""App app.

References:
    https://github.com/strawberry-graphql/strawberry-django
"""

from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    """App app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
