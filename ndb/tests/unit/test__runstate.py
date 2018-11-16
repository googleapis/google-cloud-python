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

from google.cloud.ndb import _runstate


def test_ndb_context():
    assert _runstate.states.current() is None

    with _runstate.ndb_context():
        one = _runstate.current()

        with _runstate.ndb_context():
            two = _runstate.current()
            assert one is not two
            two.eventloop = unittest.mock.Mock(spec=("run",))
            two.eventloop.run.assert_not_called()

        assert _runstate.current() is one
        two.eventloop.run.assert_called_once_with()

    assert _runstate.states.current() is None
