# [Validators](https://docs.pydantic.dev/latest/concepts/validators/)

## Annotated Validators

`Annotated` 를 사용하여 유효성 검사기를 적용하는 방법을 제공합니다.

`Model` 이나 `Field` 대신 유효성 검사를 유형에 바인딩할 때마다 이것을 사용해야 합니다:

```python
from typing import Any, List

from typing_extensions import Annotated

from pydantic import BaseModel, ValidationError
from pydantic.functional_validators import AfterValidator


def check_squares(v: int) -> int:
    assert v**0.5 % 1 == 0, f"{v} is not a square number"
    return v


def check_double(v: Any) -> Any:
    return v * 2


MyNumber = Annotated[int, AfterValidator(check_double), AfterValidator(check_squares)]


class DemoModel(BaseModel):
    number: List[MyNumber]


demo = DemoModel(number=[2, 8])
assert demo.number[0] == 4
assert demo.number[1] == 16

try:
    DemoModel(number=[2, 4])
except ValidationError as e:
    print(e)
```

```py
1 validation error for DemoModel
number.1
  Assertion failed, 8 is not a square number [type=assertion_error, input_value=4, input_type=int]
    For further information visit https://errors.pydantic.dev/2.8/v/assertion_error
```

이 예에서는 몇 가지 유형 별칭(MyNumber = Annotated[...])을 사용했습니다.  
이는 코드의 가독성에 도움이 될 수 있지만 필수는 아니지만 모델 필드 유형 힌트에 Annotated를 직접 사용할 수 있습니다.  
이러한 유형 별칭은 실제 유형이 아니지만 `TypeAliasType` 과 유사한 접근 방식을 사용하여 실제 유형을 만들 수 있습니다.  
사용자 정의 유형에 대한 자세한 설명은 [Custom Types](https://docs.pydantic.dev/latest/concepts/types/#custom-types)을 참조하세요.

`Annotated`를 다른 유형 내에 중첩할 수 있다는 점도 주목할 가치가 있습니다.  
이 예에서는 이를 사용하여 목록의 내부 항목에 유효성 검사를 적용했습니다.  
dict 키 등에 대해서도 동일한 접근 방식을 사용할 수 있습니다.

### Before, After, Wrap and Plain validators

- `After`: Pydantic의 내부 구문 분석 후 실행합니다. 일반적으로 유형이 더 안전하고 구현하기가 더 쉽습니다.
- `Before`: Pydantic의 내부 구문 분석 및 유효성 검사(예: str을 int로 강제 변환) 전에 실행합니다. 이들은 원시 입력을 수정할 수 있기 때문에 After 유효성 검사기보다 더 유연하지만 이론적으로는 임의의 개체일 수 있는 원시 입력도 처리해야 합니다.
- `Plain`: `mode='before'` 유효성 검사기와 유사하지만 즉시 유효성 검사를 종료하고 더 이상 유효성 검사기가 호출되지 않으며 Pydantic은 내부 유효성 검사를 수행하지 않습니다.
- `Wrap`: 가장 유연합니다. Pydantic 및 기타 유효성 검사기가 작업을 수행하기 전이나 후에 코드를 실행하거나 성공적인 값 또는 오류와 함께 유효성 검사를 즉시 종료할 수 있습니다.

이전, 이후 또는 `mode='wrap'` 유효성 검사기를 여러 개 사용할 수 있지만, 일반 유효성 검사기는 내부 유효성 검사기를 호출하지 않으므로 `PlainValidator`는 하나만 사용할 수 있습니다.

다음은 `mode='wrap'` 유효성 검사기의 예입니다:

```python
import json
from typing import Any, List

from typing_extensions import Annotated

from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
)
from pydantic.functional_validators import WrapValidator


def maybe_strip_whitespace(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> int:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())
    assert info.mode == "python"
    assert isinstance(v, int), "In Python mode the input must be an int!"
    # do no further validation
    return v


MyNumber = Annotated[int, WrapValidator(maybe_strip_whitespace)]


class DemoModel(BaseModel):
    number: List[MyNumber]


print(DemoModel(number=[2, 8]))
print(DemoModel.model_validate_json(json.dumps({"number": [" 2 ", "8"]})))
try:
    DemoModel(number=["2"])
except ValidationError as e:
    print(e)
```

```py
number=[2, 8]
number=[2, 8]
1 validation error for DemoModel
number.0
  Assertion failed, In Python mode the input must be an int! [type=assertion_error, input_value='2', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/assertion_error
```

### Ordering of validators within Annotated

유효성 검사는 오른쪽에서 왼쪽으로, 그리고 뒤로 진행됩니다.  
즉, 오른쪽에서 왼쪽으로 모든 "이전" 유효성 검사기를 실행(또는 "래핑" 유효성 검사기를 호출)한 다음 왼쪽에서 오른쪽으로 모든 "이후" 유효성 검사기를 호출합니다:

```python
from typing import Any, Callable, List, cast

from typing_extensions import Annotated, TypedDict

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    PlainValidator,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)
from pydantic.functional_validators import field_validator


class Context(TypedDict):
    logs: List[str]


def make_validator(label: str) -> Callable[[str, ValidationInfo], str]:
    def validator(v: Any, info: ValidationInfo) -> Any:
        context = cast(Context, info.context)
        context["logs"].append(label)
        return v

    return validator


def make_wrap_validator(
    label: str,
) -> Callable[[str, ValidatorFunctionWrapHandler, ValidationInfo], str]:
    def validator(
        v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
    ) -> Any:
        context = cast(Context, info.context)
        context["logs"].append(f"{label}: pre")
        result = handler(v)
        context["logs"].append(f"{label}: post")
        return result

    return validator


class A(BaseModel):
    x: Annotated[
        str,
        BeforeValidator(make_validator("before-1")),
        AfterValidator(make_validator("after-1")),
        WrapValidator(make_wrap_validator("wrap-1")),
        BeforeValidator(make_validator("before-2")),
        AfterValidator(make_validator("after-2")),
        WrapValidator(make_wrap_validator("wrap-2")),
        BeforeValidator(make_validator("before-3")),
        AfterValidator(make_validator("after-3")),
        WrapValidator(make_wrap_validator("wrap-3")),
        BeforeValidator(make_validator("before-4")),
        AfterValidator(make_validator("after-4")),
        WrapValidator(make_wrap_validator("wrap-4")),
    ]
    y: Annotated[
        str,
        BeforeValidator(make_validator("before-1")),
        AfterValidator(make_validator("after-1")),
        WrapValidator(make_wrap_validator("wrap-1")),
        BeforeValidator(make_validator("before-2")),
        AfterValidator(make_validator("after-2")),
        WrapValidator(make_wrap_validator("wrap-2")),
        PlainValidator(make_validator("plain")),
        BeforeValidator(make_validator("before-3")),
        AfterValidator(make_validator("after-3")),
        WrapValidator(make_wrap_validator("wrap-3")),
        BeforeValidator(make_validator("before-4")),
        AfterValidator(make_validator("after-4")),
        WrapValidator(make_wrap_validator("wrap-4")),
    ]

    val_x_before = field_validator("x", mode="before")(make_validator("val_x before"))
    val_x_after = field_validator("x", mode="after")(make_validator("val_x after"))
    val_y_wrap = field_validator("y", mode="wrap")(make_wrap_validator("val_y wrap"))


context = Context(logs=[])

A.model_validate({"x": "abc", "y": "def"}, context=context)
print(context["logs"])
```

```py
[
    'val_x before',
    'wrap-4: pre', 'before-4', 'wrap-3: pre', 'before-3', 'wrap-2: pre', 'before-2', 'wrap-1: pre',
    'before-1',
    'after-1',
    'wrap-1: post', 'after-2', 'wrap-2: post', 'after-3', 'wrap-3: post', 'after-4', 'wrap-4: post',
    'val_x after',
    'val_y wrap: pre',
    'wrap-4: pre', 'before-4', 'wrap-3: pre', 'before-3', 'plain', 'after-3', 'wrap-3: post', 'after-4', 'wrap-4: post',
    'val_y wrap: post'
]
```

## Validation of default values

기본값을 사용하면 유효성 검사기가 실행되지 않습니다.  
이는 `@field_validator` 유효성 검사기와 주석이 달린 유효성 검사기 모두에 적용됩니다.  
`Field(validate_default=True)` 를 사용하여 강제로 실행되도록 할 수 있습니다.  
일반적으로 내부 유효성 검사기가 호출되기 전에 함수가 호출되는 `@model_validator(mode='before')`를 사용하는 것이 더 좋습니다.

```python
from typing_extensions import Annotated

from pydantic import BaseModel, Field, field_validator


class Model(BaseModel):
    x: str = "abc"
    y: Annotated[str, Field(validate_default=True)] = "xyz"

    @field_validator("x", "y")
    @classmethod
    def double(cls, v: str) -> str:
        return v * 2


m = Model()
assert m.x == "abc"
assert m.y == "xyz" * 2
m = Model(x="foo")
assert m.x == "foo" * 2
m = Model(x="foo", y="bar")
assert m.x == "foo" * 2
assert m.y == "bar" * 2
```

## Field validators

특정 필드에 `@field_validator` 하기:

```python
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator


class UserModel(BaseModel):
    name: str
    id: int

    @field_validator("name")
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    # NOTE: you can select multiple fields, or use '*' to select all fields.
    @field_validator("id", "name")
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            # info.field_name is the name of the field being validated
            is_alphanumeric = v.replace(" ", "").isalnum()
            assert is_alphanumeric, f"{info.field_name} must be alphanumeric"
        return v


print(UserModel(name="John Doe", id=1))
try:
    UserModel(name="samuel", id=1)
except ValidationError as e:
    print(e)
try:
    UserModel(name="John Doe", id="abc")
except ValidationError as e:
    print(e)
try:
    UserModel(name="John Doe!", id=1)
except ValidationError as e:
    print(e)
```

```py
id=1 name='John Doe'
1 validation error for UserModel
name
  Value error, must contain a space [type=value_error, input_value='samuel', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/value_error
1 validation error for UserModel
id
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='abc', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing
1 validation error for UserModel
name
  Assertion failed, name must be alphanumeric [type=assertion_error, input_value='John Doe!', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/assertion_error
```

- `@field_validator` 아래에 `@classmethod` 를 사용하는 것이 좋습니다.
- 두 번째 인수는 유효성을 검사할 필드 값입니다. 원하는대로 이름을 지을 수 있습니다
- 세 번째 인수가 있는 경우 `pydantic.ValidationInfo` 의 인스턴스입니다.
- 유효성 검사기는 구문 분석된 값을 반환하거나 `ValueError` 또는 `AssertionError`를 발생시켜야 합니다(`assert` 문을 사용할 수 있음).
- 여러 필드 이름을 전달하여 단일 유효성 검사기를 여러 필드에 적용할 수 있습니다.
- 특수 값 `"*"`을 전달하여 모든 필드에서 단일 유효성 검사기를 호출할 수도 있습니다.

`@field_validator` 내부의 다른 필드 값에 액세스하려는 경우 필드 이름과 필드 값의 사전인 `ValidationInfo.data`를 사용하여 가능할 수 있습니다.
유효성 검사는 정의된 주문 필드에서 수행되므로 아직 유효성 검사/채워지지 않은 필드에 액세스하지 않도록 `ValidationInfo.data`를 사용할 때 주의해야 합니다.
예를 들어 위 `name_must_contain_space` 내에서 `info.data['id']` 코드에서는 액세스할 수 없습니다.
그러나 여러 필드 값을 사용하여 유효성 검사를 수행하려는 대부분의 경우 아래 섹션에서 설명하는 `@model_validator`를 사용하는 것이 좋습니다.

## Model validators

```python
from typing import Any

from typing_extensions import Self

from pydantic import BaseModel, ValidationError, model_validator


class UserModel(BaseModel):
    username: str
    password1: str
    password2: str

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert "card_number" not in data, "card_number should not be included"
        return data

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


print(UserModel(username="scolvin", password1="zxcvbn", password2="zxcvbn"))

try:
    UserModel(username="scolvin", password1="zxcvbn", password2="zxcvbn2")
except ValidationError as e:
    print(e)

try:
    UserModel(
        username="scolvin",
        password1="zxcvbn",
        password2="zxcvbn",
        card_number="1234",
    )
except ValidationError as e:
    print(e)
```

```py
username='scolvin' password1='zxcvbn' password2='zxcvbn'
1 validation error for UserModel
  Value error, passwords do not match [type=value_error, input_value={'username': 'scolvin', '... 'password2': 'zxcvbn2'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.8/v/value_error
1 validation error for UserModel
  Assertion failed, card_number should not be included [type=assertion_error, input_value={'username': 'scolvin', '..., 'card_number': '1234'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.8/v/assertion_error
```

> [!NOTE] On return type checking  
> `@model_validator` 로 장식된 메서드는 메서드 끝에서 자체 인스턴스를 반환해야 합니다.  
> 유형 확인 목적으로, 데코레이팅된 메소드의 반환 유형으로 타이핑이나 타이핑\_확장 백포트에서 `self`를 사용할 수 있습니다.  
> 위 예의 맥락에서 `def check_passwords_match(self: 'UserModel)' -> 'UserModel'`을 사용하여 메서드가 모델의 인스턴스를 반환함을 나타낼 수도 있습니다.

> [!NOTE] On Inheritance  
> 기본 클래스에 정의된 `@model_validator`는 하위 클래스 인스턴스의 유효성 검사 중에 호출됩니다.
> 하위 클래스에서 `@model_validator` 를 재정의하면 기본 클래스의 `@model_validator가` 재정의되므로 해당 `@model_validator`의 하위 클래스 버전만 호출됩니다.

모델 유효성 검사기는 `mode='before'`, `mode='after'` 또는 `mode='wrap'`일 수 있습니다.

`mode='before'`:

- 모델 유효성 검사기에 원시 입력이 전달되기 전에는 종종 `dict[str, Any]`이지만 모델 자체의 인스턴스(예: `UserModel.model_validate(UserModel.construct(...))`가 호출되는 경우) 또는 다른 것일 수도 있습니다. 왜냐하면 임의의 객체를 `model_validate`에 전달할 수 있기 때문입니다.
- 유효성 검사기는 매우 유연하고 강력하지만 번거롭고 구현 시 오류가 발생하기 쉽습니다.
- 모델 유효성 검사기 이전에는 클래스 메서드가 있어야 합니다.
- 첫 번째 인수는 `cls`여야 합니다(또한 적절한 유형 검사를 위해 `@model_validator` 아래에 `@classmethod`를 사용하는 것이 좋습니다).
- 두 번째 인수는 입력이 되며(일반적으로 `Any`로 입력하고 `isinstance`를 사용하여 유형 범위를 좁혀야 함).
- 세 번째 인수(있는 경우)는 `pydantic.ValidationInfo` 가 됩니다.

`mode='after'`:

- 유효성 검사기는 인스턴스 메서드이며 항상 모델의 인스턴스를 첫 번째 인수로 받습니다. 유효성 검사기가 끝나면 인스턴스를 반환해야 합니다.
- `(cls, ModelType)`을 서명으로 사용하면 안 됩니다. 대신 `(self)`를 사용하고 유형 검사기가 `self` 유형을 추론하도록 하십시오.
- 이는 완전히 유형에 안전하기 때문에 `mode='before'` 유효성 검사기보다 구현하기가 더 쉬운 경우가 많습니다.
- 필드가 유효성 검사에 실패하면 해당 필드에 대한 `mode='after'` 유효성 검사기가 호출되지 않습니다.

## Handling errors in validators

이전 섹션에서 언급했듯이 유효성 검사가 실패했음을 나타내기 위해 유효성 검사기 내에서 `ValueError` 또는 `AssertionError`(`assert` ... 문으로 생성된 오류 포함)를 발생시킬 수 있습니다.
좀 더 장황하지만 추가적인 유연성을 제공하는 `PydanticCustomError` 를 발생시킬 수도 있습니다.
다른 오류(`TypeError`포함)는 버블링되며`ValidationError`로 래핑되지 않습니다.

```python
from pydantic_core import PydanticCustomError

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    x: int

    @field_validator("x")
    @classmethod
    def validate_x(cls, v: int) -> int:
        if v % 42 == 0:
            raise PydanticCustomError(
                "the_answer_error",
                "{number} is the answer!",
                {"number": v},
            )
        return v


try:
    Model(x=42 * 2)
except ValidationError as e:
    print(e)
```

```py
1 validation error for Model
x
  84 is the answer! [type=the_answer_error, input_value=84, input_type=int]
```

## Special Types

Pass.

## Field checks

## Dataclass validators

`Pydantic.dataclass` 에서도 작동합니다:

```python
from pydantic import field_validator
from pydantic.dataclasses import dataclass


@dataclass
class DemoDataclass:
    product_id: str  # should be a five-digit string, may have leading zeros

    @field_validator("product_id", mode="before")
    @classmethod
    def convert_int_serial(cls, v):
        if isinstance(v, int):
            v = str(v).zfill(5)
        return v


demo = DemoDataclass(product_id="01234")
assert demo.product_id == "01234"
demo = DemoDataclass(product_id=2468)
assert demo.product_id == "02468"  # Refer to convert_in_serial.
```

## Validation Context

`info` 인수에서 장식된 유효성 검사기 함수에 액세스할 수 있는 유효성 검사 메서드에 컨텍스트 개체를 전달할 수 있습니다:

```python
from pydantic import BaseModel, ValidationInfo, field_validator


class Model(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def remove_stopwords(cls, v: str, info: ValidationInfo):
        context = info.context
        if context:
            stopwords = context.get("stopwords", set())
            v = " ".join(w for w in v.split() if w.lower() not in stopwords)
        return v


data = {"text": "This is an example document"}

m = Model.model_validate(data)
assert m.text == "This is an example document"

m = Model.model_validate(data, context={"stopwords": ["this", "is", "an"]})
assert m.text == "example document"

m = Model.model_validate(data, context={"stopwords": ["document"]})
assert m.text == "This is an example"
```

이는 런타임 중에 유효성 검사 동작을 동적으로 업데이트해야 할 때 유용합니다.  
예를 들어 필드에 동적으로 제어 가능한 허용 값 집합이 포함되도록 하려면 컨텍스트별로 허용 값을 전달하고 허용 값을 업데이트하기 위한 별도의 메커니즘을 사용하면 됩니다.

```python
from typing import Any, Dict, List

from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    field_validator,
)

_allowed_choices = ["a", "b", "c"]


def set_allowed_choices(allowed_choices: List[str]) -> None:
    global _allowed_choices
    _allowed_choices = allowed_choices


def get_context() -> Dict[str, Any]:
    return {"allowed_choices": _allowed_choices}


class Model(BaseModel):
    choice: str

    @field_validator("choice")
    @classmethod
    def validate_choice(cls, v: str, info: ValidationInfo):
        allowed_choices = info.context.get("allowed_choices")
        if allowed_choices and v not in allowed_choices:
            raise ValueError(f"choice must be one of {allowed_choices}")
        return v


print(Model.model_validate({"choice": "a"}, context=get_context()))

try:
    print(Model.model_validate({"choice": "d"}, context=get_context()))
except ValidationError as exc:
    print(exc)

set_allowed_choices(["b", "c"])
try:
    print(Model.model_validate({"choice": "a"}, context=get_context()))
except ValidationError as exc:
    print(exc)
```

```py
choice='a'
1 validation error for Model
choice
  Value error, choice must be one of ['a', 'b', 'c'] [type=value_error, input_value='d', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/value_error
1 validation error for Model
choice
  Value error, choice must be one of ['b', 'c'] [type=value_error, input_value='a', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/value_error
```

마찬가지로 [Serialization Context](https://docs.pydantic.dev/latest/concepts/serialization/#serialization-context)를 사용할 수 있습니다.

### Using validation context with `BaseModel` initialization

표준 `BaseModel` 이니셜라이저에서 컨텍스트를 지정할 수 있는 방법은 없지만 `contextvars.ContextVar` 및 사용자 정의 `__init__` 메서드를 사용하여 이 문제를 해결할 수 있습니다.

```python
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator

from pydantic import BaseModel, ValidationInfo, field_validator

_init_context_var = ContextVar("_init_context_var", default=None)


@contextmanager
def init_context(value: Dict[str, Any]) -> Iterator[None]:
    token = _init_context_var.set(value)
    try:
        yield
    finally:
        _init_context_var.reset(token)


class Model(BaseModel):
    my_number: int

    def __init__(self, /, **data: Any) -> None:
        self.__pydantic_validator__.validate_python(
            data,
            self_instance=self,
            context=_init_context_var.get(),
        )

    @field_validator("my_number")
    @classmethod
    def multiply_with_context(cls, value: int, info: ValidationInfo) -> int:
        if info.context:
            multiplier = info.context.get("multiplier", 1)
            value = value * multiplier
        return value


m = Model(my_number=2)
assert m.my_number == 2
with init_context({"multiplier": 3}):
    m = Model(my_number=2)
    assert m.my_number == 6
m = Model(my_number=2)
assert m.my_number == 2
```

## Reusing Validators

때로는 여러 필드/모델에서 동일한 유효성 검사기를 사용하고 싶을 수도 있습니다(예: 일부 입력 데이터를 정규화하기 위해).
"순진한" 접근 방식은 별도의 함수를 작성한 다음 여러 데코레이터에서 호출하는 것입니다.
분명히 이것은 많은 반복과 상용구 코드를 수반합니다.
다음 접근 방식은 중복성을 최소화하고 모델이 다시 거의 선언적이 되도록 유효성 검사기를 재사용할 수 있는 방법을 보여줍니다:

```python
from pydantic import BaseModel, field_validator


def normalize(name: str) -> str:
    return " ".join((word.capitalize()) for word in name.split(" "))


class Producer(BaseModel):
    name: str

    _normalize_name = field_validator("name")(normalize)


class Consumer(BaseModel):
    name: str

    _normalize_name = field_validator("name")(normalize)


jane_doe = Producer(name="JaNe DOE")
assert jane_doe.name == "Jane Doe"
john_doe = Consumer(name="joHN dOe")
assert john_doe.name == "John Doe"
```
