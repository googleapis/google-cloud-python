# Copyright 2017 Google Inc.
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
import pytest

from google.oauth2 import flow

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CLIENT_SECRETS_FILE = os.path.join(DATA_DIR, 'client_secrets.json')

with open(CLIENT_SECRETS_FILE, 'r') as fh:
    CLIENT_SECRETS_INFO = json.load(fh)


def test_constructor_web():
    instance = flow.Flow(CLIENT_SECRETS_INFO, scopes=mock.sentinel.scopes)
    assert instance.client_config == CLIENT_SECRETS_INFO['web']
    assert (instance.oauth2session.client_id ==
            CLIENT_SECRETS_INFO['web']['client_id'])
    assert instance.oauth2session.scope == mock.sentinel.scopes


def test_constructor_installed():
    info = {'installed': CLIENT_SECRETS_INFO['web']}
    instance = flow.Flow(info, scopes=mock.sentinel.scopes)
    assert instance.client_config == info['installed']
    assert instance.oauth2session.client_id == info['installed']['client_id']
    assert instance.oauth2session.scope == mock.sentinel.scopes


def test_constructor_bad_format():
    with pytest.raises(ValueError):
        flow.Flow({}, scopes=[])


def test_constructor_missing_keys():
    with pytest.raises(ValueError):
        flow.Flow({'web': {}}, scopes=[])


def test_from_client_secrets_file():
    instance = flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=mock.sentinel.scopes)
    assert instance.client_config == CLIENT_SECRETS_INFO['web']
    assert (instance.oauth2session.client_id ==
            CLIENT_SECRETS_INFO['web']['client_id'])
    assert instance.oauth2session.scope == mock.sentinel.scopes


@pytest.fixture
def instance():
    yield flow.Flow(CLIENT_SECRETS_INFO, scopes=mock.sentinel.scopes)


def test_redirect_uri(instance):
    instance.redirect_uri = mock.sentinel.redirect_uri
    assert (instance.redirect_uri ==
            instance.oauth2session.redirect_uri ==
            mock.sentinel.redirect_uri)


def test_authorization_url(instance):
    scope = 'scope_one'
    instance.oauth2session.scope = [scope]
    authorization_url_patch = mock.patch.object(
        instance.oauth2session, 'authorization_url',
        wraps=instance.oauth2session.authorization_url)

    with authorization_url_patch as authorization_url_spy:
        url, _ = instance.authorization_url(prompt='consent')

        assert CLIENT_SECRETS_INFO['web']['auth_uri'] in url
        assert scope in url
        authorization_url_spy.assert_called_with(
            CLIENT_SECRETS_INFO['web']['auth_uri'],
            access_type='offline',
            prompt='consent')


def test_fetch_token(instance):
    fetch_token_patch = mock.patch.object(
        instance.oauth2session, 'fetch_token', autospec=True,
        return_value=mock.sentinel.token)

    with fetch_token_patch as fetch_token_mock:
        token = instance.fetch_token(code=mock.sentinel.code)

        assert token == mock.sentinel.token
        fetch_token_mock.assert_called_with(
            CLIENT_SECRETS_INFO['web']['token_uri'],
            client_secret=CLIENT_SECRETS_INFO['web']['client_secret'],
            code=mock.sentinel.code)


def test_credentials(instance):
    instance.oauth2session.token = {
        'access_token': mock.sentinel.access_token,
        'refresh_token': mock.sentinel.refresh_token
    }

    credentials = instance.credentials

    assert credentials.token == mock.sentinel.access_token
    assert credentials._refresh_token == mock.sentinel.refresh_token
    assert credentials._client_id == CLIENT_SECRETS_INFO['web']['client_id']
    assert (credentials._client_secret ==
            CLIENT_SECRETS_INFO['web']['client_secret'])
    assert credentials._token_uri == CLIENT_SECRETS_INFO['web']['token_uri']


def test_bad_credentials(instance):
    with pytest.raises(ValueError):
        assert instance.credentials


def test_authorized_session(instance):
    instance.oauth2session.token = {
        'access_token': mock.sentinel.access_token,
        'refresh_token': mock.sentinel.refresh_token
    }

    session = instance.authorized_session()

    assert session.credentials.token == mock.sentinel.access_token
