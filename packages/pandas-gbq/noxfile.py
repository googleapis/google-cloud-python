"""Nox test automation configuration.

See: https://nox.readthedocs.io/en/latest/
"""

import os
import os.path
import shutil

import nox


supported_pythons = ["3.5", "3.6", "3.7"]
latest_python = "3.7"


@nox.session
def lint(session, python=latest_python):
    session.install("black", "flake8")
    session.install("-e", ".")
    session.run("flake8", "pandas_gbq")
    session.run("flake8", "tests")
    session.run("black", "--check", ".")


@nox.session(python=latest_python)
def blacken(session):
    session.install("black")
    session.run("black", ".")


@nox.session(python=supported_pythons)
def unit(session):
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run(
        "pytest",
        os.path.join(".", "tests", "unit"),
        "-v",
        "--cov=pandas_gbq",
        "--cov=tests.unit",
        "--cov-report",
        "xml:/tmp/pytest-cov.xml",
        *session.posargs
    )


@nox.session
def cover(session, python=latest_python):
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=74")
    session.run("coverage", "erase")


@nox.session(python=latest_python)
def docs(session):
    """Build the docs."""

    session.install("-r", os.path.join("docs", "requirements-docs.txt"))
    session.install("-e", ".")

    shutil.rmtree(os.path.join("docs", "source", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "source", "_build", "doctrees", ""),
        os.path.join("docs", "source", ""),
        os.path.join("docs", "source", "_build", "html", ""),
    )


@nox.session(python=supported_pythons)
def system(session):
    session.install("pytest", "pytest-cov")
    session.install(
        "-r",
        os.path.join(".", "ci", "requirements-{}.pip".format(session.python)),
    )
    session.install(
        "-e",
        ".",
        # Use dependencies from requirements file instead.
        # This enables testing with specific versions of the dependencies.
        "--no-dependencies",
    )

    # Skip local auth tests on CI.
    additional_args = list(session.posargs)
    if "CIRCLECI" in os.environ:
        additional_args = additional_args + ["-m", "not local_auth"]

    session.run(
        "pytest",
        os.path.join(".", "tests", "system"),
        os.path.join(".", "samples", "tests"),
        "-v",
        *additional_args
    )
