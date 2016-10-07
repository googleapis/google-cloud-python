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

import datetime
import json

import mock
import pytest
import six
from six.moves import http_client
from six.moves import urllib

from google.auth import exceptions
from google.oauth2 import _client


def test__handle_error_response():
    response_data = json.dumps({
        'error': 'help',
        'error_description': 'I\'m alive'})

    with pytest.raises(exceptions.RefreshError) as excinfo:
        _client._handle_error_response(response_data)

    assert excinfo.match(r'help: I\'m alive')


def test__handle_error_response_non_json():
    response_data = 'Help, I\'m alive'

    with pytest.raises(exceptions.RefreshError) as excinfo:
        _client._handle_error_response(response_data)

    assert excinfo.match(r'Help, I\'m alive')


@mock.patch('google.auth._helpers.utcnow', return_value=datetime.datetime.min)
def test__parse_expiry(now_mock):
    result = _client._parse_expiry({'expires_in': 500})
    assert result == datetime.datetime.min + datetime.timedelta(seconds=500)


def test__parse_expiry_none():
    assert _client._parse_expiry({}) is None


def _make_request(response_data):
    response = mock.Mock()
    response.status = http_client.OK
    response.data = json.dumps(response_data).encode('utf-8')
    return mock.Mock(return_value=response)


def test__token_endpoint_request():
    request = _make_request({'test': 'response'})

    result = _client._token_endpoint_request(
        request, 'http://example.com', {'test': 'params'})

    # Check request call
    request.assert_called_with(
        method='POST',
        url='http://example.com',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        body='test=params')

    # Check result
    assert result == {'test': 'response'}


def test__token_endpoint_request_error():
    response = mock.Mock()
    response.status = http_client.BAD_REQUEST
    response.data = b'Error'
    request = mock.Mock(return_value=response)

    with pytest.raises(exceptions.RefreshError):
        _client._token_endpoint_request(request, 'http://example.com', {})


def _verify_request_params(request, params):
    request_body = request.call_args[1]['body']
    request_params = urllib.parse.parse_qs(request_body)

    for key, value in six.iteritems(params):
        assert request_params[key][0] == value


@mock.patch('google.auth._helpers.utcnow', return_value=datetime.datetime.min)
def test_jwt_grant(now_mock):
    request = _make_request({
        'access_token': 'token',
        'expires_in': 500,
        'extra': 'data'})

    token, expiry, extra_data = _client.jwt_grant(
        request, 'http://example.com', 'assertion_value')

    # Check request call
    _verify_request_params(request, {
        'grant_type': _client._JWT_GRANT_TYPE,
        'assertion': 'assertion_value'
    })

    # Check result
    assert token == 'token'
    assert expiry == datetime.datetime.min + datetime.timedelta(seconds=500)
    assert extra_data['extra'] == 'data'


def test_jwt_grant_no_access_token():
    request = _make_request({
        # No access token.
        'expires_in': 500,
        'extra': 'data'})

    with pytest.raises(exceptions.RefreshError):
        _client.jwt_grant(request, 'http://example.com', 'assertion_value')


@mock.patch('google.auth._helpers.utcnow', return_value=datetime.datetime.min)
def test_refresh_grant(now_mock):
    request = _make_request({
        'access_token': 'token',
        'refresh_token': 'new_refresh_token',
        'expires_in': 500,
        'extra': 'data'})

    token, refresh_token, expiry, extra_data = _client.refresh_grant(
        request, 'http://example.com', 'refresh_token', 'client_id',
        'client_secret')

    # Check request call
    _verify_request_params(request, {
        'grant_type': _client._REFRESH_GRANT_TYPE,
        'refresh_token': 'refresh_token',
        'client_id': 'client_id',
        'client_secret': 'client_secret'
    })

    # Check result
    assert token == 'token'
    assert refresh_token == 'new_refresh_token'
    assert expiry == datetime.datetime.min + datetime.timedelta(seconds=500)
    assert extra_data['extra'] == 'data'


def test_refresh_grant_no_access_token():
    request = _make_request({
        # No access token.
        'refresh_token': 'new_refresh_token',
        'expires_in': 500,
        'extra': 'data'})

    with pytest.raises(exceptions.RefreshError):
        _client.refresh_grant(
            request, 'http://example.com', 'refresh_token', 'client_id',
            'client_secret')
