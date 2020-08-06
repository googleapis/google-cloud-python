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
from enum import Enum
import functools

from google.api_core.bidi import ResumableBidiRpc  # type: ignore
from google.api_core.bidi import BackgroundConsumer  # type: ignore
from google.cloud.firestore_v1.types import firestore
from google.cloud.firestore_v1 import _helpers

from google.api_core import exceptions  # type: ignore

import grpc  # type: ignore

"""Python client for Google Cloud Firestore Watch."""

_LOGGER = logging.getLogger(__name__)

WATCH_TARGET_ID = 0x5079  # "Py"

GRPC_STATUS_CODE = {
    "OK": 0,
    "CANCELLED": 1,
    "UNKNOWN": 2,
    "INVALID_ARGUMENT": 3,
    "DEADLINE_EXCEEDED": 4,
    "NOT_FOUND": 5,
    "ALREADY_EXISTS": 6,
    "PERMISSION_DENIED": 7,
    "UNAUTHENTICATED": 16,
    "RESOURCE_EXHAUSTED": 8,
    "FAILED_PRECONDITION": 9,
    "ABORTED": 10,
    "OUT_OF_RANGE": 11,
    "UNIMPLEMENTED": 12,
    "INTERNAL": 13,
    "UNAVAILABLE": 14,
    "DATA_LOSS": 15,
    "DO_NOT_USE": -1,
}
_RPC_ERROR_THREAD_NAME = "Thread-OnRpcTerminated"
_RECOVERABLE_STREAM_EXCEPTIONS = (
    exceptions.Aborted,
    exceptions.Cancelled,
    exceptions.Unknown,
    exceptions.DeadlineExceeded,
    exceptions.ResourceExhausted,
    exceptions.InternalServerError,
    exceptions.ServiceUnavailable,
    exceptions.Unauthenticated,
)
_TERMINATING_STREAM_EXCEPTIONS = (exceptions.Cancelled,)

DocTreeEntry = collections.namedtuple("DocTreeEntry", ["value", "index"])


class WatchDocTree(object):
    # TODO: Currently this uses a dict. Other implementations use a rbtree.
    # The performance of this implementation should be investigated and may
    # require modifying the underlying datastructure to a rbtree.
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

    def __iter__(self):
        for k in self._dict:
            yield k

    def __len__(self):
        return len(self._dict)

    def __contains__(self, k):
        return k in self._dict


class ChangeType(Enum):
    ADDED = 1
    REMOVED = 2
    MODIFIED = 3


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


def document_watch_comparator(doc1, doc2):
    assert doc1 == doc2, "Document watches only support one document."
    return 0


def _should_recover(exception):
    wrapped = _maybe_wrap_exception(exception)
    return isinstance(wrapped, _RECOVERABLE_STREAM_EXCEPTIONS)


def _should_terminate(exception):
    wrapped = _maybe_wrap_exception(exception)
    return isinstance(wrapped, _TERMINATING_STREAM_EXCEPTIONS)


class Watch(object):

    BackgroundConsumer = BackgroundConsumer  # FBO unit tests
    ResumableBidiRpc = ResumableBidiRpc  # FBO unit tests

    def __init__(
        self,
        document_reference,
        firestore,
        target,
        comparator,
        snapshot_callback,
        document_snapshot_cls,
        document_reference_cls,
        BackgroundConsumer=None,  # FBO unit testing
        ResumableBidiRpc=None,  # FBO unit testing
    ):
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

            document_snapshot_cls: instance of DocumentSnapshot
            document_reference_cls: instance of DocumentReference
        """
        self._document_reference = document_reference
        self._firestore = firestore
        self._api = firestore._firestore_api
        self._targets = target
        self._comparator = comparator
        self.DocumentSnapshot = document_snapshot_cls
        self.DocumentReference = document_reference_cls
        self._snapshot_callback = snapshot_callback
        self._closing = threading.Lock()
        self._closed = False

        self.resume_token = None

        rpc_request = self._get_rpc_request

        if ResumableBidiRpc is None:
            ResumableBidiRpc = self.ResumableBidiRpc  # FBO unit tests

        self._rpc = ResumableBidiRpc(
            self._api._transport.listen,
            should_recover=_should_recover,
            should_terminate=_should_terminate,
            initial_request=rpc_request,
            metadata=self._firestore._rpc_metadata,
        )

        self._rpc.add_done_callback(self._on_rpc_done)

        # Initialize state for on_snapshot
        # The sorted tree of QueryDocumentSnapshots as sent in the last
        # snapshot. We only look at the keys.
        self.doc_tree = WatchDocTree()

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
        if BackgroundConsumer is None:  # FBO unit tests
            BackgroundConsumer = self.BackgroundConsumer

        self._consumer = BackgroundConsumer(self._rpc, self.on_snapshot)
        self._consumer.start()

    def _get_rpc_request(self):
        if self.resume_token is not None:
            self._targets["resume_token"] = self.resume_token

        return firestore.ListenRequest(
            database=self._firestore._database_string, add_target=self._targets
        )

    @property
    def is_active(self):
        """bool: True if this manager is actively streaming.

        Note that ``False`` does not indicate this is complete shut down,
        just that it stopped getting new messages.
        """
        return self._consumer is not None and self._consumer.is_active

    def close(self, reason=None):
        """Stop consuming messages and shutdown all helper threads.

        This method is idempotent. Additional calls will have no effect.

        Args:
            reason (Any): The reason to close this. If None, this is considered
                an "intentional" shutdown.
        """
        with self._closing:
            if self._closed:
                return

            # Stop consuming messages.
            if self.is_active:
                _LOGGER.debug("Stopping consumer.")
                self._consumer.stop()
            self._consumer = None

            self._rpc.close()
            self._rpc = None
            self._closed = True
            _LOGGER.debug("Finished stopping manager.")

        if reason:
            # Raise an exception if a reason is provided
            _LOGGER.debug("reason for closing: %s" % reason)
            if isinstance(reason, Exception):
                raise reason
            raise RuntimeError(reason)

    def _on_rpc_done(self, future):
        """Triggered whenever the underlying RPC terminates without recovery.

        This is typically triggered from one of two threads: the background
        consumer thread (when calling ``recv()`` produces a non-recoverable
        error) or the grpc management thread (when cancelling the RPC).

        This method is *non-blocking*. It will start another thread to deal
        with shutting everything down. This is to prevent blocking in the
        background consumer and preventing it from being ``joined()``.
        """
        _LOGGER.info("RPC termination has signaled manager shutdown.")
        future = _maybe_wrap_exception(future)
        thread = threading.Thread(
            name=_RPC_ERROR_THREAD_NAME, target=self.close, kwargs={"reason": future}
        )
        thread.daemon = True
        thread.start()

    def unsubscribe(self):
        self.close()

    @classmethod
    def for_document(
        cls,
        document_ref,
        snapshot_callback,
        snapshot_class_instance,
        reference_class_instance,
    ):
        """
        Creates a watch snapshot listener for a document. snapshot_callback
        receives a DocumentChange object, but may also start to get
        targetChange and such soon

        Args:
            document_ref: Reference to Document
            snapshot_callback: callback to be called on snapshot
            snapshot_class_instance: instance of DocumentSnapshot to make
                snapshots with to pass to snapshot_callback
            reference_class_instance: instance of DocumentReference to make
                references

        """
        return cls(
            document_ref,
            document_ref._client,
            {
                "documents": {"documents": [document_ref._document_path]},
                "target_id": WATCH_TARGET_ID,
            },
            document_watch_comparator,
            snapshot_callback,
            snapshot_class_instance,
            reference_class_instance,
        )

    @classmethod
    def for_query(
        cls, query, snapshot_callback, snapshot_class_instance, reference_class_instance
    ):
        parent_path, _ = query._parent._parent_info()
        query_target = firestore.Target.QueryTarget(
            parent=parent_path, structured_query=query._to_protobuf()
        )

        return cls(
            query,
            query._client,
            {"query": query_target._pb, "target_id": WATCH_TARGET_ID},
            query._comparator,
            snapshot_callback,
            snapshot_class_instance,
            reference_class_instance,
        )

    def _on_snapshot_target_change_no_change(self, proto):
        _LOGGER.debug("on_snapshot: target change: NO_CHANGE")
        change = proto.target_change

        no_target_ids = change.target_ids is None or len(change.target_ids) == 0
        if no_target_ids and change.read_time and self.current:
            # TargetChange.TargetChangeType.CURRENT followed by
            # TargetChange.TargetChangeType.NO_CHANGE
            # signals a consistent state. Invoke the onSnapshot
            # callback as specified by the user.
            self.push(change.read_time, change.resume_token)

    def _on_snapshot_target_change_add(self, proto):
        _LOGGER.debug("on_snapshot: target change: ADD")
        target_id = proto.target_change.target_ids[0]
        if target_id != WATCH_TARGET_ID:
            raise RuntimeError("Unexpected target ID %s sent by server" % target_id)

    def _on_snapshot_target_change_remove(self, proto):
        _LOGGER.debug("on_snapshot: target change: REMOVE")
        change = proto.target_change

        code = 13
        message = "internal error"
        if change.cause:
            code = change.cause.code
            message = change.cause.message

        message = "Error %s:  %s" % (code, message)

        raise RuntimeError(message)

    def _on_snapshot_target_change_reset(self, proto):
        # Whatever changes have happened so far no longer matter.
        _LOGGER.debug("on_snapshot: target change: RESET")
        self._reset_docs()

    def _on_snapshot_target_change_current(self, proto):
        _LOGGER.debug("on_snapshot: target change: CURRENT")
        self.current = True

    def on_snapshot(self, proto):
        """
        Called everytime there is a response from listen. Collect changes
        and 'push' the changes in a batch to the customer when we receive
        'current' from the listen response.

        Args:
            listen_response(`google.cloud.firestore_v1.types.ListenResponse`):
                Callback method that receives a object to
        """
        TargetChange = firestore.TargetChange

        target_changetype_dispatch = {
            TargetChange.TargetChangeType.NO_CHANGE: self._on_snapshot_target_change_no_change,
            TargetChange.TargetChangeType.ADD: self._on_snapshot_target_change_add,
            TargetChange.TargetChangeType.REMOVE: self._on_snapshot_target_change_remove,
            TargetChange.TargetChangeType.RESET: self._on_snapshot_target_change_reset,
            TargetChange.TargetChangeType.CURRENT: self._on_snapshot_target_change_current,
        }

        target_change = getattr(proto, "target_change", "")
        document_change = getattr(proto, "document_change", "")
        document_delete = getattr(proto, "document_delete", "")
        document_remove = getattr(proto, "document_remove", "")
        filter_ = getattr(proto, "filter", "")

        if str(target_change):
            target_change_type = target_change.target_change_type
            _LOGGER.debug("on_snapshot: target change: " + str(target_change_type))
            meth = target_changetype_dispatch.get(target_change_type)
            if meth is None:
                _LOGGER.info(
                    "on_snapshot: Unknown target change " + str(target_change_type)
                )
                self.close(
                    reason="Unknown target change type: %s " % str(target_change_type)
                )
            else:
                try:
                    meth(proto)
                except Exception as exc2:
                    _LOGGER.debug("meth(proto) exc: " + str(exc2))
                    raise

            # NOTE:
            # in other implementations, such as node, the backoff is reset here
            # in this version bidi rpc is just used and will control this.

        elif str(document_change):
            _LOGGER.debug("on_snapshot: document change")

            # No other target_ids can show up here, but we still need to see
            # if the targetId was in the added list or removed list.
            target_ids = document_change.target_ids or []
            removed_target_ids = document_change.removed_target_ids or []
            changed = False
            removed = False

            if WATCH_TARGET_ID in target_ids:
                changed = True

            if WATCH_TARGET_ID in removed_target_ids:
                removed = True

            if changed:
                _LOGGER.debug("on_snapshot: document change: CHANGED")

                # google.cloud.firestore_v1.types.Document
                document = document_change.document

                data = _helpers.decode_dict(document.fields, self._firestore)

                # Create a snapshot. As Document and Query objects can be
                # passed we need to get a Document Reference in a more manual
                # fashion than self._document_reference
                document_name = document.name
                db_str = self._firestore._database_string
                db_str_documents = db_str + "/documents/"
                if document_name.startswith(db_str_documents):
                    document_name = document_name[len(db_str_documents) :]

                document_ref = self._firestore.document(document_name)

                snapshot = self.DocumentSnapshot(
                    reference=document_ref,
                    data=data,
                    exists=True,
                    read_time=None,
                    create_time=document.create_time,
                    update_time=document.update_time,
                )
                self.change_map[document.name] = snapshot

            elif removed:
                _LOGGER.debug("on_snapshot: document change: REMOVED")
                document = document_change.document
                self.change_map[document.name] = ChangeType.REMOVED

        # NB: document_delete and document_remove (as far as we, the client,
        # are concerned) are functionally equivalent

        elif str(document_delete):
            _LOGGER.debug("on_snapshot: document change: DELETE")
            name = document_delete.document
            self.change_map[name] = ChangeType.REMOVED

        elif str(document_remove):
            _LOGGER.debug("on_snapshot: document change: REMOVE")
            name = document_remove.document
            self.change_map[name] = ChangeType.REMOVED

        elif filter_:
            _LOGGER.debug("on_snapshot: filter update")
            if filter_.count != self._current_size():
                # We need to remove all the current results.
                self._reset_docs()
                # The filter didn't match, so re-issue the query.
                # TODO: reset stream method?
                # self._reset_stream();

        elif proto is None:
            self.close()
        else:
            _LOGGER.debug("UNKNOWN TYPE. UHOH")
            self.close(reason=ValueError("Unknown listen response type: %s" % proto))

    def push(self, read_time, next_resume_token):
        """
        Assembles a new snapshot from the current set of changes and invokes
        the user's callback. Clears the current changes on completion.
        """
        deletes, adds, updates = Watch._extract_changes(
            self.doc_map, self.change_map, read_time
        )

        updated_tree, updated_map, appliedChanges = self._compute_snapshot(
            self.doc_tree, self.doc_map, deletes, adds, updates
        )

        if not self.has_pushed or len(appliedChanges):
            # TODO: It is possible in the future we will have the tree order
            # on insert. For now, we sort here.
            key = functools.cmp_to_key(self._comparator)
            keys = sorted(updated_tree.keys(), key=key)

            self._snapshot_callback(keys, appliedChanges, read_time)
            self.has_pushed = True

        self.doc_tree = updated_tree
        self.doc_map = updated_map
        self.change_map.clear()
        self.resume_token = next_resume_token

    @staticmethod
    def _extract_changes(doc_map, changes, read_time):
        deletes = []
        adds = []
        updates = []

        for name, value in changes.items():
            if value == ChangeType.REMOVED:
                if name in doc_map:
                    deletes.append(name)
            elif name in doc_map:
                if read_time is not None:
                    value.read_time = read_time
                updates.append(value)
            else:
                if read_time is not None:
                    value.read_time = read_time
                adds.append(value)

        return (deletes, adds, updates)

    def _compute_snapshot(
        self, doc_tree, doc_map, delete_changes, add_changes, update_changes
    ):
        updated_tree = doc_tree
        updated_map = doc_map

        assert len(doc_tree) == len(doc_map), (
            "The document tree and document map should have the same "
            + "number of entries."
        )

        def delete_doc(name, updated_tree, updated_map):
            """
            Applies a document delete to the document tree and document map.
            Returns the corresponding DocumentChange event.
            """
            assert name in updated_map, "Document to delete does not exist"
            old_document = updated_map.get(name)
            # TODO: If a document doesn't exist this raises IndexError. Handle?
            existing = updated_tree.find(old_document)
            old_index = existing.index
            updated_tree = updated_tree.remove(old_document)
            del updated_map[name]
            return (
                DocumentChange(ChangeType.REMOVED, old_document, old_index, -1),
                updated_tree,
                updated_map,
            )

        def add_doc(new_document, updated_tree, updated_map):
            """
            Applies a document add to the document tree and the document map.
            Returns the corresponding DocumentChange event.
            """
            name = new_document.reference._document_path
            assert name not in updated_map, "Document to add already exists"
            updated_tree = updated_tree.insert(new_document, None)
            new_index = updated_tree.find(new_document).index
            updated_map[name] = new_document
            return (
                DocumentChange(ChangeType.ADDED, new_document, -1, new_index),
                updated_tree,
                updated_map,
            )

        def modify_doc(new_document, updated_tree, updated_map):
            """
            Applies a document modification to the document tree and the
            document map.
            Returns the DocumentChange event for successful modifications.
            """
            name = new_document.reference._document_path
            assert name in updated_map, "Document to modify does not exist"
            old_document = updated_map.get(name)
            if old_document.update_time != new_document.update_time:
                remove_change, updated_tree, updated_map = delete_doc(
                    name, updated_tree, updated_map
                )
                add_change, updated_tree, updated_map = add_doc(
                    new_document, updated_tree, updated_map
                )
                return (
                    DocumentChange(
                        ChangeType.MODIFIED,
                        new_document,
                        remove_change.old_index,
                        add_change.new_index,
                    ),
                    updated_tree,
                    updated_map,
                )

            return None, updated_tree, updated_map

        # Process the sorted changes in the order that is expected by our
        # clients (removals, additions, and then modifications). We also need
        # to sort the individual changes to assure that old_index/new_index
        # keep incrementing.
        appliedChanges = []

        key = functools.cmp_to_key(self._comparator)

        # Deletes are sorted based on the order of the existing document.
        delete_changes = sorted(delete_changes)
        for name in delete_changes:
            change, updated_tree, updated_map = delete_doc(
                name, updated_tree, updated_map
            )
            appliedChanges.append(change)

        add_changes = sorted(add_changes, key=key)
        _LOGGER.debug("walk over add_changes")
        for snapshot in add_changes:
            _LOGGER.debug("in add_changes")
            change, updated_tree, updated_map = add_doc(
                snapshot, updated_tree, updated_map
            )
            appliedChanges.append(change)

        update_changes = sorted(update_changes, key=key)
        for snapshot in update_changes:
            change, updated_tree, updated_map = modify_doc(
                snapshot, updated_tree, updated_map
            )
            if change is not None:
                appliedChanges.append(change)

        assert len(updated_tree) == len(updated_map), (
            "The update document "
            + "tree and document map should have the same number of entries."
        )
        return (updated_tree, updated_map, appliedChanges)

    def _affects_target(self, target_ids, current_id):
        if target_ids is None:
            return True

        return current_id in target_ids

    def _current_size(self):
        """
        Returns the current count of all documents, including the changes from
        the current changeMap.
        """
        deletes, adds, _ = Watch._extract_changes(self.doc_map, self.change_map, None)
        return len(self.doc_map) + len(adds) - len(deletes)

    def _reset_docs(self):
        """
        Helper to clear the docs on RESET or filter mismatch.
        """
        _LOGGER.debug("resetting documents")
        self.change_map.clear()
        self.resume_token = None

        # Mark each document as deleted. If documents are not deleted
        # they will be sent again by the server.
        for snapshot in self.doc_tree.keys():
            name = snapshot.reference._document_path
            self.change_map[name] = ChangeType.REMOVED

        self.current = False
