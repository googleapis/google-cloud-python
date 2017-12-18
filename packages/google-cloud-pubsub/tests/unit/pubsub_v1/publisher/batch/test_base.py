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

import mock

from google.auth import credentials
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher.batch.base import BatchStatus
from google.cloud.pubsub_v1.publisher.batch.thread import Batch


def create_batch(status=None, settings=types.BatchSettings()):
    """Create a batch object, which does not commit.

    Args:
        status (str): If provided, the batch's internal status will be set
            to the provided status.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Batch: The batch object
    """
    creds = mock.Mock(spec=credentials.Credentials)
    client = publisher.Client(credentials=creds)
    batch = Batch(client, 'topic_name', settings, autocommit=False)
    if status:
        batch._status = status
    return batch


def test_len():
    batch = create_batch(status=BatchStatus.ACCEPTING_MESSAGES)
    assert len(batch) == 0
    batch.publish(types.PubsubMessage(data=b'foo'))
    assert len(batch) == 1


def test_will_accept():
    batch = create_batch(status=BatchStatus.ACCEPTING_MESSAGES)
    message = types.PubsubMessage()
    assert batch.will_accept(message) is True


def test_will_not_accept_status():
    batch = create_batch(status='talk to the hand')
    message = types.PubsubMessage()
    assert batch.will_accept(message) is False


def test_will_not_accept_size():
    batch = create_batch(
        settings=types.BatchSettings(max_bytes=10),
        status=BatchStatus.ACCEPTING_MESSAGES,
    )
    message = types.PubsubMessage(data=b'abcdefghijklmnopqrstuvwxyz')
    assert batch.will_accept(message) is False


def test_will_not_accept_number():
    batch = create_batch(
        settings=types.BatchSettings(max_messages=-1),
        status=BatchStatus.ACCEPTING_MESSAGES,
    )
    message = types.PubsubMessage(data=b'abc')
    assert batch.will_accept(message) is False
