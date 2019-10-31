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

import pytest

from google.api_core import exceptions as core_exceptions
from google.cloud.ndb import context as context_module
from google.cloud.ndb import exceptions
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
    def test_transaction_inherits_and_merges_cache(in_context):
        original_cache = in_context.cache
        in_context.cache["test"] = "original value"
        with in_context.new(transaction=b"tx123").use() as new_context:
            assert new_context.cache is not original_cache
            assert new_context.cache["test"] == original_cache["test"]
            new_context.cache["test"] = "new_value"
            assert new_context.cache["test"] != original_cache["test"]
        assert in_context.cache["test"] == "new_value"

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
    @mock.patch("google.cloud.ndb._datastore_api")
    def test_success(_datastore_api):
        on_commit_callback = mock.Mock()

        def callback():
            context_module.get_context().call_on_commit(on_commit_callback)
            return "I tried, momma."

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(
            False, retries=0
        )
        begin_future.set_result(b"tx123")

        _datastore_api.commit.assert_called_once_with(b"tx123", retries=0)
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."
        on_commit_callback.assert_called_once_with()

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api")
    def test_success_no_retries(_datastore_api):
        def callback():
            return "I tried, momma."

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback, retries=0)

        _datastore_api.begin_transaction.assert_called_once_with(
            False, retries=0
        )
        begin_future.set_result(b"tx123")

        _datastore_api.commit.assert_called_once_with(b"tx123", retries=0)
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api")
    def test_success_callback_is_tasklet(_datastore_api):
        tasklet = tasklets.Future("tasklet")

        def callback():
            return tasklet

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        commit_future = tasklets.Future("commit transaction")
        _datastore_api.commit.return_value = commit_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(
            False, retries=0
        )
        begin_future.set_result(b"tx123")

        tasklet.set_result("I tried, momma.")

        _datastore_api.commit.assert_called_once_with(b"tx123", retries=0)
        commit_future.set_result(None)

        assert future.result() == "I tried, momma."

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api")
    def test_error(_datastore_api):
        error = Exception("Spurious error.")

        def callback():
            raise error

        begin_future = tasklets.Future("begin transaction")
        _datastore_api.begin_transaction.return_value = begin_future

        rollback_future = tasklets.Future("rollback transaction")
        _datastore_api.rollback.return_value = rollback_future

        future = _transaction.transaction_async(callback)

        _datastore_api.begin_transaction.assert_called_once_with(
            False, retries=0
        )
        begin_future.set_result(b"tx123")

        _datastore_api.rollback.assert_called_once_with(b"tx123")
        rollback_future.set_result(None)

        assert future.exception() is error

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    @mock.patch("google.cloud.ndb._datastore_api")
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
        _datastore_api.commit.assert_called_once_with(b"tx123", retries=0)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb.tasklets.sleep")
    @mock.patch("google.cloud.ndb._retry.core_retry")
    @mock.patch("google.cloud.ndb._datastore_api")
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


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api")
def test_transactional(_datastore_api):
    @_transaction.transactional()
    def simple_function(a, b):
        return a + b

    begin_future = tasklets.Future("begin transaction")
    _datastore_api.begin_transaction.return_value = begin_future

    commit_future = tasklets.Future("commit transaction")
    _datastore_api.commit.return_value = commit_future

    begin_future.set_result(b"tx123")
    commit_future.set_result(None)

    res = simple_function(100, 42)
    assert res == 142


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api")
def test_transactional_async(_datastore_api):
    @_transaction.transactional_async()
    def simple_function(a, b):
        return a + b

    begin_future = tasklets.Future("begin transaction")
    _datastore_api.begin_transaction.return_value = begin_future

    commit_future = tasklets.Future("commit transaction")
    _datastore_api.commit.return_value = commit_future

    begin_future.set_result(b"tx123")
    commit_future.set_result(None)

    res = simple_function(100, 42)
    assert res.result() == 142


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api")
def test_transactional_tasklet(_datastore_api):
    @_transaction.transactional_tasklet()
    def generator_function(dependency):
        value = yield dependency
        raise tasklets.Return(value + 42)

    begin_future = tasklets.Future("begin transaction")
    _datastore_api.begin_transaction.return_value = begin_future

    commit_future = tasklets.Future("commit transaction")
    _datastore_api.commit.return_value = commit_future

    begin_future.set_result(b"tx123")
    commit_future.set_result(None)

    dependency = tasklets.Future()
    dependency.set_result(100)

    res = generator_function(dependency)
    assert res.result() == 142


@pytest.mark.usefixtures("in_context")
def test_non_transactional_out_of_transaction():
    @_transaction.non_transactional()
    def simple_function(a, b):
        return a + b

    res = simple_function(100, 42)
    assert res == 142


@pytest.mark.usefixtures("in_context")
def test_non_transactional_in_transaction(in_context):
    with in_context.new(transaction=b"tx123").use():

        def simple_function(a, b):
            return a + b

        wrapped_function = _transaction.non_transactional()(simple_function)

        res = wrapped_function(100, 42)
        assert res == 142

        with pytest.raises(exceptions.BadRequestError):
            wrapped_function = _transaction.non_transactional(
                allow_existing=False
            )(simple_function)
            wrapped_function(100, 42)
