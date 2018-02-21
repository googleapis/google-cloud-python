# Copyright 2018, Google LLC All rights reserved.
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

from concurrent import futures
import threading

from google.api_core import exceptions
from google.auth import credentials
import mock
import pytest
from six.moves import queue

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber.futures import Future
from google.cloud.pubsub_v1.subscriber.monitor import Monitor
from google.cloud.pubsub_v1.subscriber.policy import base
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_monitor(args=None):
    if args is None:
        args = []
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    policy = thread.Policy(client, 'sub_name_c')
    return Monitor(policy, 3, args)


def test__start_true():
    monitor = create_monitor()
    monitor.thread = mock.create_autospec(monitor.thread)
    monitor.thread.is_alive.return_value = False
    monitor.event = mock.create_autospec(monitor.event)
    monitor._start(True)
    monitor.thread.start.assert_called_once()    
    monitor.event.set.assert_called_once()


def test__start_false():
    monitor = create_monitor()
    monitor.thread = mock.create_autospec(monitor.thread)
    monitor.thread.is_alive.return_value = True
    monitor.event = mock.create_autospec(monitor.event)    
    monitor._start(False)
    monitor.thread.start.assert_not_called()
    monitor.event.set.assert_not_called()


def test__stop():
    monitor = create_monitor()
    monitor.event = mock.create_autospec(monitor.event)
    monitor._stop()
    monitor.event.clear.assert_called_once()


def test__clear():
    monitor = create_monitor()
    monitor._clear()
    assert monitor._stop_thread


def test__build_output():
    monitor = create_monitor()
    monitor.subscription_name = '1'
    monitor.policy = mock.create_autospec(monitor.policy)
    monitor.policy.histogram.percentile.return_value = '2'
    monitor.policy.managed_ack_ids = ['', '', '']
    monitor.policy._consumer.pending_requests = '4'    
    monitor._build_output([Monitor.NAME,
                           Monitor.MESSAGES,
                           Monitor.P99,
                           Monitor.REQUESTS])

    assert monitor.msg == '1\n2\n3\n4\n'


def test__build_no_output():
    monitor = create_monitor()
    monitor.subscription_name = '1'
    monitor.policy = mock.create_autospec(monitor.policy)
    monitor.policy.histogram.percentile.return_value = '2'
    monitor.policy.managed_ack_ids = ['', '', '']
    monitor.policy._consumer.pending_requests = '4'    
    monitor._build_output([])
    assert monitor.msg == ''


def test__timer():
    monitor = create_monitor()
    monitor._clear()
    monitor._timer(1, monitor.event)
    # assert loop terminates
    assert 1 == 1


def test__timer_loop():
    import time
    monitor = create_monitor()
    monitor.event.set()
    monitor._stop_thread = False
    with mock.patch.object(time, 'sleep', autospec=True) as sleep:
        sleep.side_effect = []
        try:
            monitor._timer(1, monitor.event)
        except StopIteration:
            sleep.assert_called_once()

