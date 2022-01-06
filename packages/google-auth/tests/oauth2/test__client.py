# Copyright 2016 Google LLC
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

import datetime
import json
import os

import mock
import pytest  # type: ignore
import six
from six.moves import http_client
from six.moves import urllib

from google.auth import _helpers
from google.auth import crypt
from google.auth import exceptions
from google.auth import jwt
from google.auth import transport
from google.oauth2 import _client


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA_DIR, "privatekey.pem"), "rb") as fh:
    PRIVATE_KEY_BYTES = fh.read()

SIGNER = crypt.RSASigner.from_string(PRIVATE_KEY_BYTES, "1")

SCOPES_AS_LIST = [
    "https://www.googleapis.com/auth/pubsub",
    "https://www.googleapis.com/auth/logging.write",
]
SCOPES_AS_STRING = (
    "https://www.googleapis.com/auth/pubsub"
    " https://www.googleapis.com/auth/logging.write"
)


def test__handle_error_response():
    response_data = {"error": "help", "error_description": "I'm alive"}

    with pytest.raises(exceptions.RefreshError) as excinfo:
        _client._handle_error_response(response_data)

    assert excinfo.match(r"help: I\'m alive")


def test__handle_error_response_non_json():
    response_data = {"foo": "bar"}

    with pytest.raises(exceptions.RefreshError) as excinfo:
        _client._handle_error_response(response_data)

    assert excinfo.match(r"{\"foo\": \"bar\"}")


@mock.patch("google.auth._helpers.utcnow", return_value=datetime.datetime.min)
def test__parse_expiry(unused_utcnow):
    result = _client._parse_expiry({"expires_in": 500})
    assert result == datetime.datetime.min + datetime.timedelta(seconds=500)


def test__parse_expiry_none():
    assert _client._parse_expiry({}) is None


def make_request(response_data, status=http_client.OK):
    response = mock.create_autospec(transport.Response, instance=True)
    response.status = status
    response.data = json.dumps(response_data).encode("utf-8")
    request = mock.create_autospec(transport.Request)
    request.return_value = response
    return request


def test__token_endpoint_request():
    request = make_request({"test": "response"})

    result = _client._token_endpoint_request(
        request, "http://example.com", {"test": "params"}
    )

    # Check request call
    request.assert_called_with(
        method="POST",
        url="http://example.com",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        body="test=params".encode("utf-8"),
    )

    # Check result
    assert result == {"test": "response"}


def test__token_endpoint_request_use_json():
    request = make_request({"test": "response"})

    result = _client._token_endpoint_request(
        request,
        "http://example.com",
        {"test": "params"},
        access_token="access_token",
        use_json=True,
    )

    # Check request call
    request.assert_called_with(
        method="POST",
        url="http://example.com",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer access_token",
        },
        body=b'{"test": "params"}',
    )

    # Check result
    assert result == {"test": "response"}


def test__token_endpoint_request_error():
    request = make_request({}, status=http_client.BAD_REQUEST)

    with pytest.raises(exceptions.RefreshError):
        _client._token_endpoint_request(request, "http://example.com", {})


def test__token_endpoint_request_internal_failure_error():
    request = make_request(
        {"error_description": "internal_failure"}, status=http_client.BAD_REQUEST
    )

    with pytest.raises(exceptions.RefreshError):
        _client._token_endpoint_request(
            request, "http://example.com", {"error_description": "internal_failure"}
        )

    request = make_request(
        {"error": "internal_failure"}, status=http_client.BAD_REQUEST
    )

    with pytest.raises(exceptions.RefreshError):
        _client._token_endpoint_request(
            request, "http://example.com", {"error": "internal_failure"}
        )


def verify_request_params(request, params):
    request_body = request.call_args[1]["body"].decode("utf-8")
    request_params = urllib.parse.parse_qs(request_body)

    for key, value in six.iteritems(params):
        assert request_params[key][0] == value


@mock.patch("google.auth._helpers.utcnow", return_value=datetime.datetime.min)
def test_jwt_grant(utcnow):
    request = make_request(
        {"access_token": "token", "expires_in": 500, "extra": "data"}
    )

    token, expiry, extra_data = _client.jwt_grant(
        request, "http://example.com", "assertion_value"
    )

    # Check request call
    verify_request_params(
        request, {"grant_type": _client._JWT_GRANT_TYPE, "assertion": "assertion_value"}
    )

    # Check result
    assert token == "token"
    assert expiry == utcnow() + datetime.timedelta(seconds=500)
    assert extra_data["extra"] == "data"


def test_jwt_grant_no_access_token():
    request = make_request(
        {
            # No access token.
            "expires_in": 500,
            "extra": "data",
        }
    )

    with pytest.raises(exceptions.RefreshError):
        _client.jwt_grant(request, "http://example.com", "assertion_value")


def test_id_token_jwt_grant():
    now = _helpers.utcnow()
    id_token_expiry = _helpers.datetime_to_secs(now)
    id_token = jwt.encode(SIGNER, {"exp": id_token_expiry}).decode("utf-8")
    request = make_request({"id_token": id_token, "extra": "data"})

    token, expiry, extra_data = _client.id_token_jwt_grant(
        request, "http://example.com", "assertion_value"
    )

    # Check request call
    verify_request_params(
        request, {"grant_type": _client._JWT_GRANT_TYPE, "assertion": "assertion_value"}
    )

    # Check result
    assert token == id_token
    # JWT does not store microseconds
    now = now.replace(microsecond=0)
    assert expiry == now
    assert extra_data["extra"] == "data"


def test_id_token_jwt_grant_no_access_token():
    request = make_request(
        {
            # No access token.
            "expires_in": 500,
            "extra": "data",
        }
    )

    with pytest.raises(exceptions.RefreshError):
        _client.id_token_jwt_grant(request, "http://example.com", "assertion_value")


@mock.patch("google.auth._helpers.utcnow", return_value=datetime.datetime.min)
def test_refresh_grant(unused_utcnow):
    request = make_request(
        {
            "access_token": "token",
            "refresh_token": "new_refresh_token",
            "expires_in": 500,
            "extra": "data",
        }
    )

    token, refresh_token, expiry, extra_data = _client.refresh_grant(
        request,
        "http://example.com",
        "refresh_token",
        "client_id",
        "client_secret",
        rapt_token="rapt_token",
    )

    # Check request call
    verify_request_params(
        request,
        {
            "grant_type": _client._REFRESH_GRANT_TYPE,
            "refresh_token": "refresh_token",
            "client_id": "client_id",
            "client_secret": "client_secret",
            "rapt": "rapt_token",
        },
    )

    # Check result
    assert token == "token"
    assert refresh_token == "new_refresh_token"
    assert expiry == datetime.datetime.min + datetime.timedelta(seconds=500)
    assert extra_data["extra"] == "data"


@mock.patch("google.auth._helpers.utcnow", return_value=datetime.datetime.min)
def test_refresh_grant_with_scopes(unused_utcnow):
    request = make_request(
        {
            "access_token": "token",
            "refresh_token": "new_refresh_token",
            "expires_in": 500,
            "extra": "data",
            "scope": SCOPES_AS_STRING,
        }
    )

    token, refresh_token, expiry, extra_data = _client.refresh_grant(
        request,
        "http://example.com",
        "refresh_token",
        "client_id",
        "client_secret",
        SCOPES_AS_LIST,
    )

    # Check request call.
    verify_request_params(
        request,
        {
            "grant_type": _client._REFRESH_GRANT_TYPE,
            "refresh_token": "refresh_token",
            "client_id": "client_id",
            "client_secret": "client_secret",
            "scope": SCOPES_AS_STRING,
        },
    )

    # Check result.
    assert token == "token"
    assert refresh_token == "new_refresh_token"
    assert expiry == datetime.datetime.min + datetime.timedelta(seconds=500)
    assert extra_data["extra"] == "data"


def test_refresh_grant_no_access_token():
    request = make_request(
        {
            # No access token.
            "refresh_token": "new_refresh_token",
            "expires_in": 500,
            "extra": "data",
        }
    )

    with pytest.raises(exceptions.RefreshError):
        _client.refresh_grant(
            request, "http://example.com", "refresh_token", "client_id", "client_secret"
        )
