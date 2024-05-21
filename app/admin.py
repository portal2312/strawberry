"""App app admin."""

from django.contrib import admin

from app.models import Color, Fruit


class ColorAdmin(admin.ModelAdmin):
    """색상."""

    fields = [
        "name",
    ]


class FruitAdmin(admin.ModelAdmin):
    """과일."""

    fields = [
        "name",
        "color",
    ]


admin.site.register(Color, ColorAdmin)
admin.site.register(Fruit, FruitAdmin)
