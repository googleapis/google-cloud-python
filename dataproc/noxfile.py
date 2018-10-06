# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
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


@nox.session
def default(session):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary on the ``PATH`` can
    run the tests.
    """
    # Install all test dependencies, then install this package in-place.
    session.install('mock', 'pytest', 'pytest-cov', *LOCAL_DEPS)
    session.install('-e', '.')

    # Run py.test against the unit tests.
    session.run(
        'py.test',
        '--quiet',
        '--cov=google.cloud.dataproc',
        '--cov=google.cloud.dataproc_v1',
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


@nox.session(python=['2.7', '3.7'])
def system(session):
    """Run the system test suite."""

    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''):
        session.skip('Credentials must be set via environment variable.')
    # Use pre-release gRPC for system tests.
    session.install('--pre', 'grpcio')

    session.install('pytest')
    session.install('-e', '.')

    session.run('py.test', '--quiet', os.path.join('tests', 'system'),
                *session.posargs)


@nox.session(python='3.6')
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install('docutils', 'pygments')
    session.run('python', 'setup.py', 'check', '--restructuredtext',
                '--strict')
