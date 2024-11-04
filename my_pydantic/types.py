"""Strawberry types in my_pydantic app."""

from strawberry.experimental import pydantic

from .pydantic import models


@pydantic.type(model=models.Option, all_fields=True)
class Option: ...


@pydantic.type(model=models.Parameter, all_fields=True)
class Parameter: ...


@pydantic.type(model=models.SharedNetwork, all_fields=True)
class SharedNetwork: ...
