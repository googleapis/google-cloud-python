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

import io
import json
import os
import subprocess

import mock
import pytest

from google.auth import _cloud_sdk
from google.auth import environment_vars
import google.oauth2.credentials


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
AUTHORIZED_USER_FILE = os.path.join(DATA_DIR, 'authorized_user.json')

with io.open(AUTHORIZED_USER_FILE) as fh:
    AUTHORIZED_USER_FILE_DATA = json.load(fh)

SERVICE_ACCOUNT_FILE = os.path.join(DATA_DIR, 'service_account.json')

with io.open(SERVICE_ACCOUNT_FILE) as fh:
    SERVICE_ACCOUNT_FILE_DATA = json.load(fh)

with io.open(os.path.join(DATA_DIR, 'cloud_sdk_config.json'), 'rb') as fh:
    CLOUD_SDK_CONFIG_FILE_DATA = fh.read()


@pytest.mark.parametrize('data, expected_project_id', [
    (CLOUD_SDK_CONFIG_FILE_DATA, 'example-project'),
    (b'I am some bad json', None),
    (b'{}', None)
])
def test_get_project_id(data, expected_project_id):
    check_output_patch = mock.patch(
        'subprocess.check_output', autospec=True, return_value=data)

    with check_output_patch as check_output:
        project_id = _cloud_sdk.get_project_id()

    assert project_id == expected_project_id
    assert check_output.called


@mock.patch(
    'subprocess.check_output', autospec=True,
    side_effect=subprocess.CalledProcessError(-1, None))
def test_get_project_id_call_error(check_output):
    project_id = _cloud_sdk.get_project_id()
    assert project_id is None
    assert check_output.called


@mock.patch('os.name', new='nt')
def test_get_project_id_windows():
    check_output_patch = mock.patch(
        'subprocess.check_output', autospec=True,
        return_value=CLOUD_SDK_CONFIG_FILE_DATA)

    with check_output_patch as check_output:
        project_id = _cloud_sdk.get_project_id()

    assert project_id == 'example-project'
    assert check_output.called
    # Make sure the executable is `gcloud.cmd`.
    args = check_output.call_args[0]
    command = args[0]
    executable = command[0]
    assert executable == 'gcloud.cmd'


@mock.patch(
    'google.auth._cloud_sdk.get_config_path', autospec=True)
def test_get_application_default_credentials_path(get_config_dir):
    config_path = 'config_path'
    get_config_dir.return_value = config_path
    credentials_path = _cloud_sdk.get_application_default_credentials_path()
    assert credentials_path == os.path.join(
        config_path, _cloud_sdk._CREDENTIALS_FILENAME)


def test_get_config_path_env_var(monkeypatch):
    config_path_sentinel = 'config_path'
    monkeypatch.setenv(
        environment_vars.CLOUD_SDK_CONFIG_DIR, config_path_sentinel)
    config_path = _cloud_sdk.get_config_path()
    assert config_path == config_path_sentinel


@mock.patch('os.path.expanduser')
def test_get_config_path_unix(expanduser):
    expanduser.side_effect = lambda path: path

    config_path = _cloud_sdk.get_config_path()

    assert os.path.split(config_path) == (
        '~/.config', _cloud_sdk._CONFIG_DIRECTORY)


@mock.patch('os.name', new='nt')
def test_get_config_path_windows(monkeypatch):
    appdata = 'appdata'
    monkeypatch.setenv(_cloud_sdk._WINDOWS_CONFIG_ROOT_ENV_VAR, appdata)

    config_path = _cloud_sdk.get_config_path()

    assert os.path.split(config_path) == (
        appdata, _cloud_sdk._CONFIG_DIRECTORY)


@mock.patch('os.name', new='nt')
def test_get_config_path_no_appdata(monkeypatch):
    monkeypatch.delenv(_cloud_sdk._WINDOWS_CONFIG_ROOT_ENV_VAR, raising=False)
    monkeypatch.setenv('SystemDrive', 'G:')

    config_path = _cloud_sdk.get_config_path()

    assert os.path.split(config_path) == (
        'G:/\\', _cloud_sdk._CONFIG_DIRECTORY)


def test_load_authorized_user_credentials():
    credentials = _cloud_sdk.load_authorized_user_credentials(
        AUTHORIZED_USER_FILE_DATA)

    assert isinstance(credentials, google.oauth2.credentials.Credentials)

    assert credentials.token is None
    assert (credentials._refresh_token ==
            AUTHORIZED_USER_FILE_DATA['refresh_token'])
    assert credentials._client_id == AUTHORIZED_USER_FILE_DATA['client_id']
    assert (credentials._client_secret ==
            AUTHORIZED_USER_FILE_DATA['client_secret'])
    assert (credentials._token_uri ==
            google.oauth2.credentials._GOOGLE_OAUTH2_TOKEN_ENDPOINT)


def test_load_authorized_user_credentials_bad_format():
    with pytest.raises(ValueError) as excinfo:
        _cloud_sdk.load_authorized_user_credentials({})

    assert excinfo.match(r'missing fields')
