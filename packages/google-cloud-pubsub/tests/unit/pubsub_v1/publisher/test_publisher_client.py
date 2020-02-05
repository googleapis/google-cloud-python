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

from google.auth import credentials

import mock
import pytest
import time

from google.cloud.pubsub_v1.gapic import publisher_client
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types

from google.cloud.pubsub_v1.publisher._sequencer import ordered_sequencer


def test_init():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.batch_settings.max_bytes == 1 * 1000 * 1000
    assert client.batch_settings.max_latency == 0.01
    assert client.batch_settings.max_messages == 100


def test_init_w_custom_transport():
    transport = object()
    client = publisher.Client(transport=transport)

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.api.transport is transport
    assert client.batch_settings.max_bytes == 1 * 1000 * 1000
    assert client.batch_settings.max_latency == 0.01
    assert client.batch_settings.max_messages == 100


def test_init_emulator(monkeypatch):
    monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "/foo/bar/")
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = publisher.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api.transport.publish._channel
    assert channel.target().decode("utf8") == "/foo/bar/"


def test_message_ordering_enabled():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    assert not client._enable_message_ordering

    client = publisher.Client(
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
        credentials=creds,
    )
    assert client._enable_message_ordering


def test_message_ordering_changes_retry_deadline():
    creds = mock.Mock(spec=credentials.Credentials)

    client = publisher.Client(credentials=creds)
    assert client.api._method_configs["Publish"].retry._deadline == 60

    client = publisher.Client(
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
        credentials=creds,
    )
    assert client.api._method_configs["Publish"].retry._deadline == 2 ** 32 / 1000


def test_publish():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.will_accept.return_value = True
    batch.publish.side_effect = (mock.sentinel.future1, mock.sentinel.future2)

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
            mock.call(types.PubsubMessage(data=b"spam")),
            mock.call(types.PubsubMessage(data=b"foo", attributes={"bar": "baz"})),
        ]
    )


def test_publish_data_not_bytestring_error():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(TypeError):
        client.publish(topic, u"This is a text string.")
    with pytest.raises(TypeError):
        client.publish(topic, 42)


def test_publish_message_ordering_not_enabled_error():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(ValueError):
        client.publish(topic, b"bytestring body", ordering_key="ABC")


def test_publish_empty_ordering_key_when_message_ordering_enabled():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(
        publisher_options=types.PublisherOptions(enable_message_ordering=True),
        credentials=creds,
    )
    topic = "topic/path"
    assert client.publish(topic, b"bytestring body", ordering_key="") is not None


def test_publish_attrs_bytestring():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.will_accept.return_value = True

    topic = "topic/path"
    client._set_batch(topic, batch)

    # Begin publishing.
    future = client.publish(topic, b"foo", bar=b"baz")

    assert future is batch.publish.return_value

    # The attributes should have been sent as text.
    batch.publish.assert_called_once_with(
        types.PubsubMessage(data=b"foo", attributes={"bar": u"baz"})
    )


def test_publish_new_batch_needed():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # Use mocks in lieu of the actual batch class.
    batch1 = mock.Mock(spec=client._batch_class)
    batch2 = mock.Mock(spec=client._batch_class)
    # Set the first mock up to claim indiscriminately that it rejects all
    # messages and the second accepts all.
    batch1.publish.return_value = None
    batch2.publish.return_value = mock.sentinel.future

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
    )
    message_pb = types.PubsubMessage(data=b"foo", attributes={"bar": u"baz"})
    batch1.publish.assert_called_once_with(message_pb)
    batch2.publish.assert_called_once_with(message_pb)


def test_publish_attrs_type_error():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = "topic/path"
    with pytest.raises(TypeError):
        client.publish(topic, b"foo", answer=42)


def test_stop():
    creds = mock.Mock(spec=credentials.Credentials)
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


def test_gapic_instance_method():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    ct = mock.Mock()
    client.api._inner_api_calls["create_topic"] = ct

    client.create_topic("projects/foo/topics/bar")
    assert ct.call_count == 1
    _, args, _ = ct.mock_calls[0]
    assert args[0] == types.Topic(name="projects/foo/topics/bar")


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


def test_gapic_class_method_on_instance():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    answer = client.topic_path("foo", "bar")
    assert answer == "projects/foo/topics/bar"


def test_commit_thread_created_on_publish():
    creds = mock.Mock(spec=credentials.Credentials)
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


def test_commit_thread_not_created_on_publish_if_max_latency_is_inf():
    creds = mock.Mock(spec=credentials.Credentials)
    # Max latency is infinite so a commit thread is not created.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    assert client.publish("topic", b"bytestring body", ordering_key="") is not None
    assert client._commit_thread is None


def test_wait_and_commit_sequencers():
    creds = mock.Mock(spec=credentials.Credentials)
    # Max latency is infinite so a commit thread is not created.
    # We don't want a commit thread to interfere with this test.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    # Mock out time so no sleep is actually done.
    with mock.patch.object(time, "sleep"):
        with mock.patch.object(
            publisher.Client, "_commit_sequencers"
        ) as _commit_sequencers:
            assert (
                client.publish("topic", b"bytestring body", ordering_key="") is not None
            )
            # Call _wait_and_commit_sequencers to simulate what would happen if a
            # commit thread actually ran.
            client._wait_and_commit_sequencers()
            assert _commit_sequencers.call_count == 1


def test_stopped_client_does_not_commit_sequencers():
    creds = mock.Mock(spec=credentials.Credentials)
    # Max latency is infinite so a commit thread is not created.
    # We don't want a commit thread to interfere with this test.
    batch_settings = types.BatchSettings(max_latency=float("inf"))
    client = publisher.Client(batch_settings=batch_settings, credentials=creds)

    # Mock out time so no sleep is actually done.
    with mock.patch.object(time, "sleep"):
        with mock.patch.object(
            publisher.Client, "_commit_sequencers"
        ) as _commit_sequencers:
            assert (
                client.publish("topic", b"bytestring body", ordering_key="") is not None
            )

            client.stop()

            # Call _wait_and_commit_sequencers to simulate what would happen if a
            # commit thread actually ran after the client was stopped.
            client._wait_and_commit_sequencers()
            # Should not be called since Client is stopped.
            assert _commit_sequencers.call_count == 0


def test_publish_with_ordering_key():
    creds = mock.Mock(spec=credentials.Credentials)
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.will_accept.return_value = True
    batch.publish.side_effect = (mock.sentinel.future1, mock.sentinel.future2)

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
            mock.call(types.PubsubMessage(data=b"spam", ordering_key="k1")),
            mock.call(
                types.PubsubMessage(
                    data=b"foo", attributes={"bar": "baz"}, ordering_key="k1"
                )
            ),
        ]
    )


def test_ordered_sequencer_cleaned_up():
    creds = mock.Mock(spec=credentials.Credentials)
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


def test_resume_publish():
    creds = mock.Mock(spec=credentials.Credentials)
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    topic = "topic"
    ordering_key = "ord_key"
    sequencer = mock.Mock(spec=ordered_sequencer.OrderedSequencer)
    client._set_sequencer(topic=topic, sequencer=sequencer, ordering_key=ordering_key)

    client.resume_publish(topic, ordering_key)
    assert sequencer.unpause.called_once()


def test_resume_publish_no_sequencer_found():
    creds = mock.Mock(spec=credentials.Credentials)
    publisher_options = types.PublisherOptions(enable_message_ordering=True)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Check no exception is thrown if a sequencer with the (topic, ordering_key)
    # pair does not exist.
    client.resume_publish("topic", "ord_key")


def test_resume_publish_ordering_keys_not_enabled():
    creds = mock.Mock(spec=credentials.Credentials)
    publisher_options = types.PublisherOptions(enable_message_ordering=False)
    client = publisher.Client(publisher_options=publisher_options, credentials=creds)

    # Throw on calling resume_publish() when enable_message_ordering is False.
    with pytest.raises(ValueError):
        client.resume_publish("topic", "ord_key")
