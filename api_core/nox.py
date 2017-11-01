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

import nox


@nox.session
@nox.parametrize('py', ['2.7', '3.4', '3.5', '3.6'])
def unit(session, py):
    """Run the unit test suite."""

    # Run unit tests against all supported versions of Python.
    session.interpreter = 'python{}'.format(py)

    # Set the virtualenv dirname.
    session.virtualenv_dirname = 'unit-' + py

    # Install all test dependencies, then install this package in-place.
    session.install(
        'mock',
        'pytest',
        'pytest-cov',
        'grpcio >= 1.0.2',
    )
    session.install('-e', '.')

    # Run py.test against the unit tests.
    session.run(
        'py.test',
        '--quiet',
        '--cov=google.api_core',
        '--cov=tests.unit',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        '--cov-fail-under=97',
        os.path.join('tests', 'unit'),
        *session.posargs
    )


@nox.session
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.interpreter = 'python3.6'
    session.install('flake8', 'flake8-import-order')
    session.install('.')
    session.run('flake8', 'google', 'tests')


@nox.session
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.interpreter = 'python3.6'

    # Set the virtualenv dirname.
    session.virtualenv_dirname = 'setup'

    session.install('docutils', 'Pygments')
    session.run(
        'python', 'setup.py', 'check', '--restructuredtext', '--strict')


@nox.session
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.interpreter = 'python3.6'
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing', '--fail-under=100')
    session.run('coverage', 'erase')
