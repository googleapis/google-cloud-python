# Copyright 2018 Google LLC
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

import unittest

from google.cloud.ndb import _eventloop
from google.cloud.ndb import async_


@unittest.mock.patch("google.cloud.ndb.async_._eventloop.EventLoop")
def test_async_context(EventLoop):
    one = unittest.mock.Mock(spec=("run",))
    two = unittest.mock.Mock(spec=("run",))
    EventLoop.side_effect = [one, two]
    assert _eventloop.contexts.current() is None

    with async_.async_context():
        assert _eventloop.contexts.current() is one
        one.run.assert_not_called()

        with async_.async_context():
            assert _eventloop.contexts.current() is two
            two.run.assert_not_called()

        assert _eventloop.contexts.current() is one
        one.run.assert_not_called()
        two.run.assert_called_once_with()

    assert _eventloop.contexts.current() is None
    one.run.assert_called_once_with()
