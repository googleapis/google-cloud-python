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
import logging

from google.cloud.ndb import exceptions
from google.cloud.ndb import _retry
from google.cloud.ndb import tasklets

log = logging.getLogger(__name__)


def in_transaction():
    """Determine if there is a currently active transaction.

    Returns:
        bool: :data:`True` if there is a transaction for the current context,
            otherwise :data:`False`.
    """
    # Avoid circular import in Python 2.7
    from google.cloud.ndb import context as context_module

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
    # Avoid circular import in Python 2.7
    from google.cloud.ndb import context as context_module

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
    # Avoid circular import in Python 2.7
    from google.cloud.ndb import _datastore_api

    # Start the transaction
    log.debug("Start transaction")
    transaction_id = yield _datastore_api.begin_transaction(
        read_only, retries=0
    )
    log.debug("Transaction Id: {}".format(transaction_id))

    on_commit_callbacks = []
    tx_context = context.new(
        transaction=transaction_id, on_commit_callbacks=on_commit_callbacks
    )
    with tx_context.use():
        try:
            # Run the callback
            result = callback()
            if isinstance(result, tasklets.Future):
                result = yield result

            # Commit the transaction
            yield _datastore_api.commit(transaction_id, retries=0)

        # Rollback if there is an error
        except Exception as e:  # noqa: E722
            yield _datastore_api.rollback(transaction_id)
            raise e

        tx_context._clear_global_cache()
        for callback in on_commit_callbacks:
            callback()

        raise tasklets.Return(result)


def transactional(
    retries=_retry._DEFAULT_RETRIES, read_only=False, xg=True, propagation=None
):
    """A decorator to run a function automatically in a transaction.

    Usage example:

    @transactional(retries=1, read_only=False)
    def callback(args):
        ...

    See google.cloud.ndb.transaction for available options.
    """

    def transactional_wrapper(wrapped):
        @functools.wraps(wrapped)
        def transactional_inner_wrapper(*args, **kwargs):
            def callback():
                return wrapped(*args, **kwargs)

            return transaction(
                callback,
                retries=retries,
                read_only=read_only,
                xg=xg,
                propagation=propagation,
            )

        return transactional_inner_wrapper

    return transactional_wrapper


def transactional_async(
    retries=_retry._DEFAULT_RETRIES, read_only=False, xg=True, propagation=None
):
    """A decorator to run a function in an async transaction.

    Usage example:

    @transactional_async(retries=1, read_only=False)
    def callback(args):
        ...

    See google.cloud.ndb.transaction above for available options.
    """

    def transactional_async_wrapper(wrapped):
        @functools.wraps(wrapped)
        def transactional_async_inner_wrapper(*args, **kwargs):
            def callback():
                return wrapped(*args, **kwargs)

            return transaction_async(
                callback,
                retries=retries,
                read_only=read_only,
                xg=xg,
                propagation=propagation,
            )

        return transactional_async_inner_wrapper

    return transactional_async_wrapper


def transactional_tasklet(
    retries=_retry._DEFAULT_RETRIES, read_only=False, xg=True, propagation=None
):
    """A decorator that turns a function into a tasklet running in transaction.

    Wrapped function returns a Future.

    See google.cloud.ndb.transaction above for available options.
    """

    def transactional_tasklet_wrapper(wrapped):
        @functools.wraps(wrapped)
        def transactional_tasklet_inner_wrapper(*args, **kwargs):
            def callback():
                tasklet = tasklets.tasklet(wrapped)
                return tasklet(*args, **kwargs)

            return transaction_async(
                callback,
                retries=retries,
                read_only=read_only,
                xg=xg,
                propagation=propagation,
            )

        return transactional_tasklet_inner_wrapper

    return transactional_tasklet_wrapper


def non_transactional(allow_existing=True):
    """A decorator that ensures a function is run outside a transaction.

    If there is an existing transaction (and allow_existing=True), the existing
    transaction is paused while the function is executed.

    Args:
        allow_existing: If false, an exception will be thrown when called from
            within a transaction. If true, a new non-transactional context will
            be created for running the function; the original transactional
            context will be saved and then restored after the function is
            executed. Defaults to True.
    """

    def non_transactional_wrapper(wrapped):
        @functools.wraps(wrapped)
        def non_transactional_inner_wrapper(*args, **kwargs):
            from . import context

            ctx = context.get_context()
            if not ctx.in_transaction():
                return wrapped(*args, **kwargs)
            if not allow_existing:
                raise exceptions.BadRequestError(
                    "{} cannot be called within a transaction".format(
                        wrapped.__name__
                    )
                )
            new_ctx = ctx.new(transaction=None)
            with new_ctx.use():
                return wrapped(*args, **kwargs)

        return non_transactional_inner_wrapper

    return non_transactional_wrapper
