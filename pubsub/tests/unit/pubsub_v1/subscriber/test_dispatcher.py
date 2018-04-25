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

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import subscriber
from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import helper_threads
from google.cloud.pubsub_v1.subscriber._protocol import requests

import mock
from six.moves import queue
import pytest


@pytest.mark.parametrize('item,method_name', [
    (requests.AckRequest(0, 0, 0), 'ack'),
    (requests.DropRequest(0, 0), 'drop'),
    (requests.LeaseRequest(0, 0), 'lease'),
    (requests.ModAckRequest(0, 0), 'modify_ack_deadline'),
    (requests.NackRequest(0, 0), 'nack')
])
def test_dispatch_callback(item, method_name):
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [item]

    with mock.patch.object(dispatcher_, method_name) as method:
        dispatcher_.dispatch_callback(items)

    method.assert_called_once_with([item])


def test_dispatch_callback_inactive():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    subscriber_.is_active = False
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    dispatcher_.dispatch_callback([requests.AckRequest(0, 0, 0)])

    subscriber_.send.assert_not_called()


def test_ack():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.AckRequest(
        ack_id='ack_id_string', byte_size=0, time_to_ack=20)]
    dispatcher_.ack(items)

    subscriber_.send.assert_called_once_with(types.StreamingPullRequest(
        ack_ids=['ack_id_string'],
    ))

    subscriber_.leaser.remove.assert_called_once_with(items)
    subscriber_.maybe_resume_consumer.assert_called_once()
    subscriber_.ack_histogram.add.assert_called_once_with(20)


def test_ack_no_time():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.AckRequest(
        ack_id='ack_id_string', byte_size=0, time_to_ack=None)]
    dispatcher_.ack(items)

    subscriber_.send.assert_called_once_with(types.StreamingPullRequest(
        ack_ids=['ack_id_string'],
    ))

    subscriber_.ack_histogram.add.assert_not_called()


def test_lease():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.LeaseRequest(ack_id='ack_id_string', byte_size=10)]
    dispatcher_.lease(items)

    subscriber_.leaser.add.assert_called_once_with(items)
    subscriber_.maybe_pause_consumer.assert_called_once()


def test_drop():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.DropRequest(ack_id='ack_id_string', byte_size=10)]
    dispatcher_.drop(items)

    subscriber_.leaser.remove.assert_called_once_with(items)
    subscriber_.maybe_resume_consumer.assert_called_once()


def test_nack():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.NackRequest(ack_id='ack_id_string', byte_size=10)]
    dispatcher_.nack(items)

    subscriber_.send.assert_called_once_with(types.StreamingPullRequest(
        modify_deadline_ack_ids=['ack_id_string'],
        modify_deadline_seconds=[0],
    ))


def test_modify_ack_deadline():
    subscriber_ = mock.create_autospec(subscriber.Subscriber, instance=True)
    dispatcher_ = dispatcher.Dispatcher(mock.sentinel.queue, subscriber_)

    items = [requests.ModAckRequest(ack_id='ack_id_string', seconds=60)]
    dispatcher_.modify_ack_deadline(items)

    subscriber_.send.assert_called_once_with(types.StreamingPullRequest(
        modify_deadline_ack_ids=['ack_id_string'],
        modify_deadline_seconds=[60],
    ))


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
