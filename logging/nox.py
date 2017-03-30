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
@nox.parametrize('python_version', ['2.7', '3.6'])
def system_tests(session, python_version):
    """Run the system test suite."""

    # Sanity check: Only run system tests if the environment variable is set.
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''):
        return

    # Run the system tests against latest Python 2 and Python 3 only.
    session.interpreter = 'python{}'.format(python_version)

    # Install all test dependencies, then install this package into the
    # virutalenv's dist-packages.
    session.install('mock', 'pytest',
                    '../core/', '../test_utils/',
                    '../bigquery/', '../pubsub/', '../storage/')
    session.install('.')

    # Run py.test against the system tests.
    session.run('py.test', '-vv', 'tests/system.py')
