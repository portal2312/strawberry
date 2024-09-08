# [Fields](https://docs.pydantic.dev/latest/concepts/fields/)

`Field` function 은 모델 필드에 메타데이터를 사용자 정의하고 추가하는 데 사용됩니다.

## Default values

`default`: 기본 값 정의하기.

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(default="John Doe")


user = User()
assert user.name == "John Doe"
```

`default_factory`: 기본 값을 생성하기 위해 호출될 콜러블을 정의할 수도 있습니다.

```python
from uuid import uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

> [!INFO] `default` 및 `default_factory` 매개변수는 상호 배타적입니다.

> [!NOTE] `typing.Optional` 을 사용한다고 해서 필드의 기본 값이 `None` 이라는 의미는 아닙니다.

## Using Annotated

`Field` 기능은 `Annotated` 와 함께 사용할 수도 있습니다.

```python
from uuid import uuid4

from typing_extensions import Annotated

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
```

> [!NOTE]  
> 기본 값은 `Annotated` 외부에서 할당된 값으로 설정하거나 `Annotated` 내부의 `Field.default_factory`를 사용하여 설정할 수 있습니다.  
> **`Field.default` 인수는 `Annotated` 내에서 지원되지 않습니다.**

## Field aliases

유효성 검사 및 직렬화를 위해 필드에 대한 별칭을 정의할 수 있습니다.

- `Field(..., alias='foo')`: Validation and Serialization
- `Field(..., validation_alias='foo')`: Validation
- `Field(..., serialization_alias='foo')`: Serialization

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., alias="username")


user = User(username="johndoe")
assert user.name == "johndoe"
assert user.model_dump(by_alias=True) == {"username": "johndoe"}
```

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., validation_alias="username")


user = User(username="johndoe")
assert user.name == "johndoe"
assert user.model_dump(by_alias=True) == {"name": "johndoe"}
```

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., serialization_alias="username")


user = User(name="johndoe")
assert user.name == "johndoe"
assert user.model_dump(by_alias=True) == {"username": "johndoe"}
```

> [!NOTE] **Alias precedence and priority**  
> `validation_alias` > `alias` > `serialization_alias` 우선 순위입니다.  
> [`Model Config`](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.alias_generator) 의 `alias_generator` 사용 시, 우선 순위를 정의할 수 있습니다.

> **VSCode and Pyright users**  
> `populate_by_name` 사용 시, 자세한 내용은 공식에서 참조하기.

자세한 내용은 [Alias](https://docs.pydantic.dev/latest/concepts/alias/) 참조하기.

## Numeric Constraints

- `gt`: greater than
- `lt`: less than
- `ge`: greater than or equal to
- `le`: less than or equal to
- `multiple_of`: - 배수
- `allow_inf_nan`: allow 'inf', '-inf', 'nan' values

```python
from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=2,
    love_for_pydantic=float("inf"),
)
print(foo)
foo.model_json_schema()
```

```py
positive=1 non_negative=0 negative=-1 non_positive=0 even=2 love_for_pydantic=inf
```

> [!INFO] JSON Schema
>
> JSON Schema:
>
> - `gt` and `lt`: `exclusiveMinimum` and `exclusiveMaximum`.
> - `ge` and `le`: `minimum` and `maximum`.
> - `multiple_of` `multipleOf`.

> [!WARN] Constraints on compound types  
> 오류를 피하기 위해 `Annotated` 사용하기:

```python
from typing import Optional

from typing_extensions import Annotated

from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: Optional[Annotated[int, Field(gt=0)]]
    # Can error in some cases, not recommended:
    non_negative: Optional[int] = Field(ge=0)
```

## String Constraints

문자열을 제한하는 데 사용할 수 있는 필드가 있습니다:

- `min_length`: 문자열의 최소 길이입니다.
- `max_length`: 문자열의 최대 길이입니다.
- `pattern`: 문자열이 일치해야 하는 정규식입니다.

```python
from pydantic import BaseModel, Field


class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r"^\d*$")


Foo(short="abc", long="0123456789", regex="123")
```

```py
Foo(short='abc', long='0123456789', regex='123')
```

## Decimal Constraints

- `max_digits`: 십진수 내 최대 자릿수입니다. 소수점 앞의 0이나 후행 소수점 0은 포함되지 않습니다.
- `decimal_places`: 허용되는 최대 소수 자릿수입니다. 후행 소수점 0은 포함되지 않습니다.

```python
from decimal import Decimal

from pydantic import BaseModel, Field


class Foo(BaseModel):
    precise: Decimal = Field(max_digits=5, decimal_places=2)


Foo(precise=Decimal("123.45"))
```

```py
Foo(precise=Decimal('123.45'))
```

## Dataclass Constraints

Pass.

## Validate Default Values

`pydantic.Field.validate_default`: 기본값을 검증해야 하는지 여부를 제어하기.

```python
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    age: int = Field(default="twelve", validate_default=True)


try:
    user = User()
except ValidationError as e:
    print(e)
```

```py
1 validation error for User
age
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='twelve', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing
```

## Field Representation

`pydantic.Field.repr`:

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    age: int = Field(repr=False)
    name: str = Field(repr=True)


User(name="John", age=42)
```

```py
User(name='John')
```

## Discriminator

매개변수 `discriminator` 는 공용체에서 서로 다른 모델을 구별하는 데 사용되는 필드를 제어하는 ​​데 사용할 수 있습니다.  
필드 이름이나 `Discriminator` 인스턴스 중 하나를 사용합니다.  
`Discriminator` 접근 방식은 판별자 필드가 `Union` 의 모든 모델에 대해 동일하지 않을 때 유용할 수 있습니다.

```python
from typing import Literal

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal["cat"]
    age: int


class Dog(BaseModel):
    pet_type: Literal["dog"]
    age: int


class Model(BaseModel):
    pet: Cat | Dog = Field(discriminator="pet_type")


cat = Model.model_validate({"pet": {"pet_type": "cat", "age": 12}})
print(repr(cat))
assert isinstance(cat.pet, Cat) is True
```

다음 예에서는 `Discriminator` 인스턴스와 함께 `discriminator` 키워드 인수를 사용하는 방법을 보여줍니다:

```python
from typing import Literal, Union

from typing_extensions import Annotated

from pydantic import BaseModel, Discriminator, Field, Tag


class Cat(BaseModel):
    pet_type: Literal["cat"]  # NOTE: pet_type or pet_kind.
    age: int


class Dog(BaseModel):
    pet_kind: Literal["dog"]  # NOTE: pet_type or pet_kind.
    age: int


def pet_discriminator(v):
    if isinstance(v, dict):
        return v.get("pet_type", v.get("pet_kind"))
    return getattr(v, "pet_type", getattr(v, "pet_kind", None))


class Model(BaseModel):
    pet: Union[Annotated[Cat, Tag("cat")], Annotated[Dog, Tag("dog")]] = Field(
        discriminator=Discriminator(pet_discriminator)
    )


cat = Model.model_validate({"pet": {"pet_type": "cat", "age": 12}})
assert isinstance(cat.pet, Cat) is True
dog = Model.model_validate({"pet": {"pet_kind": "dog", "age": 12}})
assert isinstance(dog.pet, Dog) is True
```

또한 `Annotated`를 활용하여 구별된 공용체를 정의할 수도 있습니다. 자세한 내용은 [Discriminate Unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions) 문서를 참조하세요.

## Strict Mode

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(strict=True)
    age: int = Field(strict=False)
    is_staff: bool = Field(strict=False)


user = User(name="John", age="42", is_staff=1)
assert isinstance(user.age, int) is True
assert isinstance(user.is_staff, int) is True
```

자세한 내용은 [Strict Mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) 을 참조하세요.

Pydantic 이 엄격 모드와 완화 모드 모두에서 데이터를 변환하는 방법에 대한 자세한 내용은 [변환 표](https://docs.pydantic.dev/latest/concepts/conversion_table/)를 참조하세요.

## Immutability

불변하기 위해, `pydantic.Field` 의 `frozen` 매개변수 사용합니다:

```python
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    name: str = Field(frozen=True)
    age: int


user = User(name="John", age=42)

try:
    user.name = "Jane"
except ValidationError as e:
    print(e)
```

```py
1 validation error for User
name
  Field is frozen [type=frozen_field, input_value='Jane', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/frozen_field
```

자세한 내용은 [frozen dataclass documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances) 참조하세요.

## Exclude

The `exclude` parameter:

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    age: int = Field(exclude=True)


user = User(name="John", age=42)
assert user.model_dump() == {"name": "John"}
```

자세한 내용은 [Serialization](https://docs.pydantic.dev/latest/concepts/serialization/#model-and-field-level-include-and-exclude) 을 참조하세요.

## Deprecated fields

### deprecated as a string

### deprecated via the warnings.deprecated decorator

### deprecated as a boolean

## Customizing JSON Schema

## The computed_field decorator

모델이나 데이터 클래스를 직렬화할 때 `computed_field` decorator 를 사용하여 `property` 또는 `cached_property` 속성을 포함할 수 있습니다.  
이는 다른 필드에서 계산되는 필드 또는 계산 비용이 많이 드는(그래서 캐시되는) 필드에 유용할 수 있습니다.

`@deprecated` 도 사용 가능합니다.

```python
from typing_extensions import deprecated

from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    def volume(self) -> float:
        return self.width * self.height * self.depth

    @computed_field
    @deprecated("'weight' is deprecated")
    def weight(self) -> float:
        return 0.0


box = Box(width=1, height=2, depth=3)
assert box.model_dump()["volume"] == 6.0
```
