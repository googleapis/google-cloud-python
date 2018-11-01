# Copyright 2017, Google LLC All rights reserved.
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
    os.path.join('..', 'core'),
)


def default(session):
    """Run the unit test suite.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    session.install('mock', 'pytest', 'pytest-cov', *LOCAL_DEPS)
    session.install('-e', '.')

    session.run(
        'py.test',
        '--quiet',
        '--cov=google.cloud.securitycenter_v1beta1',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        '--cov-fail-under=89', # TODO: Coverage should be raised to 97%
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
    session.install('.')
    session.run('flake8', 'google', 'tests')


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
    session.chdir(os.path.dirname(__file__))
    session.install('coverage', 'pytest-cov')
    # TODO: fail-under should be changed to 100.
    session.run('coverage', 'report', '--show-missing', '--fail-under=89')
    session.run('coverage', 'erase')

