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
@nox.parametrize('python_version', ['2.7', '3.4', '3.5', '3.6'])
def unit_tests(session, python_version):
    """Run the unit test suite."""

    session.interpreter = 'python{}'.format(python_version)

    session.virtualenv_dirname = 'unit-' + python_version

    session.install('mock', 'pytest', 'pytest-cov')
    session.install('-e', '.')

    session.run(
        'py.test',
        '--quiet',
        '--cov=dialogflow',
        '--cov=dialogflow_v2beta1',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        os.path.join('tests', 'unit'),
    )


@nox.session
def sample_tests(session):
    """Run the sample tests."""
    session.install('mock', 'pytest')
    session.install('-e', '.')
    session.run('py.test', '--quiet', os.path.join('samples', 'tests'))


@nox.session
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install('docutils', 'pygments')
    session.run('python', 'setup.py', 'check', '--restructuredtext',
                '--strict')


@nox.session
def docs(session):
    """Build the docs."""

    session.install('sphinx', 'sphinx_rtd_theme')
    session.install('.')

    # Build the docs!
    session.run('rm', '-rf', 'docs/_build/')
    session.run('sphinx-build', '-W', '-b', 'html', '-d',
                'docs/_build/doctrees', 'docs/', 'docs/_build/html/')


@nox.session
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing')
    session.run('coverage', 'erase')
