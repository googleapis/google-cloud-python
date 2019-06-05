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

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1.gapic import subscriber_client
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import futures


def test_init():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    assert isinstance(client.api, subscriber_client.SubscriberClient)


def test_init_w_custom_transport():
    transport = object()
    client = subscriber.Client(transport=transport)
    assert isinstance(client.api, subscriber_client.SubscriberClient)
    assert client.api.transport is transport


def test_init_emulator(monkeypatch):
    monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "/baz/bacon/")
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = subscriber.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api.transport.pull._channel
    assert channel.target().decode("utf8") == "/baz/bacon/"


def test_class_method_factory():
    patch = mock.patch(
        "google.oauth2.service_account.Credentials.from_service_account_file"
    )

    with patch:
        client = subscriber.Client.from_service_account_file("filename.json")

    assert isinstance(client, subscriber.Client)


@mock.patch(
    "google.cloud.pubsub_v1.subscriber._protocol.streaming_pull_manager."
    "StreamingPullManager.open",
    autospec=True,
)
def test_subscribe(manager_open):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)

    future = client.subscribe("sub_name_a", callback=mock.sentinel.callback)
    assert isinstance(future, futures.StreamingPullFuture)

    assert future._manager._subscription == "sub_name_a"
    manager_open.assert_called_once_with(
        mock.ANY, mock.sentinel.callback, future.set_exception
    )


@mock.patch(
    "google.cloud.pubsub_v1.subscriber._protocol.streaming_pull_manager."
    "StreamingPullManager.open",
    autospec=True,
)
def test_subscribe_options(manager_open):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    flow_control = types.FlowControl(max_bytes=42)
    scheduler = mock.sentinel.scheduler

    future = client.subscribe(
        "sub_name_a",
        callback=mock.sentinel.callback,
        flow_control=flow_control,
        scheduler=scheduler,
    )
    assert isinstance(future, futures.StreamingPullFuture)

    assert future._manager._subscription == "sub_name_a"
    assert future._manager.flow_control == flow_control
    assert future._manager._scheduler == scheduler
    manager_open.assert_called_once_with(
        mock.ANY, mock.sentinel.callback, future.set_exception
    )
