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


@nox.session
@nox.parametrize('python_version', ['3.6', '3.7'])
def unit(session, python_version='3.7'):
    """Run the unit test suite."""

    session.interpreter = 'python{0}'.format(python_version)

    session.virtualenv_dirname = 'unit-{0}'.format(python_version)

    session.install('coverage', 'pytest', 'pytest-cov')
    session.install('-e', '.')

    session.run(
        'py.test',
        '--quiet',
        '--cov=gapic',
        '--cov-config=.coveragerc',
        '--cov-report=term',
        '--cov-report=html',
        os.path.join('tests', 'unit'),
    )


@nox.session
def docs(session):
    """Build the docs."""

    session.interpreter = 'python3.6'
    session.install('sphinx', 'sphinx_rtd_theme')
    session.install('.')

    # Build the docs!
    session.run('rm', '-rf', 'docs/_build/')
    session.run('sphinx-build', '-W', '-b', 'html', '-d',
                'docs/_build/doctrees', 'docs/', 'docs/_build/html/')
