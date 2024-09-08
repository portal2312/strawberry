# Poetry

[Poetry](https://python-poetry.org/)는 Python의 종속성 관리 및 패키징을 위한 도구입니다. 이를 통해 프로젝트가 의존하는 라이브러리를 선언할 수 있으며 이를 관리(설치/업데이트)합니다. Poetry는 반복 가능한 설치를 보장하기 위해 잠금 파일을 제공하고 배포용 프로젝트를 구축할 수 있습니다.

Table of Contents:

- [Poetry](#poetry)
  - [Introduction](#introduction)
    - [Installation](#installation)
    - [Enable tab completion for Bash, Fish, or Zsh](#enable-tab-completion-for-bash-fish-or-zsh)
  - [Basic Usage](#basic-usage)
    - [Project setup](#project-setup)
      - [Setting a Python Version](#setting-a-python-version)
      - [Operating modes](#operating-modes)
      - [Specifying dependencies](#specifying-dependencies)
    - [Using your virtual environment](#using-your-virtual-environment)
      - [Using poetry run](#using-poetry-run)
      - [Activating the virtual environment](#activating-the-virtual-environment)
    - [Version constraints](#version-constraints)
    - [Installing dependencies](#installing-dependencies)
      - [Installing dependencies only](#installing-dependencies-only)
    - [Updating dependencies to their latest versions](#updating-dependencies-to-their-latest-versions)
  - [Managing dependencies](#managing-dependencies)
    - [Dependency groups](#dependency-groups)
      - [Optional groups](#optional-groups)
      - [Adding a dependency to a group](#adding-a-dependency-to-a-group)
      - [Installing group dependencies](#installing-group-dependencies)
      - [Removing dependencies from a group](#removing-dependencies-from-a-group)
    - [Synchronizing dependencies](#synchronizing-dependencies)
    - [Layering optional groups](#layering-optional-groups)
  - [The pyproject.toml file](#the-pyprojecttoml-file)
  - [Extras](#extras)

## Introduction

With [pipx](./pipx.md).

Refer to [Introduction](https://python-poetry.org/docs/).

### Installation

```bash
pipx install poetry
# pipx upgrade poetry
# pipx uninstall poetry
```

### Enable tab completion for Bash, Fish, or Zsh

Zsh:

```bash
poetry completions zsh > ~/.zfunc/_poetry
```

## Basic Usage

Refer to [Basic Usage](https://python-poetry.org/docs/basic-usage/).

### Project setup

`pyproject.toml` 기록됩니다.

#### Setting a Python Version

````toml
[tool.poetry.dependencies]
python = "^3.7.0"
``~/.zfunc/_poetry`

#### Initialising a pre-existing project

```bash
poetry init
````

Then, see `pyproject.toml`.

#### Operating modes

종속성 관리하고 패키징에는 사용하지 않으려면 비패키지 모드를 사용할 수 있습니다, `pyproject.toml`:

```toml
# ...

[tool.poetry]
package-mode = false
```

- `[tool.poetry]` 의 `name`, `version` 가 (필수에서) 옵션이 됩니다.
- 프로젝트 자체를 설치하려고 시도하지 않고 해당 종속성만 설치하려고 합니다.(`poetry install --no-root`와 동일).

#### Specifying dependencies

```bash
poetry add PACKAGE
```

`pyproject.toml`:

```toml
# ...

[tool.poetry.dependencies]
PACKAGE = "^0.1"
```

### Using your virtual environment

[pyenv](https://github.com/pyenv/pyenv) 를 사용하고 프로젝트 최상위 경로에 `.venv` 를 만들어 관리하기 하는 경우, [virtualenvs.in-project](https://python-poetry.org/docs/configuration/#virtualenvsin-project) 설정을 합니다:

```bash
poetry config virtualenvs.in-project true
poetry config --list
poetry install
```

- [`virtualenvs.in-project`](https://python-poetry.org/docs/configuration/#virtualenvsin-project)

#### Using poetry run

```bash
poetry run python MODULE.py
poetry run black
poetry run which python
poetry shell
which python
```

#### Activating the virtual environment

```bash
poetry shell  # source .venv/bin/python
exit          # deactivate
```

- `poetry env info --path`: 가상 환경 위치를 보여줍니다.
- `poetry env list`: 가상 환경 목록을 보여줍니다.

### Version constraints

`^2.1` is `>=2.1.0 < 3.0.0`

### Installing dependencies

```bash
poetry install
```

#### Installing dependencies only

```bash
poetry install --no-root
```

### Updating dependencies to their latest versions

```bash
poetry update PACKAGE
```

## Managing dependencies

Refer to [Managing dependencies](https://python-poetry.org/docs/managing-dependencies/).

### Dependency groups

```toml
[tool.poetry.group.test]  # This part can be left out

[tool.poetry.group.test.dependencies]
pytest = "^6.0.0"
pytest-mock = "*"
```

#### Optional groups

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "*"
```

```bash
poetry install --with docs
```

#### Adding a dependency to a group

```bash
poetry add pytest --group test
```

#### Installing group dependencies

```bash
# Install group.test.dependencies (Exclude group.docs.dependencies).
poetry install --with test --without docs

# Install group.docs.dependencies.
poetry install --only docs

# Install dependencies and group.dev.dependencies.
poetry install --only main,dev
```

- `--with`
- `--without`
- `--only`

#### Removing dependencies from a group

```bash
poetry remove --group docs mkdocs
```

- `--group GROUP`: 권장합니다. 예로 위는 `[tool.poetry.group.docs.dependencies]` 안에 `mkdocs` 만 삭제됩니다. `[tool.poetry.group.docs]` 삭제되지 않습니다.

### Synchronizing dependencies

`poetry.lock` 정리합니다:

```bash
poetry install --with dev,docs,test --sync
```

### Layering optional groups

## The pyproject.toml file

Refer to [The pyproject.toml file](https://python-poetry.org/docs/pyproject/).

## Extras

https://python-poetry.org/docs/pyproject/#extras

For examples:

```bash
poetry add bandit --group dev --extras toml
```
