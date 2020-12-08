# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os
import tempfile
import typing
import nox  # type: ignore

from contextlib import contextmanager
from os import path


showcase_version = "0.11.0"
ADS_TEMPLATES = path.join(path.dirname(__file__), "gapic", "ads-templates")


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def unit(session):
    """Run the unit test suite."""

    session.install(
        "coverage", "pytest", "pytest-cov", "pytest-xdist", "pyfakefs",
    )
    session.install("-e", ".")

    session.run(
        "py.test",
        *(
            session.posargs
            or [
                "-vv",
                "-n=auto",
                "--cov=gapic",
                "--cov-config=.coveragerc",
                "--cov-report=term",
                "--cov-report=html",
                path.join("tests", "unit"),
            ]
        ),
    )


# TODO(yon-mg): -add compute context manager that includes rest transport
#               -add compute unit tests
#               (to test against temporarily while rest transport is incomplete)
#               (to be removed once all features are complete)
@contextmanager
def showcase_library(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = ()
):
    """Install the generated library into the session for showcase tests."""

    # Try to make it clear if Showcase is not running, so that
    # people do not end up with tons of difficult-to-debug failures over
    # an obvious problem.
    if not os.environ.get("CIRCLECI"):
        session.log("-" * 70)
        session.log("Note: Showcase must be running for these tests to work.")
        session.log("See https://github.com/googleapis/gapic-showcase")
        session.log("-" * 70)

    # Install gapic-generator-python
    session.install("-e", ".")

    # Install a client library for Showcase.
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Download the Showcase descriptor.
        session.run(
            "curl",
            "https://github.com/googleapis/gapic-showcase/releases/"
            f"download/v{showcase_version}/"
            f"gapic-showcase-{showcase_version}.desc",
            "-L",
            "--output",
            path.join(tmp_dir, "showcase.desc"),
            external=True,
            silent=True,
        )

        # Write out a client library for Showcase.
        template_opt = f"python-gapic-templates={templates}"
        # TODO(yon-mg): add "transports=grpc+rest" when all rest features required for
        #               Showcase are implemented i.e. (grpc transcoding, LROs, etc)
        opts = "--python_gapic_opt="
        opts += ",".join(other_opts + (f"{template_opt}",))
        cmd_tup = (
            f"protoc",
            f"--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            opts,
            f"--python_gapic_out={tmp_dir}",
            f"google/showcase/v1beta1/echo.proto",
            f"google/showcase/v1beta1/identity.proto",
            f"google/showcase/v1beta1/messaging.proto",
        )
        session.run(
            *cmd_tup,
            external=True,
        )

        # Install the library.
        session.install(tmp_dir)

        yield tmp_dir


@nox.session(python="3.8")
def showcase(
    session,
    templates="DEFAULT",
    other_opts: typing.Iterable[str] = (),
    env: typing.Optional[typing.Dict[str, str]] = None,
):
    """Run the Showcase test suite."""

    with showcase_library(session, templates=templates, other_opts=other_opts):
        session.install("mock", "pytest", "pytest-asyncio")
        session.run(
            "py.test", "--quiet", *(session.posargs or [path.join("tests", "system")]),
            env=env,
        )


@nox.session(python="3.8")
def showcase_mtls(
    session,
    templates="DEFAULT",
    other_opts: typing.Iterable[str] = (),
    env: typing.Optional[typing.Dict[str, str]] = None,
):
    """Run the Showcase mtls test suite."""

    with showcase_library(session, templates=templates, other_opts=other_opts):
        session.install("mock", "pytest", "pytest-asyncio")
        session.run(
            "py.test",
            "--quiet",
            "--mtls",
            *(session.posargs or [path.join("tests", "system")]),
            env=env,
        )


@nox.session(python="3.8")
def showcase_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase(
        session,
        templates=templates,
        other_opts=("old-naming",),
        env={"GAPIC_PYTHON_ASYNC": "False"},
    )


@nox.session(python="3.8")
def showcase_mtls_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase_mtls(
        session,
        templates=templates,
        other_opts=("old-naming",),
        env={"GAPIC_PYTHON_ASYNC": "False"},
    )


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def showcase_unit(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the generated unit tests against the Showcase library."""

    session.install(
        "coverage",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "asyncmock",
        "pytest-asyncio",
    )

    with showcase_library(session, templates=templates, other_opts=other_opts) as lib:
        session.chdir(lib)

        # Run the tests.
        session.run(
            "py.test",
            "-n=auto",
            "--quiet",
            "--cov=google",
            "--cov-report=term",
            *(session.posargs or [path.join("tests", "unit")]),
        )


@nox.session(python=["3.7", "3.8", "3.9"])
def showcase_unit_alternative_templates(session):
    showcase_unit(session, templates=ADS_TEMPLATES, other_opts=("old-naming",))


@nox.session(python=["3.8"])
def showcase_unit_add_iam_methods(session):
    showcase_unit(session, other_opts=("add-iam-methods",))


@nox.session(python="3.8")
def showcase_mypy(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Perform typecheck analysis on the generated Showcase library."""

    # Install pytest and gapic-generator-python
    session.install("mypy")

    with showcase_library(session, templates=templates, other_opts=other_opts) as lib:
        session.chdir(lib)

        # Run the tests.
        session.run("mypy", "google")


@nox.session(python="3.8")
def showcase_mypy_alternative_templates(session):
    showcase_mypy(session, templates=ADS_TEMPLATES, other_opts=("old-naming",))


@nox.session(python="3.8")
def docs(session):
    """Build the docs."""

    session.install("sphinx < 1.8", "sphinx_rtd_theme")
    session.install(".")

    # Build the docs!
    session.run("rm", "-rf", "docs/_build/")
    session.run(
        "sphinx-build",
        "-W",
        "-b",
        "html",
        "-d",
        "docs/_build/doctrees",
        "docs/",
        "docs/_build/html/",
    )


@nox.session(python=["3.7", "3.8", "3.9"])
def mypy(session):
    """Perform typecheck analysis."""

    session.install("mypy")
    session.install(".")
    session.run("mypy", "gapic")
