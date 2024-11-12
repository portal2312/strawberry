# [Pydantic support](https://strawberry.rocks/docs/integrations/pydantic)

`strawberry.experimental.pydantic.type` decorator 사용하기.

```python
import strawberry

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto
    friends: strawberry.auto
```

`strawberry.experimental.pydantic.type` decorator 는 `User` 과 감싸진 `User` 가 포함한 dataclass style 의 `strawberry.auto` 를 type annotation 로 한 fields 를 접근합니다.

모든 필드를 적용하려면, `strawberry.experimental.pydantic.type` decorator 안에 `all_fields=True` 를 합니다.

> [!WARN] 의도하지 않은 field 접근을 주의하십시오.

```python
import strawberry

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType: ...
```

## Input types

`strawberry.experimental.pydantic.input` decorator 를 사용하세요:

```python
import strawberry


@strawberry.experimental.pydantic.input(model=User)
class UserInput:
    id: strawberry.auto
    name: strawberry.auto
    friends: strawberry.auto
```

## Interface types

`strawberry.experimental.pydantic.interface` decorator 를 사용하세요:

```python
import strawberry
from pydantic import BaseModel
from typing import List


# pydantic types
class User(BaseModel):
    id: int
    name: str


class NormalUser(User):
    friends: List[int] = []


class AdminUser(User):
    role: int


# strawberry types
@strawberry.experimental.pydantic.interface(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto


@strawberry.experimental.pydantic.type(model=NormalUser)
class NormalUserType(UserType):  # note the base class
    friends: strawberry.auto


@strawberry.experimental.pydantic.type(model=AdminUser)
class AdminUserType(UserType):
    role: strawberry.auto
```

## Error Types

```python
from pydantic import BaseModel, ValidationError, constr
import strawberry


class User(BaseModel):
    id: int
    name: constr(min_length=2)
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


@strawberry.experimental.pydantic.error_type(model=User)
class UserError:
    id: strawberry.auto
    name: strawberry.auto
    friends: strawberry.auto


try:
    User(id="a", name="n")
except ValidationError as e:
    for error in e.errors():
        print(error)
    user_error = UserError(e)
    print(user_error)
```

## Extending types

Pydantic model 에 정의되지 않은 필드를 Strawberry 문법을 사용하여 `UserType` 에 `age` 를 추가 가능합니다:

```python
import strawberry
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto
    age: int
```

## Converting types

생성된 유형은 어떠한 단순한 검증도 실행하지 않습니다.
이는 유형을 확장할 때 혼란을 방지하고 필요한 곳에서 정확하게 유효성 검사를 실행할 수 있도록 하기 위한 것입니다.

Pydantic instance 를 Strawberry instance 로 변환하려면 Strawberry 유형에서 `from_pydantic` 을 사용할 수 있습니다:

```python
import strawberry
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto


instance = User(id="123", name="Jake")
data = UserType.from_pydantic(instance)
```

Strawberry 유형에 Pydantic 모델에 정의되지 않은 추가 필드가 포함된 경우 `from_pydantic` 의 `extra` 매개변수를 사용하여 해당 필드에 할당할 값을 지정해야 합니다:

```python
import strawberry
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto
    age: int  # extra age


instance = User(id="123", name="Jake")
data = UserType.from_pydantic(instance, extra={"age": 10})
```

데이터 사전 구조는 데이터 구조를 따릅니다.
`User` 목록이 있는 경우 데이터가 누락된 `User` 목록인 추가 항목(이 경우 `age`)을 보내야 합니다.

Strawberry instance 를 Pydantic instance 로 변환하고 유효성 검사를 촉발하려면 Strawberry instance 에서 `to_pydantic`을 사용할 수 있습니다:

```python
import strawberry
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


@strawberry.experimental.pydantic.input(model=User)
class UserInput:
    id: strawberry.auto
    name: strawberry.auto


input_data = UserInput(id="abc", name="Jake")
try:
    instance = input_data.to_pydantic()
except ValidationError as e:
    print(e)
```

```python
1 validation error for User
id
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='abc', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/int_parsing
```

## Constrained types

[`Pydantic constrained types`](https://pydantic-docs.helpmanual.io/usage/types/#constrained-types) 를 지원합니다.
graphql 유형에는 제약 조건이 적용되지 않습니다.
따라서 유효성 검사가 시행되도록 항상 pydantic 유형으로 작업하는 것이 좋습니다.

```python
from pydantic import BaseModel, conlist
import strawberry


class Example(BaseModel):
    friends: conlist(str, min_length=1)


@strawberry.experimental.pydantic.input(model=Example, all_fields=True)
class ExampleGQL: ...


@strawberry.type
class Query:
    @strawberry.field()
    def test(self, example: ExampleGQL) -> None:
        # friends may be an empty list here
        print(example.friends)
        # calling to_pydantic() runs the validation and raises
        # an error if friends is empty
        print(example.to_pydantic().friends)


schema = strawberry.Schema(query=Query)
```

## Classes with `__get_validators__`

아마 Pydantic BaseModels 에 `__get_validators__` 로직과 함게 사용자 정의 type 이 정의되어 있을 것입니다. Schema class 안에 `scalar_overrides` 인자에 scalar type 과 관계 추가가 필요할 것입니다:

```python
import strawberry
from pydantic import BaseModel


class MyCustomType:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return MyCustomType()


class Example(BaseModel):
    custom: MyCustomType


@strawberry.experimental.pydantic.type(model=Example, all_fields=True)
class ExampleGQL: ...


MyScalarType = strawberry.scalar(
    MyCustomType,
    # or another function describing how to represent MyCustomType in the response
    serialize=str,
    parse_value=lambda v: MyCustomType(),
)


@strawberry.type
class Query:
    @strawberry.field()
    def test(self) -> ExampleGQL:
        return Example(custom=MyCustomType())


# Tells strawberry to convert MyCustomType into MyScalarType
schema = strawberry.Schema(query=Query, scalar_overrides={MyCustomType: MyScalarType})
```

## Custom Conversion Logic

때로는 라이브러리에 제공된 로직을 사용하여 Pydantic 모델을 Strawberry로 변환하고 싶지 않을 수도 있습니다. 때때로 Pydantic의 유형은 GraphQL에서 표현할 수 없거나(예: 스칼라 값의 결합) 데이터가 스키마에 노출되기 전에 구조적 변경이 필요합니다. 이러한 경우 변환 논리를 보다 직접적으로 제어하는 ​​데 사용할 수 있는 두 가지 방법이 있습니다.

### 필드 유형에 대한 Strawberry 모델의 다른 유형 주석 사용

`strawberry.auto` 를 사용하여 동등한 유형을 선택하는 대신 필드 유형에 대한 Strawberry 모델의 다른 유형 주석을 사용할 수 있습니다.  
값을 사용자 정의 scalar 유형으로 변환하거나 기본 유형 간 변환과 같은 작업을 수행할 수 있습니다.  
Strawberry는 필드 값을 입력으로 사용하여 새 유형 주석의 생성자를 호출하므로 이는 생성자를 통해 변환이 가능한 경우에만 작동합니다:

```python
import base64
import strawberry
from pydantic import BaseModel
from typing import Union, NewType


class User(BaseModel):
    id: Union[int, str]  # Not representable in GraphQL
    hash: bytes


Base64 = strawberry.scalar(
    NewType("Base64", bytes),
    serialize=lambda v: base64.b64encode(v).decode("utf-8"),
    parse_value=lambda v: base64.b64decode(v.encode("utf-8")),
)


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: str  # Serialize int values to strings
    hash: Base64  # Use a custom scalar to serialize values


@strawberry.type
class Query:
    @strawberry.field
    def test() -> UserType:
        return UserType.from_pydantic(User(id=123, hash=b"abcd"))


schema = strawberry.Schema(query=Query)

print(schema.execute_sync("query { test { id, hash } }").data)
# {"test": {"id": "123", "hash": "YWJjZA=="}}
```

### `from_pydantic` 및 `to_pydantic` 의 사용자 정의 구현

변환 논리를 수정하는 보다 포괄적인 다른 방법은 `from_pydantic` 및 `to_pydantic` 의 사용자 정의 구현을 제공하는 것입니다. 이를 통해 변환 프로세스를 완전히 제어할 수 있으며 Strawberry에 내장된 변환 규칙을 완전히 무시하는 동시에 새로운 유형을 Pydantic 변환 유형으로 등록하여 다른 모델에서 참조할 수 있습니다.

이는 기본 Pydantic 모델을 변경하지 않고 GraphQL 표준과 매우 다른 구조를 표현해야 할 때 유용합니다. 예를 들어 `dict` 필드를 사용하여 일부 반구조화된 콘텐츠를 저장하는 사용 사례가 있는데, 이는 GraphQL의 엄격한 유형 시스템에서 표현하기 어렵습니다.

```python
import enum
import dataclasses
import strawberry
from pydantic import BaseModel
from typing import Any, Dict, Optional


class ContentType(enum.Enum):
    NAME = "name"
    DESCRIPTION = "description"


class User(BaseModel):
    id: str
    content: Dict[ContentType, str]


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    # Flatten the content dict into specific fields in the query
    content_name: Optional[str] = None
    content_description: Optional[str] = None

    @staticmethod
    def from_pydantic(instance: User, extra: Dict[str, Any] = None) -> "UserType":
        data = instance.dict()
        content = data.pop("content")
        data.update({f"content_{k.value}": v for k, v in content.items()})
        return UserType(**data)

    def to_pydantic(self) -> User:
        data = dataclasses.asdict(self)

        # Pull out the content_* fields into a dict
        content = {}
        for enum_member in ContentType:
            key = f"content_{enum_member.value}"
            if data.get(key) is not None:
                content[enum_member.value] = data.pop(key)
        return User(content=content, **data)


user = User(id="abc", content={ContentType.NAME: "Bob"})
print(UserType.from_pydantic(user))
user_type = UserType(id="abc", content_name="Bob", content_description=None)
print(user_type.to_pydantic())
```

```python
UserType(content_name='Bob', content_description=None, id='abc')
id='abc' content={<ContentType.NAME: 'name'>: 'Bob'}
```
