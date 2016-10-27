# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

from google.auth import _cloud_sdk
import pytest

SKIP_TEST_ENV = 'SKIP_APP_ENGINE_SYSTEM_TEST'
HERE = os.path.dirname(__file__)
TEST_APP_DIR = os.path.join(HERE, 'app')
TEST_APP_SERVICE = 'google-auth-system-tests'


def vendor_app_dependencies():
    """Vendors in the test application's third-party dependencies."""
    subprocess.check_call(
        ['pip', 'install', '--target', 'lib', '-r', 'requirements.txt'])


def deploy_app():
    """Deploys the test application using gcloud."""
    subprocess.check_call(
        ['gcloud', 'app', 'deploy', '-q', 'app.yaml'])


@pytest.fixture
def app(monkeypatch):
    monkeypatch.chdir(TEST_APP_DIR)

    vendor_app_dependencies()
    deploy_app()

    application_id = _cloud_sdk.get_project_id()
    application_url = 'https://{}-dot-{}.appspot.com'.format(
        TEST_APP_SERVICE, application_id)

    yield application_url


@pytest.mark.skipif(
    SKIP_TEST_ENV in os.environ,
    reason='Explicitly skipping App Engine system tests.')
def test_live_application(app, http_request):
    response = http_request(method='GET', url=app)
    assert response.status == 200, response.data.decode('utf-8')
