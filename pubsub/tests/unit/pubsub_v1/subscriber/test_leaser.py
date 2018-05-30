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

import logging
import threading

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import histogram
from google.cloud.pubsub_v1.subscriber._protocol import leaser
from google.cloud.pubsub_v1.subscriber._protocol import requests
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager

import mock
import pytest


def test_add_and_remove():
    leaser_ = leaser.Leaser(mock.sentinel.manager)

    leaser_.add([
        requests.LeaseRequest(ack_id='ack1', byte_size=50)])
    leaser_.add([
        requests.LeaseRequest(ack_id='ack2', byte_size=25)])

    assert leaser_.message_count == 2
    assert set(leaser_.ack_ids) == set(['ack1', 'ack2'])
    assert leaser_.bytes == 75

    leaser_.remove([
        requests.DropRequest(ack_id='ack1', byte_size=50)])

    assert leaser_.message_count == 1
    assert set(leaser_.ack_ids) == set(['ack2'])
    assert leaser_.bytes == 25


def test_add_already_managed(caplog):
    caplog.set_level(logging.DEBUG)

    leaser_ = leaser.Leaser(mock.sentinel.manager)

    leaser_.add([
        requests.LeaseRequest(ack_id='ack1', byte_size=50)])
    leaser_.add([
        requests.LeaseRequest(ack_id='ack1', byte_size=50)])

    assert 'already lease managed' in caplog.text


def test_remove_not_managed(caplog):
    caplog.set_level(logging.DEBUG)

    leaser_ = leaser.Leaser(mock.sentinel.manager)

    leaser_.remove([
        requests.DropRequest(ack_id='ack1', byte_size=50)])

    assert 'not managed' in caplog.text


def test_remove_negative_bytes(caplog):
    caplog.set_level(logging.DEBUG)

    leaser_ = leaser.Leaser(mock.sentinel.manager)

    leaser_.add([
        requests.LeaseRequest(ack_id='ack1', byte_size=50)])
    leaser_.remove([
        requests.DropRequest(ack_id='ack1', byte_size=75)])

    assert leaser_.bytes == 0
    assert 'unexpectedly negative' in caplog.text


def create_manager(flow_control=types.FlowControl()):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True)
    manager.dispatcher = mock.create_autospec(
        dispatcher.Dispatcher, instance=True)
    manager.is_active = True
    manager.flow_control = flow_control
    manager.ack_histogram = histogram.Histogram()
    return manager


def test_maintain_leases_inactive(caplog):
    caplog.set_level(logging.INFO)
    manager = create_manager()
    manager.is_active = False

    leaser_ = leaser.Leaser(manager)

    leaser_.maintain_leases()

    assert 'exiting' in caplog.text


def test_maintain_leases_stopped(caplog):
    caplog.set_level(logging.INFO)
    manager = create_manager()

    leaser_ = leaser.Leaser(manager)
    leaser_.stop()

    leaser_.maintain_leases()

    assert 'exiting' in caplog.text


def make_sleep_mark_manager_as_inactive(leaser):
    # Make sleep mark the manager as inactive so that maintain_leases
    # exits at the end of the first run.
    def trigger_inactive(timeout):
        assert 0 < timeout < 10
        leaser._manager.is_active = False

    leaser._stop_event.wait = trigger_inactive


def test_maintain_leases_ack_ids():
    manager = create_manager()
    leaser_ = leaser.Leaser(manager)
    make_sleep_mark_manager_as_inactive(leaser_)
    leaser_.add([requests.LeaseRequest(ack_id='my ack id', byte_size=50)])

    leaser_.maintain_leases()

    manager.dispatcher.modify_ack_deadline.assert_called_once_with([
        requests.ModAckRequest(
            ack_id='my ack id',
            seconds=10,
        )
    ])


def test_maintain_leases_no_ack_ids():
    manager = create_manager()
    leaser_ = leaser.Leaser(manager)
    make_sleep_mark_manager_as_inactive(leaser_)

    leaser_.maintain_leases()

    manager.dispatcher.modify_ack_deadline.assert_not_called()


@mock.patch('time.time', autospec=True)
def test_maintain_leases_outdated_items(time):
    manager = create_manager()
    leaser_ = leaser.Leaser(manager)
    make_sleep_mark_manager_as_inactive(leaser_)

    # Add these items at the beginning of the timeline
    time.return_value = 0
    leaser_.add([
        requests.LeaseRequest(ack_id='ack1', byte_size=50)])

    # Add another item at towards end of the timeline
    time.return_value = manager.flow_control.max_lease_duration - 1
    leaser_.add([
        requests.LeaseRequest(ack_id='ack2', byte_size=50)])

    # Now make sure time reports that we are at the end of our timeline.
    time.return_value = manager.flow_control.max_lease_duration + 1

    leaser_.maintain_leases()

    # Only ack2 should be renewed. ack1 should've been dropped
    manager.dispatcher.modify_ack_deadline.assert_called_once_with([
        requests.ModAckRequest(
            ack_id='ack2',
            seconds=10,
        )
    ])
    manager.dispatcher.drop.assert_called_once_with([
        requests.DropRequest(ack_id='ack1', byte_size=50)
    ])


@mock.patch('threading.Thread', autospec=True)
def test_start(thread):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True)
    leaser_ = leaser.Leaser(manager)

    leaser_.start()

    thread.assert_called_once_with(
        name=leaser._LEASE_WORKER_NAME, target=leaser_.maintain_leases)

    thread.return_value.start.assert_called_once()

    assert leaser_._thread is not None


@mock.patch('threading.Thread', autospec=True)
def test_start_already_started(thread):
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True)
    leaser_ = leaser.Leaser(manager)
    leaser_._thread = mock.sentinel.thread

    with pytest.raises(ValueError):
        leaser_.start()

    thread.assert_not_called()


def test_stop():
    manager = mock.create_autospec(
        streaming_pull_manager.StreamingPullManager, instance=True)
    leaser_ = leaser.Leaser(manager)
    thread = mock.create_autospec(threading.Thread, instance=True)
    leaser_._thread = thread

    leaser_.stop()

    assert leaser_._stop_event.is_set()
    thread.join.assert_called_once()
    assert leaser_._thread is None


def test_stop_no_join():
    leaser_ = leaser.Leaser(mock.sentinel.manager)

    leaser_.stop()
