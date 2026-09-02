# uv-template

Template for uv-based Python projects: src layout, ruff, mypy, pytest,
pre-commit, a PyCharm run configuration. Nothing else.

## Make it yours

Clone it, then run the initializer. It is stdlib-only, so it works before a venv
exists.

```bash
python3 init_project.py             # interactive rename, then it deletes itself
python3 init_project.py --dry-run   # preview only
```

It asks for a project name, a package name and a description, then:

- rewrites both names through every text file — `pyproject.toml`, `README.md`,
  `src/`, `tests/`, `.pre-commit-config.yaml`
- renames `src/uv_template/` and the PyCharm run configuration to match
- deletes `uv.lock` and `.venv/`, so the next `uv sync` resolves fresh
- resets git history, if you want it to
- runs `uv sync` and `uvx pre-commit install`, then deletes itself

Everything above this point is template boilerplate and disappears when you run
it. Everything below becomes your project's README.

## Use it

Needs [uv](https://docs.astral.sh/uv/) and Python 3.14+. `uv sync` fetches the
interpreter if you don't already have one.

| Command | |
| --- | --- |
| `uv sync` | create `.venv` and install dependencies |
| `uv run uv-template` | run the CLI |
| `uv run pytest` | run the tests |
| `uv run ruff check --fix .` | lint |
| `uv run ruff format .` | format |
| `uv run mypy` | type-check |
| `uvx pre-commit install` | check every commit, once per clone |

### Layout

| Path | |
| --- | --- |
| `src/uv_template/main.py` | `main()`, what the console script calls |
| `tests/test_main.py` | its test |
| `pyproject.toml` | dependencies, entry point, ruff, mypy and pytest config |
| `.pre-commit-config.yaml` | the commit hooks |
| `.idea/runConfigurations/` | the PyCharm run config, committed so it is shared |

### Dependencies

`uv add <pkg>` for runtime, `uv add --dev <pkg>` for tooling. Both write to
`uv.lock`, which is committed so every clone resolves to the same versions.

### Hooks

The pre-commit hooks shell out to `uv run ruff` and `uv run mypy` rather than
pinning versions of their own. There is one of each — the ones in the `dev`
group — so a hook can never disagree with what you run by hand. Bump them with
`uv add --dev ruff@latest mypy@latest` and both sides move together.

mypy runs in `strict` mode over `src`, `tests` and `init_project.py`. Loosen it
in the `[tool.mypy]` block if a dependency ships no stubs.
