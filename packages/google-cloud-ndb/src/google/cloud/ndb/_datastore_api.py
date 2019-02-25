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

"""Functions that interact with Datastore backend."""

import itertools

import grpc

from google.cloud import _helpers
from google.cloud import _http
from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import datastore_pb2_grpc
from google.cloud.datastore_v1.proto import entity_pb2

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _eventloop
from google.cloud.ndb import tasklets

EVENTUAL = datastore_pb2.ReadOptions.EVENTUAL
EVENTUAL_CONSISTENCY = EVENTUAL  # Legacy NDB
_NOT_FOUND = object()


def stub():
    """Get the stub for the `Google Datastore` API.

    Gets the stub from the current context.

    Returns:
        :class:`~google.cloud.datastore_v1.proto.datastore_pb2_grpc.DatastoreStub`:
            The stub instance.
    """
    context = context_module.get_context()
    return context.stub


def make_stub(client):
    """Create the stub for the `Google Datastore` API.

    Args:
        client (client.Client): The NDB client.

    Returns:
        :class:`~google.cloud.datastore_v1.proto.datastore_pb2_grpc.DatastoreStub`:
            The stub instance.
    """
    if client.secure:
        channel = _helpers.make_secure_channel(
            client._credentials, _http.DEFAULT_USER_AGENT, client.host
        )
    else:
        channel = grpc.insecure_channel(client.host)

    return datastore_pb2_grpc.DatastoreStub(channel)


class RemoteCall:
    """Represents a remote call.

    This is primarily a wrapper for futures returned by gRPC. This holds some
    information about the call to make debugging easier. Can be used for
    anything that returns a future for something running outside of our own
    event loop.

    Arguments:
        future (Union[grpc.Future, tasklets.Future]): The future handed back
            from initiating the call.
        info (str): Helpful human readable string about the call. This string
            will be handed back verbatim by calls to :meth:`__repr__`.
    """

    def __init__(self, future, info):
        self.future = future
        self.info = info

    def __repr__(self):
        return self.info

    def exception(self):
        """Calls :meth:`grpc.Future.exception` on attr:`future`."""
        return self.future.exception()

    def result(self):
        """Calls :meth:`grpc.Future.result` on attr:`future`."""
        return self.future.result()

    def add_done_callback(self, callback):
        """Calls :meth:`grpc.Future.add_done_callback` on attr:`future`."""
        return self.future.add_done_callback(callback)


def lookup(key, **options):
    """Look up a Datastore entity.

    Gets an entity from Datastore, asynchronously. Actually adds the request to
    a batch and fires off a Datastore Lookup call as soon as some code asks for
    the result of one of the batched requests.

    Args:
        key (~datastore.Key): The key for the entity to retrieve.
        options (Dict[str, Any]): The options for the request. For example,
            ``{"read_consistency": EVENTUAL}``.

    Returns:
        :class:`~tasklets.Future`: If not an exception, future's result will be
            either an entity protocol buffer or _NOT_FOUND.
    """
    _check_unsupported_options(options)

    batch = _get_batch(_LookupBatch, options)
    return batch.add(key)


def _get_batch(batch_cls, options):
    """Gets a data structure for storing batched calls to Datastore Lookup.

    The batch data structure is stored in the current context. If there is
    not already a batch started, a new structure is created and an idle
    callback is added to the current event loop which will eventually perform
    the batch look up.

    Args:
        batch_cls (type): Class representing the kind of operation being
            batched.
        options (Dict[str, Any]): The options for the request. For example,
            ``{"read_consistency": EVENTUAL}``. Calls with different options
            will be placed in different batches.

    Returns:
        batch_cls: An instance of the batch class.
    """
    context = context_module.get_context()
    batches = context.batches.get(batch_cls)
    if batches is None:
        context.batches[batch_cls] = batches = {}

    options_key = tuple(sorted(options.items()))
    batch = batches.get(options_key)
    if batch is not None:
        return batch

    def idle():
        batch = batches.pop(options_key)
        batch.idle_callback()

    batches[options_key] = batch = batch_cls(options)
    _eventloop.add_idle(idle)
    return batch


class _LookupBatch:
    """Batch for Lookup requests.

    Attributes:
        options (Dict[str, Any]): See Args.
        todo (Dict[bytes, List[tasklets.Future]]: Mapping of serialized key
            protocol buffers to dependent futures.

    Args:
        options (Dict[str, Any]): The options for the request. For example,
            ``{"read_consistency": EVENTUAL}``. Calls with different options
            will be placed in different batches.
    """

    def __init__(self, options):
        self.options = options
        self.todo = {}

    def add(self, key):
        """Add a key to the batch to look up.

        Args:
            key (datastore.Key): The key to look up.

        Returns:
            tasklets.Future: A future for the eventual result.
        """
        todo_key = key.to_protobuf().SerializeToString()
        future = tasklets.Future(info="add({})".format(key))
        self.todo.setdefault(todo_key, []).append(future)
        return future

    def idle_callback(self):
        """Perform a Datastore Lookup on all batched Lookup requests."""
        keys = []
        for todo_key in self.todo.keys():
            key_pb = entity_pb2.Key()
            key_pb.ParseFromString(todo_key)
            keys.append(key_pb)

        read_options = _get_read_options(self.options)
        rpc = _datastore_lookup(keys, read_options)
        _eventloop.queue_rpc(rpc, self.lookup_callback)

    def lookup_callback(self, rpc):
        """Process the results of a call to Datastore Lookup.

        Each key in the batch will be in one of `found`, `missing`, or
        `deferred`. `found` keys have their futures' results set with the
        protocol buffers for their entities. `missing` keys have their futures'
        results with `_NOT_FOUND`, a sentinel value. `deferrred` keys are
        loaded into a new batch so they can be tried again.

        Args:
            rpc (RemoteCall): If not an exception, the result will be an
                instance of
                :class:`google.cloud.datastore_v1.datastore_pb.LookupResponse`
        """
        # If RPC has resulted in an exception, propagate that exception to all
        # waiting futures.
        exception = rpc.exception()
        if exception is not None:
            for future in itertools.chain(*self.todo.values()):
                future.set_exception(exception)
            return

        # Process results, which are divided into found, missing, and deferred
        results = rpc.result()

        # For all deferred keys, batch them up again with their original
        # futures
        if results.deferred:
            next_batch = _get_batch(type(self), self.options)
            for key in results.deferred:
                todo_key = key.SerializeToString()
                next_batch.todo.setdefault(todo_key, []).extend(
                    self.todo[todo_key]
                )

        # For all missing keys, set result to _NOT_FOUND and let callers decide
        # how to handle
        for result in results.missing:
            todo_key = result.entity.key.SerializeToString()
            for future in self.todo[todo_key]:
                future.set_result(_NOT_FOUND)

        # For all found entities, set the result on their corresponding futures
        for result in results.found:
            entity = result.entity
            todo_key = entity.key.SerializeToString()
            for future in self.todo[todo_key]:
                future.set_result(entity)


def _datastore_lookup(keys, read_options):
    """Issue a Lookup call to Datastore using gRPC.

    Args:
        keys (Iterable[entity_pb2.Key]): The entity keys to
            look up.
        read_options (Union[datastore_pb2.ReadOptions, NoneType]): Options for
            the request.

    Returns:
        RemoteCall: Future object for eventual result of lookup.
    """
    client = context_module.get_context().client
    request = datastore_pb2.LookupRequest(
        project_id=client.project,
        keys=[key for key in keys],
        read_options=read_options,
    )

    api = stub()
    return RemoteCall(api.Lookup.future(request), "Lookup({})".format(request))


def _get_read_options(options):
    """Get the read options for a request.

    Args:
        options (Dict[str, Any]): The options for the request. For example,
            ``{"read_consistency": EVENTUAL}``. May contain options unrelated
            to creating a :class:`datastore_pb2.ReadOptions` instance, which
            will be ignored.

    Returns:
        datastore_pb2.ReadOptions: The options instance for passing to the
            Datastore gRPC API.

    Raises:
        ValueError: When ``read_consistency`` is set to ``EVENTUAL`` and there
            is a transaction.
    """
    transaction = _get_transaction(options)

    read_consistency = options.get("read_consistency")
    if read_consistency is None:
        read_consistency = options.get("read_policy")  # Legacy NDB

    if transaction is not None and read_consistency is EVENTUAL:
        raise ValueError(
            "read_consistency must be EVENTUAL when in transaction"
        )

    return datastore_pb2.ReadOptions(
        read_consistency=read_consistency, transaction=transaction
    )


def _get_transaction(options):
    """Get the transaction for a request.

    If specified, this will return the transaction from ``options``. Otherwise,
    it will return the transaction for the current context.

    Args:
        options (Dict[str, Any]): The options for the request. Only
            ``transaction`` will have any bearing here.

    Returns:
        Union[bytes, NoneType]: The transaction identifier, or :data:`None`.
    """
    context = context_module.get_context()
    return options.get("transaction", context.transaction)


def put(entity_pb, **options):
    """Store an entity in datastore.

    The entity can be a new entity to be saved for the first time or an
    existing entity that has been updated.

    Args:
        entity_pb (datastore_v1.types.Entity): The entity to be stored.
        options (Dict[str, Any]): Options for this request.

    Returns:
        tasklets.Future: Result will be completed datastore key
            (entity_pb2.Key) for the entity.
    """
    _check_unsupported_options(options)

    batch = _get_batch(_CommitBatch, options)
    return batch.put(entity_pb)


class _CommitBatch:
    """Batch for tracking a set of mutations for a commit.

    Attributes:
        options (Dict[str, Any]): See Args.
        mutations (List[datastore_pb2.Mutation]): Sequence of mutation protocol
            buffers accumumlated for this batch.
        futures (List[tasklets.Future]): Sequence of futures for return results
            of the commit. The i-th element of ``futures`` corresponds to the
            i-th element of ``mutations``.`

    Args:
        options (Dict[str, Any]): The options for the request. Calls with
            different options will be placed in different batches.
    """

    def __init__(self, options):
        self.options = options
        self.mutations = []
        self.futures = []

    def put(self, entity_pb):
        """Add an entity to batch to be stored.

        Args:
            entity_pb (datastore_v1.types.Entity): The entity to be stored.

        Returns:
            tasklets.Future: Result will be completed datastore key
                (entity_pb2.Key) for the entity.
        """
        future = tasklets.Future(info="put({})".format(entity_pb))
        mutation = datastore_pb2.Mutation(upsert=entity_pb)
        self.mutations.append(mutation)
        self.futures.append(future)
        return future

    def idle_callback(self):
        """Send the commit for this batch to Datastore."""
        rpc = _datastore_commit(self.mutations, _get_transaction(self.options))
        _eventloop.queue_rpc(rpc, self.commit_callback)

    def commit_callback(self, rpc):
        """Process the results of a commit request.

        For each mutation, set the result to the key handed back from
            Datastore. If a key wasn't allocated for the mutation, this will be
            :data:`None`.

        Args:
            rpc (RemoteCall): If not an exception, the result will be an
                instance of
                :class:`google.cloud.datastore_v1.datastore_pb2.CommitResponse`
        """
        # If RPC has resulted in an exception, propagate that exception to all
        # waiting futures.
        exception = rpc.exception()
        if exception is not None:
            for future in self.futures:
                future.set_exception(exception)
            return

        # "The i-th mutation result corresponds to the i-th mutation in the
        # request."
        #
        # https://github.com/googleapis/googleapis/blob/master/google/datastore/v1/datastore.proto#L241
        response = rpc.result()
        results_futures = zip(response.mutation_results, self.futures)
        for mutation_result, future in results_futures:
            # Datastore only sends a key if one is allocated for the
            # mutation. Confusingly, though, if a key isn't allocated, instead
            # of getting None, we get a key with an empty path.
            if mutation_result.key.path:
                key = mutation_result.key
            else:
                key = None
            future.set_result(key)


def _datastore_commit(mutations, transaction):
    """Call Commit on Datastore.

    Args:
        mutations (List[datastore_pb2.Mutation]): The changes to persist to
            Datastore.
        transaction (Union[bytes, NoneType]): The identifier for the
            transaction for this commit, or :data:`None` if no transaction is
            being used.

    Returns:
        RemoteCall: A future for
            :class:`google.cloud.datastore_v1.datastore_pb2.CommitResponse`
    """
    if transaction is None:
        mode = datastore_pb2.CommitRequest.NON_TRANSACTIONAL
    else:
        mode = datastore_pb2.CommitRequest.TRANSACTIONAL

    client = context_module.get_context().client
    request = datastore_pb2.CommitRequest(
        project_id=client.project,
        mode=mode,
        mutations=mutations,
        transaction=transaction,
    )

    api = stub()
    return RemoteCall(api.Commit.future(request), "Commit({})".format(request))


_OPTIONS_SUPPORTED = {"transaction", "read_consistency", "read_policy"}

_OPTIONS_NOT_IMPLEMENTED = {
    "deadline",
    "force_writes",
    "use_cache",
    "use_memcache",
    "use_datastore",
    "memcache_timeout",
    "max_memcache_items",
    "xg",
    "propagation",
    "retries",
}


def _check_unsupported_options(options):
    """Check to see if any passed options are not supported.

    options (Dict[str, Any]): The options for the request. For example,
        ``{"read_consistency": EVENTUAL}``.

    Raises: NotImplementedError if any options are not supported.
    """
    for key in options:
        if key in _OPTIONS_NOT_IMPLEMENTED:
            # option is used in Legacy NDB, but has not yet been implemented in
            # the rewrite, nor have we determined it won't be used, yet.
            raise NotImplementedError(
                "Support for option {!r} has not yet been implemented".format(
                    key
                )
            )

        elif key not in _OPTIONS_SUPPORTED:
            raise NotImplementedError("Passed bad option: {!r}".format(key))
