# Copyright 2017 Google LLC
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

import datetime
import itertools

import mock

from google.api_core import timeout


def test__exponential_timeout_generator_base_2():
    gen = timeout._exponential_timeout_generator(
        1.0, 60.0, 2.0, deadline=None)

    result = list(itertools.islice(gen, 8))
    assert result == [1, 2, 4, 8, 16, 32, 60, 60]


@mock.patch('google.api_core.datetime_helpers.utcnow', autospec=True)
def test__exponential_timeout_generator_base_deadline(utcnow):
    # Make each successive call to utcnow() advance one second.
    utcnow.side_effect = [
        datetime.datetime.min + datetime.timedelta(seconds=n)
        for n in range(15)]

    gen = timeout._exponential_timeout_generator(
        1.0, 60.0, 2.0, deadline=30.0)

    result = list(itertools.islice(gen, 14))
    # Should grow until the cumulative time is > 30s, then start decreasing as
    # the cumulative time approaches 60s.
    assert result == [1, 2, 4, 8, 16, 24, 23, 22, 21, 20, 19, 18, 17, 16]


class TestConstantTimeout(object):

    def test_constructor(self):
        timeout_ = timeout.ConstantTimeout()
        assert timeout_._timeout is None

    def test_constructor_args(self):
        timeout_ = timeout.ConstantTimeout(42.0)
        assert timeout_._timeout == 42.0

    def test___str__(self):
        timeout_ = timeout.ConstantTimeout(1)
        assert str(timeout_) == '<ConstantTimeout timeout=1.0>'

    def test_apply(self):
        target = mock.Mock(spec=['__call__', '__name__'], __name__='target')
        timeout_ = timeout.ConstantTimeout(42.0)
        wrapped = timeout_(target)

        wrapped()

        target.assert_called_once_with(timeout=42.0)

    def test_apply_passthrough(self):
        target = mock.Mock(spec=['__call__', '__name__'], __name__='target')
        timeout_ = timeout.ConstantTimeout(42.0)
        wrapped = timeout_(target)

        wrapped(1, 2, meep='moop')

        target.assert_called_once_with(1, 2, meep='moop', timeout=42.0)


class TestExponentialTimeout(object):

    def test_constructor(self):
        timeout_ = timeout.ExponentialTimeout()
        assert timeout_._initial == timeout._DEFAULT_INITIAL_TIMEOUT
        assert timeout_._maximum == timeout._DEFAULT_MAXIMUM_TIMEOUT
        assert timeout_._multiplier == timeout._DEFAULT_TIMEOUT_MULTIPLIER
        assert timeout_._deadline == timeout._DEFAULT_DEADLINE

    def test_constructor_args(self):
        timeout_ = timeout.ExponentialTimeout(1, 2, 3, 4)
        assert timeout_._initial == 1
        assert timeout_._maximum == 2
        assert timeout_._multiplier == 3
        assert timeout_._deadline == 4

    def test_with_timeout(self):
        original_timeout = timeout.ExponentialTimeout()
        timeout_ = original_timeout.with_deadline(42)
        assert original_timeout is not timeout_
        assert timeout_._initial == timeout._DEFAULT_INITIAL_TIMEOUT
        assert timeout_._maximum == timeout._DEFAULT_MAXIMUM_TIMEOUT
        assert timeout_._multiplier == timeout._DEFAULT_TIMEOUT_MULTIPLIER
        assert timeout_._deadline == 42

    def test___str__(self):
        timeout_ = timeout.ExponentialTimeout(1, 2, 3, 4)
        assert str(timeout_) == (
            '<ExponentialTimeout initial=1.0, maximum=2.0, multiplier=3.0, '
            'deadline=4.0>')

    def test_apply(self):
        target = mock.Mock(spec=['__call__', '__name__'], __name__='target')
        timeout_ = timeout.ExponentialTimeout(1, 10, 2)
        wrapped = timeout_(target)

        wrapped()
        target.assert_called_with(timeout=1)

        wrapped()
        target.assert_called_with(timeout=2)

        wrapped()
        target.assert_called_with(timeout=4)

    def test_apply_passthrough(self):
        target = mock.Mock(spec=['__call__', '__name__'], __name__='target')
        timeout_ = timeout.ExponentialTimeout(42.0, 100, 2)
        wrapped = timeout_(target)

        wrapped(1, 2, meep='moop')

        target.assert_called_once_with(1, 2, meep='moop', timeout=42.0)
