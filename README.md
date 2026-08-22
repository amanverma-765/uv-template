# uv-template

Template for uv-based Python projects: src layout, ruff, pytest, pre-commit.
Nothing else.

## Make it yours

Clone it, then run the initializer. It is stdlib-only, so it works before a venv
exists.

```bash
python3 init_project.py             # interactive rename, then it deletes itself
python3 init_project.py --dry-run   # preview only
```

It asks for a project name, a package name and a description, then:

- rewrites those names across `pyproject.toml`, `README.md`, `src/` and `tests/`
- renames the `src/uv_template/` directory
- deletes `uv.lock` and `.venv/`
- resets git history, if you want it to
- runs `uv sync` and `uvx pre-commit install`

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
| `uvx pre-commit install` | lint and format on every commit, once per clone |

### Layout

- `src/uv_template/main.py` — `main()`, what the console script calls
- `tests/test_main.py` — its test
- `pyproject.toml` — dependencies, entry point, ruff and pytest config

### Dependencies

`uv add <pkg>` for runtime, `uv add --dev <pkg>` for tooling. Both write to
`uv.lock`, which is committed so every clone resolves to the same versions.
