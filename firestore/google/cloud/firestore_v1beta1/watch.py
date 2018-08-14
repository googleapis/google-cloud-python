# Copyright 2017 Google LLC All rights reserved.
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

import logging
import collections
import threading
import datetime
from enum import Enum

from google.cloud.firestore_v1beta1.bidi import ResumableBidiRpc
from google.cloud.firestore_v1beta1.bidi import BackgroundConsumer
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.api_core import exceptions
from google.protobuf import json_format


# from bidi import BidiRpc, ResumableBidiRpc
import time
import random
import grpc

"""Python client for Google Cloud Firestore Watch."""

_LOGGER = logging.getLogger(__name__)

WATCH_TARGET_ID = 0x5079  # "Py"

GRPC_STATUS_CODE = {
    'OK': 0,
    'CANCELLED': 1,
    'UNKNOWN': 2,
    'INVALID_ARGUMENT': 3,
    'DEADLINE_EXCEEDED': 4,
    'NOT_FOUND': 5,
    'ALREADY_EXISTS': 6,
    'PERMISSION_DENIED': 7,
    'UNAUTHENTICATED': 16,
    'RESOURCE_EXHAUSTED': 8,
    'FAILED_PRECONDITION': 9,
    'ABORTED': 10,
    'OUT_OF_RANGE': 11,
    'UNIMPLEMENTED': 12,
    'INTERNAL': 13,
    'UNAVAILABLE': 14,
    'DATA_LOSS': 15,
    'DO_NOT_USE': -1
}
_RPC_ERROR_THREAD_NAME = 'Thread-OnRpcTerminated'
_RETRYABLE_STREAM_ERRORS = (
    exceptions.DeadlineExceeded,
    exceptions.ServiceUnavailable,
    exceptions.InternalServerError,
    exceptions.Unknown,
    exceptions.GatewayTimeout
)

DocTreeEntry = collections.namedtuple('DocTreeEntry', ['value', 'index'])


class WatchDocTree(object):
    def __init__(self):
        self._dict = {}
        self._index = 0

    def keys(self):
        return list(self._dict.keys())

    def _copy(self):
        wdt = WatchDocTree()
        wdt._dict = self._dict.copy()
        wdt._index = self._index
        self = wdt
        return self

    def insert(self, key, value):
        self = self._copy()
        self._dict[key] = DocTreeEntry(value, self._index)
        self._index += 1
        return self

    def find(self, key):
        return self._dict[key]

    def remove(self, key):
        self = self._copy()
        del self._dict[key]
        return self

    def __len__(self):
        return len(self._dict)


class ChangeType(Enum):
    ADDED = 0
    MODIFIED = 1
    REMOVED = 2


class DocumentChange(object):
    def __init__(self, type, document, old_index, new_index):
        """DocumentChange

        Args:
            type (ChangeType):
            document (document.DocumentSnapshot):
            old_index (int):
            new_index (int):
        """
        # TODO: spec indicated an isEqual param also
        self.type = type
        self.document = document
        self.old_index = old_index
        self.new_index = new_index


class WatchResult(object):
    def __init__(self, snapshot, name, change_type):
        self.snapshot = snapshot
        self.name = name
        self.change_type = change_type


def _maybe_wrap_exception(exception):
    """Wraps a gRPC exception class, if needed."""
    if isinstance(exception, grpc.RpcError):
        return exceptions.from_grpc_error(exception)
    return exception


def is_permanent_error(self, error):
    try:
        if (error.code == GRPC_STATUS_CODE['CANCELLED'] or
                error.code == GRPC_STATUS_CODE['UNKNOWN'] or
                error.code == GRPC_STATUS_CODE['DEADLINE_EXCEEDED'] or
                error.code == GRPC_STATUS_CODE['RESOURCE_EXHAUSTED'] or
                error.code == GRPC_STATUS_CODE['INTERNAL'] or
                error.code == GRPC_STATUS_CODE['UNAVAILABLE'] or
                error.code == GRPC_STATUS_CODE['UNAUTHENTICATED']):
            return False
        else:
            return True
    except AttributeError:
        _LOGGER.error("Unable to determine error code")
        return False


def document_watch_comparator(doc1, doc2):
    assert doc1 == doc2, 'Document watches only support one document.'
    return 0


class ExponentialBackOff(object):
    _INITIAL_SLEEP = 1.0
    """float: Initial "max" for sleep interval."""
    _MAX_SLEEP = 30.0
    """float: Eventual "max" sleep time."""
    _MULTIPLIER = 2.0
    """float: Multiplier for exponential backoff."""

    def __init__(self, initial_sleep=_INITIAL_SLEEP, max_sleep=_MAX_SLEEP,
                 multiplier=_MULTIPLIER):
        self.initial_sleep = self.current_sleep = initial_sleep
        self.max_sleep = max_sleep
        self.multipler = multiplier

    def back_off(self):
        self.current_sleep = self._sleep(self.current_sleep,
                                         self.max_sleep,
                                         self.multipler)

    def reset_to_max(self):
        self.current_sleep = self.max_sleep

    def reset(self):
        self.current_sleep = self._INITIAL_SLEEP

    def _sleep(self, current_sleep, max_sleep=_MAX_SLEEP,
               multiplier=_MULTIPLIER):
        """Sleep and produce a new sleep time.

        .. _Exponential Backoff And Jitter:
            https://www.awsarchitectureblog.com/2015/03/backoff.html

        Select a duration between zero and ``current_sleep``. It might seem
        counterintuitive to have so much jitter, but
        `Exponential Backoff And Jitter`_ argues that "full jitter" is
        the best strategy.

        Args:
            current_sleep (float): The current "max" for sleep interval.
            max_sleep (Optional[float]): Eventual "max" sleep time
            multiplier (Optional[float]): Multiplier for exponential backoff.

        Returns:
            float: Newly doubled ``current_sleep`` or ``max_sleep`` (whichever
            is smaller)
        """
        actual_sleep = random.uniform(0.0, self.current_sleep)
        time.sleep(actual_sleep)
        return min(self.multiplier * self.current_sleep, self.max_sleep)


class Watch(object):
    def __init__(self,
                 document_reference,
                 firestore,
                 target,
                 comparator,
                 snapshot_callback,
                 DocumentSnapshotCls):
        """
        Args:
            firestore:
            target:
            comparator:
            snapshot_callback: Callback method to process snapshots.
                Args:
                    docs (List(DocumentSnapshot)): A callback that returns the
                        ordered list of documents stored in this snapshot.
                    changes (List(str)): A callback that returns the list of
                        changed documents since the last snapshot delivered for
                        this watch.
                    read_time (string): The ISO 8601 time at which this
                        snapshot was obtained.
                    # TODO: Go had an err here and node.js provided size.
                    # TODO: do we want to include either?                    
            DocumentSnapshotCls: instance of the DocumentSnapshot class
        """
        self._document_reference = document_reference
        self._firestore = firestore
        self._api = firestore._firestore_api
        self._targets = target
        self._comparator = comparator
        self.DocumentSnapshot = DocumentSnapshotCls
        self._snapshot_callback = snapshot_callback

        def should_recover(exc):
            return (
                isinstance(exc, grpc.RpcError) and
                exc.code() == grpc.StatusCode.UNVAILABLE)

        initial_request = firestore_pb2.ListenRequest(
            database=self._firestore._database_string,
            add_target=self._targets
        )

        self.rpc = ResumableBidiRpc(
            self._api.firestore_stub.Listen,
            initial_request=initial_request,
            should_recover=should_recover)

        self.rpc.add_done_callback(self._on_rpc_done)

        # Initialize state for on_snapshot
        # The sorted tree of QueryDocumentSnapshots as sent in the last
        # snapshot. We only look at the keys.
        # TODO: using ordered dict right now but not great maybe
        self.doc_tree = WatchDocTree()  # TODO: rbtree(this._comparator)

        # A map of document names to QueryDocumentSnapshots for the last sent
        # snapshot.
        self.doc_map = {}

        # The accumulates map of document changes (keyed by document name) for
        # the current snapshot.
        self.change_map = {}

        # The current state of the query results.
        self.current = False
        
        # We need this to track whether we've pushed an initial set of changes,
        # since we should push those even when there are no changes, if there
        # aren't docs.
        self.has_pushed = False

        # The server assigns and updates the resume token.
        self.resume_token = None

        self._consumer = BackgroundConsumer(self.rpc, self.on_snapshot)
        self._consumer.start()

    def _on_rpc_done(self, future):
        """Triggered whenever the underlying RPC terminates without recovery.

        This is typically triggered from one of two threads: the background
        consumer thread (when calling ``recv()`` produces a non-recoverable
        error) or the grpc management thread (when cancelling the RPC).

        This method is *non-blocking*. It will start another thread to deal
        with shutting everything down. This is to prevent blocking in the
        background consumer and preventing it from being ``joined()``.
        """
        # TODO: look at pushing this down into the background consumer
        _LOGGER.info(
            'RPC termination has signaled shutdown.')
        future = _maybe_wrap_exception(future)
        thread = threading.Thread(
            name=_RPC_ERROR_THREAD_NAME,
            target=self.close,
            kwargs={'reason': future})
        thread.daemon = True
        thread.start()

    @classmethod
    def for_document(cls, document_ref, snapshot_callback,
                     snapshot_class_instance):
        """
        Creates a watch snapshot listener for a document. snapshot_callback
        receives a DocumentChange object, but may also start to get
        targetChange and such soon

        Args:
            document_ref: Reference to Document
            snapshot_callback: callback to be called on snapshot
            snapshot_class_instance: instance of snapshot cls to make 
                snapshots with to pass to snapshot_callback

        """
        return cls(document_ref,
                   document_ref._client,
                   {
                       'documents': {
                           'documents': [document_ref._document_path]},
                       'target_id': WATCH_TARGET_ID
                   },
                   document_watch_comparator,
                   snapshot_callback,
                   snapshot_class_instance)

    # @classmethod
    # def for_query(cls, query, snapshot_callback):
    #     return cls(query._client,
    #                {
    #                    'query': query.to_proto(),
    #                    'target_id': WATCH_TARGET_ID
    #                },
    #                query.comparator(),
    #                snapshot_callback)

    def on_snapshot(self, proto):
        """
        Called everytime there is a response from listen. Collect changes
        and 'push' the changes in a batch to the customer when we receive
        'current' from the listen response.

        Args:
            listen_response(`google.cloud.firestore_v1beta1.types.ListenResponse`):
                Callback method that receives a object to
        """
        TargetChange = firestore_pb2.TargetChange

        if str(proto.target_change):
            _LOGGER.debug('on_snapshot: target change')

            # google.cloud.firestore_v1beta1.types.TargetChange
            change = proto.target_change

            no_target_ids = change.target_ids is None or \
                len(change.target_ids) == 0
            if change.target_change_type == TargetChange.NO_CHANGE:
                _LOGGER.debug('on_snapshot: target change: NO_CHANGE')
                if no_target_ids and change.read_time and self.current: 
                    # TargetChange.CURRENT followed by TargetChange.NO_CHANGE
                    # signals a consistent state. Invoke the onSnapshot
                    # callback as specified by the user.
                    self.push(change.read_time, change.resume_token)
            elif change.target_change_type == TargetChange.ADD:
                _LOGGER.debug("on_snapshot: target change: ADD")
                assert WATCH_TARGET_ID == change.target_ids[0], \
                    'Unexpected target ID sent by server'
                # TODO : do anything here? Node didn't so I think this isn't
                # the right thing to do
                # wr = WatchResult(
                #     None,
                #     self._document_reference.id,
                #     ChangeType.ADDED)
                # self._snapshot_callback(wr)

            elif change.target_change_type == TargetChange.REMOVE:
                _LOGGER.debug("on_snapshot: target change: REMOVE")

                code = 13
                message = 'internal error'
                if change.cause:
                    code = change.cause.code
                    message = change.cause.message

                # TODO: Surface a .code property on the exception.
                raise Exception('Error ' + code + ': ' + message)
            elif change.target_change_type == TargetChange.RESET:
                # Whatever changes have happened so far no longer matter.
                _LOGGER.debug("on_snapshot: target change: RESET")
                self._reset_docs()
            elif change.target_change_type == TargetChange.CURRENT:
                _LOGGER.debug("on_snapshot: target change: CURRENT")
                self.current = True
            else:
                _LOGGER.info('on_snapshot: Unknown target change ' +
                             str(change.target_change_type))

                self._consumer.stop()
                # closeStream(
                #   new Error('Unknown target change type: ' +
                #       JSON.stringify(change))
                # TODO : make this exit the inner function and stop processing?
                raise Exception('Unknown target change type: ' + str(change))

            if change.resume_token and self._affects_target(change.target_ids,
                                                            WATCH_TARGET_ID):
                # TODO: they node version resets backoff here. We allow
                # bidi rpc to do its thing.
                pass

        elif str(proto.document_change):
            _LOGGER.debug('on_snapshot: document change')

            # No other target_ids can show up here, but we still need to see 
            # if the targetId was in the added list or removed list.
            target_ids = proto.document_change.target_ids or []
            removed_target_ids = proto.document_change.removed_target_ids or []
            changed = False
            removed = False

            for target in target_ids:
                if target == WATCH_TARGET_ID:
                    changed = True

            for target in removed_target_ids:
                if target == WATCH_TARGET_ID:
                    removed = True

            if changed:
                _LOGGER.debug('on_snapshot: document change: CHANGED')

                # google.cloud.firestore_v1beta1.types.DocumentChange
                document_change = proto.document_change
                # google.cloud.firestore_v1beta1.types.Document
                document = document_change.document

                data = json_format.MessageToDict(document)

                snapshot = self.DocumentSnapshot(
                    reference=self._document_reference,
                    data=data['fields'],
                    exists=True,
                    read_time=None,
                    create_time=document.create_time,
                    update_time=document.update_time)

                self.change_map[document.name] = snapshot
                # TODO: ensure we call this later, on current returend.
                # wr = WatchResult(snapshot,
                #                    self._document_reference.id,
                #                    ChangeType.MODIFIED)
                # self._snapshot_callback(wr)

            elif removed:
                _LOGGER.debug('on_snapshot: document change: REMOVED')
                self.change_map[document.name] = ChangeType.REMOVED

        elif (proto.document_delete or proto.document_remove):
            _LOGGER.debug('on_snapshot: document change: DELETE/REMOVE')
            name = (proto.document_delete or proto.document_remove).document
            self.change_map[name] = ChangeType.REMOVED
            # wr = WatchResult(None,
            #                    self._document_reference.id,
            #                    ChangeType.REMOVED)
            # self._snapshot_callback(wr)

        elif (proto.filter):
            _LOGGER.debug('on_snapshot: filter update')
            if proto.filter.count != self._current_size():
                # We need to remove all the current results.
                self._reset_docs()
                # The filter didn't match, so re-issue the query.
                # TODO: reset stream method?
                # self._reset_stream();

        else:
            _LOGGER.debug("UNKNOWN TYPE. UHOH")
            self._consumer.stop()
            raise Exception(
                'Unknown listen response type: ' + proto)
            # TODO: can we stop but raise an error?
            #   closeStream(
            #     new Error('Unknown listen response type: ' +
            #        JSON.stringify(proto))
            #   )

    def push(self, read_time, next_resume_token):
        """
        Assembles a new snapshot from the current set of changes and invokes
        the user's callback. Clears the current changes on completion.
        """
        # TODO: may need to lock here to avoid races on collecting snapshots
        # and sending them to the user.

        deletes, adds, updates = Watch._extract_changes(
            self.doc_map, self.change_map, read_time)
        updated_tree, updated_map, appliedChanges = \
            Watch._compute_snapshot(
                self.doc_tree, self.doc_map, deletes, adds, updates)
#         _LOGGER.debug(f"""push
#     self.doc_map {self.doc_map}
#     self.change_map {self.change_map}
#     read_time {read_time}
#     deletes {deletes}
#     adds {adds}
#     updates {updates}
#     updated_tree {updated_tree}
# """)
        if not self.has_pushed or len(appliedChanges):
            _LOGGER.debug(
                f'Sending snapshot with {len(appliedChanges)} changes'
                f' and {len(updated_tree)} documents')

            _LOGGER.debug(f"updatedTree:{updated_tree}")
            self._snapshot_callback(
                updated_tree.keys(),
                appliedChanges,
                datetime.datetime.fromtimestamp(read_time.seconds)
            )
            self.has_pushed = True

        self.doc_tree = updated_tree
        self.doc_map = updated_map
        self.change_map.clear()
        self.resume_token = next_resume_token

    def _extract_changes(doc_map, changes, read_time):
        deletes = []
        adds = []
        updates = []

        for name, value in changes.items():
            if value == ChangeType.REMOVED:
                if name in doc_map:
                    deletes.append(name)
            elif name in doc_map:
                value.read_time = read_time
                updates.append(value)
            else:
                value.read_time = read_time
                adds.append(value)
        _LOGGER.debug(f'deletes:{len(deletes)} adds:{len(adds)}')
        return (deletes, adds, updates)

    def _compute_snapshot(doc_tree, doc_map, delete_changes, add_changes,
                          update_changes):
        # TODO: ACTUALLY NEED TO CALCULATE
        # return {updated_tree, updated_map, appliedChanges};
        # return doc_tree, doc_map, changes

        updated_tree = doc_tree
        updated_map = doc_map

        assert len(doc_tree) == len(doc_map), \
            'The document tree and document map should have the same ' + \
            'number of entries.'

        def delete_doc(name, updated_tree, updated_map):
            """
            Applies a document delete to the document tree and document map.
            Returns the corresponding DocumentChange event.
            """
            assert name in updated_map, 'Document to delete does not exist'
            old_document = updated_map.get(name)
            existing = updated_tree.find(old_document)
            old_index = existing.index
            # TODO: was existing.remove returning tree (presumably immuatable?)
            updated_tree = updated_tree.remove(old_document)
            del updated_map[name]
            return (DocumentChange(ChangeType.REMOVED,
                                   old_document,
                                   old_index,
                                   -1),
                    updated_tree, updated_map)

        def add_doc(new_document, updated_tree, updated_map):
            """
            Applies a document add to the document tree and the document map.
            Returns the corresponding DocumentChange event.
            """
            name = new_document.reference._document_path
            assert name not in updated_map, 'Document to add already exists'
            updated_tree = updated_tree.insert(new_document, None)
            new_index = updated_tree.find(new_document).index
            updated_map[name] = new_document
            return (DocumentChange(ChangeType.ADDED,
                                   new_document,
                                   -1,
                                   new_index),
                    updated_tree, updated_map)

        def modify_doc(new_document, updated_tree, updated_map):
            """
            Applies a document modification to the document tree and the
            document map.
            Returns the DocumentChange event for successful modifications.
            """
            name = new_document.reference.formattedName
            assert updated_map.has(name), 'Document to modify does not exist'
            oldDocument = updated_map.get(name)
            if oldDocument.updateTime != new_document.updateTime:
                removeChange, updated_tree, updated_map = delete_doc(
                    name, updated_tree, updated_map)
                addChange, updated_tree, updated_map = add_doc(
                    new_document, updated_tree, updated_map)
                return (DocumentChange(ChangeType.MODIFIED,
                                       new_document,
                                       removeChange.old_index,
                                       addChange.new_index),
                        updated_tree, updated_map)

            return None

        # Process the sorted changes in the order that is expected by our
        # clients (removals, additions, and then modifications). We also need
        # to sort the individual changes to assure that old_index/new_index
        # keep incrementing.
        appliedChanges = []

        # Deletes are sorted based on the order of the existing document.

        # TODO: SORT
        # delete_changes.sort(
        #     lambda name1, name2:
        #     self._comparator(updated_map.get(name1), updated_map.get(name2)))

        for name in delete_changes:
            change, updated_tree, updated_map = delete_doc(
                name, updated_tree, updated_map)
            if change:
                appliedChanges.append(change)

        # TODO: SORT
        # add_changes.sort(self._comparator)
        _LOGGER.debug('walk over add_changes')
        for snapshot in add_changes:
            _LOGGER.debug('in add_changes')
            change, updated_tree, updated_map = add_doc(
                snapshot, updated_tree, updated_map)
            if change:
                appliedChanges.append(change)

        # TODO: SORT
        # update_changes.sort(self._comparator)
        for snapshot in update_changes:
            change, updated_tree, updated_map = modify_doc(
                snapshot, updated_tree, updated_map)
            if change:
                appliedChanges.append(change)

        assert len(updated_tree) == len(updated_map), \
            'The update document ' + \
            'tree and document map should have the same number of entries.'
        _LOGGER.debug(f"tree:{updated_tree}, map:{updated_map}, applied:{appliedChanges}")
        return (updated_tree, updated_map, appliedChanges)

    def _affects_target(self, target_ids, current_id):
        if target_ids is None or len(target_ids) == 0:
            return True

        for target_id in target_ids:
            if target_id == current_id:
                return True

        return False

    def _current_size(self):
        """
        Returns the current count of all documents, including the changes from
        the current changeMap.
        """
        deletes, adds, _ = Watch._extract_changes(self.docMap, self.changeMap)
        return self.docMap.size + len(adds) - len(deletes)

    def _reset_docs(self):
        """
        Helper to clear the docs on RESET or filter mismatch.
        """
        _LOGGER.debug("resetting documents")
        self.change_map.clear()
        self.resume_token = None

        # TODO: mark each document as deleted. If documents are not delete
        # they will be sent again by the server.
        for snapshot in self.doc_tree:
            document_name = snapshot.reference.formattedName
            self.change_map[document_name] = ChangeType.REMOVED

        self.current = False
