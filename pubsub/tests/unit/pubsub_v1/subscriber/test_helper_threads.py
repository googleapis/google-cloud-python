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

import mock
from six.moves import queue

from google.cloud.pubsub_v1.subscriber import _helper_threads


def test_queue_callback_worker():
    queue_ = queue.Queue()
    callback = mock.Mock(spec=())
    qct = _helper_threads.QueueCallbackWorker(queue_, callback)

    # Set up an appropriate mock for the queue, and call the queue callback
    # thread.
    with mock.patch.object(queue.Queue, 'get') as get:
        item1 = ('action', mock.sentinel.A)
        get.side_effect = (item1, _helper_threads.STOP)
        qct()

        # Assert that we got the expected calls.
        assert get.call_count == 2
        callback.assert_called_once_with('action', mock.sentinel.A)


def test_queue_callback_worker_exception():
    queue_ = queue.Queue()
    callback = mock.Mock(spec=(), side_effect=(Exception,))
    qct = _helper_threads.QueueCallbackWorker(queue_, callback)

    # Set up an appropriate mock for the queue, and call the queue callback
    # thread.
    with mock.patch.object(queue.Queue, 'get') as get:
        item1 = ('action', mock.sentinel.A)
        get.side_effect = (item1, _helper_threads.STOP)
        qct()

        # Assert that we got the expected calls.
        assert get.call_count == 2
        callback.assert_called_once_with('action', mock.sentinel.A)
