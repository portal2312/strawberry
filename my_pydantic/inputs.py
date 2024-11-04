"""Inputs in mypydantic app.

References:
    https://strawberry.rocks/docs/integrations/pydantic#input-types
    https://strawberry.rocks/docs/integrations/pydantic#custom-conversion-logic
    https://docs.python.org/dev/library/dataclasses.html#dataclasses.asdict
    https://docs.pydantic.dev/latest/concepts/models/#validating-data
"""

import dataclasses

import strawberry

from .pydantic import models


@strawberry.experimental.pydantic.input(model=models.Option, all_fields=True)
class OptionInput: ...


@strawberry.experimental.pydantic.input(model=models.Parameter, all_fields=True)
class ParameterInput: ...


@strawberry.experimental.pydantic.input(model=models.Subnet6, all_fields=True)
class Subnet6Input: ...


@strawberry.experimental.pydantic.input(model=models.SharedNetwork, all_fields=True)
class SharedNetworkInput:
    def to_pydantic(self) -> models.SharedNetwork:
        """Override to_pydantic_default.

        Generally using to_pydnatic_default is not found loc attribute for ValidateError.
        So, overrides this.
        """
        # FIXME: Mypy(call-overload), No overload variant of "asdict" matches argument type "SharedNetworkInput".
        data = dataclasses.asdict(self)  # type: ignore[call-overload]
        return models.SharedNetwork.model_validate(data)
