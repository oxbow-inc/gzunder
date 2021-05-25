"""Nox sessions."""
import os
from pathlib import Path
from typing import Iterator

from nox.sessions import Session
from nox_poetry import session  # type: ignore[import]

# @session(python=["3.8", "3.9"])
# def tests(session):
#     session.install("pytest", ".")
#     session.run("pytest")


locations = (
    "src/",
    # "tests/",
    "noxfile.py",
    # "docs/conf.py",
)


def get_files() -> Iterator[str]:
    for path in map(Path, locations):
        if path.is_dir():
            yield from map(str, path.rglob("*.py"))
        else:
            yield str(path)


@session(python="3.8")
def reorder_imports(session: Session) -> None:
    """Reformat imports."""
    colon_dirs = ":".join(filter(os.path.isdir, locations))
    session.install("reorder-python-imports", ".")
    session.run(
        "reorder-python-imports",
        "--py38-plus",
        "--unclassifiable-application-module=gzunder",
        f"--application-directories={colon_dirs}:.",
        *get_files(),
        success_codes=[0, 1],
    )


@session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.8")
def autoflake(session: Session) -> None:
    """Upgrade syntax to newer versions."""
    args = session.posargs or locations
    session.install("autoflake")
    session.run(
        "autoflake",
        "--in-place",
        "--remove-all-unused-imports",
        "--remove-unused-variable",
        "--recursive",
        *args,
    )


@session(python="3.8")
def pyupgrade(session: Session) -> None:
    """Upgrade syntax to newer versions."""
    session.install("pyupgrade")
    session.run("pyupgrade", "--py37-plus")


@session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    session.install("safety", ".")
    session.run("safety", "check", "--full-report")


@session(python=["3.8", "3.9"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy", ".")
    session.run("mypy", "--show-error-codes", *args)


# @nox.session(python=["3.8", "3.7"])
@session(python="3.8")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(".[lint]")
    session.run("pflake8", *args)
    session.run(
        "yamllint",
        "--format",
        "parsable",
        "--strict",
        "docker-compose.yml",
        # ".github/",
        # ".readthedocs.yml",
    )
