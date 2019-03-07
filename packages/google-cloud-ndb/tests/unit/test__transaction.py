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

from unittest import mock

import pytest

from google.cloud.ndb import tasklets
from google.cloud.ndb import _transaction


class Test_transaction:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_retries():
        with pytest.raises(NotImplementedError):
            _transaction.transaction(None, retries=2)

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
            "callback", read_only=False, retries=0, xg=True, propagation=None
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
