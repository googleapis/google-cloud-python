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

import json
import os

import mock
import py
import pytest

from google.auth import _cloud_sdk
from google.auth import environment_vars
import google.oauth2.credentials


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
AUTHORIZED_USER_FILE = os.path.join(DATA_DIR, 'authorized_user.json')

with open(AUTHORIZED_USER_FILE) as fh:
    AUTHORIZED_USER_FILE_DATA = json.load(fh)

SERVICE_ACCOUNT_FILE = os.path.join(DATA_DIR, 'service_account.json')

with open(SERVICE_ACCOUNT_FILE) as fh:
    SERVICE_ACCOUNT_FILE_DATA = json.load(fh)

with open(os.path.join(DATA_DIR, 'cloud_sdk.cfg')) as fh:
    CLOUD_SDK_CONFIG_DATA = fh.read()

CONFIG_PATH_PATCH = mock.patch(
    'google.auth._cloud_sdk.get_config_path', autospec=True)


@pytest.fixture
def config_dir(tmpdir):
    config_dir = tmpdir.join(
        '.config', _cloud_sdk._CONFIG_DIRECTORY)

    with CONFIG_PATH_PATCH as mock_get_config_dir:
        mock_get_config_dir.return_value = str(config_dir)
        yield config_dir


@pytest.fixture
def config_file(config_dir):
    config_file = py.path.local(_cloud_sdk._get_config_file(
        str(config_dir), 'default'))
    yield config_file


def test_get_project_id(config_file):
    config_file.write(CLOUD_SDK_CONFIG_DATA, ensure=True)
    project_id = _cloud_sdk.get_project_id()
    assert project_id == 'example-project'


def test_get_project_id_non_existent(config_file):
    project_id = _cloud_sdk.get_project_id()
    assert project_id is None


def test_get_project_id_bad_file(config_file):
    config_file.write('<<<badconfig', ensure=True)
    project_id = _cloud_sdk.get_project_id()
    assert project_id is None


def test_get_project_id_no_section(config_file):
    config_file.write('[section]', ensure=True)
    project_id = _cloud_sdk.get_project_id()
    assert project_id is None


def test_get_project_id_non_default_config(config_dir):
    active_config = config_dir.join('active_config')
    test_config = py.path.local(_cloud_sdk._get_config_file(
        str(config_dir), 'test'))

    # Create an active config file that points to the 'test' config.
    active_config.write('test', ensure=True)
    test_config.write(CLOUD_SDK_CONFIG_DATA, ensure=True)

    project_id = _cloud_sdk.get_project_id()

    assert project_id == 'example-project'


@CONFIG_PATH_PATCH
def test_get_application_default_credentials_path(mock_get_config_dir):
    config_path = 'config_path'
    mock_get_config_dir.return_value = config_path
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
def test_get_config_path_unix(mock_expanduser):
    mock_expanduser.side_effect = lambda path: path

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
    assert credentials._token_uri == _cloud_sdk._GOOGLE_OAUTH2_TOKEN_ENDPOINT


def test_load_authorized_user_credentials_bad_format():
    with pytest.raises(ValueError) as excinfo:
        _cloud_sdk.load_authorized_user_credentials({})

    assert excinfo.match(r'missing fields')
