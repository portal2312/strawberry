"""Types in my_pydantic app."""

from strawberry.experimental import pydantic

from . import models


@pydantic.type(model=models.Parameter, all_fields=True)
class Parameter: ...


@pydantic.type(model=models.SharedNetwork, all_fields=True)
class SharedNetwork: ...
