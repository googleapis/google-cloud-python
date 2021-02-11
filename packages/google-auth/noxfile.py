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
    "requests",
    "urllib3",
    "cryptography",
    "responses",
    "grpcio",
]

ASYNC_DEPENDENCIES = ["pytest-asyncio", "aioresponses", "asynctest"]

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


@nox.session(python="3.6")
def blacken(session):
    """Run black.

    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
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
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "tests",
        "tests_async",
    )


@nox.session(python=["2.7"])
def unit_prev_versions(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(".")
    session.run(
        "pytest", "--cov=google.auth", "--cov=google.oauth2", "--cov=tests", "tests"
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
    session.install("sphinx", "-r", "docs/requirements-docs.txt")
    session.install(".")
    session.run("make", "-C", "docs", "html")


@nox.session(python="pypy")
def pypy(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(*ASYNC_DEPENDENCIES)
    session.install(".")
    session.run(
        "pytest",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "tests",
        "tests_async",
    )
