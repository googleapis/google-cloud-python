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
import tempfile

import nox


@nox.session(python=['3.6', '3.7'])
def unit(session):
    """Run the unit test suite."""

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


@nox.session(python='3.7')
def showcase(session):
    """Run the Showcase test suite."""

    # Try to make it clear if Showcase is not running, so that
    # people do not end up with tons of difficult-to-debug failures over
    # an obvious problem.
    if not os.environ.get('CIRCLECI'):
        session.log('-' * 70)
        session.log('Note: Showcase must be running for these tests to work.')
        session.log('See https://github.com/googleapis/gapic-showcase')
        session.log('-' * 70)
        session.run('netstat', '-plnt', '|', 'grep', ':7469', silent=True)

    # Install pytest and gapic-generator-python
    session.install('pytest')
    session.install('-e', '.')

    # Install a client library for Showcase.
    with tempfile.TemporaryDirectory() as tmp_dir:
        showcase_version = '0.0.3'

        # Download the Showcase descriptor.
        session.run(
            'curl', 'https://github.com/googleapis/gapic-showcase/releases/'
                    f'download/v{showcase_version}/'
                    f'gapic-showcase-v1alpha1-{showcase_version}.desc',
            '-L', '--output', os.path.join(tmp_dir, 'showcase.desc'),
            silent=True,
        )

        # Write out a client library for Showcase.
        session.run('protoc',
            f'--descriptor_set_in={tmp_dir}{os.path.sep}showcase.desc',
            f'--python_out={tmp_dir}', f'--pyclient_out={tmp_dir}',
            'google/showcase/v1alpha1/showcase.proto',
        )

        # Install the library.
        session.install(tmp_dir)

    session.run('py.test', '--quiet', os.path.join('tests', 'system'))


@nox.session(python='3.6')
def docs(session):
    """Build the docs."""

    session.install('sphinx < 1.8', 'sphinx_rtd_theme')
    session.install('.')

    # Build the docs!
    session.run('rm', '-rf', 'docs/_build/')
    session.run('sphinx-build', '-W', '-b', 'html', '-d',
                'docs/_build/doctrees', 'docs/', 'docs/_build/html/')
