# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from unittest import mock

import pytest

from google import showcase_v1alpha3
from google.api_core import exceptions
from google.rpc import code_pb2


def test_retry_nonidempotent(echo):
    # Define our error and OK responses.
    err = exceptions.ServiceUnavailable(message='whups')
    ok = showcase_v1alpha3.EchoResponse(content='foo')
    server = mock.Mock(side_effect=(err, err, ok))

    # Mock the transport to send back the error responses followed by a
    # success response.
    transport = type(echo).get_transport_class()
    with mock.patch.object(transport, 'echo',
            new_callable=mock.PropertyMock(return_value=server)):
        with mock.patch.object(time, 'sleep'):
            response = echo.echo({'content': 'bar'})
        assert response.content == 'foo'
        assert server.call_count == 3


def test_retry_idempotent(identity):
    # Define our error and OK responses.
    err409 = exceptions.Aborted(message='derp de derp')
    err503 = exceptions.ServiceUnavailable(message='whups')
    errwtf = exceptions.Unknown(message='huh?')
    ok = showcase_v1alpha3.User(name='users/0', display_name='Guido')
    server = mock.Mock(side_effect=(err409, err503, errwtf, ok))

    # Mock the transport to send back the error responses followed by a
    # success response.
    transport = type(identity).get_transport_class()
    with mock.patch.object(transport, 'get_user',
            new_callable=mock.PropertyMock(return_value=server)):
        with mock.patch.object(time, 'sleep'):
            response = identity.get_user({'name': 'users/0'})
        assert response.name == 'users/0'
        assert response.display_name == 'Guido'
        assert server.call_count == 4


def test_retry_bubble(echo):
    with pytest.raises(exceptions.DeadlineExceeded):
        echo.echo({
            'error': {
                'code': code_pb2.Code.Value('DEADLINE_EXCEEDED'),
                'message': 'This took longer than you said it should.',
            },
        })
