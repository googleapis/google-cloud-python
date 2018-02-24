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

from google.auth import credentials

import mock
import pytest

from google.cloud.pubsub_v1.gapic import publisher_client
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types


def test_init():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.batch_settings.max_bytes == 10 * (2 ** 20)
    assert client.batch_settings.max_latency == 0.05
    assert client.batch_settings.max_messages == 1000


def test_init_emulator(monkeypatch):
    monkeypatch.setenv('PUBSUB_EMULATOR_HOST', '/foo/bar/')
    # NOTE: When the emulator host is set, a custom channel will be used, so
    #       no credentials (mock ot otherwise) can be passed in.
    client = publisher.Client()

    # Establish that a gRPC request would attempt to hit the emulator host.
    #
    # Sadly, there seems to be no good way to do this without poking at
    # the private API of gRPC.
    channel = client.api.publisher_stub.Publish._channel
    assert channel.target().decode('utf8') == '/foo/bar/'


def test_batch_create():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    assert len(client._batches) == 0
    topic = 'topic/path'
    batch = client.batch(topic, autocommit=False)
    assert client._batches == {topic: batch}


def test_batch_exists():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    topic = 'topic/path'
    client._batches[topic] = mock.sentinel.batch

    # A subsequent request should return the same batch.
    batch = client.batch(topic, autocommit=False)
    assert batch is mock.sentinel.batch
    assert client._batches == {topic: batch}


def test_batch_create_and_exists():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    topic = 'topic/path'
    client._batches[topic] = mock.sentinel.batch

    # A subsequent request should return the same batch.
    batch = client.batch(topic, create=True, autocommit=False)
    assert batch is not mock.sentinel.batch
    assert client._batches == {topic: batch}


def test_publish():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.will_accept.return_value = True
    batch.publish.side_effect = (
        mock.sentinel.future1,
        mock.sentinel.future2,
    )

    topic = 'topic/path'
    client._batches[topic] = batch

    # Begin publishing.
    future1 = client.publish(topic, b'spam')
    future2 = client.publish(topic, b'foo', bar='baz')

    assert future1 is mock.sentinel.future1
    assert future2 is mock.sentinel.future2

    # Check mock.
    batch.publish.assert_has_calls(
        [
            mock.call(types.PubsubMessage(data=b'spam')),
            mock.call(types.PubsubMessage(
                data=b'foo',
                attributes={'bar': 'baz'},
            )),
        ],
    )


def test_publish_data_not_bytestring_error():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = 'topic/path'
    with pytest.raises(TypeError):
        client.publish(topic, u'This is a text string.')
    with pytest.raises(TypeError):
        client.publish(topic, 42)


def test_publish_data_too_large():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = 'topic/path'
    client.batch_settings = types.BatchSettings(
        0,
        client.batch_settings.max_latency,
        client.batch_settings.max_messages
    )
    with pytest.raises(ValueError):
        client.publish(topic, b'This is a text string.')


def test_publish_attrs_bytestring():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)

    # Use a mock in lieu of the actual batch class.
    batch = mock.Mock(spec=client._batch_class)
    # Set the mock up to claim indiscriminately that it accepts all messages.
    batch.will_accept.return_value = True

    topic = 'topic/path'
    client._batches[topic] = batch

    # Begin publishing.
    future = client.publish(topic, b'foo', bar=b'baz')

    assert future is batch.publish.return_value

    # The attributes should have been sent as text.
    batch.publish.assert_called_once_with(
        types.PubsubMessage(
            data=b'foo',
            attributes={'bar': u'baz'},
        ),
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

    topic = 'topic/path'
    client._batches[topic] = batch1

    # Actually mock the batch class now.
    batch_class = mock.Mock(spec=(), return_value=batch2)
    client._batch_class = batch_class

    # Publish a message.
    future = client.publish(topic, b'foo', bar=b'baz')
    assert future is mock.sentinel.future

    # Check the mocks.
    batch_class.assert_called_once_with(
        autocommit=True,
        client=client,
        settings=client.batch_settings,
        topic=topic,
    )
    message_pb = types.PubsubMessage(
        data=b'foo',
        attributes={'bar': u'baz'},
    )
    batch1.publish.assert_called_once_with(message_pb)
    batch2.publish.assert_called_once_with(message_pb)


def test_publish_attrs_type_error():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    topic = 'topic/path'
    with pytest.raises(TypeError):
        client.publish(topic, b'foo', answer=42)


def test_gapic_instance_method():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    with mock.patch.object(client.api, '_create_topic', autospec=True) as ct:
        client.create_topic('projects/foo/topics/bar')
        assert ct.call_count == 1
        _, args, _ = ct.mock_calls[0]
        assert args[0] == types.Topic(name='projects/foo/topics/bar')


def test_gapic_class_method():
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    answer = client.topic_path('foo', 'bar')
    assert answer == 'projects/foo/topics/bar'
