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

import itertools

try:
    from unittest import mock
except ImportError:  # pragma: NO PY3 COVER
    import mock

import grpc
import pytest

from google.api_core import exceptions as core_exceptions
from google.cloud.ndb import _retry
from google.cloud.ndb import tasklets


class Test_retry:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_success():
        def callback():
            return "foo"

        retry = _retry.retry_async(callback)
        assert retry().result() == "foo"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_success_callback_is_tasklet():
        tasklet_future = tasklets.Future()

        @tasklets.tasklet
        def callback():
            result = yield tasklet_future
            raise tasklets.Return(result)

        retry = _retry.retry_async(callback)
        tasklet_future.set_result("foo")
        assert retry().result() == "foo"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_unhandled_error():
        error = Exception("Spurious error")

        def callback():
            raise error

        retry = _retry.retry_async(callback)
        assert retry().exception() is error

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_transient_error(core_retry, sleep):
        core_retry.exponential_sleep_generator.return_value = itertools.count()
        core_retry.if_transient_error.return_value = True

        sleep_future = tasklets.Future("sleep")
        sleep.return_value = sleep_future

        callback = mock.Mock(side_effect=[Exception("Spurious error."), "foo"])
        retry = _retry.retry_async(callback)
        sleep_future.set_result(None)
        assert retry().result() == "foo"

        sleep.assert_called_once_with(0)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_too_many_transient_errors(core_retry, sleep):
        core_retry.exponential_sleep_generator.return_value = itertools.count()
        core_retry.if_transient_error.return_value = True

        sleep_future = tasklets.Future("sleep")
        sleep.return_value = sleep_future
        sleep_future.set_result(None)

        error = Exception("Spurious error")

        def callback():
            raise error

        retry = _retry.retry_async(callback)
        with pytest.raises(core_exceptions.RetryError) as error_context:
            retry().check_success()

        assert error_context.value.cause is error
        assert sleep.call_count == 4
        assert sleep.call_args[0][0] == 3

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_too_many_transient_errors_pass_retries(core_retry, sleep):
        core_retry.exponential_sleep_generator.return_value = itertools.count()
        core_retry.if_transient_error.return_value = True

        sleep_future = tasklets.Future("sleep")
        sleep.return_value = sleep_future
        sleep_future.set_result(None)

        error = Exception("Spurious error")

        def callback():
            raise error

        retry = _retry.retry_async(callback, retries=4)
        with pytest.raises(core_exceptions.RetryError) as error_context:
            retry().check_success()

        assert error_context.value.cause is error
        assert sleep.call_count == 5
        assert sleep.call_args[0][0] == 4


class Test_is_transient_error:
    @staticmethod
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_core_says_yes(core_retry):
        error = object()
        core_retry.if_transient_error.return_value = True
        assert _retry.is_transient_error(error) is True
        core_retry.if_transient_error.assert_called_once_with(error)

    @staticmethod
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_core_says_no_we_say_no(core_retry):
        error = object()
        core_retry.if_transient_error.return_value = False
        assert _retry.is_transient_error(error) is False
        core_retry.if_transient_error.assert_called_once_with(error)

    @staticmethod
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_unavailable(core_retry):
        error = mock.Mock(
            code=mock.Mock(return_value=grpc.StatusCode.UNAVAILABLE)
        )
        core_retry.if_transient_error.return_value = False
        assert _retry.is_transient_error(error) is True
        core_retry.if_transient_error.assert_called_once_with(error)

    @staticmethod
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_internal(core_retry):
        error = mock.Mock(
            code=mock.Mock(return_value=grpc.StatusCode.INTERNAL)
        )
        core_retry.if_transient_error.return_value = False
        assert _retry.is_transient_error(error) is True
        core_retry.if_transient_error.assert_called_once_with(error)

    @staticmethod
    @mock.patch("google.cloud.ndb._retry.core_retry")
    def test_unauthenticated(core_retry):
        error = mock.Mock(
            code=mock.Mock(return_value=grpc.StatusCode.UNAUTHENTICATED)
        )
        core_retry.if_transient_error.return_value = False
        assert _retry.is_transient_error(error) is False
        core_retry.if_transient_error.assert_called_once_with(error)
