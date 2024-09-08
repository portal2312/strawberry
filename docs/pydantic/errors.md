# [Error Handling](https://docs.pydantic.dev/latest/errors/errors/)

Pydantic 은 검증 중인 데이터에서 오류를 발견할 때마다 `ValidationError` 를 발생시킵니다.

> [!NOTE]
> 유효성 검사 코드는 `ValidationError` 자체를 발생시켜서는 안되며, ValidationError를 채우는 데 사용되는 `ValueError` 또는 `AssertionError`(또는 그 하위 클래스)를 발생시켜야 합니다.

발견된 오류 수에 관계없이 한 가지 예외가 발생합니다. `ValidationError` 에는 모든 오류와 오류 발생 방식에 대한 정보가 포함됩니다.

여러 가지 방법으로 이러한 오류에 액세스할 수 있습니다:

| Method            | Description                                    |
| ----------------- | ---------------------------------------------- |
| `e.errors()`      | 입력 데이터에서 발견된 오류 목록을 반환합니다. |
| `e.error_count()` | 오류에서 발견된 오류 수를 반환합니다.          |
| `e.json()`        | 오류에 대한 JSON 표현을 반환합니다.            |
| `str(e)`          | 사람이 읽을 수 있는 오류 표현을 반환합니다.    |

각 오류 개체에는 다음이 포함됩니다:

| Property | Description                                                       |
| -------- | ----------------------------------------------------------------- |
| `ctx`    | 오류 메시지를 렌더링하는 데 필요한 값이 포함된 선택적 개체입니다. |
| `input`  | 유효성 검사를 위해 제공된 입력입니다.                             |
| `loc`    | 오류 위치를 목록으로 표시합니다.                                  |
| `msg`    | 사람이 읽을 수 있는 오류 설명입니다.                              |
| `type`   | 컴퓨터에서 읽을 수 있는 오류 유형 식별자입니다.                   |
| `url`    | 오류에 대한 추가 정보에 대한 URL입니다.                           |

`loc` 목록의 첫 번째 항목은 오류가 발생한 필드가 되며, 해당 필드가 하위 모델인 경우 후속 항목이 나타나 오류의 중첩 위치를 나타냅니다.

```python
from typing import List

from pydantic import BaseModel, ValidationError, conint


class Location(BaseModel):
    lat: float = 0.1
    lng: float = 10.1


class Model(BaseModel):
    is_required: float
    gt_int: conint(gt=42)
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None


data = dict(
    list_of_ints=["1", 2, "bad"],
    a_float="not a float",
    recursive_model={"lat": 4.2, "lng": "New York"},
    gt_int=21,
)

try:
    Model(**data)
except ValidationError as e:
    print(e)

try:
    Model(**data)
except ValidationError as e:
    print(e.errors())
```

```bash
5 validation errors for Model
is_required
  Field required [type=missing, input_value={'list_of_ints': ['1', 2,...ew York'}, 'gt_int': 21}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.8/v/missing
gt_int
  Input should be greater than 42 [type=greater_than, input_value=21, input_type=int]
    For further information visit https://errors.pydantic.dev/2.8/v/greater_than
list_of_ints.2
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing
a_float
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/float_parsing
recursive_model.lng
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='New York', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/float_parsing
```

```python
[
    {
        "type": "missing",
        "loc": ("is_required",),
        "msg": "Field required",
        "input": {
            "list_of_ints": ["1", 2, "bad"],
            "a_float": "not a float",
            "recursive_model": {"lat": 4.2, "lng": "New York"},
            "gt_int": 21,
        },
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    },
    {
        "type": "greater_than",
        "loc": ("gt_int",),
        "msg": "Input should be greater than 42",
        "input": 21,
        "ctx": {"gt": 42},
        "url": "https://errors.pydantic.dev/2.8/v/greater_than",
    },
    {
        "type": "int_parsing",
        "loc": ("list_of_ints", 2),
        "msg": "Input should be a valid integer, unable to parse string as an integer",
        "input": "bad",
        "url": "https://errors.pydantic.dev/2.8/v/int_parsing",
    },
    {
        "type": "float_parsing",
        "loc": ("a_float",),
        "msg": "Input should be a valid number, unable to parse string as a number",
        "input": "not a float",
        "url": "https://errors.pydantic.dev/2.8/v/float_parsing",
    },
    {
        "type": "float_parsing",
        "loc": ("recursive_model", "lng"),
        "msg": "Input should be a valid number, unable to parse string as a number",
        "input": "New York",
        "url": "https://errors.pydantic.dev/2.8/v/float_parsing",
    },
]
```

## Custom Errors

사용자 정의 데이터 유형 또는 유효성 검사기에서는 오류를 발생시키려면 `ValueError` 또는 `AssertionError` 를 사용해야 합니다.

`@validator` decorator 사용에 대한 자세한 내용은 [Validators](https://docs.pydantic.dev/latest/concepts/validators/)를 참조하세요:

```python
from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    foo: str

    @field_validator("foo")
    def value_must_equal_bar(cls, v):
        if v != "bar":
            raise ValueError('value must be "bar"')

        return v


try:
    Model(foo="ber")
except ValidationError as e:
    print(e)
    print(e.errors())
```

```bash
1 validation error for Model
foo
    Value error, value must be "bar" [type=value_error, input_value='ber', input_type=str]
```

```python
[
    {
        'type': 'value_error',
        'loc': ('foo',),
        'msg': 'Value error, value must be "bar"',
        'input': 'ber',
        'ctx': {'error': ValueError('value must be "bar"')},
        'url': 'https://errors.pydantic.dev/2/v/value_error',
    }
]
```

`PydanticCustomError` 를 사용하여 오류 구조를 완전히 제어할 수도 있습니다:

```python
from pydantic_core import PydanticCustomError

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    foo: str

    @field_validator("foo")
    def value_must_equal_bar(cls, v):
        if v != "bar":
            raise PydanticCustomError(
                "not_a_bar",
                'value is not "bar", got "{wrong_value}"',
                dict(wrong_value=v),
            )
        return v


try:
    Model(foo="ber")
except ValidationError as e:
    print(e)
```

```bash
1 validation error for Model
foo
  value is not "bar", got "ber" [type=not_a_bar, input_value='ber', input_type=str]
```

## Error messages

Pydantic 은 유효성 검사 및 사용 오류에 대해 유용한 기본 오류 메시지를 제공하려고 시도합니다.

다음 섹션에서는 기본 오류 코드에 대한 설명서를 제공했습니다:

- [Validation errors](https://docs.pydantic.dev/latest/errors/validation_errors/): 참조 용도로 활용하기.
- [Usage errors](https://docs.pydantic.dev/latest/errors/usage_errors/): 참조 용도로 활용하기.

### Customize error messages

사용자 정의 오류 핸들러를 생성하여 오류 메시지를 사용자 정의할 수 있습니다.

일반적인 사용 사례는 오류 메시지를 번역하는 것입니다.
예를 들어 아래와 같이 `CUSTOM_MESSAGES` 사전을 번역 사전으로 대체하여 오류 메시지를 번역할 수 있습니다:

```python
from typing import Dict, List

from pydantic_core import ErrorDetails

from pydantic import BaseModel, HttpUrl, ValidationError

CUSTOM_MESSAGES = {
    "int_parsing": "This is not an integer! 🤦",
    "url_scheme": "Hey, use the right URL scheme! I wanted {expected_schemes}.",
}


def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error["type"])
        if custom_message:
            ctx = error.get("ctx")
            error["msg"] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors


class Model(BaseModel):
    a: int
    b: HttpUrl


try:
    Model(a="wrong", b="ftp://example.com")
except ValidationError as e:
    errors = convert_errors(e, CUSTOM_MESSAGES)
    print(errors)
```

```python
[
    {
        "type": "int_parsing",
        "loc": ("a",),
        "msg": "This is not an integer! 🤦",
        "input": "wrong",
        "url": "https://errors.pydantic.dev/2.8/v/int_parsing",
    },
    {
        "type": "url_scheme",
        "loc": ("b",),
        "msg": "Hey, use the right URL scheme! I wanted 'http' or 'https'.",
        "input": "ftp://example.com",
        "ctx": {"expected_schemes": "'http' or 'https'"},
        "url": "https://errors.pydantic.dev/2.8/v/url_scheme",
    },
]
```

또 다른 예는 오류의 `loc` 값이 표시되는 방식을 사용자 정의하는 것입니다:

```python
from typing import Any, Dict, List, Tuple, Union

from pydantic import BaseModel, ValidationError


def loc_to_dot_sep(loc: Tuple[Union[str, int], ...]) -> str:
    path = ""
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += "."
            path += x
        elif isinstance(x, int):
            path += f"[{x}]"
        else:
            raise TypeError("Unexpected type")
    return path


def convert_errors(e: ValidationError) -> List[Dict[str, Any]]:
    new_errors: List[Dict[str, Any]] = e.errors()
    for error in new_errors:
        error["loc"] = loc_to_dot_sep(error["loc"])
    return new_errors


class TestNestedModel(BaseModel):
    key: str
    value: str


class TestModel(BaseModel):
    items: List[TestNestedModel]


data = {"items": [{"key": "foo", "value": "bar"}, {"key": "baz"}]}

try:
    TestModel.model_validate(data)
except ValidationError as e:
    print(e.errors())
    pretty_errors = convert_errors(e)
    print(pretty_errors)
```

```python
[
    {
        "type": "missing",
        "loc": ("items", 1, "value"),
        "msg": "Field required",
        "input": {"key": "baz"},
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    }
]
[
    {
        "type": "missing",
        "loc": "items[1].value",
        "msg": "Field required",
        "input": {"key": "baz"},
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    }
]
```
