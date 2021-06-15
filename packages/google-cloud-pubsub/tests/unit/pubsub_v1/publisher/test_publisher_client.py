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

from __future__ import absolute_import
from __future__ import division

import inspect

import grpc

import mock
import pytest
import time

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.gapic_v1.client_info import METRICS_METADATA_KEY
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types

from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher._sequencer import ordered_sequencer

from google.pubsub_v1 import types as gapic_types
from google.pubsub_v1.services.publisher import client as publisher_client
from google.pubsub_v1.services.publisher.transports.grpc import PublisherGrpcTransport


def _assert_retries_equal(retry, retry2):
    # Retry instances cannot be directly compared, because their predicates are
    # different instances of the same function. We thus manually compare their other
    # attributes, and then heuristically compare their predicates.
    for attr in ("_deadline", "_initial", "_maximum", "_multiplier"):
        assert getattr(retry, attr) == getattr(retry2, attr)

    pred = retry._predicate
    pred2 = retry2._predicate
    assert inspect.getsource(pred) == inspect.getsource(pred2)
    assert inspect.getclosurevars(pred) == inspect.getclosurevars(pred2)


def test_init(creds):
    client = publisher.Client(credentials=creds)

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.batch_settings.max_bytes == 1 * 1000 * 1000
    assert client.batch_settings.max_latency == 0.01
    assert client.batch_settings.max_messages == 100


def test_init_default_client_info(creds):
    client = publisher.Client(credentials=creds)

    installed_version = publisher.client.__version__
    expected_client_info = f"gccl/{installed_version}"

    for wrapped_method in client.api.transport._wrapped_methods.values():
        user_agent = next(
            (
                header_value
                for header, header_value in wrapped_method._metadata
                if header == METRICS_METADATA_KEY
            ),
            None,  # pragma: NO COVER
        )
        assert user_agent is not None
        assert expected_client_info in user_agent


def test_init_w_custom_transport(creds):
    transport = PublisherGrpcTransport(credentials=creds)
    client = publisher.Client(transport=transport)

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.api._transport is transport
    assert client.batch_settings.max_bytes == 1 * 1000 * 1000
    assert client.batch_settings.max_latency == 0.01
    assert client.batch_settings.max_messages == 100


def test_init_w_api_endpoint(creds):
    client_options = {"api_endpoint": "testendpoint.google.com"}
    client = publisher.Client(client_options=client_options, credentials=creds)

    assert isinstance(client.api, publisher_client.PublisherClient)
    assert (client.api._transport.grpc_channel._channel.target()).decode(
        "utf-8"
    ) == "testendpoint.google.com:443"


def test_init_w_empty_client_options(creds):
    client = publisher.Client(client_options={}, credentials=creds)

    assert isinstance(client.api, publisher_client.PublisherClient)
    assert (client.api._transport.grpc_channel._channel.target()).decode(
        "utf-8"
    ) == publisher_client.PublisherClient.SERVICE_ADDRESS


def test_init_client_options_pass_through():
    mock_ssl_creds = grpc.ssl_channel_credentials()

    def init(self, *args, **kwargs):
        self.kwargs = kwargs
        self._transport = mock.Mock()
        self._transport._host = "testendpoint.google.com"
        self._transport._ssl_channel_credentials = mock_ssl_creds

    with mock.patch.object(publisher_client.PublisherClient, "__init__", init):
        client = publisher.Client(
            client_options={
                "quota_project_id": "42",
                "scopes": [],
                "credentials_file": "file.json",
            }
        )
        client_options = client.api.kwargs["client_options"]
        assert client_options.get("quota_project_id") == "42"
        assert client_options.get("scopes") == []
        assert client_options.get("credentials_file") == "file.json"
        assert client.target == "testendpoint.google.com"
        assert client.api.transport._ssl_channel_credentials == mock_ssl_creds


def test_init_emulator(monkeypatch):
    monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "/foo/bar:123")
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = publisher.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api._transport.publish._channel
    assert channel.target().decode("utf8") == "/foo/bar:123"


def test_message_ordering_enabled(creds):
    client = publisher.Client(credentials=creds)
    assert not client._enable_message_ordering

    client = publisher.Client(
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
        credentials=creds,
    )
    assert client._enable_message_ordering


def test_publish(creds):
    client = publisher.Client(credentials=creds)

    future1 = mock.sentinel.future1
    future2 = mock.sentinel.future2
    future1.add_done_callback = mock.Mock(spec=["__call__"])
    future2.add_done_callback = mock.Mock(spec=["__call__"])

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)

    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.publish.side_effect = (future1, future2)

    topic = "topic/path"
    client._set_batch(topic, batch)

    # Begin publishing.
    future1 = client.publish(topic, b"spam")
    future2 = client.publish(topic, b"foo", bar="baz")

    assert future1 is mock.sentinel.future1
    assert future2 is mock.sentinel.future2

    # Check mock.
    batch.publish.assert_has_calls(
        [
            mock.call(gapic_types.PubsubMessage(data=b"spam")),
            mock.call(
                gapic_types.PubsubMessage(data=b"foo", attributes={"bar": "baz"})
            ),
        ]
    )


def test_publish_error_exceeding_flow_control_limits(creds):
    publisher_options = types.PublisherOptions(
        flow_control=types.PublishFlowControl(
            message_limit=10,
            byte_limit=150,
            limit_exceeded_behavior=types.LimitExceededBehavior.ERROR,
        )
    )
    client = publisher.Client(credentials=creds, publisher_options=publisher_options)

    mock_batch = mock.Mock(spec=client._batch_class)
    topic = "topic/path"
    client._set_batch(topic, mock_batch)

    future1 = client.publish(topic, b"a" * 100)
    future2 = client.publish(topic, b"b" * 100)

    future1.result()  # no error, still within flow control limits
    with pytest.raises(exceptions.FlowControlLimitError):
        future2.result()


def test_publish_data_not_bytestring_error(creds):
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(TypeError):
        client.publish(topic, "This is a text string.")
    with pytest.raises(TypeError):
        client.publish(topic, 42)


def test_publish_message_ordering_not_enabled_error(creds):
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(ValueError):
        client.publish(topic, b"bytestring body", ordering_key="ABC")


def test_publish_empty_ordering_key_when_message_ordering_enabled(creds):
    client = publisher.Client(
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
        credentials=creds,
    )
    topic = "topic/path"
    assert client.publish(topic, b"bytestring body", ordering_key="") is not None


def test_publish_with_ordering_key_uses_extended_retry_deadline(creds):
    client = publisher.Client(
        credentials=creds,
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
    )

    # Use mocks in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    future = mock.sentinel.future
    future.add_done_callback = mock.Mock(spec=["__call__"])
    batch.publish.return_value = future

    topic = "topic/path"
    client._set_batch(topic, batch)

    # Actually mock the batch class now.
    batch_class = mock.Mock(spec=(), return_value=batch)
    client._set_batch_class(batch_class)

    # Publish a message with custom retry settings.
    custom_retry = retries.Retry(
        initial=1,
        maximum=20,
        multiplier=3.3,
        deadline=999,
        predicate=retries.if_exception_type(TimeoutError, KeyboardInterrupt),
    )
    future = client.publish(topic, b"foo", ordering_key="first", retry=custom_retry)
    assert future is mock.sentinel.future

    # Check the retry settings used for the batch.
    batch_class.assert_called_once()
    _, kwargs = batch_class.call_args

    batch_commit_retry = kwargs["commit_retry"]
    expected_retry = custom_retry.with_deadline(2.0 ** 32)
    _assert_retries_equal(batch_commit_retry, expected_retry)


def test_publish_attrs_bytestring(creds):
    client = publisher.Client(credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.

    topic = "topic/path"
    client._set_batch(topic, batch)

    # Begin publishing.
    future = client.publish(topic, b"foo", bar=b"baz")

    assert future is batch.publish.return_value

    # The attributes should have been sent as text.
    batch.publish.assert_called_once_with(
        gapic_types.PubsubMessage(data=b"foo", attributes={"bar": "baz"})
    )


def test_publish_new_batch_needed(creds):
    client = publisher.Client(credentials=creds)

    # Use mocks in lieu of the actual batch class.
    batch1 = mock.Mock(spec=client._batch_class)
    batch2 = mock.Mock(spec=client._batch_class)

    # Set the first mock up to claim indiscriminately that it rejects all
    # messages and the second accepts all.
    future = mock.sentinel.future
    future.add_done_callback = mock.Mock(spec=["__call__"])
    batch1.publish.return_value = None
    batch2.publish.return_value = future

    topic = "topic/path"
    client._set_batch(topic, batch1)

    # Actually mock the batch class now.
    batch_class = mock.Mock(spec=(), return_value=batch2)
    client._set_batch_class(batch_class)

    # Publish a message.
    future = client.publish(topic, b"foo", bar=b"baz")
    assert future is mock.sentinel.future

    # Check the mocks.
    batch_class.assert_called_once_with(
        client=mock.ANY,
        topic=topic,
        settings=client.batch_settings,
        batch_done_callback=None,
        commit_when_full=True,
        commit_retry=gapic_v1.method.DEFAULT,
        commit_timeout=gapic_v1.method.DEFAULT,
    )
    message_pb = gapic_types.PubsubMessage(data=b"foo", attributes={"bar": "baz"})
    batch1.publish.assert_called_once_with(message_pb)
    batch2.publish.assert_called_once_with(message_pb)


def test_publish_attrs_type_error(creds):
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(TypeError):
        client.publish(topic, b"foo", answer=42)


def test_publish_custom_retry_overrides_configured_retry(creds):
    client = publisher.Client(
        credentials=creds,
        publisher_options=types.PublisherOptions(retry=mock.sentinel.publish_retry),
    )

    topic = "topic/path"
    client._flow_controller = mock.Mock()
    fake_sequencer = mock.Mock()
    client._get_or_create_sequencer = mock.Mock(return_value=fake_sequencer)
    client.publish(topic, b"hello!", retry=mock.sentinel.custom_retry)

    fake_sequencer.publish.assert_called_once_with(
        mock.ANY, retry=mock.sentinel.custom_retry, timeout=mock.ANY
    )
    message = fake_sequencer.publish.call_args.args[0]
    assert message.data == b"hello!"


def test_publish_custom_timeout_overrides_configured_timeout(creds):
    client = publisher.Client(
        credentials=creds,
        publisher_options=types.PublisherOptions(timeout=mock.sentinel.publish_timeout),
    )

    topic = "topic/path"
    client._flow_controller = mock.Mock()
    fake_sequencer = mock.Mock()
    client._get_or_create_sequencer = mock.Mock(return_value=fake_sequencer)
    client.publish(topic, b"hello!", timeout=mock.sentinel.custom_timeout)

    fake_sequencer.publish.assert_called_once_with(
        mock.ANY, retry=mock.ANY, timeout=mock.sentinel.custom_timeout
    )
    message = fake_sequencer.publish.call_args.args[0]
    assert message.data == b"hello!"


def test_stop(creds):
    client = publisher.Client(credentials=creds)

    batch1 = mock.Mock(spec=client._batch_class)
    topic = "topic/path"
    client._set_batch(topic, batch1)

    client.stop()

    assert batch1.commit.call_count == 1

    with pytest.raises(RuntimeError):
        client.publish("topic1", b"msg2")

    with pytest.raises(RuntimeError):
        client.resume_publish("topic", "ord_key")

    with pytest.raises(RuntimeError):
        client.stop()


def test_gapic_instance_method(creds):
    client = publisher.Client(credentials=creds)

    transport_mock = mock.Mock(create_topic=mock.sentinel)
    fake_create_topic_rpc = mock.Mock()
    transport_mock._wrapped_methods = {
        transport_mock.create_topic: fake_create_topic_rpc
    }
    patcher = mock.patch.object(client.api, "_transport", new=transport_mock)

    topic = gapic_types.Topic(name="projects/foo/topics/bar")

    with patcher:
        client.create_topic(topic)

    assert fake_create_topic_rpc.call_count == 1
    _, args, _ = fake_create_topic_rpc.mock_calls[0]
    assert args[0] == gapic_types.Topic(name="projects/foo/topics/bar")


def test_gapic_class_method_on_class():
    answer = publisher.Client.topic_path("foo", "bar")
    assert answer == "projects/foo/topics/bar"


def test_class_method_factory():
    patch = mock.patch(
        "google.oauth2.service_account.Credentials.from_service_account_file"
    )

    with patch:
        client = publisher.Client.from_service_account_file("filename.json")

    assert isinstance(client, publisher.Client)


def test_gapic_class_method_on_instance(creds):
    client = publisher.Client(credentials=creds)
    answer = client.topic_path("foo", "bar")
    assert answer == "projects/foo/topics/bar"


def test_commit_thread_created_on_publish(creds):
    # Max latency is not infinite so a commit thread is created.
    batch_settings = types.BatchSettings(max_latency=600)
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    with mock.patch.object(
        client, "_start_commit_thread", autospec=True
    ) as _start_commit_thread:
        # First publish should create a commit thread.
        assert client.publish("topic", b"bytestring body", ordering_key="") is not None
        _start_commit_thread.assert_called_once()

        # Since _start_commit_thread is a mock, no actual thread has been
        # created, so let's put a sentinel there to mimic real behavior.
        client._commit_thread = mock.Mock()

        # Second publish should not create a commit thread since one (the mock)
        # already exists.
        assert client.publish("topic", b"bytestring body", ordering_key="") is not None
        # Call count should remain 1.
        _start_commit_thread.assert_called_once()


def test_commit_thread_not_created_on_publish_if_max_latency_is_inf(creds):
    # Max latency is infinite so a commit thread is not created.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    assert client.publish("topic", b"bytestring body", ordering_key="") is not None
    assert client._commit_thread is None


def test_wait_and_commit_sequencers(creds):
    # Max latency is infinite so a commit thread is not created.
    # We don't want a commit thread to interfere with this test.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    # Mock out time so no sleep is actually done.
    with mock.patch.object(time, "sleep"):
        with mock.patch.object(client, "_commit_sequencers") as _commit_sequencers:
            assert (
                client.publish("topic", b"bytestring body", ordering_key="") is not None
            )
            # Call _wait_and_commit_sequencers to simulate what would happen if a
            # commit thread actually ran.
            client._wait_and_commit_sequencers()
            assert _commit_sequencers.call_count == 1


def test_stopped_client_does_not_commit_sequencers(creds):
    # Max latency is infinite so a commit thread is not created.
    # We don't want a commit thread to interfere with this test.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    # Mock out time so no sleep is actually done.
    with mock.patch.object(time, "sleep"):
        with mock.patch.object(client, "_commit_sequencers") as _commit_sequencers:
            assert (
                client.publish("topic", b"bytestring body", ordering_key="") is not None
            )

            client.stop()

            # Call _wait_and_commit_sequencers to simulate what would happen if a
            # commit thread actually ran after the client was stopped.
            client._wait_and_commit_sequencers()
            # Should not be called since Client is stopped.
            assert _commit_sequencers.call_count == 0


def test_publish_with_ordering_key(creds):
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)

    # Set the mock up to claim indiscriminately that it accepts all messages.
    future1 = mock.sentinel.future1
    future2 = mock.sentinel.future2
    future1.add_done_callback = mock.Mock(spec=["__call__"])
    future2.add_done_callback = mock.Mock(spec=["__call__"])

    batch.publish.side_effect = (future1, future2)

    topic = "topic/path"
    ordering_key = "k1"
    client._set_batch(topic, batch, ordering_key=ordering_key)

    # Begin publishing.
    future1 = client.publish(topic, b"spam", ordering_key=ordering_key)
    future2 = client.publish(topic, b"foo", bar="baz", ordering_key=ordering_key)

    assert future1 is mock.sentinel.future1
    assert future2 is mock.sentinel.future2

    # Check mock.
    batch.publish.assert_has_calls(
        [
            mock.call(gapic_types.PubsubMessage(data=b"spam", ordering_key="k1")),
            mock.call(
                gapic_types.PubsubMessage(
                    data=b"foo", attributes={"bar": "baz"}, ordering_key="k1"
                )
            ),
        ]
    )


def test_ordered_sequencer_cleaned_up(creds):
    # Max latency is infinite so a commit thread is not created.
    # We don't want a commit thread to interfere with this test.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(
        batch_settings=batch_settings,
        publisher_options=publisher_options,
        credentials=creds,
    )

    topic = "topic"
    ordering_key = "ord_key"
    sequencer = mock.Mock(spec=ordered_sequencer.OrderedSequencer)
    sequencer.is_finished.return_value = False
    client._set_sequencer(topic=topic, sequencer=sequencer, ordering_key=ordering_key)

    assert len(client._sequencers) == 1
    # 'sequencer' is not finished yet so don't remove it.
    client._commit_sequencers()
    assert len(client._sequencers) == 1

    sequencer.is_finished.return_value = True
    # 'sequencer' is finished so remove it.
    client._commit_sequencers()
    assert len(client._sequencers) == 0


def test_resume_publish(creds):
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    topic = "topic"
    ordering_key = "ord_key"
    sequencer = mock.Mock(spec=ordered_sequencer.OrderedSequencer)
    client._set_sequencer(topic=topic, sequencer=sequencer, ordering_key=ordering_key)

    client.resume_publish(topic, ordering_key)
    assert sequencer.unpause.called_once()


def test_resume_publish_no_sequencer_found(creds):
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Check no exception is thrown if a sequencer with the (topic, ordering_key)
    # pair does not exist.
    client.resume_publish("topic", "ord_key")


def test_resume_publish_ordering_keys_not_enabled(creds):
    publisher_options = types.PublisherOptions(enable_message_ordering=False)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Throw on calling resume_publish() when enable_message_ordering is False.
    with pytest.raises(ValueError):
        client.resume_publish("topic", "ord_key")
