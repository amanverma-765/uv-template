#!/usr/bin/env python3
"""Turn this template into your own project. Run once: `python3 init_project.py`

stdlib only, so it works before `uv sync`.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD_NAME = "uv-template"
OLD_PKG = "uv_template"
SKIP_DIRS = {
    ".git",
    ".venv",
    ".idea",
    ".omc",
    "dist",
    "__pycache__",
    ".ruff_cache",
    ".pytest_cache",
}
# ponytail: text files only; a template has no binaries worth rewriting
TEXT_SUFFIXES = {".py", ".toml", ".md", ".yaml", ".yml", ".cfg", ".txt", ".ini"}


def to_slug(name: str) -> str:
    """Anything -> a valid PEP 508 distribution name."""
    return re.sub(r"[^a-z0-9._-]+", "-", name.strip().lower()).strip("-._")


def to_package(name: str) -> str:
    """Project name -> importable package name."""
    pkg = re.sub(r"[^0-9a-zA-Z_]+", "_", name.strip().lower()).strip("_")
    return f"_{pkg}" if pkg[:1].isdigit() else pkg


def files() -> list[Path]:
    return [
        p
        for p in ROOT.rglob("*")
        if p.is_file()
        and p.suffix in TEXT_SUFFIXES
        and not SKIP_DIRS & set(p.relative_to(ROOT).parts)
        and p != Path(__file__).resolve()
    ]


def ask(prompt: str, default: str) -> str:
    return input(f"{prompt} [{default}]: ").strip() or default


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="preview, touch nothing")
    ap.add_argument("--self-test", action="store_true", help="run internal checks")
    args = ap.parse_args()

    if args.self_test:
        assert to_package("My Cool App") == "my_cool_app"
        assert to_package("uv-template") == "uv_template"
        assert to_package("2fast") == "_2fast"
        assert to_slug("My Cool App") == "my-cool-app"
        assert to_slug("  Foo_Bar!! ") == "foo_bar"
        assert to_slug("!!!") == ""
        print("ok")
        return

    if not (ROOT / "src" / OLD_PKG).is_dir():
        sys.exit(f"src/{OLD_PKG}/ not found — already initialised?")

    name = to_slug(ask("Project name", ROOT.name))
    if not name:
        sys.exit("project name must contain a letter or digit")
    pkg = ask(f"Package name (project: {name})", to_package(name))
    if not pkg.isidentifier():
        sys.exit(f"{pkg!r} is not a valid Python identifier")
    desc = ask("Description", "Your description here")
    fresh_git = ask("Reset git history? (y/n)", "y").lower().startswith("y")

    changed = [p for p in files() if OLD_NAME in (t := p.read_text()) or OLD_PKG in t]
    print(f"\n  rename  src/{OLD_PKG}/ -> src/{pkg}/")
    for p in changed:
        print(f"  rewrite {p.relative_to(ROOT)}")
    print(f"  delete  uv.lock, .venv/, {Path(__file__).name}")
    if fresh_git:
        print("  delete  .git/ and re-init")
    if args.dry_run:
        return
    if not ask("\nProceed? (y/n)", "y").lower().startswith("y"):
        sys.exit("aborted")

    for p in changed:
        text = p.read_text().replace(OLD_NAME, name).replace(OLD_PKG, pkg)
        if p.name == "README.md":
            # everything above "## Use it" is template boilerplate; the rest is yours
            body = text.split("## Use it", 1)[-1]
            text = f"# {name}\n\n{desc}\n\n## Use it{body.rstrip()}\n"
        if p.name == "pyproject.toml":
            text = re.sub(
                r'^description = ".*"', f'description = "{desc}"', text, flags=re.M
            )
        p.write_text(text)

    (ROOT / "src" / OLD_PKG).rename(ROOT / "src" / pkg)
    shutil.rmtree(ROOT / ".venv", ignore_errors=True)
    (ROOT / "uv.lock").unlink(missing_ok=True)
    if fresh_git:
        shutil.rmtree(ROOT / ".git", ignore_errors=True)
        subprocess.run(["git", "init", "-q"], cwd=ROOT, check=False)

    Path(__file__).unlink()

    sys.stdout.flush()  # keep our output ordered ahead of the subprocesses'
    # ponytail: best-effort — needs network, and a rename is still valid without it
    for cmd in (["uv", "sync"], ["uvx", "pre-commit", "install"]):
        if shutil.which(cmd[0]) is None:
            print(f"skipped `{' '.join(cmd)}` ({cmd[0]} not installed)")
        elif subprocess.run(cmd, cwd=ROOT, check=False).returncode:
            print(f"`{' '.join(cmd)}` failed — run it yourself")

    print(f"\nDone. Try:\n  uv run {name}\n  uv run pytest")


if __name__ == "__main__":
    main()
