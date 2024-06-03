"""App models."""

from django.db import models
from django_choices_field import TextChoicesField


class FruitCategory(models.TextChoices):
    """과일 종류."""

    CITRUS = "citrus", "Citrus"
    BERRY = "berry", "Berry"


class Color(models.Model):
    """색상."""

    name = models.CharField(
        max_length=20,
        help_text="이름",
    )
    description = models.CharField(max_length=128, blank=True)

    def __str__(self) -> str:
        """이름."""
        return self.name


class Fruit(models.Model):
    """과일."""

    name = models.CharField(
        max_length=20,
        help_text="이름",
    )
    category = TextChoicesField(
        choices_enum=FruitCategory,
        help_text="종류",
    )
    wiki_urls = models.SlugField(blank=True, help_text="Wiki URLs")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일자")
    updated_at = models.DateTimeField(auto_now=True, help_text="변경 일자")
    # Relation Fields.
    color = models.ForeignKey(
        "Color",
        on_delete=models.CASCADE,
        related_name="fruits",
        blank=True,
        null=True,
        help_text="색상",
    )

    def __str__(self) -> str:
        """이름."""
        return self.name
