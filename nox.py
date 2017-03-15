# Copyright 2017 Google Inc.
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

import os

import nox


@nox.session
def docs(session):
    """Build the docs."""

    # Build docs against the latest version of Python, because we can.
    session.interpreter = 'python3.6'

    # Install Sphinx and also all of the google-cloud-* packages.
    session.chdir(os.path.realpath(os.path.dirname(__file__)))
    session.install('sphinx', 'sphinx_rtd_theme')
    session.install(
        'core/', 'bigquery/', 'bigtable/', 'datastore/', 'error_reporting/',
        'language/', 'logging/', 'monitoring/', 'pubsub/', 'resource_manager/',
        'runtimeconfig/', 'spanner/', 'speech/', 'storage/', 'translate/',
        'vision/',
    )
    session.install('.')

    # Build the docs!
    session.run('bash', './test_utils/scripts/update_docs.sh')
