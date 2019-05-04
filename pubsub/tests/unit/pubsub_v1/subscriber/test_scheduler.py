# Copyright 2018, Google LLC
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

import concurrent.futures
import threading

import mock
from six.moves import queue

from google.cloud.pubsub_v1.subscriber import scheduler


def test_subclasses_base_abc():
    assert issubclass(scheduler.ThreadScheduler, scheduler.Scheduler)


def test_constructor_defaults():
    scheduler_ = scheduler.ThreadScheduler()

    assert isinstance(scheduler_.queue, queue.Queue)
    assert isinstance(scheduler_._executor, concurrent.futures.Executor)


def test_constructor_options():
    scheduler_ = scheduler.ThreadScheduler(executor=mock.sentinel.executor)

    assert scheduler_._executor == mock.sentinel.executor


def test_schedule():
    called_with = []
    called = threading.Event()

    def callback(*args, **kwargs):
        called_with.append((args, kwargs))
        called.set()

    scheduler_ = scheduler.ThreadScheduler()

    scheduler_.schedule(callback, "arg1", kwarg1="meep")

    called.wait()
    scheduler_.shutdown()

    assert called_with == [(("arg1",), {"kwarg1": "meep"})]
