"""Exceptions in my_pydantic app.

References:
    https://docs.pydantic.dev/latest/errors/errors/
"""

from pydantic import ValidationError
from pydantic_core import ErrorDetails

CUSTOM_MESSAGES = {
    "greater_than": "입력값은 {gt}보다 커야 합니다.",
}


def convert_errors(e: ValidationError) -> list[ErrorDetails]:
    """Convert errors msg."""
    errors: list[ErrorDetails] = []
    for error in e.errors(include_url=False):
        if custom_message := CUSTOM_MESSAGES.get(error["type"]):
            if ctx := error.get("ctx"):
                error["msg"] = custom_message.format(**ctx)
        errors.append(error)
    return errors
