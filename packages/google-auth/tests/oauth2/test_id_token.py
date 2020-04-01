# Copyright 2014 Google Inc.
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

from google.auth import environment_vars
from google.auth import exceptions
from google.auth import transport
import google.auth.compute_engine._metadata
from google.oauth2 import id_token

SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__), "../data/service_account.json"
)


def make_request(status, data=None):
    response = mock.create_autospec(transport.Response, instance=True)
    response.status = status

    if data is not None:
        response.data = json.dumps(data).encode("utf-8")

    request = mock.create_autospec(transport.Request)
    request.return_value = response
    return request


def test__fetch_certs_success():
    certs = {"1": "cert"}
    request = make_request(200, certs)

    returned_certs = id_token._fetch_certs(request, mock.sentinel.cert_url)

    request.assert_called_once_with(mock.sentinel.cert_url, method="GET")
    assert returned_certs == certs


def test__fetch_certs_failure():
    request = make_request(404)

    with pytest.raises(exceptions.TransportError):
        id_token._fetch_certs(request, mock.sentinel.cert_url)

    request.assert_called_once_with(mock.sentinel.cert_url, method="GET")


@mock.patch("google.auth.jwt.decode", autospec=True)
@mock.patch("google.oauth2.id_token._fetch_certs", autospec=True)
def test_verify_token(_fetch_certs, decode):
    result = id_token.verify_token(mock.sentinel.token, mock.sentinel.request)

    assert result == decode.return_value
    _fetch_certs.assert_called_once_with(
        mock.sentinel.request, id_token._GOOGLE_OAUTH2_CERTS_URL
    )
    decode.assert_called_once_with(
        mock.sentinel.token, certs=_fetch_certs.return_value, audience=None
    )


@mock.patch("google.auth.jwt.decode", autospec=True)
@mock.patch("google.oauth2.id_token._fetch_certs", autospec=True)
def test_verify_token_args(_fetch_certs, decode):
    result = id_token.verify_token(
        mock.sentinel.token,
        mock.sentinel.request,
        audience=mock.sentinel.audience,
        certs_url=mock.sentinel.certs_url,
    )

    assert result == decode.return_value
    _fetch_certs.assert_called_once_with(mock.sentinel.request, mock.sentinel.certs_url)
    decode.assert_called_once_with(
        mock.sentinel.token,
        certs=_fetch_certs.return_value,
        audience=mock.sentinel.audience,
    )


@mock.patch("google.oauth2.id_token.verify_token", autospec=True)
def test_verify_oauth2_token(verify_token):
    result = id_token.verify_oauth2_token(
        mock.sentinel.token, mock.sentinel.request, audience=mock.sentinel.audience
    )

    assert result == verify_token.return_value
    verify_token.assert_called_once_with(
        mock.sentinel.token,
        mock.sentinel.request,
        audience=mock.sentinel.audience,
        certs_url=id_token._GOOGLE_OAUTH2_CERTS_URL,
    )


@mock.patch("google.oauth2.id_token.verify_token", autospec=True)
def test_verify_firebase_token(verify_token):
    result = id_token.verify_firebase_token(
        mock.sentinel.token, mock.sentinel.request, audience=mock.sentinel.audience
    )

    assert result == verify_token.return_value
    verify_token.assert_called_once_with(
        mock.sentinel.token,
        mock.sentinel.request,
        audience=mock.sentinel.audience,
        certs_url=id_token._GOOGLE_APIS_CERTS_URL,
    )


def test_fetch_id_token_from_metadata_server():
    def mock_init(self, request, audience, use_metadata_identity_endpoint):
        assert use_metadata_identity_endpoint
        self.token = "id_token"

    with mock.patch.multiple(
        google.auth.compute_engine.IDTokenCredentials,
        __init__=mock_init,
        refresh=mock.Mock(),
    ):
        request = mock.Mock()
        token = id_token.fetch_id_token(request, "https://pubsub.googleapis.com")
        assert token == "id_token"


@mock.patch.object(
    google.auth.compute_engine.IDTokenCredentials,
    "__init__",
    side_effect=exceptions.TransportError(),
)
def test_fetch_id_token_from_explicit_cred_json_file(mock_init, monkeypatch):
    monkeypatch.setenv(environment_vars.CREDENTIALS, SERVICE_ACCOUNT_FILE)

    def mock_refresh(self, request):
        self.token = "id_token"

    with mock.patch.object(
        google.oauth2.service_account.IDTokenCredentials, "refresh", mock_refresh
    ):
        request = mock.Mock()
        token = id_token.fetch_id_token(request, "https://pubsub.googleapis.com")
        assert token == "id_token"


@mock.patch.object(
    google.auth.compute_engine.IDTokenCredentials,
    "__init__",
    side_effect=exceptions.TransportError(),
)
def test_fetch_id_token_no_cred_json_file(mock_init, monkeypatch):
    monkeypatch.delenv(environment_vars.CREDENTIALS, raising=False)

    with pytest.raises(exceptions.DefaultCredentialsError):
        request = mock.Mock()
        id_token.fetch_id_token(request, "https://pubsub.googleapis.com")


@mock.patch.object(
    google.auth.compute_engine.IDTokenCredentials,
    "__init__",
    side_effect=exceptions.TransportError(),
)
def test_fetch_id_token_invalid_cred_file(mock_init, monkeypatch):
    not_json_file = os.path.join(os.path.dirname(__file__), "../data/public_cert.pem")
    monkeypatch.setenv(environment_vars.CREDENTIALS, not_json_file)

    with pytest.raises(exceptions.DefaultCredentialsError):
        request = mock.Mock()
        id_token.fetch_id_token(request, "https://pubsub.googleapis.com")
