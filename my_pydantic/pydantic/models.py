"""Models in the my_pydantif app.

References:
    https://docs.pydantic.dev/latest/api/base_model/
    https://docs.pydantic.dev/latest/concepts/fields/
    https://docs.pydantic.dev/latest/concepts/serialization/
    https://docs.pydantic.dev/latest/concepts/validators/
    https://docs.pydantic.dev/latest/errors/errors/
"""

from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

from .types import IPAddress


class AbstractModel(BaseModel): ...


class Option(BaseModel):
    """Options."""

    model_config = ConfigDict(
        validate_assignment=True,
    )

    dns_servers: list[IPAddress] | None = Field(default=None)
    domain_list: list[str] | None = Field(default=None)

    @field_validator("domain_list", mode="before")
    @classmethod
    def check_domain_list(cls, value: Any) -> list[str] | Any:
        """Check and parse domain_list.

        Args:
            value (Any): Unparsed domain_list value.

        Returns:
            list[str] | Any: parsed domain_list or any.
        """
        if isinstance(value, str):
            # Split the string by commas and strip whitespace
            value = [item.strip() for item in value.split(",")]

        # Return the value as-is if it's neither string, list, nor tuple
        return value

    @field_serializer("domain_list")
    def serialize_domain_list(self, domain_list: list[str], info) -> str:
        """Serialize dns_servers field."""
        return ", ".join(domain for domain in domain_list)


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
    option: Option
    parameter: Parameter
