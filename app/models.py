"""App models."""

from django.db import models


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
