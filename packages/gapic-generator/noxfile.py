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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import sys
import tempfile
import typing
import nox  # type: ignore

from contextlib import contextmanager
from os import path
import shutil


nox.options.error_on_missing_interpreters = True


showcase_version = os.environ.get("SHOWCASE_VERSION", "0.35.0")
ADS_TEMPLATES = path.join(path.dirname(__file__), "gapic", "ads-templates")


ALL_PYTHON = (
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
)

NEWEST_PYTHON = ALL_PYTHON[-1]


@nox.session(python=ALL_PYTHON)
def unit(session):
    """Run the unit test suite."""
    session.install(
        "coverage", "pytest-cov", "pytest", "pytest-xdist", "pyfakefs", "grpcio-status", "proto-plus",
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
                "--cov-fail-under=100",
                path.join("tests", "unit"),
            ]
        ),
    )


FRAG_DIR = Path("tests") / "fragments"
FRAGMENT_FILES = tuple(
    Path(dirname).relative_to(FRAG_DIR) / f
    for dirname, _, files in os.walk(FRAG_DIR)
    for f in files
    if os.path.splitext(f)[1] == ".proto" and f.startswith("test_")
)

# Note: this class lives outside 'fragment'
# so that, if necessary, it can be pickled for a ProcessPoolExecutor
# A callable class is necessary so that the session can be closed over
# instead of passed in, which simplifies the invocation via map.
class FragTester:
    def __init__(self, session, use_ads_templates):
        self.session = session
        self.use_ads_templates = use_ads_templates

    def __call__(self, frag):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Generate the fragment GAPIC.
            outputs = []
            templates = (
                path.join(path.dirname(__file__), "gapic", "ads-templates")
                if self.use_ads_templates
                else "DEFAULT"
            )
            maybe_old_naming = ",old-naming" if self.use_ads_templates else ""

            session_args = [
                "python",
                "-m",
                "grpc_tools.protoc",
                f"--proto_path={str(FRAG_DIR)}",
                f"--python_gapic_out={tmp_dir}",
                f"--python_gapic_opt=transport=grpc+rest,python-gapic-templates={templates}{maybe_old_naming}",
            ]

            outputs.append(
                self.session.run(*session_args, str(frag), external=True, silent=True,)
            )

            # Install the generated fragment library.
            if self.use_ads_templates:
                self.session.install(tmp_dir, "-e", ".", "-qqq")
            else:
                # Use the constraints file for the specific python runtime version.
                # We do this to make sure that we're testing against the lowest
                # supported version of a dependency.
                # This is needed to recreate the issue reported in
                # https://github.com/googleapis/gapic-generator-python/issues/1748
                # The ads templates do not have constraints files.
                constraints_path = str(
                f"{tmp_dir}/testing/constraints-{self.session.python}.txt"
                )
                self.session.install(tmp_dir, "-e", ".", "-qqq", "-r", constraints_path)

            # Run the fragment's generated unit tests.
            # Don't bother parallelizing them: we already parallelize
            # the fragments, and there usually aren't too many tests per fragment.
            outputs.append(
                self.session.run(
                    "py.test",
                    "--quiet",
                    f"--cov-config={str(Path(tmp_dir) / '.coveragerc')}",
                    "--cov-report=term",
                    "--cov-fail-under=100",
                    str(Path(tmp_dir) / "tests" / "unit"),
                    silent=True,
                )
            )

            return "".join(outputs)


@nox.session(python=ALL_PYTHON)
def fragment(session, use_ads_templates=False):
    session.install(
        "coverage",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "asyncmock; python_version < '3.8'",
        "pytest-asyncio",
        "grpcio-tools",
    )
    session.install("-e", ".")

    frag_files = [Path(f) for f in session.posargs] if session.posargs else FRAGMENT_FILES

    if os.environ.get("PARALLEL_FRAGMENT_TESTS", "false").lower() == "true":
        with ThreadPoolExecutor() as p:
            all_outs = p.map(FragTester(session, use_ads_templates), frag_files)

        output = "".join(all_outs)
        session.log(output)
    else:
        tester = FragTester(session, use_ads_templates)
        for frag in frag_files:
            session.log(tester(frag))


@nox.session(python=ALL_PYTHON)
def fragment_alternative_templates(session):
    fragment(session, use_ads_templates=True)

# `_add_python_settings` consumes a path to a temporary directory (str; i.e. tmp_dir) and 
# python settings (Dict; i.e. python settings) and modifies the service yaml within 
# tmp_dir to include python settings. The primary purpose of this function is to modify 
# the service yaml and include `rest_async_io_enabled=True` to test the async rest
# optional feature.
def _add_python_settings(tmp_dir, python_settings):
    return f"""
import yaml
from pathlib import Path
temp_file_path = Path(f"{tmp_dir}/showcase_v1beta1.yaml")
with temp_file_path.open('r') as file:
    data = yaml.safe_load(file)
    data['publishing']['library_settings'] = {python_settings}

with temp_file_path.open('w') as file:
    yaml.safe_dump(data, file, default_flow_style=False, sort_keys=False)
"""

# TODO(https://github.com/googleapis/gapic-generator-python/issues/2121): `rest_async_io_enabled` must be removed once async rest is GA.
@contextmanager
def showcase_library(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
    include_service_yaml=True,
    retry_config=True,
    rest_async_io_enabled=False
):
    """Install the generated library into the session for showcase tests."""

    session.log("-" * 70)
    session.log("Note: Showcase must be running for these tests to work.")
    session.log("See https://github.com/googleapis/gapic-showcase")
    session.log("-" * 70)

    # Install gapic-generator-python
    session.install("-e", ".")

    # Install grpcio-tools for protoc
    session.install("grpcio-tools")

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
        if include_service_yaml:
            session.run(
                "curl",
                "https://github.com/googleapis/gapic-showcase/releases/"
                f"download/v{showcase_version}/"
                f"showcase_v1beta1.yaml",
                "-L",
                "--output",
                path.join(tmp_dir, "showcase_v1beta1.yaml"),
                external=True,
                silent=True,
            )
            # TODO(https://github.com/googleapis/gapic-generator-python/issues/2121): The section below updates the showcase service yaml
            # to test experimental async rest transport. It must be removed once support for async rest is GA.
            if rest_async_io_enabled:
                # Install pyYAML for yaml.
                session.install("pyYAML")

                python_settings = [
                    {
                        'version': 'google.showcase.v1beta1',
                        'python_settings': {
                            'experimental_features': {
                                'rest_async_io_enabled': True
                            }
                        }
                    }
                ]
                update_service_yaml = _add_python_settings(tmp_dir, python_settings)
                session.run("python", "-c" f"{update_service_yaml}")
            # END TODO section to remove.
        if retry_config:
            session.run(
                "curl",
                "https://github.com/googleapis/gapic-showcase/releases/"
                f"download/v{showcase_version}/"
                f"showcase_grpc_service_config.json",
                "-L",
                "--output",
                path.join(tmp_dir, "showcase_grpc_service_config.json"),
                external=True,
                silent=True,
            )
        # Write out a client library for Showcase.
        template_opt = f"python-gapic-templates={templates}"
        opts = "--python_gapic_opt="
        if include_service_yaml and retry_config:
            opts += ",".join(other_opts + (f"{template_opt}", "transport=grpc+rest", f"service-yaml={tmp_dir}/showcase_v1beta1.yaml", f"retry-config={tmp_dir}/showcase_grpc_service_config.json"))
        else:
            opts += ",".join(other_opts + (f"{template_opt}", "transport=grpc+rest",))            
        cmd_tup = (
            "python",
            "-m",
            "grpc_tools.protoc",
            f"--experimental_allow_proto3_optional",
            f"--descriptor_set_in={tmp_dir}{path.sep}showcase.desc",
            opts,
            f"--python_gapic_out={tmp_dir}",
            f"google/showcase/v1beta1/echo.proto",
            f"google/showcase/v1beta1/identity.proto",
            f"google/showcase/v1beta1/messaging.proto",
        )
        session.run(
            *cmd_tup, external=True,
        )

        # Install the generated showcase library.
        if templates == "DEFAULT":
            # Use the constraints file for the specific python runtime version.
            # We do this to make sure that we're testing against the lowest
            # supported version of a dependency.
            # This is needed to recreate the issue reported in
            # https://github.com/googleapis/google-cloud-python/issues/12254
            constraints_path = str(
            f"{tmp_dir}/testing/constraints-{session.python}.txt"
            )
            # Install the library with a constraints file.
            session.install("-e", tmp_dir, "-r", constraints_path)
        else:
            # The ads templates do not have constraints files.
            # See https://github.com/googleapis/gapic-generator-python/issues/1788
            # Install the library without a constraints file.
            session.install("-e", tmp_dir)

        yield tmp_dir


@nox.session(python=ALL_PYTHON)
def showcase(
    session,
    templates="DEFAULT",
    other_opts: typing.Iterable[str] = (),
    env: typing.Optional[typing.Dict[str, str]] = {},
):
    """Run the Showcase test suite."""

    with showcase_library(session, templates=templates, other_opts=other_opts):
        session.install("pytest", "pytest-asyncio")
        test_directory = Path("tests", "system")
        ignore_file = env.get("IGNORE_FILE")
        pytest_command = [
            "py.test",
            "--quiet",
            *(session.posargs or [str(test_directory)]),
        ]
        if ignore_file:
            ignore_path = test_directory / ignore_file
            pytest_command.extend(["--ignore", str(ignore_path)])

        session.run(
            *pytest_command,
            env=env,
        )


@nox.session(python=NEWEST_PYTHON)
def showcase_mtls(
    session,
    templates="DEFAULT",
    other_opts: typing.Iterable[str] = (),
    env: typing.Optional[typing.Dict[str, str]] = {},
):
    """Run the Showcase mtls test suite."""

    with showcase_library(session, templates=templates, other_opts=other_opts):
        session.install("pytest", "pytest-asyncio")
        test_directory = Path("tests", "system")
        ignore_file = env.get("IGNORE_FILE")
        pytest_command = [
            "py.test",
            "--quiet",
            "--mtls",
            *(session.posargs or [str(test_directory)]),
        ]
        if ignore_file:
            ignore_path = test_directory / ignore_file
            pytest_command.extend(["--ignore", str(ignore_path)])

        session.run(
            *pytest_command,
            env=env,
        )


@nox.session(python=ALL_PYTHON)
def showcase_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase(
        session,
        templates=templates,
        other_opts=("old-naming",),
        env={"GAPIC_PYTHON_ASYNC": "False", "IGNORE_FILE": "test_universe_domain.py"},
    )


@nox.session(python=NEWEST_PYTHON)
def showcase_mtls_alternative_templates(session):
    templates = path.join(path.dirname(__file__), "gapic", "ads-templates")
    showcase_mtls(
        session,
        templates=templates,
        other_opts=("old-naming",),
        env={"GAPIC_PYTHON_ASYNC": "False", "IGNORE_FILE": "test_universe_domain.py"},
    )


def run_showcase_unit_tests(session, fail_under=100):
    session.install(
        "coverage",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "asyncmock; python_version < '3.8'",
        "pytest-asyncio",
    )

    # Run the tests.
    session.run(
        "py.test",
        *(
            session.posargs
            or [
                "-n=auto",
                "--quiet",
                "--cov=google",
                "--cov-append",
                f"--cov-fail-under={str(fail_under)}",
                path.join("tests", "unit"),
            ]
        ),
    )


@nox.session(python=ALL_PYTHON)
def showcase_unit(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the generated unit tests against the Showcase library."""
    with showcase_library(session, templates=templates, other_opts=other_opts) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session)


# TODO: `showcase_unit_w_rest_async` nox session runs showcase unit tests with the
# experimental async rest transport and must be removed once support for async rest is GA.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2121.
@nox.session(python=ALL_PYTHON)
def showcase_unit_w_rest_async(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Run the generated unit tests with async rest transport against the Showcase library."""
    with showcase_library(session, templates=templates, other_opts=other_opts, rest_async_io_enabled=True) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session)


@nox.session(python=ALL_PYTHON)
def showcase_unit_alternative_templates(session):
    with showcase_library(
        session, templates=ADS_TEMPLATES, other_opts=("old-naming",)
    ) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session)


@nox.session(python=NEWEST_PYTHON)
def showcase_unit_add_iam_methods(session):
    with showcase_library(session, other_opts=("add-iam-methods",)) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session, fail_under=100)


@nox.session(python=ALL_PYTHON)
def showcase_unit_mixins(session):
    with showcase_library(session, include_service_yaml=True) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session)


@nox.session(python=ALL_PYTHON)
def showcase_unit_alternative_templates_mixins(session):
    with showcase_library(
        session, templates=ADS_TEMPLATES, other_opts=("old-naming",),
        include_service_yaml=True
    ) as lib:
        session.chdir(lib)
        run_showcase_unit_tests(session)


@nox.session(python=NEWEST_PYTHON)
def showcase_mypy(
    session, templates="DEFAULT", other_opts: typing.Iterable[str] = (),
):
    """Perform typecheck analysis on the generated Showcase library."""

    session.install("mypy", "types-setuptools", "types-protobuf", "types-requests", "types-dataclasses")

    with showcase_library(session, templates=templates, other_opts=other_opts) as lib:
        session.chdir(lib)

        # Run the tests.
        session.run("mypy", "-p", "google")


@nox.session(python=NEWEST_PYTHON)
def showcase_mypy_alternative_templates(session):
    showcase_mypy(session, templates=ADS_TEMPLATES, other_opts=("old-naming",))


@nox.session(python=NEWEST_PYTHON)
def snippetgen(session):
    # Clone googleapis/api-common-protos which are referenced by the snippet
    # protos
    api_common_protos = "api-common-protos"
    try:
        session.run("git", "-C", api_common_protos, "pull", external=True)
    except nox.command.CommandFailed:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{api_common_protos}",
            external=True,
        )

    # Install gapic-generator-python
    session.install("-e", ".")

    session.install("grpcio-tools", "pytest", "pytest-asyncio")

    session.run("py.test", "-vv", "tests/snippetgen")


@nox.session(python="3.10")
def docs(session):
    """Build the docs."""

    session.install(
        # We need to pin to specific versions of the `sphinxcontrib-*` packages
        # which still support sphinx 4.x.
        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/344
        # and https://github.com/googleapis/sphinx-docfx-yaml/issues/345.
        "sphinxcontrib-applehelp==1.0.4",
        "sphinxcontrib-devhelp==1.0.2",
        "sphinxcontrib-htmlhelp==2.0.1",
        "sphinxcontrib-qthelp==1.0.3",
        "sphinxcontrib-serializinghtml==1.1.5",
        "sphinx==4.5.0",
        "sphinx_rtd_theme"
    )
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


@nox.session(python=ALL_PYTHON)
def mypy(session):
    """Perform typecheck analysis."""
    # Pin to click==8.1.3 to workaround https://github.com/pallets/click/issues/2558
    session.install(
        "mypy",
        "types-protobuf<=3.19.7",
        "types-PyYAML",
        "types-dataclasses",
        "click==8.1.3",
    )
    session.install(".")
    session.run("mypy", "-p", "gapic")
