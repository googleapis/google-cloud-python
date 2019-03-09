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

from unittest import mock

import pytest

from google.api_core import exceptions as core_exceptions
from google.cloud.ndb import tasklets
from google.cloud.ndb import _transaction


class Test_in_transaction:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_false():
        assert _transaction.in_transaction() is False

    @staticmethod
    def test_true(in_context):
        with in_context.new(transaction=b"tx123").use():
            assert _transaction.in_transaction() is True


class Test_transaction:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_propagation():
        with pytest.raises(NotImplementedError):
            _transaction.transaction(None, propagation=1)

    @staticmethod
    def test_already_in_transaction(in_context):
        with in_context.new(transaction=b"tx123").use():
            with pytest.raises(NotImplementedError):
                _transaction.transaction(None)

    @staticmethod
    @mock.patch("google.cloud.ndb._transaction.transaction_async")
    def test_success(transaction_async):
        transaction_async.return_value.result.return_value = 42
        assert _transaction.transaction("callback") == 42
        transaction_async.assert_called_once_with(
            "callback", read_only=False, retries=3, xg=True, propagation=None
        )


class Test_transaction_async:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_success(_datastore_api):
        def callback():
            return "I tried, momma."

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(False)
        begin_future.set_result(b"tx123")

        _datastore_api.commit.assert_called_once_with(b"tx123")
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_success_no_retries(_datastore_api):
        def callback():
            return "I tried, momma."

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback, retries=0)

        _datastore_api.begin_transaction.assert_called_once_with(False)
        begin_future.set_result(b"tx123")

        _datastore_api.commit.assert_called_once_with(b"tx123")
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_success_callback_is_tasklet(_datastore_api):
        tasklet = tasklets.Future("tasklet")

        def callback():
            return tasklet

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(False)
        begin_future.set_result(b"tx123")

        tasklet.set_result("I tried, momma.")

        _datastore_api.commit.assert_called_once_with(b"tx123")
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_error(_datastore_api):
        error = Exception("Spurious error.")

        def callback():
            raise error

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        rollback_future = tasklets.Future("rollback transaction")
        _datastore_api.rollback.return_value = rollback_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(False)
        begin_future.set_result(b"tx123")

        _datastore_api.rollback.assert_called_once_with(b"tx123")
        rollback_future.set_result(None)

        assert future.exception() is error

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_transient_error(_datastore_api, core_retry, sleep):
        core_retry.exponential_sleep_generator.return_value = itertools.count()
        core_retry.if_transient_error.return_value = True

        callback = mock.Mock(side_effect=[Exception("Spurious error."), "foo"])

        begin_future = tasklets.Future("begin transaction")
        begin_future.set_result(b"tx123")
        _datastore_api.begin_transaction.return_value = begin_future

        rollback_future = tasklets.Future("rollback transaction")
        _datastore_api.rollback.return_value = rollback_future
        rollback_future.set_result(None)

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future
        commit_future.set_result(None)

        sleep_future = tasklets.Future("sleep")
        sleep_future.set_result(None)
        sleep.return_value = sleep_future

        future = _transaction.transaction_async(callback)
        assert future.result() == "foo"

        _datastore_api.begin_transaction.call_count == 2
        _datastore_api.rollback.assert_called_once_with(b"tx123")
        sleep.assert_called_once_with(0)
        _datastore_api.commit.assert_called_once_with(b"tx123")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    @mock.patch("google.cloud.ndb._transaction._datastore_api")
    def test_too_many_transient_errors(_datastore_api, core_retry, sleep):
        core_retry.exponential_sleep_generator.return_value = itertools.count()
        core_retry.if_transient_error.return_value = True

        error = Exception("Spurious error.")

        def callback():
            raise error

        begin_future = tasklets.Future("begin transaction")
        begin_future.set_result(b"tx123")
        _datastore_api.begin_transaction.return_value = begin_future

        rollback_future = tasklets.Future("rollback transaction")
        _datastore_api.rollback.return_value = rollback_future
        rollback_future.set_result(None)

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future
        commit_future.set_result(None)

        sleep_future = tasklets.Future("sleep")
        sleep_future.set_result(None)
        sleep.return_value = sleep_future

        future = _transaction.transaction_async(callback)
        with pytest.raises(core_exceptions.RetryError) as error_context:
            future.check_success()

        assert error_context.value.cause is error

        assert _datastore_api.begin_transaction.call_count == 4
        assert _datastore_api.rollback.call_count == 4
        assert sleep.call_count == 4
        _datastore_api.commit.assert_not_called()
