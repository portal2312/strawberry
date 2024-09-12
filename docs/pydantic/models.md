# [Models](https://docs.pydantic.dev/latest/concepts/models)


## Basic model usage



```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "Jane Doe"


user = User(id="123")
assert user.id == 123
# NOTE: The id field value override string to int.
assert isinstance(user.id, int)
# NOTE: Check the name field default value.
assert user.name == "Jane Doe"
# NOTE: The name field is not initialized.
assert user.model_fields_set == {"id"}
# NOTE: The using model_dump function.
assert user.model_dump() == {"id": 123, "name": "Jane Doe"}
```

### Model methods and properties


#### model_validate



```python
user = User.model_validate({"id": "123"})
assert user.id == 123
# NOTE: The id field value override string to int.
assert isinstance(user.id, int)
# NOTE: Check the name field default value.
assert user.name == "Jane Doe"
# NOTE: The name field is not initialized.
assert user.model_fields_set == {"id"}
# NOTE: The using model_dump function.
assert user.model_dump() == {"id": 123, "name": "Jane Doe"}
```

## Nested models



```python
from typing import List, Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = "x"
    banana: str = "y"


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]


m = Spam(foo={"count": 4}, bars=[{"apple": "x1"}, {"apple": "x2"}])
print(m)
print(m.model_dump())
```

```py
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
{'foo': {'count': 4, 'size': None}, 'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}]}
```


## Rebuild model schema

모델 스키마는 `model_rebuild()`를 사용하여 다시 구축할 수 있습니다. 이는 **재귀적인 일반 모델**을 구축하는 데 유용합니다.



```python
from pydantic import BaseModel, PydanticUserError


class Foo(BaseModel):
    x: "Bar"


try:
    Foo.model_json_schema()
except PydanticUserError as e:
    print(e)


class Bar(BaseModel):
    pass


Foo.model_rebuild()
print(Foo.model_json_schema())
```

```py
{'$defs': {'Bar': {'properties': {}, 'title': 'Bar', 'type': 'object'}}, 'properties': {'x': {'$ref': '#/$defs/Bar'}}, 'required': ['x'], 'title': 'Foo', 'type': 'object'}
```


## Arbitrary class instances

To do this, set the config attribute `model_config['from_attributes'] = True`. See [`Model Config`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.from_attributes) and [`ConfigDict`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict) for more information.


### Reserved names

`pydantic.Field` 의 `alias` 사용하기.

`.model_dump(by_alias=True)` 사용하기.



```python
import typing


from pydantic import BaseModel, Field


class MyModel(BaseModel):
    metadata: typing.Dict[str, str] = Field(alias="metadata_")


# NOTE: The obj key field is Field.alias value.
my_model = MyModel.model_validate({"metadata_": {"fieldname": "value"}})
print(my_model.model_dump())
print(my_model.model_dump(by_alias=True))
```

```py
{'metadata': {'key': 'value'}}
{'metadata_': {'key': 'value'}}
```


### Nested attributes



```python
from typing import List

from pydantic import BaseModel, ConfigDict


class PetCls:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: List[PetCls]):
        self.name = name
        self.age = age
        self.pets = pets


class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    species: str


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: float = None
    pets: List[Pet]


bones = PetCls(name="Bones", species="dog")
orion = PetCls(name="Orion", species="cat")
anna = PersonCls(name="Anna", age=20, pets=[bones, orion])
anna_model = Person.model_validate(anna)
print(anna_model)
```

```py
name='Anna' age=20.0 pets=[Pet(name='Bones', species='dog'), Pet(name='Orion', species='cat')]
```


## Error handling

`pydantic.ValidationError` 사용하기.

자세한 내용은 [Error Handling](https://docs.pydantic.dev/latest/errors/errors/) 참조하기.



```python
from typing import List

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    list_of_ints: List[int]
    a_float: float


data = dict(
    list_of_ints=["1", 2, "bad"],
    a_float="not a float",
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
```

```py
2 validation errors for Model
list_of_ints.2
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing
a_float
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/float_parsing
```


## Validating data

Pydantic은 데이터 구문 분석을 위해 모델 클래스에 세 가지 방법을 제공합니다.

- `model_validate()`: 이는 키워드 인수 대신 사전이나 객체를 취한다는 점을 제외하면 모델의 `__init__` 메서드와 매우 유사합니다.
  전달된 객체의 유효성을 검사할 수 없거나 문제의 모델의 사전이나 인스턴스가 아닌 경우 `ValidationError`가 발생합니다.
- `model_validate_json()`: 이는 제공된 데이터를 JSON 문자열 또는 바이트열 객체로 검증합니다.
  수신 데이터가 JSON 페이로드 인 경우 일반적으로 데이터를 사전으로 수동으로 구문 분석하는 대신 더 빠른 것으로 간주됩니다.
  문서의 JSON 섹션에서 [JSON](https://docs.pydantic.dev/latest/concepts/json/) 구문 분석에 대해 자세히 알아보세요.
- `model_validate_strings()`: 이는 문자열 키와 값이 포함된 사전(중첩 가능)을 취하고 해당 문자열이 올바른 유형으로 강제 변환될 수 있도록 JSON 모드에서 데이터의 유효성을 검사합니다.



```python
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Optional[datetime] = None


m = User.model_validate({"id": 123, "name": "James"})
print(m)
# > id=123 name='James' signup_ts=None

try:
    User.model_validate(["not", "a", "dict"])
except ValidationError as e:
    print(e)
    """
    1 validation error for User
      Input should be a valid dictionary or instance of User [type=model_type, input_value=['not', 'a', 'dict'], input_type=list]
    """

m = User.model_validate_json('{"id": 123, "name": "James"}')
print(m)
# > id=123 name='James' signup_ts=None

try:
    m = User.model_validate_json('{"id": 123, "name": 123}')
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    name
      Input should be a valid string [type=string_type, input_value=123, input_type=int]
    """

try:
    m = User.model_validate_json("invalid JSON")
except ValidationError as e:
    print(e)
    """
    1 validation error for User
      Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='invalid JSON', input_type=str]
    """

m = User.model_validate_strings({"id": "123", "name": "James"})
print(m)
# > id=123 name='James' signup_ts=None

m = User.model_validate_strings(
    {"id": "123", "name": "James", "signup_ts": "2024-04-01T12:00:00"}
)
print(m)
# > id=123 name='James' signup_ts=datetime.datetime(2024, 4, 1, 12, 0)

try:
    m = User.model_validate_strings(
        {"id": "123", "name": "James", "signup_ts": "2024-04-01"}, strict=True
    )
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    signup_ts
      Input should be a valid datetime, invalid datetime separator, expected `T`, `t`, `_` or space [type=datetime_parsing, input_value='2024-04-01', input_type=str]
    """
```

JSON 이외의 형식으로 직렬화된 데이터의 유효성을 검사하려면 데이터를 직접 사전에 로드한 다음 `model_validate` 에 전달해야 합니다.

> [!NOTE]
> 관련된 유형 및 모델 구성에 따라 `model_validate` 및 `model_validate_json` 의 유효성 검사 동작이 다를 수 있습니다.
> JSON 이 아닌 소스에서 오는 데이터가 있지만 `model_validate_json` 에서 얻을 수 있는 것과 동일한 유효성 검사 동작 및 오류를 원하는 경우 현재로서는 `model_validate_json(json.dumps(data))`을 사용하거나 다음과 같은 경우 `model_validate_strings`를 사용하는 것이 좋습니다.
> 데이터는 문자열 키와 값이 포함된 (중첩될 수 있는) 사전의 형태를 취합니다.

> [!NOTE]
> 모델 인스턴스를 `model_validate`에 전달하는 경우 모델 구성에서 `revalidate_instances` 설정을 고려하는 것이 좋습니다.
> 이 값을 설정하지 않으면 모델 인스턴스에서 유효성 검사를 건너뜁니다. 아래 예를 참조하세요.


`revalidate_instances="never"`:



```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int


m = Model(a=0)
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = "not an int"

# doesn't raise a validation error even though m is invalid
m2 = Model.model_validate(m)
```

`revalidate_instances="always"`:



```python
from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    a: int

    model_config = ConfigDict(revalidate_instances="always")


m = Model(a=0)
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = "not an int"

try:
    m2 = Model.model_validate(m)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    a
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an int', input_type=str]
    """
```

    1 validation error for Model
    a
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an int', input_type=str]
        For further information visit https://errors.pydantic.dev/2.8/v/int_parsing


### Creating models without validation

Pydantic 은 검증 없이 모델을 생성할 수 있는 `model_construct()` 메서드도 제공합니다.  
이는 최소한 몇 가지 경우에 유용할 수 있습니다:

- 이미 유효한 것으로 알려진 복잡한 데이터로 작업할 때 (성능상의 이유로).
- 하나 이상의 유효성 검사기 함수가 멱등성이 아닌 경우.
- 하나 이상의 유효성 검사기 기능에 트리거되고 싶지 않은 부작용이 있는 경우.

> [!WARN] > `model_construct()` 는 유효성 검사를 수행하지 않습니다.
> 이는 유효하지 않은 모델을 생성할 수 있음을 의미합니다.
> 이미 검증되었거나 확실히 신뢰할 수 있는 데이터에만 `model_construct()` 메서드를 사용해야 합니다.

> [!NOTE]
> Pydantic V2에서는 검증(직접 인스턴스화 또는 `model_validate*` 메소드 사용)과 `model_construct()` 사이의 성능 격차가 상당히 줄어들었습니다.
> 단순한 모델의 경우 검증을 수행하는 것이 더 빠를 수 있습니다.
> 성능상의 이유로 `model_construct()`를 사용하는 경우, 실제로 더 빠르다고 가정하기 전에 사용 사례를 프로파일링할 수 있습니다.

자세한 내용은 [이 곳](https://docs.pydantic.dev/latest/concepts/models/#validating-data)을 참조바랍니다.


## Generic models

Pass.


## Dynamic model creation

Pass.


## RootModel and custom root types

Pass.


## Faux immutability

Pass.


## Abstract base classes



```python
import abc

from pydantic import BaseModel


class FooBarModel(BaseModel, abc.ABC):
    a: str
    b: int

    @abc.abstractmethod
    def my_abstract_method(self):
        pass
```

## Field ordering

Read.


## Required fields



```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    a: int
    b: int = ...  # NOTE: Not supported mypy.
    c: int = Field(..., alias="C")


model = Model.model_validate(dict(a=1, b=2, C=3))
print(model)
print(model.model_dump())
print(model.model_dump(by_alias=True))
```

```py
a=1 b=2 c=3
{'a': 1, 'b': 2, 'c': 3}
{'a': 1, 'b': 2, 'C': 3}
```


## Fields with non-hashable default values



```python
from typing import Dict, List

from pydantic import BaseModel


class Model(BaseModel):
    item_counts: List[Dict[str, int]] = [{}]


m1 = Model()
m1.item_counts[0]["a"] = 1
print(m1.item_counts)
m2 = Model()
print(m2.item_counts)
```

```py
[{'a': 1}]
[{}]
```


## Fields with dynamic default values

`pydantic.Field.default_factory` 사용하기



```python
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=datetime_now)


m1 = Model()
m2 = Model()
assert m1.uid != m2.uid
```

자세한 내용은 [`Field` function](https://docs.pydantic.dev/latest/concepts/fields/) 참조하기.


## Automatically excluded attributes

### Class vars

`typing.ClassVar` 사용 시, 처리는 하지만 들어나지 않는다.



```python
from typing import ClassVar

from pydantic import BaseModel


class Model(BaseModel):
    x: int = 2
    y: ClassVar[int] = 1


m = Model()
print(m)
print(Model.y)
print(m.model_dump())
```

```py
x=2
1
```


### Private model attributes

- 속성은 `undercore` 를 명은 앞에 사용하여 정의하기.
- 속성은 `pydantic.PrivateAttr` 를 사용하여 정의하기.
- 속성은 `__init__`, `model_validate` 안에 정의하지 않는 경우, 다른 속성과 함께 사용되지 않는다.
- `__attr__` 과 같음 이름은 지원하지 않는다.



```python
from datetime import datetime
from random import randint

from pydantic import BaseModel, PrivateAttr


class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str

    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self._secret_value = randint(1, 5)


m = TimeAwareModel()
print("m:", m)
print("m._processed_at:", m._processed_at)
print("m._secret_value:", m._secret_value)
print("m.model_validate({}):", m.model_validate({}))
```

```py
m:
m._processed_at: 2024-08-26 08:15:19.787157
m._secret_value: 1
m.model_validate({}):
```


## Data conversion

데이터가 손실 될 수 있지만, 의도적인 것이다. 자세한 것 내용은 [이 곳](https://github.com/pydantic/pydantic/issues/578)을 참조하기.

또는 [엄격한 모드](https://docs.pydantic.dev/latest/concepts/strict_mode/) 참조하기.



```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int
    b: float
    c: str


print(Model(a=3.000, b="2.72", c=b"binary data").model_dump())
```

```py
{'a': 3, 'b': 2.72, 'c': 'binary data'}
```


## Model signature



```python
import inspect

from pydantic import BaseModel, Field


class FooModel(BaseModel):
    id: int
    name: str = None
    description: str = "Foo"
    apple: int = Field(alias="pear")


print(inspect.signature(FooModel))
```

```py
(*, id: int, name: str = None, description: str = 'Foo', pear: int) -> None
```


`__init__` 도 존중한다:



```python
import inspect

from pydantic import BaseModel, create_model


class MyModel(BaseModel):
    id: int
    info: str = "Foo"

    def __init__(self, id: int = 1, *, bar: str, **data) -> None:
        """My custom init!"""
        super().__init__(id=id, bar=bar, **data)


print(inspect.signature(MyModel))
```

```py
(id: int = 1, *, bar: str, info: str = 'Foo') -> None
```


필드의 별칭과 이름이 모두 유효한 식별자가 아닌 경우(`create_model` 의 이국적인 사용을 통해 가능할 수 있음) `**data` 인수가 추가됩니다.
또한, `model_config['extra'] == 'allow'`인 경우 `**data` 인수는 서명에 항상 존재합니다.



```python
import inspect

from pydantic import BaseModel, ConfigDict, create_model


class MyModel(BaseModel):
    id: int
    info: str = "Foo"

    # NOTE: Allow extra for model config.
    model_config = ConfigDict(extra="allow")

    def __init__(self, id: int = 1, *, bar: str, **data) -> None:
        """My custom init!"""
        super().__init__(id=id, bar=bar, **data)


print(inspect.signature(MyModel))
print(MyModel(id=1, info="foo", **{"bar": "bar"}))
DymaicModel = create_model(
    "You",
    id=(int, 1),
    bar=(str, ...),
    info=(str, "Foo"),
    __config__=ConfigDict(extra="allow"),
)
print(inspect.signature(DymaicModel))
print(DymaicModel(id=1, info="foo", **{"bar": "bar"}))
```

```py
(id: int = 1, *, bar: str, info: str = 'Foo', **data) -> None
id=1 info='foo' bar='bar'
(*, id: int = 1, bar: str, info: str = 'Foo', **extra_data: Any) -> None
id=1 bar='bar' info='foo'
```


## Structural pattern matching



```python
from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    species: str


a = Pet(name="Bones", species="dog")

match a:
    # match `species` to 'dog', declare and initialize `dog_name`
    case Pet(species="dog", name=dog_name):
        print(f"{dog_name} is a dog")
    # > Bones is a dog
    # default case
    case _:
        print("No dog matched")
```

## Attribute copies



```python
from typing import List

from pydantic import BaseModel


class C1:
    arr = []

    def __init__(self, in_arr):
        self.arr = in_arr


class C2(BaseModel):
    arr: List[int]


arr_orig = [1, 9, 10, 3]


c1 = C1(arr_orig)
c2 = C2(arr=arr_orig)
assert id(c1.arr) != id(c2.arr)
arr_orig.append(0)
assert c1.arr[-1] == 0
assert c2.arr[-1] == 3
```

## Extra fields

정의 되지 않은 속성에 값 추가 시, 일반적으로 무시 된다:



```python
from pydantic import BaseModel


class Model(BaseModel):
    x: int


m = Model(x=1, y="a")
assert m.model_dump() == {"x": 1}
```

만약 정의 되지 않은 속성에 값을 추가 시 오류를 발생하려면, `pydantic.ConfigDict` 에 `extra="forbid"` 사용한다:



```python
from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    x: int

    model_config = ConfigDict(extra="forbid")


try:
    Model(x=1, y="a")
except ValidationError as exc:
    print(exc)
```

```py
1 validation error for Model
y
  Extra inputs are not permitted [type=extra_forbidden, input_value='a', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/extra_forbidden

```


`pydantic.ConfigDict` 에 `extra="allow"` 사용 시, `__pydantic_extra__` 저장 된다:



```python
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    x: int

    model_config = ConfigDict(extra="allow")


m = Model(x=1, y="a")
assert m.__pydantic_extra__ == {"y": "a"}
```

기본적으로 이러한 추가 항목에는 유효성 검사가 적용되지 않는다.  
그러나 `__pydantic_extra__` 에 대한 유형 주석을 재정의하여 값에 대한 유형을 설정할 수 있습니다:



```python
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Model(BaseModel):
    __pydantic_extra__: Dict[str, int] = Field(init=False)

    x: int

    model_config = ConfigDict(extra="allow")


try:
    Model(x=1, y="a")
except ValidationError as exc:
    print(exc)

m = Model(x=1, y="2")
assert m.x == 1
assert m.y == 2
assert m.model_dump() == {"x": 1, "y": 2}
assert m.__pydantic_extra__ == {"y": 2}
```

```py
1 validation error for Model
y
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing

```

`TypedDict` 및 `dataclass` 에는 동일한 구성이 적용됩니다.  
단, 구성은 클래스의 `__pydantic_config__` 속성을 유효한 `ConfigDict` 로 설정하여 제어됩니다.

