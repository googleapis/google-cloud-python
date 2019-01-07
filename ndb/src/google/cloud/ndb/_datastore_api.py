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

from google.cloud.ndb import _eventloop
from google.cloud.ndb import _runstate
from google.cloud.ndb import tasklets

_BATCH_LOOKUP = "Lookup"
_NOT_FOUND = object()


def stub():
    """Get the stub for the `Google Datastore` API.

    Gets the stub from the current context, creating one if there isn't one
    already.

    Returns:
        :class:`~google.cloud.datastore_v1.proto.datastore_pb2_grpc.DatastoreStub`:
            The stub instance.
    """
    state = _runstate.current()

    if state.stub is None:
        client = state.client
        if client.secure:
            channel = _helpers.make_secure_channel(
                client._credentials, _http.DEFAULT_USER_AGENT, client.host
            )
        else:
            channel = grpc.insecure_channel(client.host)

        state.stub = datastore_pb2_grpc.DatastoreStub(channel)

    return state.stub


def lookup(key):
    """Look up a Datastore entity.

    Gets an entity from Datastore, asynchronously. Actually adds the request to
    a batch and fires off a Datastore Lookup call as soon as some code asks for
    the result of one of the batched requests.

    Args:
        key (~datastore.Key): The key for the entity to retrieve.

    Returns:
        :class:`~tasklets.Future`: If not an exception, future's result will be
            either an entity protocol buffer or _NOT_FOUND.
    """
    future = tasklets.Future()
    batch = _get_lookup_batch()
    batch_key = key.to_protobuf().SerializeToString()
    batch.setdefault(batch_key, []).append(future)
    return future


def _get_lookup_batch():
    """Gets a data structure for storing batched calls to Datastore Lookup.

    The batch data structure is stored in the current run state. If there is
    not already a batch started, a new structure is created and an idle
    callback is added to the current event loop which will eventually perform
    the batch look up.

    Returns:
        Dict[~datastore_v1.proto.entity_pb2.Key, List[~tasklets.Future]]
    """
    state = _runstate.current()
    batch = state.batches.get(_BATCH_LOOKUP)
    if batch is not None:
        return batch

    state.batches[_BATCH_LOOKUP] = batch = {}
    _eventloop.add_idle(_perform_batch_lookup)
    return batch


def _perform_batch_lookup():
    """Perform a Datastore Lookup on all batched Lookup requests.

    Meant to be used as an idle callback, so that calls to lookup entities can
    be batched into a single request to the back end service as soon as running
    code has need of one of the results.
    """
    state = _runstate.current()
    batch = state.batches.pop(_BATCH_LOOKUP, None)
    if batch is None:
        return

    keys = []
    for batch_key in batch.keys():
        key_pb = entity_pb2.Key()
        key_pb.ParseFromString(batch_key)
        keys.append(key_pb)

    rpc = _datastore_lookup(keys)
    _eventloop.queue_rpc(rpc, BatchLookupCallback(batch))


class BatchLookupCallback:
    """Callback for processing the results of a call to Datastore Lookup.

    Args:
        batch (Dict[~datastore_v1.proto.entity_pb2.Key, List[~tasklets.Future]]):
            Mapping of keys to futures for the batch request.
    """

    def __init__(self, batch):
        self.batch = batch

    def __call__(self, rpc):
        """Process the results of a call to Datastore Lookup.

        Each key in the batch will be in one of `found`, `missing`, or
        `deferred`. `found` keys have their futures' results set with the
        protocol buffers for their entities. `missing` keys have their futures'
        results with `_NOT_FOUND`, a sentinel value. `deferrred` keys are
        loaded into a new batch so they can be tried again.

        Args:
            rpc (grpc.Future): If not an exception, the result will be an
            instance of
            :class:`google.cloud.datastore_v1.datastore_pb.LookupResponse`
        """
        batch = self.batch

        # If RPC has resulted in an exception, propagate that exception to all
        # waiting futures.
        exception = rpc.exception()
        if exception is not None:
            for future in itertools.chain(*batch.values()):
                future.set_exception(exception)
            return

        # Process results, which are divided into found, missing, and deferred
        results = rpc.result()

        # For all deferred keys, batch them up again with their original
        # futures
        if results.deferred:
            next_batch = _get_lookup_batch()
            for key in results.deferred:
                batch_key = key.SerializeToString()
                next_batch.setdefault(batch_key, []).extend(batch[batch_key])

        # For all missing keys, set result to _NOT_FOUND and let callers decide
        # how to handle
        for result in results.missing:
            batch_key = result.entity.key.SerializeToString()
            for future in batch[batch_key]:
                future.set_result(_NOT_FOUND)

        # For all found entities, set the result on their corresponding futures
        for result in results.found:
            entity = result.entity
            batch_key = entity.key.SerializeToString()
            for future in batch[batch_key]:
                future.set_result(entity)


def _datastore_lookup(keys):
    """Issue a Lookup call to Datastore using gRPC.

    Args:
        keys (Iterable[datastore_v1.proto.entity_pb2.Key]): The entity keys to
            look up.

    Returns:
        :class:`grpc.Future`: Future object for eventual result of lookup.
    """
    client = _runstate.current().client
    request = datastore_pb2.LookupRequest(
        project_id=client.project, keys=[key for key in keys]
    )

    api = stub()
    return api.Lookup.future(request)
