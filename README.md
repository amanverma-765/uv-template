# uv-template

Template for uv-based Python projects.

## Use it

```bash
uv sync                       # create .venv + install deps
uv run uv-template            # run the CLI
uv run pytest                 # tests
uv run ruff check --fix .     # lint
uv run ruff format .          # format
uvx pre-commit install        # lint/format on commit (once per clone)
```

## Rename for a new project

```bash
python3 init_project.py       # interactive: renames everything, then deletes itself
python3 init_project.py --dry-run   # preview only
```

It rewrites the project/package name and description across `pyproject.toml`,
`README.md`, `tests/` and `src/`, renames `src/uv_template/`, drops `uv.lock`
and `.venv/`, and optionally resets git history.
