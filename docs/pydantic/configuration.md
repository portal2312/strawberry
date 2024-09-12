# [Configuration](https://docs.pydantic.dev/latest/api/config)

Pydantic models 에 대한 설정입니다.


## ConfigDict

Bases: `TypedDict`

Pydantic 동작을 구성하기 위한 TypedDict 입니다.


### [validate_assignment](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_assignment) `instance-attribute`

```python
validate_assignment: bool
```

모델이 변경될 때 데이터의 유효성을 검사할지 여부입니다. 기본값은 `False` 입니다.

Pydantic의 기본 동작은 모델이 생성될 때 데이터를 검증하는 것입니다.

모델이 생성된 후 사용자가 데이터를 변경하는 경우 모델이 재검증되지 않습니다:



```python
from pydantic import BaseModel


class User(BaseModel):
    name: str


user = User(name="John Doe")
assert isinstance(user.name, str)

user.name = 123
assert isinstance(user.name, int)
```

데이터가 변경될 때 모델을 재검증하려는 경우에는 `verify_location=True`를 사용할 수 있습니다:



```python
from pydantic import BaseModel, ValidationError


class User(BaseModel, validate_assignment=True):
    name: str


user = User(name="John Doe")
assert isinstance(user.name, str)

try:
    user.name = 123
except ValidationError as e:
    for error in e.errors():
        match error["type"]:
            case "string_type":
                assert isinstance(error["input"], str) is False
            case _:
                continue
```

### [revalidate_instances](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.revalidate_instances) `instance-attribute`

```python
revalidate_instances: Literal[
    "always", "never", "subclass-instances"
]
```

검증 중에 모델과 데이터 클래스를 재검증하는 시기와 방법. `"never"`, `"always"` 및 `"subclass-instances"`의 문자열 값을 허용합니다. 기본값은 `"never"` 입니다:

- `"never"`: 검증 중에는 모델과 데이터 클래스를 재검증하지 않습니다.
- `"always"`: 검증 중에 모델과 데이터 클래스를 재검증합니다.
- `"subclass-instances"`: 인스턴스가 모델이나 데이터 클래스의 하위 클래스인 경우 유효성 검사 중에 모델과 데이터 클래스의 유효성을 다시 검사합니다.

기본적으로 모델 및 데이터 클래스 인스턴스는 검증 중에 재검증되지 않습니다:



```python
from typing import List

from pydantic import BaseModel


class User(BaseModel, revalidate_instances="never"):
    hobbies: List[str]


class SubUser(User):
    sins: List[str]


class Transaction(BaseModel):
    user: User


my_user = User(hobbies=["reading"])
t = Transaction(user=my_user)
assert isinstance(t.user, User)
assert isinstance(t.user.hobbies[0], str)

my_user.hobbies = [1]
t = Transaction(user=my_user)
assert isinstance(t.user, User)
assert isinstance(t.user.hobbies[0], str) is False

my_sub_user = SubUser(hobbies=["scuba diving"], sins=["lying"])
t = Transaction(user=my_sub_user)
assert isinstance(t.user, User)
assert hasattr(t.user, "hobbies")
assert isinstance(t.user, SubUser)
assert hasattr(t.user, "sins")
```

검증 중에 인스턴스를 재검증하려면 모델 구성에서 `revalidate_instances` 를 `"always"`로 설정할 수 있습니다:



```python
from typing import List

from pydantic import BaseModel, ValidationError


class User(BaseModel, revalidate_instances="always"):
    hobbies: List[str]


class SubUser(User):
    sins: List[str]


class Transaction(BaseModel):
    user: User


my_user = User(hobbies=["reading"])
t = Transaction(user=my_user)
assert isinstance(t.user, User)
assert isinstance(t.user.hobbies[0], str)

my_user.hobbies = [1]
try:
    Transaction(user=my_user)
except ValidationError as e:
    for error in e.errors():
        match error["type"]:
            case "string_type":
                assert error["loc"] == ("user", "hobbies", 0)
                assert isinstance(error["input"], str) is False
            case _:
                continue

my_sub_user = SubUser(hobbies=["scuba diving"], sins=["lying"])
t = Transaction(user=my_sub_user)
assert isinstance(t.user, User)
assert hasattr(t.user, "hobbies")
assert isinstance(t.user, SubUser) is False
assert hasattr(t.user, "sins") is False
```

모델의 하위 클래스 인스턴스만 재검증하기 위해 `revalidate_instances` 를 `"subclass-instances"`로 설정하는 것도 가능합니다:



```python
from typing import List

from pydantic import BaseModel


class User(BaseModel, revalidate_instances="subclass-instances"):
    hobbies: List[str]


class SubUser(User):
    sins: List[str]


class Transaction(BaseModel):
    user: User


my_user = User(hobbies=["reading"])
t = Transaction(user=my_user)
assert isinstance(t.user, User)
assert isinstance(t.user.hobbies[0], str)

my_user.hobbies = [1]
t = Transaction(user=my_user)
assert isinstance(t.user, User)
assert isinstance(t.user.hobbies[0], str) is False

my_sub_user = SubUser(hobbies=["scuba diving"], sins=["lying"])
t = Transaction(user=my_sub_user)
assert isinstance(t.user, User)
assert hasattr(t.user, "hobbies")
assert isinstance(t.user, SubUser) is False
assert hasattr(t.user, "sins") is False
```
