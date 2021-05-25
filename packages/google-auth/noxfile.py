# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil
import os
import nox

TEST_DEPENDENCIES = [
    "flask",
    "freezegun",
    "mock",
    "oauth2client",
    "pyopenssl",
    "pytest",
    "pytest-cov",
    "pytest-localserver",
    "pyu2f",
    "requests",
    "urllib3",
    "cryptography",
    "responses",
    "grpcio",
]

ASYNC_DEPENDENCIES = [
    "pytest-asyncio",
    "aioresponses",
    "asynctest",
    "aiohttp!=3.7.4.post0",
]

BLACK_VERSION = "black==19.3b0"
BLACK_PATHS = [
    "google",
    "tests",
    "tests_async",
    "noxfile.py",
    "setup.py",
    "docs/conf.py",
]


@nox.session(python="3.7")
def lint(session):
    session.install("flake8", "flake8-import-order", "docutils", BLACK_VERSION)
    session.install(".")
    session.run("black", "--check", *BLACK_PATHS)
    session.run(
        "flake8",
        "--import-order-style=google",
        "--application-import-names=google,tests,system_tests",
        "google",
        "tests",
        "tests_async",
    )
    session.run(
        "python", "setup.py", "check", "--metadata", "--restructuredtext", "--strict"
    )


@nox.session(python="3.8")
def blacken(session):
    """Run black.
    Format code to uniform standard.
    The Python version should be consistent with what is
    supplied in the Python Owlbot postprocessor.

    https://github.com/googleapis/synthtool/blob/master/docker/owlbot/python/Dockerfile
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def unit(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(*(ASYNC_DEPENDENCIES))
    session.install(".")
    session.run(
        "pytest",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "tests",
        "tests_async",
    )


@nox.session(python=["2.7"])
def unit_prev_versions(session):
    session.install(".")
    session.install(*TEST_DEPENDENCIES)
    session.run(
        "pytest",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "tests",
    )


@nox.session(python="3.7")
def cover(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(*(ASYNC_DEPENDENCIES))
    session.install(".")
    session.run(
        "pytest",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "--cov=tests_async",
        "--cov-report=",
        "tests",
        "tests_async",
    )
    session.run("coverage", "report", "--show-missing", "--fail-under=100")


@nox.session(python="3.7")
def docgen(session):
    session.env["SPHINX_APIDOC_OPTIONS"] = "members,inherited-members,show-inheritance"
    session.install(*TEST_DEPENDENCIES)
    session.install("sphinx")
    session.install(".")
    session.run("rm", "-r", "docs/reference")
    session.run(
        "sphinx-apidoc",
        "--output-dir",
        "docs/reference",
        "--separate",
        "--module-first",
        "google",
    )


@nox.session(python="3.7")
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".[aiohttp]")
    session.install(
        "sphinx<3.0.0", "alabaster", "recommonmark", "sphinx-docstring-typing"
    )

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-T",  # show full traceback on exception
        "-W",  # warnings as errors
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python="pypy")
def pypy(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(*ASYNC_DEPENDENCIES)
    session.install(".")
    session.run(
        "pytest",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "tests",
        "tests_async",
    )
