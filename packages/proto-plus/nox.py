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

import nox


@nox.session(python=['3.5', '3.6', '3.7'])
def unit(session, proto='python'):
    """Run the unit test suite."""

    session.env['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = proto
    session.install('coverage', 'pytest', 'pytest-cov')
    session.install('-e', '.')

    session.run(
        'py.test',
        '-W=error',
        '--quiet',
        '--cov=proto',
        '--cov-config=.coveragerc',
        '--cov-report=term',
        '--cov-report=html',
        os.path.join('tests', ''),
    )


@nox.session(python=['3.5', '3.6', '3.7'])
def unitcpp(session):
    return unit(session, proto='cpp')


@nox.session(python='3.6')
def docs(session):
    """Build the docs."""

    session.install('sphinx', 'sphinx_rtd_theme')
    session.install('.')

    # Build the docs!
    session.run('rm', '-rf', 'docs/_build/')
    session.run('sphinx-build', '-W', '-b', 'html', '-d',
                'docs/_build/doctrees', 'docs/', 'docs/_build/html/')
