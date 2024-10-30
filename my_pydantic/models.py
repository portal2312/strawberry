"""Models in the my_pydantif app.

References:
    https://docs.pydantic.dev/latest/api/base_model/
    https://docs.pydantic.dev/latest/concepts/fields/
    https://docs.pydantic.dev/latest/concepts/validators/
    https://docs.pydantic.dev/latest/errors/errors/
"""

from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pydantic_core import PydanticCustomError


class AbstractModel(BaseModel): ...


class Parameter(BaseModel):
    """Parameter."""

    model_config = ConfigDict(
        validate_assignment=True,
    )

    preferred_lifetime: int = Field(
        gt=0,
        description="Preferred Lifetime",
    )
    valid_lifetime: int = Field(
        gt=0,
        description="Valid Lifetime",
    )

    @model_validator(mode="after")
    def check_preferred_lifetime__lte__valid_lifetime(self) -> Self:
        """Check preferred_lifetime less than or equal valid_lifetime."""
        if self.preferred_lifetime is None:
            return self
        if self.valid_lifetime is None:
            raise PydanticCustomError(
                "preferred_lifetime__lte__valid_lifetime__is_none",
                "Preferred Lifetime 의 값이 있는 경우, Valid Lifetime 의 값이 존재해야 합니다.",
            )
        if self.preferred_lifetime > self.valid_lifetime:
            raise PydanticCustomError(
                "preferred_lifetime__lte__valid_lifetime__greater",
                "Preferred Lifetime 이 Valid Lifetime 보다 큽니다: {preferred_lifetime} <= {valid_lifetime} 은 올바르지 않습니다.",
                {
                    "preferred_lifetime": self.preferred_lifetime,
                    "valid_lifetime": self.valid_lifetime,
                },
            )
        return self


class SharedNetwork(BaseModel):
    """SharedNetwork."""

    name: str = Field(min_length=1, pattern=r"^\w*$")
    description: str | None = Field(default=None, max_length=79)
    parameter: Parameter
