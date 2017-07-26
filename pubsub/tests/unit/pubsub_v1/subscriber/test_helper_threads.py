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

import queue
import threading

import mock

from google.cloud.pubsub_v1.subscriber import helper_threads


def test_start():
    registry = helper_threads.HelperThreadRegistry()
    queue_ = queue.Queue()
    target = mock.Mock(spec=())
    with mock.patch.object(threading.Thread, 'start', autospec=True) as start:
        registry.start('foo', queue_, target)
        assert start.called
