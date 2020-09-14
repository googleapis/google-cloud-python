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
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import futures
from google.pubsub_v1.services.subscriber import client as subscriber_client
from google.pubsub_v1.services.subscriber.transports.grpc import SubscriberGrpcTransport


def test_init():
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    assert isinstance(client.api, subscriber_client.SubscriberClient)


def test_init_w_custom_transport():
    transport = SubscriberGrpcTransport()
    client = subscriber.Client(transport=transport)
    assert isinstance(client.api, subscriber_client.SubscriberClient)
    assert client.api._transport is transport


def test_init_w_api_endpoint():
    client_options = {"api_endpoint": "testendpoint.google.com"}
    client = subscriber.Client(client_options=client_options)

    assert isinstance(client.api, subscriber_client.SubscriberClient)
    assert (client.api._transport.grpc_channel._channel.target()).decode(
        "utf-8"
    ) == "testendpoint.google.com"


def test_init_w_unicode_api_endpoint():
    client_options = {"api_endpoint": u"testendpoint.google.com"}
    client = subscriber.Client(client_options=client_options)

    assert isinstance(client.api, subscriber_client.SubscriberClient)
    assert (client.api._transport.grpc_channel._channel.target()).decode(
        "utf-8"
    ) == "testendpoint.google.com"


def test_init_w_empty_client_options():
    client = subscriber.Client(client_options={})

    assert isinstance(client.api, subscriber_client.SubscriberClient)
    assert (client.api._transport.grpc_channel._channel.target()).decode(
        "utf-8"
    ) == subscriber_client.SubscriberClient.SERVICE_ADDRESS


def test_init_client_options_pass_through():
    def init(self, *args, **kwargs):
        self.kwargs = kwargs

    with mock.patch.object(subscriber_client.SubscriberClient, "__init__", init):
        client = subscriber.Client(
            client_options={
                "quota_project_id": "42",
                "scopes": [],
                "credentials_file": "file.json",
            }
        )
        client_options = client._api.kwargs["client_options"]
        assert client_options.get("quota_project_id") == "42"
        assert client_options.get("scopes") == []
        assert client_options.get("credentials_file") == "file.json"


def test_init_emulator(monkeypatch):
    monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "/baz/bacon/")
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = subscriber.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api._transport.pull._channel
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
        mock.ANY,
        callback=mock.sentinel.callback,
        on_callback_error=future.set_exception,
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
        mock.ANY,
        callback=mock.sentinel.callback,
        on_callback_error=future.set_exception,
    )


def test_close():
    client = subscriber.Client()
    patcher = mock.patch.object(client.api._transport.grpc_channel, "close")

    with patcher as patched_close:
        client.close()

    patched_close.assert_called()


def test_closes_channel_as_context_manager():
    client = subscriber.Client()
    patcher = mock.patch.object(client.api._transport.grpc_channel, "close")

    with patcher as patched_close:
        with client:
            pass

    patched_close.assert_called()


def test_streaming_pull_gapic_monkeypatch():
    client = subscriber.Client()

    with mock.patch("google.api_core.gapic_v1.method.wrap_method"):
        client.streaming_pull(requests=iter([]))

    transport = client.api._transport
    assert hasattr(transport.streaming_pull, "_prefetch_first_result_")
    assert not transport.streaming_pull._prefetch_first_result_
