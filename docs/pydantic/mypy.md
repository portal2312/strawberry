# [Mypy](https://docs.pydantic.dev/latest/integrations/mypy/)

`pyproject.toml`:

```toml
[tool.mypy]
plugins = [
  "pydantic.mypy"
]

follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_reexport = true

# for strict mypy: (this is the tricky one :-))
disallow_untyped_defs = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

```

## Overrides modules

```bash
# https://mypy.readthedocs.io/en/stable/config_file.html#example-pyproject-toml
[[tool.mypy.overrides]]
module = ["app.tests"]
check_untyped_defs = false
disallow_untyped_defs = false
```
