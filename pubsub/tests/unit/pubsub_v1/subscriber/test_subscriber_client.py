# Copyright 2017, Google LLC All rights reserved.
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

from google.auth import credentials
import mock
import pytest

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1.subscriber.policy import thread


def test_init():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    assert client._policy_class is thread.Policy


def test_init_emulator(monkeypatch):
    monkeypatch.setenv('PUBSUB_EMULATOR_HOST', '/baz/bacon/')
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = subscriber.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api.subscriber_stub.Pull._channel
    assert channel.target().decode('utf8') == '/baz/bacon/'


def test_subscribe():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    subscription = client.subscribe('sub_name_a')
    assert isinstance(subscription, thread.Policy)


def test_subscribe_with_callback():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    callback = mock.Mock()
    with mock.patch.object(thread.Policy, 'open') as open_:
        subscription = client.subscribe('sub_name_b', callback)
        open_.assert_called_once_with(callback)
    assert isinstance(subscription, thread.Policy)


def test_subscribe_with_failed_callback():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    callback = 'abcdefg'
    with pytest.raises(TypeError) as exc_info:
        client.subscribe('sub_name_b', callback)
    assert callback in str(exc_info.value)
