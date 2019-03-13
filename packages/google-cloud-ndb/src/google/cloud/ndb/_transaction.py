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

import functools

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _datastore_api
from google.cloud.ndb import exceptions
from google.cloud.ndb import _retry
from google.cloud.ndb import tasklets


def in_transaction():
    """Determine if there is a currently active transaction.

    Returns:
        bool: :data:`True` if there is a transaction for the current context,
            otherwise :data:`False`.
    """
    return context_module.get_context().transaction is not None


def transaction(
    callback,
    retries=_retry._DEFAULT_RETRIES,
    read_only=False,
    xg=True,
    propagation=None,
):
    """Run a callback in a transaction.

    Args:
        callback (Callable): The function or tasklet to be called.
        retries (int): Number of times to potentially retry the callback in
            case of transient server errors.
        read_only (bool): Whether to run the transaction in read only mode.
        xg (bool): Enable cross-group transactions. This argument is included
            for backwards compatibility reasons and is ignored. All Datastore
            transactions are cross-group, up to 25 entity groups, all the time.
        propagation (Any): Deprecated, will raise `NotImplementedError` if
            passed. Transaction propagation was a feature of the old Datastore
            RPC library and is no longer available.
    """
    future = transaction_async(
        callback,
        retries=retries,
        read_only=read_only,
        xg=xg,
        propagation=propagation,
    )
    return future.result()


def transaction_async(
    callback,
    retries=_retry._DEFAULT_RETRIES,
    read_only=False,
    xg=True,
    propagation=None,
):
    """Run a callback in a transaction.

    This is the asynchronous version of :func:`transaction`.
    """
    if propagation is not None:
        raise exceptions.NoLongerImplementedError()

    # Keep transaction propagation simple: don't do it.
    context = context_module.get_context()
    if context.transaction:
        raise NotImplementedError(
            "Can't start a transaction during a transaction."
        )

    tasklet = functools.partial(
        _transaction_async, context, callback, read_only=read_only
    )
    if retries:
        tasklet = _retry.retry_async(tasklet, retries=retries)

    return tasklet()


@tasklets.tasklet
def _transaction_async(context, callback, read_only=False):
    # Start the transaction
    transaction_id = yield _datastore_api.begin_transaction(
        read_only, retries=0
    )

    with context.new(transaction=transaction_id).use():
        try:
            # Run the callback
            result = callback()
            if isinstance(result, tasklets.Future):
                result = yield result

            # Commit the transaction
            yield _datastore_api.commit(transaction_id, retries=0)

        # Rollback if there is an error
        except:
            yield _datastore_api.rollback(transaction_id)
            raise

        return result
