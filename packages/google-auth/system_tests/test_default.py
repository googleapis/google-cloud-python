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

import py

import google.auth
from google.auth import environment_vars
import google.oauth2.credentials
from google.oauth2 import service_account


def validate_refresh(credentials, http_request):
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['email', 'profile'])

    credentials.refresh(http_request)

    assert credentials.token
    assert credentials.valid


def test_explicit_credentials_service_account(
        monkeypatch, service_account_file, http_request):
    monkeypatch.setitem(
        os.environ, environment_vars.CREDENTIALS, service_account_file)

    credentials, project_id = google.auth.default()

    assert isinstance(credentials, service_account.Credentials)
    assert project_id is not None

    validate_refresh(credentials, http_request)


def test_explicit_credentials_authorized_user(
        monkeypatch, authorized_user_file, http_request):
    monkeypatch.setitem(
        os.environ, environment_vars.CREDENTIALS, authorized_user_file)

    credentials, project_id = google.auth.default()

    assert isinstance(credentials, google.oauth2.credentials.Credentials)
    assert project_id is None

    validate_refresh(credentials, http_request)


def test_explicit_credentials_explicit_project_id(
        monkeypatch, service_account_file, http_request):
    project = 'system-test-project'
    monkeypatch.setitem(
        os.environ, environment_vars.CREDENTIALS, service_account_file)
    monkeypatch.setitem(
        os.environ, environment_vars.PROJECT, project)

    _, project_id = google.auth.default()

    assert project_id == project


def generate_cloud_sdk_config(
        tmpdir, credentials_file, active_config='default', project=None):
    tmpdir.join('active_config').write(
        '{}\n'.format(active_config), ensure=True)

    if project is not None:
        config_file = tmpdir.join(
            'configurations', 'config_{}'.format(active_config))
        config_file.write(
            '[core]\nproject = {}'.format(project), ensure=True)

    py.path.local(credentials_file).copy(
        tmpdir.join('application_default_credentials.json'))


def test_cloud_sdk_credentials_service_account(
        tmpdir, monkeypatch, service_account_file, http_request):
    # Create the Cloud SDK configuration tree
    project = 'system-test-project'
    generate_cloud_sdk_config(tmpdir, service_account_file, project=project)
    monkeypatch.setitem(
        os.environ, environment_vars.CLOUD_SDK_CONFIG_DIR, str(tmpdir))

    credentials, project_id = google.auth.default()

    assert isinstance(credentials, service_account.Credentials)
    assert project_id is not None
    # The project ID should be the project ID specified in the the service
    # account file, not the project in the config.
    assert project_id is not project

    validate_refresh(credentials, http_request)


def test_cloud_sdk_credentials_authorized_user(
        tmpdir, monkeypatch, authorized_user_file, http_request):
    # Create the Cloud SDK configuration tree
    project = 'system-test-project'
    generate_cloud_sdk_config(tmpdir, authorized_user_file, project=project)
    monkeypatch.setitem(
        os.environ, environment_vars.CLOUD_SDK_CONFIG_DIR, str(tmpdir))

    credentials, project_id = google.auth.default()

    assert isinstance(credentials, google.oauth2.credentials.Credentials)
    assert project_id == project

    validate_refresh(credentials, http_request)
