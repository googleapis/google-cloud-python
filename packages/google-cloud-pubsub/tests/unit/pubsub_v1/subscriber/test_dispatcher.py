# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading

from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber._protocol import requests
from google.cloud.pubsub_v1.subscriber import subscriber

import mock
from six.moves import queue
import pytest


@pytest.mark.parametrize('item,method', [
    (requests.AckRequest(0, 0, 0), 'ack'),
    (requests.DropRequest(0, 0), 'drop'),
    (requests.LeaseRequest(0, 0), 'lease'),
    (requests.ModAckRequest(0, 0), 'modify_ack_deadline'),
    (requests.NackRequest(0, 0), 'nack')
])
def test_dispatch_callback(item, method):
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [item]
    dispatcher_.dispatch_callback(items)

    getattr(subscriber_, method).assert_called_once_with([item])


def test_dispatch_callback_inactive():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    subscriber_.is_active = False
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    dispatcher_.dispatch_callback([requests.AckRequest(0, 0, 0)])

    subscriber_.ack.assert_not_called()


@mock.patch('threading.Thread', autospec=True)
def test_start(thread):
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    dispatcher_.start()

    thread.assert_called_once_with(
        name=dispatcher._CALLBACK_WORKER_NAME, target=mock.ANY)

    thread.return_value.start.assert_called_once()

    assert dispatcher_._thread is not None


@mock.patch('threading.Thread', autospec=True)
def test_start_already_started(thread):
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)
    dispatcher_._thread = mock.sentinel.thread

    with pytest.raises(ValueError):
        dispatcher_.start()

    thread.assert_not_called()


def test_stop():
    queue_ = queue.Queue()
    dispatcher_ = dispatcher.Dispatcher(queue_, mock.sentinel.subscriber)
    thread = mock.create_autospec(threading.Thread, instance=True)
    dispatcher_._thread = thread

    dispatcher_.stop()

    assert queue_.get() is helper_threads.STOP
    thread.join.assert_called_once()
    assert dispatcher_._thread is None


def test_stop_no_join():
    dispatcher_ = dispatcher.Dispatcher(
        mock.sentinel.queue, mock.sentinel.subscriber)

    dispatcher_.stop()
