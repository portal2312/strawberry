"""Inputs in mypydantic app."""

import strawberry

from . import models


@strawberry.experimental.pydantic.input(model=models.Parameter, all_fields=True)
class ParameterInput: ...


@strawberry.experimental.pydantic.input(model=models.SharedNetwork, all_fields=True)
class SharedNetworkInput: ...
