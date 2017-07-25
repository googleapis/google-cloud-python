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

import time

import mock

import pytest

from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher.batch.thread import Batch
from google.cloud.pubsub_v1.publisher.batch.thread import Future


def create_batch(status=None):
    """Create a batch object, which does not commit.

    Args:
        status (str): If provided, the batch's internal status will be set
            to the provided status.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Batch: The batch object
    """
    client = publisher.Client()
    batch_settings = types.BatchSettings()
    batch = Batch(client, 'topic_name', batch_settings, autocommit=False)
    if status:
        batch._status = status
    return batch


def create_future(batch=None):
    """Create a Future object to test.

    Args:
        ~.pubsub_v1.publisher.batch.thread.Batch: A batch object, such
            as one returned from :meth:`create_batch`. If none is provided,
            a batch will be automatically created.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Future: The Future object (the
            class being tested in this module).
    """
    if batch is None:
        batch = create_batch()
    return Future(batch=batch)


def test_cancel():
    assert create_future().cancel() is False


def test_cancelled():
    assert create_future().cancelled() is False


def test_running():
    assert create_future().running() is True


def test_done():
    batch = create_batch()
    future = create_future(batch=batch)
    assert future.done() is False
    batch._status = batch.Status.SUCCESS
    assert future._batch.status == 'success'
    assert future.done() is True


def test_exception_no_error():
    batch = create_batch(status='success')
    future = create_future(batch=batch)
    assert future.exception() is None


def test_exception_with_error():
    batch = create_batch(status='error')
    batch.error = RuntimeError('Something really bad happened.')
    future = create_future(batch=batch)

    # Make sure that the exception that is returned is the batch's error.
    # Also check the type to ensure the batch's error did not somehow
    # change internally.
    assert future.exception() is batch.error
    assert isinstance(future.exception(), RuntimeError)


def test_exception_timeout():
    future = create_future()
    with mock.patch.object(time, 'sleep') as sleep:
        with pytest.raises(exceptions.TimeoutError):
            future.exception(timeout=10)

        # The sleep should have been called with 1, 2, 4, then 3 seconds
        # (the first three due to linear backoff, then the last one because
        # only three seconds were left before the timeout was to be hit).
        assert sleep.call_count == 4
        assert sleep.mock_calls[0]


def test_result_no_error():
    batch = create_batch(status='success')
    future = create_future(batch=batch)
    batch.message_ids[hash(future)] = '42'
    assert future.result() == '42'


def test_result_with_error():
    batch = create_batch(status='error')
    batch.error = RuntimeError('Something really bad happened.')
    future = create_future(batch=batch)
    with pytest.raises(RuntimeError):
        future.result()


def test_add_done_callback_pending_batch():
    future = create_future()
    callback = mock.Mock()
    future.add_done_callback(callback)
    assert len(future._callbacks) == 1
    assert callback in future._callbacks
    assert callback.call_count == 0


def test_add_done_callback_completed_batch():
    batch = create_batch(status='success')
    future = create_future(batch=batch)
    callback = mock.Mock()
    future.add_done_callback(callback)
    callback.assert_called_once_with(future)


def test_trigger():
    future = create_future()
    callback = mock.Mock()
    future.add_done_callback(callback)
    assert callback.call_count == 0
    future._trigger()
    callback.assert_called_once_with(future)
