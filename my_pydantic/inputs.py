"""Inputs in mypydantic app.

References:
    https://strawberry.rocks/docs/integrations/pydantic#custom-conversion-logic
"""

import dataclasses

import strawberry

from . import models


@strawberry.experimental.pydantic.input(model=models.Parameter, all_fields=True)
class ParameterInput: ...


@strawberry.experimental.pydantic.input(model=models.SharedNetwork, all_fields=True)
class SharedNetworkInput:
    def to_pydantic(self) -> models.SharedNetwork:
        """Override to_pydantic_default.

        Generally using to_pydnatic_default is not found loc attribute for ValidateError.
        So, overrides this.
        """
        # FIXME: Mypy(call-overload), No overload variant of "asdict" matches argument type "SharedNetworkInput".
        data = dataclasses.asdict(self)
        return models.SharedNetwork.model_validate(data)
