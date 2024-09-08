"""Exceptions in my_pydantic app.

References:
    https://docs.pydantic.dev/latest/errors/errors/
"""

from pydantic import ValidationError
from pydantic_core import ErrorDetails

CUSTOM_MESSAGES = {
    "int_parsing": "This is not an integer!",
    "url_scheme": "Hey, use the right URL scheme! I wanted {expected_schemes}.",
}


def convert_errors(e: ValidationError) -> list[ErrorDetails]:
    """Convert errors.

    Args:
        e (ValidationError): Error instance.

    Returns:
        list[ErrorDetails]: Error instance list.
    """
    new_errors: list[ErrorDetails] = []
    for error in e.errors():
        if message := CUSTOM_MESSAGES.get(error["type"]):
            ctx = error.get("ctx")
            error["msg"] = message.format(**ctx) if ctx else message
        new_errors.append(error)
    return new_errors
