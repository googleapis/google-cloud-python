# Copyright 2016 Google LLC
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
import shutil

import nox


LOCAL_DEPS = (
    os.path.join('..', 'api_core'),
    os.path.join('..', 'core'),
)


@nox.session
def default(session):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    # Install all test dependencies, then install local packages in-place.
    session.install('mock', 'pytest', 'pytest-cov')
    for local_dep in LOCAL_DEPS:
        session.install('-e', local_dep)
    session.install('-e', '.')

    # Run py.test against the unit tests.
    session.run(
        'py.test',
        '--quiet',
        '--cov=google.cloud.storage',
        '--cov=tests.unit',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        '--cov-fail-under=97',
        'tests/unit',
        *session.posargs
    )


@nox.session(python=['2.7', '3.5', '3.6', '3.7'])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=['2.7', '3.6'])
def system(session):
    """Run the system test suite."""

    # Sanity check: Only run system tests if the environment variable is set.
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''):
        session.skip('Credentials must be set via environment variable.')

    # Use pre-release gRPC for system tests.
    session.install('--pre', 'grpcio')

    # Install all test dependencies, then install local packages in-place.
    session.install('mock', 'pytest')
    for local_dep in LOCAL_DEPS:
        session.install('-e', local_dep)
    systest_deps = [
        '../test_utils/',
        '../pubsub',
        '../kms',
    ]
    for systest_dep in systest_deps:
        session.install('-e', systest_dep)
    session.install('-e', '.')

    # Run py.test against the system tests.
    session.run('py.test', '--quiet', 'tests/system.py', *session.posargs)


@nox.session(python='3.6')
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing', '--fail-under=100')
    session.run('coverage', 'erase')


@nox.session(python='3.6')
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install('flake8', *LOCAL_DEPS)
    session.install('.')
    session.run('flake8', 'google', 'tests')


@nox.session(python='3.6')
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install('docutils', 'Pygments')
    session.run(
        'python', 'setup.py', 'check', '--restructuredtext', '--strict')


@nox.session(python="3.6")
def blacken(session):
    """Run black.
    Format code to uniform standard.
    """
    session.install("black")
    session.run(
        "black",
        "google",
        "tests",
        "docs",
    )

@nox.session(python="3.7")
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )
