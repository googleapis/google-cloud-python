# Copyright 2016 Google Inc.
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
@nox.parametrize('python_version', ['2.7', '3.4', '3.5', '3.6'])
def unit_tests(session, python_version):
    """Run the unit test suite."""

    # Run unit tests against all supported versions of Python.
    session.interpreter = 'python%s' % python_version

    # Install all test dependencies, then install this package in-place.
    session.install('mock', 'pytest', 'pytest-cov', '../core/')
    session.install('-e', '.')

    # Run py.test against the unit tests.
    session.run('py.test', '--quiet',
        '--cov=google.cloud.bigtable', '--cov=tests.unit', '--cov-append',
        '--cov-config=.coveragerc', '--cov-report=', '--cov-fail-under=97',
        'tests/unit',
    )


@nox.session
@nox.parametrize('python_version', ['2.7', '3.6'])
def system_tests(session, python_version):
    """Run the system test suite."""

    # Sanity check: Only run system tests if the environment variable is set.
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''):
        return

    # Run the system tests against latest Python 2 and Python 3 only.
    session.interpreter = 'python%s' % python_version

    # Install all test dependencies, then install this package into the
    # virutalenv's dist-packages.
    session.install('mock', 'pytest',
                    '../core/', '../test_utils/')
    session.install('.')

    # Run py.test against the system tests.
    session.run('py.test', '--quiet', 'tests/system.py')


@nox.session
def lint(session):
    """Run flake8.

    Returns a failure if flake8 finds linting errors or sufficiently
    serious code quality issues.
    """
    session.interpreter = 'python3.6'
    session.install('flake8')
    session.install('.')
    session.run('flake8', 'google/cloud/bigtable')


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
