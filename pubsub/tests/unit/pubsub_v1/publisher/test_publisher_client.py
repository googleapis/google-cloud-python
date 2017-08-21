# Copyright 2017, Google Inc. All rights reserved.
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

import mock

import pytest

from google.auth import credentials
from google.cloud.gapic.pubsub.v1 import publisher_client
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types


def create_client():
    creds = mock.Mock(spec=credentials.Credentials)
    return publisher.Client(credentials=creds)


def test_init():
    client = create_client()

    # A plain client should have an `api` (the underlying GAPIC) and a
    # batch settings object, which should have the defaults.
    assert isinstance(client.api, publisher_client.PublisherClient)
    assert client.batch_settings.max_bytes == 5 * (2 ** 20)
    assert client.batch_settings.max_latency == 0.05
    assert client.batch_settings.max_messages == 1000


def test_batch_accepting():
    """Establish that an existing batch is returned if it accepts messages."""
    client = create_client()
    message = types.PubsubMessage(data=b'foo')

    # At first, there are no batches, so this should return a new batch
    # which is also saved to the object.
    ante = len(client._batches)
    batch = client.batch('topic_name', message, autocommit=False)
    assert len(client._batches) == ante + 1
    assert batch is client._batches['topic_name']

    # A subsequent request should return the same batch.
    batch2 = client.batch('topic_name', message, autocommit=False)
    assert batch is batch2
    assert batch2 is client._batches['topic_name']


def test_batch_without_autocreate():
    client = create_client()
    message = types.PubsubMessage(data=b'foo')

    # If `create=False` is sent, then when the batch is not found, None
    # is returned instead.
    ante = len(client._batches)
    batch = client.batch('topic_name', message, create=False)
    assert batch is None
    assert len(client._batches) == ante


def test_publish():
    client = create_client()

    # Use a mock in lieu of the actual batch class; set the mock up to claim
    # indiscriminately that it accepts all messages.
    batch = mock.Mock(spec=client._batch_class)
    batch.will_accept.return_value = True
    client._batches['topic_name'] = batch

    # Begin publishing.
    client.publish('topic_name', b'spam')
    client.publish('topic_name', b'foo', bar='baz')

    # The batch's publish method should have been called twice.
    assert batch.publish.call_count == 2

    # In both cases
    # The first call should correspond to the first message.
    _, args, _ = batch.publish.mock_calls[0]
    assert args[0].data == b'spam'
    assert not args[0].attributes

    # The second call should correspond to the second message.
    _, args, _ = batch.publish.mock_calls[1]
    assert args[0].data == b'foo'
    assert args[0].attributes == {u'bar': u'baz'}


def test_publish_data_not_bytestring_error():
    client = create_client()
    with pytest.raises(TypeError):
        client.publish('topic_name', u'This is a text string.')
    with pytest.raises(TypeError):
        client.publish('topic_name', 42)


def test_publish_attrs_bytestring():
    client = create_client()

    # Use a mock in lieu of the actual batch class; set the mock up to claim
    # indiscriminately that it accepts all messages.
    batch = mock.Mock(spec=client._batch_class)
    batch.will_accept.return_value = True
    client._batches['topic_name'] = batch

    # Begin publishing.
    client.publish('topic_name', b'foo', bar=b'baz')

    # The attributes should have been sent as text.
    _, args, _ = batch.publish.mock_calls[0]
    assert args[0].data == b'foo'
    assert args[0].attributes == {u'bar': u'baz'}


def test_publish_attrs_type_error():
    client = create_client()
    with pytest.raises(TypeError):
        client.publish('topic_name', b'foo', answer=42)


def test_gapic_instance_method():
    client = create_client()
    with mock.patch.object(client.api, '_create_topic', autospec=True) as ct:
        client.create_topic('projects/foo/topics/bar')
        assert ct.call_count == 1
        _, args, _ = ct.mock_calls[0]
        assert args[0] == types.Topic(name='projects/foo/topics/bar')


def test_gapic_class_method():
    client = create_client()
    answer = client.topic_path('foo', 'bar')
    assert answer == 'projects/foo/topics/bar'
