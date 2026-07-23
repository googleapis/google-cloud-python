# Copyright 2018 Google LLC
#
# Licensed under the Apache License,0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations operate under the License.

import os
import shutil
from contextlib import contextmanager

import nox

DEFAULT_PYTHON_VERSION = "3.14"
UNIT_TEST_PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
    "3.15",
]

# Set error on warnings flag for pytest
ERR_ON_WARNINGS = "-Werror"

# 'showcase_unit' sessions will run with 'google' scope by default.
# Users can override it by setting environment variable.
LOGGING_SCOPE = os.getenv("GOOGLE_SDK_PYTHON_LOGGING_SCOPE", "google")

nox.options.sessions = [
    "unit",
    "docs",
    "lint",
    "mypy",
]


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run unit tests."""
    session.install("-e", ".")
    session.install(
        "pytest",
        "pytest-cov",
        "pytest-xdist",
    )
    # Run the tests.
    session.run(
        "pytest",
        ERR_ON_WARNINGS,
        "-n",
        "auto",
        "--cov=gapic",
        "--cov-config=.coveragerc",
        "--cov-report=term-missing",
        "tests/unit",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the documentation."""
    session.install("-e", ".")
    session.install("sphinx", "sphinx_rtd_theme")

    # Build documentation.
    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees"),
        "docs",
        os.path.join("docs", "_build", "html"),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run the linter."""
    session.install("flake8")
    session.run(
        "flake8",
        "gapic",
        "tests",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run mypy type checking."""
    session.install("-e", ".")
    session.install("mypy", "types-protobuf", "types-setuptools", "types-requests")
    session.run(
        "mypy",
        "gapic",
        "tests/unit",
    )


class FragTester:

    def __init__(self, session, tmp_dir):
        self.session = session
        self.tmp_dir = tmp_dir

    def run_tests(self):
        # We need to run python -m protoc (not protoc directly) to get the gapic plugin.
        # This requires the cwd to be python package root directory gapic-generator-python.
        self.session.run(
            "python",
            "-m",
            "grpc_tools.protoc",
            "--proto_path=gapic/cli/common_protos",
            "--proto_path=gapic/cli/sample_protos",
            f"--python_gapic_out={self.tmp_dir}",
            "--python_gapic_opt=transport=grpc+rest",
            "gapic/cli/sample_protos/planet.proto",
        )

        for template in ["_alternative_templates", "_mixins"]:
            self.session.run(
                "python",
                "-m",
                "grpc_tools.protoc",
                "--proto_path=gapic/cli/common_protos",
                "--proto_path=gapic/cli/sample_protos",
                f"--python_gapic_out={self.tmp_dir}",
                "--python_gapic_opt=transport=grpc+rest",
                f"--python_gapic_opt=templates={template}",
                "gapic/cli/sample_protos/planet.proto",
            )

        # Make sure that the fragment output can compile.
        with self.session.chdir(self.tmp_dir):
            constraints_path = str(
                f"{self.tmp_dir}/testing/constraints-{self.session.python}.txt"
            )

            # Generate constraints file for current python version
            self.session.run(
                "python",
                "-m",
                "pip",
                "install",
                "pip-tools",
            )

            self.session.run(
                "pip-compile",
                "--output-file",
                constraints_path,
                "pyproject.toml",
            )

            # Constraint file does not apply to Python 3.10 and 3.14+
            if self.session.python in ["3.10", "3.14", "3.15"]:
                self.session.install(self.tmp_dir, "-e", ".", "-qqq")
            else:
                constraints_path = str(
                    f"{self.tmp_dir}/testing/constraints-{self.session.python}.txt"
                )
                self.session.install(self.tmp_dir, "-e", ".", "-qqq", "-r", constraints_path)

            self.session.install("-e", "../google-api-core", "-qqq")

            # Run the fragment's generated unit tests.
            # Don't bother parallelizing them: we already parallelize
            # at the matrix level in GitHub Actions.
            self.session.run(
                "pytest",
                ERR_ON_WARNINGS,
                f"--logging-scope={LOGGING_SCOPE}",
                "tests/unit",
            )


@nox.session(python=["3.10", "3.14", "3.15"])
def fragment(session, use_ads_templates=False):
    """Run generated code tests for a small fragment."""
    tmp_dir = session.create_tmp()

    session.install(
        "pytest",
        "pytest-asyncio",
        "grpcio-tools",
    )
    session.install("-e", ".")
    session.install("-e", "../google-api-core")

    # The specific failure is `Plugin output is unparseable`
    if session.python == "3.10":
        shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)
        FragTester(session, tmp_dir).run_tests()
    else:
        FragTester(session, tmp_dir).run_tests()


@nox.session(python=DEFAULT_PYTHON_VERSION)
def snippetgen(session):
    """Run snippetgen tests."""
    session.install(
        "pytest",
        "pytest-asyncio",
        "grpcio-tools",
    )
    session.install("-e", ".")

    session.run(
        "pytest",
        "tests/snippetgen",
    )


def showcase_version() -> str:
    """Read showcase version from environment or default to 0.35.0."""
    return os.environ.get("SHOWCASE_VERSION", "0.35.0")


@contextmanager
def showcase_library(
    session,
    version: str,
    templates: str = "default",
    mixins: str = "",
    rest_numeric_enums: bool = False,
    is_async: bool = False,
    use_ads_templates: bool = False,
):
    """Context manager to generate and install showcase library."""
    opts = []
    if templates != "default":
        opts.append(f"templates={templates}")
    if mixins != "":
        opts.append(f"mixins={mixins}")
    if rest_numeric_enums:
        opts.append("rest-numeric-enums")
    if is_async:
        opts.append("transport=grpc+rest")

    opt_str = f"--python_gapic_opt={','.join(opts)}" if opts else ""

    # Download showcase proto
    showcase_proto = session.create_tmp()
    session.run(
        "curl",
        "--location",
        f"https://github.com/googleapis/gapic-showcase/archive/v{version}.tar.gz",
        "--output",
        f"{showcase_proto}/showcase.tar.gz",
        external=True,
    )
    session.run(
        "tar",
        "-xzf",
        f"{showcase_proto}/showcase.tar.gz",
        "-C",
        showcase_proto,
        external=True,
    )

    # Generate showcase code
    tmp_dir = session.create_tmp()
    session.run(
        "python",
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={showcase_proto}/gapic-showcase-{version}/schema",
        "--proto_path=gapic/cli/common_protos",
        f"--python_gapic_out={tmp_dir}",
        opt_str,
        f"{showcase_proto}/gapic-showcase-{version}/schema/google/showcase/v1beta1/echo.proto",
        f"{showcase_proto}/gapic-showcase-{version}/schema/google/showcase/v1beta1/identity.proto",
        f"{showcase_proto}/gapic-showcase-{version}/schema/google/showcase/v1beta1/messaging.proto",
        f"{showcase_proto}/gapic-showcase-{version}/schema/google/showcase/v1beta1/testing.proto",
    )

    # Install showcase library
    with session.chdir(tmp_dir):
        constraints_path = str(
            f"{tmp_dir}/testing/constraints-{session.python}.txt"
        )

        # Generate constraints file for current python version
        session.run(
            "python",
            "-m",
            "pip",
            "install",
            "pip-tools",
        )

        session.run(
            "pip-compile",
            "--output-file",
            constraints_path,
            "pyproject.toml",
        )

        # Constraint file does not apply to Python 3.10 and 3.14+
        if session.python in ["3.10", "3.14", "3.15"]:
            extras = ""
            if is_async:
                extras = "[async_rest]"
            session.install("-e", f"{tmp_dir}{extras}")
        elif not use_ads_templates:
            extras = ""
            if is_async:
                extras = "[async_rest]"

            session.install("-e", f"{tmp_dir}{extras}", "-r", constraints_path)
        else:
            # The ads templates do not have constraints files.
            # See https://github.com/googleapis/gapic-generator-python/issues/1788
            # Install the library without a constraints file.
            session.install("-e", tmp_dir)

        session.install("-e", "../google-api-core")

        yield tmp_dir


def _run_showcase_unit(
    session,
    templates: str = "default",
    mixins: str = "",
    rest_numeric_enums: bool = False,
    is_async: bool = False,
    use_ads_templates: bool = False,
):
    """Run showcase unit tests."""
    session.install(
        "pytest",
        "pytest-asyncio",
        "grpcio-tools",
    )
    session.install("-e", ".")

    ver = showcase_version()
    with showcase_library(
        session,
        ver,
        templates,
        mixins,
        rest_numeric_enums,
        is_async,
        use_ads_templates,
    ) as showcase_dir:
        # Run showcase unit tests
        session.run(
            "pytest",
            ERR_ON_WARNINGS,
            f"--logging-scope={LOGGING_SCOPE}",
            os.path.join(showcase_dir, "tests", "unit"),
            *session.posargs,
        )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def showcase_unit(session):
    """Run showcase unit tests with default templates."""
    _run_showcase_unit(session)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def showcase_unit_alternative_templates(session):
    """Run showcase unit tests with alternative templates."""
    _run_showcase_unit(session, templates="_alternative_templates")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def showcase_unit_mixins(session):
    """Run showcase unit tests with mixins."""
    _run_showcase_unit(session, mixins="google.cloud.location.Locations")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def showcase_unit_alternative_templates_mixins(session):
    """Run showcase unit tests with alternative templates and mixins."""
    _run_showcase_unit(
        session,
        templates="_alternative_templates",
        mixins="google.cloud.location.Locations",
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def showcase_unit_w_rest_async(session):
    """Run showcase unit tests with rest async transport."""
    _run_showcase_unit(session, is_async=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def showcase_mypy(session):
    """Run showcase mypy type checking."""
    session.install(
        "mypy",
        "types-protobuf",
        "types-setuptools",
        "types-requests",
        "grpcio-tools",
    )
    session.install("-e", ".")

    ver = showcase_version()
    with showcase_library(session, ver) as showcase_dir:
        session.run(
            "mypy",
            os.path.join(showcase_dir, "google"),
            os.path.join(showcase_dir, "tests"),
        )
