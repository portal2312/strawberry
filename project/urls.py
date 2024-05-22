"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # strawberry-graphql: Integrations/Django/Async Django
    # https://strawberry.rocks/docs/integrations/django#async-django
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
    # django-debug-toolbar: Add the URLs
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-urls
    path("__debug__/", include("debug_toolbar.urls")),
    # https://docs.djangoproject.com/en/5.0/howto/static-files/#serving-static-files-during-development
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
