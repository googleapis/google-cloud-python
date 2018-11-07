# Copyright 2018, Google LLC
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

import nox


LOCAL_DEPS = (
    os.path.join('..', 'api_core'),
)


def default(session):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary on the ``PATH`` can
    run the tests.
    """
    # Install all test dependencies, then install this package in-place.
    session.install('mock', 'pytest', 'pytest-cov')
    for local_dep in LOCAL_DEPS:
        session.install('-e', local_dep)
    session.install('-e', '.')

    # Run py.test against the unit tests.
    session.run(
        'py.test',
        '--quiet',
        '--cov=google.cloud.bigquery_storage',
        '--cov=google.cloud.bigquery_storage_v1beta1',
        '--cov=tests.unit',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        os.path.join('tests', 'unit'),
        *session.posargs
    )


@nox.session(python=['2.7', '3.5', '3.6', '3.7'])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python='3.6')
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """

    session.install('flake8', *LOCAL_DEPS)
    session.install('-e', '.')
    session.run(
        'flake8', os.path.join('google', 'cloud', 'bigquery_storage_v1beta1'))
    session.run('flake8', 'tests')


@nox.session(python='3.6')
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install('docutils', 'pygments')
    session.run('python', 'setup.py', 'check', '--restructuredtext',
                '--strict')


@nox.session(python='3.6')
def cover(session):
    """Run the final coverage report.
    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing', '--fail-under=100')
    session.run('coverage', 'erase')


@nox.session(python=['2.7', '3.6'])
def system(session):
    """Run the system test suite."""

    # Sanity check: Only run system tests if the environment variable is set.
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''):
        session.skip('Credentials must be set via environment variable.')

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install('pytest')
    session.install('-e', os.path.join('..', 'test_utils'))
    for local_dep in LOCAL_DEPS:
        session.install('-e', local_dep)
    session.install('.')

    # Run py.test against the system tests.
    session.run('py.test', '--quiet', 'tests/system/')
