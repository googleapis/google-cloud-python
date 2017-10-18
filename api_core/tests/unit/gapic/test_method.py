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

import mock

from google.api_core import exceptions
from google.api_core import retry
from google.api_core import timeout
import google.api_core.gapic_v1.method
import google.api_core.page_iterator


def _utcnow_monotonic():
    curr_value = datetime.datetime.min
    delta = datetime.timedelta(seconds=0.5)
    while True:
        yield curr_value
        curr_value += delta


def test_wrap_method_basic():
    method = mock.Mock(spec=['__call__'], return_value=42)

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, metadata=None)

    result = wrapped_method(1, 2, meep='moop')

    assert result == 42
    method.assert_called_once_with(1, 2, meep='moop')


def test_wrap_method_with_default_metadata():
    method = mock.Mock(spec=['__call__'])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(method)

    wrapped_method(1, 2, meep='moop')

    method.assert_called_once_with(1, 2, meep='moop', metadata=mock.ANY)

    metadata = method.call_args[1]['metadata']
    assert len(metadata) == 1
    assert metadata[0][0] == 'x-goog-api-client'
    assert 'api-core' in metadata[0][1]


def test_wrap_method_with_custom_metadata():
    method = mock.Mock(spec=['__call__'])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, metadata={'foo': 'bar'})

    wrapped_method(1, 2, meep='moop')

    method.assert_called_once_with(1, 2, meep='moop', metadata=mock.ANY)

    metadata = method.call_args[1]['metadata']
    assert len(metadata) == 2
    assert ('foo', 'bar') in metadata


def test_wrap_method_with_merged_metadata():
    method = mock.Mock(spec=['__call__'])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, metadata={'x-goog-api-client': 'foo/1.2.3'})

    wrapped_method(1, 2, meep='moop')

    method.assert_called_once_with(1, 2, meep='moop', metadata=mock.ANY)

    metadata = method.call_args[1]['metadata']
    assert len(metadata) == 1
    assert metadata[0][0] == 'x-goog-api-client'
    assert metadata[0][1].endswith(' foo/1.2.3')


@mock.patch('time.sleep')
def test_wrap_method_with_default_retry_and_timeout(unusued_sleep):
    method = mock.Mock(
        spec=['__call__'],
        side_effect=[exceptions.InternalServerError(None), 42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout)

    result = wrapped_method()

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(timeout=60, metadata=mock.ANY)


@mock.patch('time.sleep')
def test_wrap_method_with_default_retry_and_timeout_using_sentinel(
        unusued_sleep):
    method = mock.Mock(
        spec=['__call__'],
        side_effect=[exceptions.InternalServerError(None), 42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout)

    result = wrapped_method(
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT)

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(timeout=60, metadata=mock.ANY)


@mock.patch('time.sleep')
def test_wrap_method_with_overriding_retry_and_timeout(unusued_sleep):
    method = mock.Mock(
        spec=['__call__'],
        side_effect=[exceptions.NotFound(None), 42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout)

    result = wrapped_method(
        retry=retry.Retry(retry.if_exception_type(exceptions.NotFound)),
        timeout=timeout.ConstantTimeout(22))

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(timeout=22, metadata=mock.ANY)


@mock.patch('time.sleep')
@mock.patch(
    'google.api_core.datetime_helpers.utcnow',
    side_effect=_utcnow_monotonic(),
    autospec=True)
def test_wrap_method_with_overriding_retry_deadline(utcnow, unused_sleep):
    method = mock.Mock(
        spec=['__call__'],
        side_effect=([exceptions.InternalServerError(None)] * 4) + [42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ExponentialTimeout(deadline=60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout)

    # Overriding only the retry's deadline should also override the timeout's
    # deadline.
    result = wrapped_method(
        retry=default_retry.with_deadline(30))

    assert result == 42
    timeout_args = [call[1]['timeout'] for call in method.call_args_list]
    assert timeout_args == [5.0, 10.0, 20.0, 26.0, 25.0]
    assert utcnow.call_count == (
        1 +  # First to set the deadline.
        5 +  # One for each min(timeout, maximum, (DEADLINE - NOW).seconds)
        5
    )


def test_wrap_method_with_overriding_timeout_as_a_number():
    method = mock.Mock(spec=['__call__'], return_value=42)
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout)

    result = wrapped_method(timeout=22)

    assert result == 42
    method.assert_called_once_with(timeout=22, metadata=mock.ANY)


def test_wrap_with_paging():
    page_one = mock.Mock(
        spec=['items', 'page_token', 'next_page_token'],
        items=[1, 2],
        next_page_token='icanhasnextpls')
    page_two = mock.Mock(
        spec=['items', 'page_token', 'next_page_token'],
        items=[3, 4],
        next_page_token=None)
    method = mock.Mock(
        spec=['__call__', '__name__'], side_effect=(page_one, page_two))
    method.__name__ = 'mockmethod'

    wrapped_method = google.api_core.gapic_v1.method.wrap_with_paging(
        method, 'items', 'page_token', 'next_page_token')

    request = mock.Mock(spec=['page_token'], page_token=None)
    result = wrapped_method(request, extra='param')

    # Should return an iterator and should not have actually called the
    # method yet.
    assert isinstance(result, google.api_core.page_iterator.Iterator)
    method.assert_not_called()
    assert request.page_token is None

    # Draining the iterator should call the method until no more pages are
    # returned.
    results = list(result)

    assert results == [1, 2, 3, 4]
    assert method.call_count == 2
    method.assert_called_with(request, extra='param')
    assert request.page_token == 'icanhasnextpls'
