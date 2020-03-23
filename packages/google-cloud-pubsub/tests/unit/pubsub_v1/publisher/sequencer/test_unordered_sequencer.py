# Copyright 2019, Google LLC All rights reserved.
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
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher._batch import base
from google.cloud.pubsub_v1.publisher._sequencer import unordered_sequencer


def create_message():
    return types.PubsubMessage(data=b"foo", attributes={"bar": u"baz"})


def create_client():
    creds = mock.Mock(spec=credentials.Credentials)
    return publisher.Client(credentials=creds)


def test_stop():
    client = create_client()
    message = create_message()

    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")

    sequencer.publish(message)
    sequencer.stop()

    # Publish after stop() throws
    with pytest.raises(RuntimeError):
        sequencer.publish(message)

    # Commit after stop() throws
    with pytest.raises(RuntimeError):
        sequencer.commit()

    # Stop after stop() throws
    with pytest.raises(RuntimeError):
        sequencer.stop()


def test_commit():
    client = create_client()
    batch = mock.Mock(spec=client._batch_class)

    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    sequencer._set_batch(batch)

    sequencer.commit()
    batch.commit.assert_called_once()


def test_commit_no_batch():
    client = create_client()
    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    sequencer.commit()


def test_unpause():
    client = create_client()
    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    with pytest.raises(NotImplementedError):
        sequencer.unpause()


def test_basic_publish():
    client = create_client()
    message = create_message()
    batch = mock.Mock(spec=client._batch_class)

    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    sequencer._set_batch(batch)

    sequencer.publish(message)
    batch.publish.assert_called_once_with(message)


def test_publish_batch_full():
    client = create_client()
    message = create_message()
    batch = mock.Mock(spec=client._batch_class)
    # Make batch full.
    batch.publish.return_value = None

    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    sequencer._set_batch(batch)

    # Will create a new batch since the old one is full, and return a future.
    future = sequencer.publish(message)
    batch.publish.assert_called_once_with(message)
    assert future is not None


def test_publish_after_batch_error():
    client = create_client()
    message = create_message()
    batch = mock.Mock(spec=client._batch_class)

    sequencer = unordered_sequencer.UnorderedSequencer(client, "topic_name")
    sequencer._set_batch(batch)

    sequencer.commit()
    batch.commit.assert_called_once()

    # Simulate publish RPC failing.
    batch._set_status(base.BatchStatus.ERROR)

    # Will create a new batch since the old one has been committed. The fact
    # that the old batch errored should not matter in the publish of the next
    # message.
    future = sequencer.publish(message)
    assert future is not None
