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

from os import path


showcase_version = "0.11.0"


@nox.session(python=["3.6", "3.7", "3.8"])
def unit(session):
    """Run the unit test suite."""

    session.install(
        "coverage", "pytest", "pytest-cov", "pytest-xdist", "pyfakefs",
    )
    session.install("-e", ".")

    session.run(
        "py.test",
        "-vv",
        "-n=auto",
        "--cov=gapic",
        "--cov-config=.coveragerc",
        "--cov-report=term",
        "--cov-report=html",
        *(session.posargs or [path.join("tests", "unit")]),
    )


@nox.session(python="3.8")
def showcase(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the Showcase test suite."""

    # Try to make it clear if Showcase is not running, so that
    # people do not end up with tons of difficult-to-debug failures over
    # an obvious problem.
    if not os.environ.get("CIRCLECI"):
        session.log("-" * 70)
        session.log("Note: Showcase must be running for these tests to work.")
        session.log("See https://github.com/googleapis/gapic-showcase")
        session.log("-" * 70)

    # Install pytest and gapic-generator-python
    session.install("mock")
    session.install("pytest")
    session.install("pytest-asyncio")
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
        opts = f"--python_gapic_opt={template_opt}"
        opts += ",".join(other_opts + ("lazy-import",))
        session.run(
            "protoc",
            "--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            f"--python_gapic_out={tmp_dir}",
            "google/showcase/v1beta1/echo.proto",
            "google/showcase/v1beta1/identity.proto",
            "google/showcase/v1beta1/messaging.proto",
            external=True,
        )

        # Install the library.
        session.install(tmp_dir)

    session.run(
        "py.test", "--quiet", *(session.posargs or [path.join("tests", "system")])
    )


@nox.session(python="3.8")
def showcase_mtls(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the Showcase mtls test suite."""

    # Try to make it clear if Showcase is not running, so that
    # people do not end up with tons of difficult-to-debug failures over
    # an obvious problem.
    if not os.environ.get("CIRCLECI"):
        session.log("-" * 70)
        session.log("Note: Showcase must be running for these tests to work.")
        session.log("See https://github.com/googleapis/gapic-showcase")
        session.log("-" * 70)

    # Install pytest and gapic-generator-python
    session.install("mock")
    session.install("pytest")
    session.install("pytest-asyncio")
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
        opts = f"--python_gapic_opt={template_opt}"
        opts += ",".join(other_opts + ("lazy-import",))
        session.run(
            "protoc",
            "--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            f"--python_gapic_out={tmp_dir}",
            "google/showcase/v1beta1/echo.proto",
            "google/showcase/v1beta1/identity.proto",
            "google/showcase/v1beta1/messaging.proto",
            external=True,
        )

        # Install the library.
        session.install(tmp_dir)

    session.run(
        "py.test",
        "--quiet",
        "--mtls",
        *(session.posargs or [path.join("tests", "system")]),
    )


@nox.session(python="3.8")
def showcase_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase(session, templates=templates, other_opts=("old-naming",))


@nox.session(python="3.8")
def showcase_mtls_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase_mtls(session, templates=templates, other_opts=("old-naming",))


@nox.session(python=["3.6", "3.7", "3.8"])
def showcase_unit(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the generated unit tests against the Showcase library."""

    session.install(
        "coverage", "pytest", "pytest-cov", "pytest-xdist", 'asyncmock', 'pytest-asyncio'
    )
    session.install(".")

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
        opts = [
            f"python-gapic-templates={templates}",
        ]
        opts.extend(other_opts)
        if session.python == "3.8":
            opts.append("lazy-import")

        opt_str = f'--python_gapic_opt={",".join(opts)},'

        session.run(
            "protoc",
            "--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            f"--python_gapic_out={tmp_dir}",
            opt_str,
            "google/showcase/v1beta1/echo.proto",
            "google/showcase/v1beta1/identity.proto",
            "google/showcase/v1beta1/messaging.proto",
            "google/showcase/v1beta1/testing.proto",
            external=True,
        )

        # Install the library.
        session.chdir(tmp_dir)
        session.install("-e", tmp_dir)

        # Run the tests.
        session.run(
            "py.test",
            "-n=auto",
            "--quiet",
            "--cov=google",
            "--cov-report=term",
            *(session.posargs or [path.join("tests", "unit")]),
        )


@nox.session(python=["3.6", "3.7", "3.8"])
def showcase_unit_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase_unit(session, templates=templates, other_opts=("old-naming",))


@nox.session(python="3.8")
def showcase_mypy(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Perform typecheck analysis on the generated Showcase library."""

    # Install pytest and gapic-generator-python
    session.install("mypy")
    session.install(".")

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
        gapic_opts = f"--python_gapic_opt={template_opt},"
        gapic_opts += ",".join(other_opts)
        session.run(
            "protoc",
            "--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            f"--python_gapic_out={tmp_dir}",
            gapic_opts,
            "google/showcase/v1beta1/echo.proto",
            "google/showcase/v1beta1/identity.proto",
            "google/showcase/v1beta1/messaging.proto",
            "google/showcase/v1beta1/testing.proto",
            external=True,
        )

        # Install the library.
        session.chdir(tmp_dir)
        session.install("-e", tmp_dir)

        # Run the tests.
        session.run("mypy", "google")


@nox.session(python="3.8")
def showcase_mypy_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase_mypy(session, templates=templates, other_opts=("old-naming",))


@nox.session(python="3.6")
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


@nox.session(python=["3.7", "3.8"])
def mypy(session):
    """Perform typecheck analysis."""

    session.install("mypy")
    session.install(".")
    session.run("mypy", "gapic")
