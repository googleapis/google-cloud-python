"""Nox test automation configuration.

See: https://nox.readthedocs.io/en/latest/
"""

import os
import os.path

import nox

PANDAS_PRE_WHEELS = (
    "https://7933911d6844c6c53a7d-47bd50c35cd79bd838daf386af554a83"
    ".ssl.cf2.rackcdn.com"
)


latest_python = "3.6"


@nox.session
def test(session):
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".")

    # Skip local auth tests on Travis.
    additional_args = list(session.posargs)
    if "TRAVIS_BUILD_DIR" in os.environ:
        additional_args = additional_args + ["-m", "not local_auth"]

    session.run(
        "pytest",
        os.path.join(".", "tests"),
        "--quiet",
        "--cov=pandas_gbq",
        "--cov=tests.unit",
        "--cov-report",
        "xml:/tmp/pytest-cov.xml",
        *additional_args
    )


@nox.session
def unit(session):
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".")
    session.run(
        "pytest",
        os.path.join(".", "tests", "unit"),
        "--quiet",
        "--cov=pandas_gbq",
        "--cov=tests.unit",
        "--cov-report",
        "xml:/tmp/pytest-cov.xml",
        *session.posargs
    )


@nox.session
def test_earliest_deps(session, python="3.5"):
    session.install(
        "-r", os.path.join(".", "ci", "requirements-3.5-0.18.1.pip")
    )
    test(session)


@nox.session
def test_latest_deps(session, python=latest_python):
    session.install(
        "--pre", "--upgrade", "--timeout=60", "-f", PANDAS_PRE_WHEELS, "pandas"
    )
    session.install(
        "-r", os.path.join(".", "ci", "requirements-3.6-MASTER.pip")
    )
    test(session)


@nox.session
def lint(session, python=latest_python):
    session.install("black")
    session.run(
        "black",
        "--check",
        "--exclude",
        "(\.git|\.hg|\.mypy_cache|\.tox|\.nox|\.venv|_build|buck-out|build|dist)",
        ".",
    )


@nox.session
def cover(session, python=latest_python):
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=40")
    session.run("coverage", "erase")
