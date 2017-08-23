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

import threading
import time

import mock

from google.auth import credentials
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher.batch.base import BatchStatus
from google.cloud.pubsub_v1.publisher.batch.thread import Batch


def create_client():
    creds = mock.Mock(spec=credentials.Credentials)
    return publisher.Client(credentials=creds)


def create_batch(autocommit=False, **batch_settings):
    """Return a batch object suitable for testing.

    Args:
        autocommit (bool): Whether the batch should commit after
            ``max_latency`` seconds. By default, this is ``False``
            for unit testing.
        kwargs (dict): Arguments passed on to the
            :class:``~.pubsub_v1.types.BatchSettings`` constructor.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Batch: A batch object.
    """
    client = create_client()
    settings = types.BatchSettings(**batch_settings)
    return Batch(client, 'topic_name', settings, autocommit=autocommit)


def test_init():
    """Establish that a monitor thread is usually created on init."""
    client = create_client()

    # Do not actually create a thread, but do verify that one was created;
    # it should be running the batch's "monitor" method (which commits the
    # batch once time elapses).
    with mock.patch.object(threading, 'Thread', autospec=True) as Thread:
        batch = Batch(client, 'topic_name', types.BatchSettings())
        Thread.assert_called_once_with(target=batch.monitor)

    # New batches start able to accept messages by default.
    assert batch.status == BatchStatus.ACCEPTING_MESSAGES


def test_init_infinite_latency():
    batch = create_batch(max_latency=float('inf'))
    assert batch._thread is None


def test_client():
    client = create_client()
    settings = types.BatchSettings()
    batch = Batch(client, 'topic_name', settings, autocommit=False)
    assert batch.client is client


def test_commit():
    batch = create_batch()
    with mock.patch.object(threading, 'Thread', autospec=True) as Thread:
        batch.commit()

        # A thread should have been created to do the actual commit.
        Thread.assert_called_once_with(target=batch._commit)
        Thread.return_value.start.assert_called_once_with()

    # The batch's status needs to be something other than "accepting messages",
    # since the commit started.
    assert batch.status != BatchStatus.ACCEPTING_MESSAGES


def test_blocking_commit():
    batch = create_batch()
    futures = (
        batch.publish({'data': b'This is my message.'}),
        batch.publish({'data': b'This is another message.'}),
    )

    # Set up the underlying API publish method to return a PublishResponse.
    with mock.patch.object(type(batch.client.api), 'publish') as publish:
        publish.return_value = types.PublishResponse(message_ids=['a', 'b'])

        # Actually commit the batch.
        batch._commit()

        # Establish that the underlying API call was made with expected
        # arguments.
        publish.assert_called_once_with('topic_name', [
            types.PubsubMessage(data=b'This is my message.'),
            types.PubsubMessage(data=b'This is another message.'),
        ])

    # Establish that all of the futures are done, and that they have the
    # expected values.
    assert all([f.done() for f in futures])
    assert futures[0].result() == 'a'
    assert futures[1].result() == 'b'


def test_blocking_commit_no_messages():
    batch = create_batch()
    with mock.patch.object(type(batch.client.api), 'publish') as publish:
        batch._commit()
        assert publish.call_count == 0


def test_blocking_commit_wrong_messageid_length():
    batch = create_batch()
    futures = (
        batch.publish({'data': b'blah blah blah'}),
        batch.publish({'data': b'blah blah blah blah'}),
    )

    # Set up a PublishResponse that only returns one message ID.
    with mock.patch.object(type(batch.client.api), 'publish') as publish:
        publish.return_value = types.PublishResponse(message_ids=['a'])
        batch._commit()
    for future in futures:
        assert future.done()
        assert isinstance(future.exception(), exceptions.PublishError)


def test_monitor():
    batch = create_batch(max_latency=5.0)
    with mock.patch.object(time, 'sleep') as sleep:
        with mock.patch.object(type(batch), '_commit') as _commit:
            batch.monitor()

            # The monitor should have waited the given latency.
            sleep.assert_called_once_with(5.0)

            # Since `monitor` runs in its own thread, it should call
            # the blocking commit implementation.
            _commit.assert_called_once_with()


def test_monitor_already_committed():
    batch = create_batch(max_latency=5.0)
    batch._status = 'something else'
    with mock.patch.object(time, 'sleep') as sleep:
        batch.monitor()

        # The monitor should have waited the given latency.
        sleep.assert_called_once_with(5.0)

        # The status should not have changed.
        assert batch._status == 'something else'


def test_publish():
    batch = create_batch()
    messages = (
        types.PubsubMessage(data=b'foobarbaz'),
        types.PubsubMessage(data=b'spameggs'),
        types.PubsubMessage(data=b'1335020400'),
    )

    # Publish each of the messages, which should save them to the batch.
    for message in messages:
        batch.publish(message)

    # There should be three messages on the batch, and three futures.
    assert len(batch.messages) == 3
    assert len(batch._futures) == 3

    # The size should have been incremented by the sum of the size of the
    # messages.
    assert batch.size == sum([m.ByteSize() for m in messages])
    assert batch.size > 0  # I do not always trust protobuf.


def test_publish_dict():
    batch = create_batch()
    batch.publish({'data': b'foobarbaz', 'attributes': {'spam': 'eggs'}})

    # There should be one message on the batch.
    assert len(batch.messages) == 1

    # It should be an actual protobuf Message at this point, with the
    # expected values.
    message = batch.messages[0]
    assert isinstance(message, types.PubsubMessage)
    assert message.data == b'foobarbaz'
    assert message.attributes == {'spam': 'eggs'}
