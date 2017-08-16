# Copyright 2017 Google Inc.
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
import pytest

from google.api.core import exceptions
from google.api.core import retry


def test_if_exception_type():
    predicate = retry.if_exception_type(ValueError)

    assert predicate(ValueError())
    assert not predicate(TypeError())


def test_if_exception_type_multiple():
    predicate = retry.if_exception_type(ValueError, TypeError)

    assert predicate(ValueError())
    assert predicate(TypeError())
    assert not predicate(RuntimeError())


def test_if_transient_error():
    assert retry.if_transient_error(exceptions.InternalServerError(''))
    assert retry.if_transient_error(exceptions.TooManyRequests(''))
    assert not retry.if_transient_error(exceptions.InvalidArgument(''))


def test_exponential_sleep_generator_base_2():
    gen = retry.exponential_sleep_generator(
        1, 60, 2, jitter=0.0)

    result = list(itertools.islice(gen, 8))
    assert result == [1, 2, 4, 8, 16, 32, 60, 60]


@mock.patch('random.uniform')
def test_exponential_sleep_generator_jitter(uniform):
    uniform.return_value = 1
    gen = retry.exponential_sleep_generator(
        1, 60, 2, jitter=2.2)

    result = list(itertools.islice(gen, 7))
    assert result == [1, 3, 7, 15, 31, 60, 60]
    uniform.assert_called_with(0.0, 2.2)


@mock.patch('time.sleep')
@mock.patch(
    'google.api.core.helpers.datetime_helpers.utcnow',
    return_value=datetime.datetime.min)
def test_retry_target_success(utcnow, sleep):
    predicate = retry.if_exception_type(ValueError)
    call_count = [0]

    def target():
        call_count[0] += 1
        if call_count[0] < 3:
            raise ValueError()
        return 42

    result = retry.retry_target(target, predicate, range(10), None)

    assert result == 42
    assert call_count[0] == 3
    sleep.assert_has_calls([mock.call(0), mock.call(1)])


@mock.patch('time.sleep')
@mock.patch(
    'google.api.core.helpers.datetime_helpers.utcnow',
    return_value=datetime.datetime.min)
def test_retry_target_non_retryable_error(utcnow, sleep):
    predicate = retry.if_exception_type(ValueError)
    exception = TypeError()
    target = mock.Mock(side_effect=exception)

    with pytest.raises(TypeError) as exc_info:
        retry.retry_target(target, predicate, range(10), None)

    assert exc_info.value == exception
    sleep.assert_not_called()


@mock.patch('time.sleep')
@mock.patch(
    'google.api.core.helpers.datetime_helpers.utcnow')
def test_retry_target_deadline_exceeded(utcnow, sleep):
    predicate = retry.if_exception_type(ValueError)
    exception = ValueError('meep')
    target = mock.Mock(side_effect=exception)
    # Setup the timeline so that the first call takes 5 seconds but the second
    # call takes 6, which puts the retry over the deadline.
    utcnow.side_effect = [
        # The first call to utcnow establishes the start of the timeline.
        datetime.datetime.min,
        datetime.datetime.min + datetime.timedelta(seconds=5),
        datetime.datetime.min + datetime.timedelta(seconds=11)]

    with pytest.raises(exceptions.RetryError) as exc_info:
        retry.retry_target(target, predicate, range(10), deadline=10)

    assert exc_info.value.cause == exception
    assert exc_info.match('Deadline of 10.0s exceeded')
    assert exc_info.match('last exception: meep')
    assert target.call_count == 2


def test_retry_target_bad_sleep_generator():
    with pytest.raises(ValueError, match='Sleep generator'):
        retry.retry_target(
            mock.sentinel.target, mock.sentinel.predicate, [], None)
