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


@nox.session
def default(session):
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
def test27(session):
    session.interpreter = "python2.7"
    session.install(
        "-r", os.path.join(".", "ci", "requirements-2.7-0.19.2.pip")
    )
    default(session)


@nox.session
def test35(session):
    session.interpreter = "python3.5"
    session.install(
        "-r", os.path.join(".", "ci", "requirements-3.5-0.18.1.pip")
    )
    default(session)


@nox.session
def test36(session):
    session.interpreter = "python3.6"
    session.install(
        "-r", os.path.join(".", "ci", "requirements-3.6-0.20.1.conda")
    )
    default(session)


@nox.session
def test36master(session):
    session.interpreter = "python3.6"
    session.install(
        "--pre", "--upgrade", "--timeout=60", "-f", PANDAS_PRE_WHEELS, "pandas"
    )
    session.install(
        "-r", os.path.join(".", "ci", "requirements-3.6-MASTER.pip")
    )
    default(session)


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "pandas_gbq", "tests", "-v")


@nox.session
def cover(session):
    session.interpreter = "python3.5"

    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=40")
    session.run("coverage", "erase")
