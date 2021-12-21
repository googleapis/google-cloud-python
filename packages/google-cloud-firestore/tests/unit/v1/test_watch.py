# Copyright 2020 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import mock
import pytest


def _make_watch_doc_tree(*args, **kwargs):
    from google.cloud.firestore_v1.watch import WatchDocTree

    return WatchDocTree(*args, **kwargs)


def test_watchdoctree_insert_and_keys():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    inst = inst.insert("a", 2)
    assert sorted(inst.keys()) == ["a", "b"]


def test_watchdoctree_remove_and_keys():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    inst = inst.insert("a", 2)
    inst = inst.remove("a")
    assert sorted(inst.keys()) == ["b"]


def test_watchdoctree_insert_and_find():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    inst = inst.insert("a", 2)
    val = inst.find("a")
    assert val.value == 2


def test_watchdoctree___len__():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    inst = inst.insert("a", 2)
    assert len(inst) == 2


def test_watchdoctree___iter__():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    inst = inst.insert("a", 2)
    assert sorted(list(inst)) == ["a", "b"]


def test_watchdoctree___contains__():
    inst = _make_watch_doc_tree()
    inst = inst.insert("b", 1)
    assert "b" in inst
    assert "a" not in inst


def test_documentchange_ctor():
    from google.cloud.firestore_v1.watch import DocumentChange

    inst = DocumentChange("type", "document", "old_index", "new_index")
    assert inst.type == "type"
    assert inst.document == "document"
    assert inst.old_index == "old_index"
    assert inst.new_index == "new_index"


def test_watchresult_ctor():
    from google.cloud.firestore_v1.watch import WatchResult

    inst = WatchResult("snapshot", "name", "change_type")
    assert inst.snapshot == "snapshot"
    assert inst.name == "name"
    assert inst.change_type == "change_type"


def test__maybe_wrap_exception_w_grpc_error():
    import grpc
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud.firestore_v1.watch import _maybe_wrap_exception

    exc = grpc.RpcError()
    result = _maybe_wrap_exception(exc)
    assert result.__class__ == GoogleAPICallError


def test__maybe_wrap_exception_w_non_grpc_error():
    from google.cloud.firestore_v1.watch import _maybe_wrap_exception

    exc = ValueError()
    result = _maybe_wrap_exception(exc)
    assert result.__class__ == ValueError


def test_document_watch_comparator_wsame_doc():
    from google.cloud.firestore_v1.watch import document_watch_comparator

    result = document_watch_comparator(1, 1)
    assert result == 0


def test_document_watch_comparator_wdiff_doc():
    from google.cloud.firestore_v1.watch import document_watch_comparator

    with pytest.raises(AssertionError):
        document_watch_comparator(1, 2)


def test__should_recover_w_unavailable():
    from google.api_core.exceptions import ServiceUnavailable
    from google.cloud.firestore_v1.watch import _should_recover

    exception = ServiceUnavailable("testing")

    assert _should_recover(exception)


def test__should_recover_w_non_recoverable():
    from google.cloud.firestore_v1.watch import _should_recover

    exception = ValueError("testing")

    assert not _should_recover(exception)


def test__should_terminate_w_unavailable():
    from google.api_core.exceptions import Cancelled
    from google.cloud.firestore_v1.watch import _should_terminate

    exception = Cancelled("testing")

    assert _should_terminate(exception)


def test__should_terminate_w_non_recoverable():
    from google.cloud.firestore_v1.watch import _should_terminate

    exception = ValueError("testing")

    assert not _should_terminate(exception)


@pytest.fixture(scope="function")
def snapshots():
    yield []


def _document_watch_comparator(doc1, doc2):  # pragma: NO COVER
    return 0


def _make_watch(
    snapshots=None, comparator=_document_watch_comparator,
):
    from google.cloud.firestore_v1.watch import Watch

    WATCH_TARGET_ID = 0x5079  # "Py"
    target = {"documents": {"documents": ["/"]}, "target_id": WATCH_TARGET_ID}

    if snapshots is None:
        snapshots = []

    def snapshot_callback(*args):
        snapshots.append(args)

    return Watch(
        document_reference=DummyDocumentReference(),
        firestore=DummyFirestore(),
        target=target,
        comparator=comparator,
        snapshot_callback=snapshot_callback,
        document_snapshot_cls=DummyDocumentSnapshot,
        document_reference_cls=DummyDocumentReference,
        BackgroundConsumer=DummyBackgroundConsumer,
        ResumableBidiRpc=DummyRpc,
    )


def test_watch_ctor():
    from google.cloud.firestore_v1.types import firestore
    from google.cloud.firestore_v1.watch import _should_recover
    from google.cloud.firestore_v1.watch import _should_terminate

    inst = _make_watch()
    assert inst._consumer.started
    assert inst._rpc.callbacks, [inst._on_rpc_done]
    assert inst._rpc.start_rpc is inst._api._transport.listen
    assert inst._rpc.should_recover is _should_recover
    assert inst._rpc.should_terminate is _should_terminate
    assert isinstance(inst._rpc.initial_request, firestore.ListenRequest)
    assert inst._rpc.metadata == DummyFirestore._rpc_metadata


def test_watch__on_rpc_done():
    from google.cloud.firestore_v1.watch import _RPC_ERROR_THREAD_NAME

    inst = _make_watch()
    threading = DummyThreading()

    with mock.patch("google.cloud.firestore_v1.watch.threading", threading):
        inst._on_rpc_done(True)

    assert threading.threads[_RPC_ERROR_THREAD_NAME].started


def test_watch_close():
    inst = _make_watch()
    inst.close()
    assert inst._consumer is None
    assert inst._rpc is None
    assert inst._closed


def test_watch_close_already_closed():
    inst = _make_watch()
    inst._closed = True
    old_consumer = inst._consumer
    inst.close()
    assert inst._consumer == old_consumer


def test_watch_close_inactive():
    inst = _make_watch()
    old_consumer = inst._consumer
    old_consumer.is_active = False
    inst.close()
    assert not old_consumer.stopped


def test_watch_unsubscribe():
    inst = _make_watch()
    inst.unsubscribe()
    assert inst._rpc is None


def test_watch_for_document(snapshots):
    from google.cloud.firestore_v1.watch import Watch

    def snapshot_callback(*args):  # pragma: NO COVER
        snapshots.append(args)

    docref = DummyDocumentReference()
    snapshot_class_instance = DummyDocumentSnapshot
    document_reference_class_instance = DummyDocumentReference
    modulename = "google.cloud.firestore_v1.watch"

    with mock.patch("%s.Watch.ResumableBidiRpc" % modulename, DummyRpc):
        with mock.patch(
            "%s.Watch.BackgroundConsumer" % modulename, DummyBackgroundConsumer
        ):
            inst = Watch.for_document(
                docref,
                snapshot_callback,
                snapshot_class_instance,
                document_reference_class_instance,
            )
    assert inst._consumer.started
    assert inst._rpc.callbacks == [inst._on_rpc_done]


def test_watch_for_query(snapshots):
    from google.cloud.firestore_v1.watch import Watch

    def snapshot_callback(*args):  # pragma: NO COVER
        snapshots.append(args)

    snapshot_class_instance = DummyDocumentSnapshot
    document_reference_class_instance = DummyDocumentReference
    client = DummyFirestore()
    parent = DummyCollection(client)
    modulename = "google.cloud.firestore_v1.watch"
    pb2 = DummyPb2()
    with mock.patch("%s.firestore" % modulename, pb2):
        with mock.patch("%s.Watch.ResumableBidiRpc" % modulename, DummyRpc):
            with mock.patch(
                "%s.Watch.BackgroundConsumer" % modulename, DummyBackgroundConsumer
            ):
                query = DummyQuery(parent=parent)
                inst = Watch.for_query(
                    query,
                    snapshot_callback,
                    snapshot_class_instance,
                    document_reference_class_instance,
                )
    assert inst._consumer.started
    assert inst._rpc.callbacks == [inst._on_rpc_done]
    assert inst._targets["query"] == "dummy query target"


def test_watch_for_query_nested(snapshots):
    from google.cloud.firestore_v1.watch import Watch

    def snapshot_callback(*args):  # pragma: NO COVER
        snapshots.append(args)

    snapshot_class_instance = DummyDocumentSnapshot
    document_reference_class_instance = DummyDocumentReference
    client = DummyFirestore()
    root = DummyCollection(client)
    grandparent = DummyDocument("document", parent=root)
    parent = DummyCollection(client, parent=grandparent)
    modulename = "google.cloud.firestore_v1.watch"
    pb2 = DummyPb2()
    with mock.patch("%s.firestore" % modulename, pb2):
        with mock.patch("%s.Watch.ResumableBidiRpc" % modulename, DummyRpc):
            with mock.patch(
                "%s.Watch.BackgroundConsumer" % modulename, DummyBackgroundConsumer
            ):
                query = DummyQuery(parent=parent)
                inst = Watch.for_query(
                    query,
                    snapshot_callback,
                    snapshot_class_instance,
                    document_reference_class_instance,
                )
    assert inst._consumer.started
    assert inst._rpc.callbacks == [inst._on_rpc_done]
    assert inst._targets["query"] == "dummy query target"


def test_watch_on_snapshot_target_w_none():
    inst = _make_watch()
    proto = None
    inst.on_snapshot(proto)  # nothing to assert, no mutations, no rtnval
    assert inst._consumer is None
    assert inst._rpc is None


def test_watch_on_snapshot_target_no_change_no_target_ids_not_current():
    inst = _make_watch()
    proto = DummyProto()
    inst.on_snapshot(proto)  # nothing to assert, no mutations, no rtnval


def test_watch_on_snapshot_target_no_change_no_target_ids_current():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change.read_time = 1
    inst.current = True

    def push(read_time, next_resume_token):
        inst._read_time = read_time
        inst._next_resume_token = next_resume_token

    inst.push = push
    inst.on_snapshot(proto)
    assert inst._read_time == 1
    assert inst._next_resume_token is None


def test_watch_on_snapshot_target_add():
    from google.cloud.firestore_v1.types import firestore

    inst = _make_watch()
    proto = DummyProto()
    proto.target_change.target_change_type = firestore.TargetChange.TargetChangeType.ADD
    proto.target_change.target_ids = [1]  # not "Py"

    with pytest.raises(Exception) as exc:
        inst.on_snapshot(proto)

    assert str(exc.value) == "Unexpected target ID 1 sent by server"


def test_watch_on_snapshot_target_remove():
    from google.cloud.firestore_v1.types import firestore

    inst = _make_watch()
    proto = DummyProto()
    target_change = proto.target_change
    target_change.target_change_type = firestore.TargetChange.TargetChangeType.REMOVE

    with pytest.raises(Exception) as exc:
        inst.on_snapshot(proto)

    assert str(exc.value) == "Error 1:  hi"


def test_watch_on_snapshot_target_remove_nocause():
    from google.cloud.firestore_v1.types import firestore

    inst = _make_watch()
    proto = DummyProto()
    target_change = proto.target_change
    target_change.cause = None
    target_change.target_change_type = firestore.TargetChange.TargetChangeType.REMOVE

    with pytest.raises(Exception) as exc:
        inst.on_snapshot(proto)

    assert str(exc.value) == "Error 13:  internal error"


def test_watch_on_snapshot_target_reset():
    from google.cloud.firestore_v1.types import firestore

    inst = _make_watch()

    def reset():
        inst._docs_reset = True

    inst._reset_docs = reset
    proto = DummyProto()
    target_change = proto.target_change
    target_change.target_change_type = firestore.TargetChange.TargetChangeType.RESET
    inst.on_snapshot(proto)
    assert inst._docs_reset


def test_watch_on_snapshot_target_current():
    from google.cloud.firestore_v1.types import firestore

    inst = _make_watch()
    inst.current = False
    proto = DummyProto()
    target_change = proto.target_change
    target_change.target_change_type = firestore.TargetChange.TargetChangeType.CURRENT
    inst.on_snapshot(proto)
    assert inst.current


def test_watch_on_snapshot_target_unknown():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change.target_change_type = "unknown"

    with pytest.raises(Exception) as exc:
        inst.on_snapshot(proto)

    assert inst._consumer is None
    assert inst._rpc is None
    assert str(exc.value) == "Unknown target change type: unknown "


def test_watch_on_snapshot_document_change_removed():
    from google.cloud.firestore_v1.watch import WATCH_TARGET_ID, ChangeType

    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change.removed_target_ids = [WATCH_TARGET_ID]

    class DummyDocument:
        name = "fred"

    proto.document_change.document = DummyDocument()
    inst.on_snapshot(proto)
    assert inst.change_map["fred"] is ChangeType.REMOVED


def test_watch_on_snapshot_document_change_changed():
    from google.cloud.firestore_v1.watch import WATCH_TARGET_ID

    inst = _make_watch()

    proto = DummyProto()
    proto.target_change = ""
    proto.document_change.target_ids = [WATCH_TARGET_ID]

    class DummyDocument:
        name = "fred"
        fields = {}
        create_time = None
        update_time = None

    proto.document_change.document = DummyDocument()
    inst.on_snapshot(proto)
    assert inst.change_map["fred"].data == {}


def test_watch_on_snapshot_document_change_changed_docname_db_prefix():
    # TODO: Verify the current behavior. The change map currently contains
    # the db-prefixed document name and not the bare document name.
    from google.cloud.firestore_v1.watch import WATCH_TARGET_ID

    inst = _make_watch()

    proto = DummyProto()
    proto.target_change = ""
    proto.document_change.target_ids = [WATCH_TARGET_ID]

    class DummyDocument:
        name = "abc://foo/documents/fred"
        fields = {}
        create_time = None
        update_time = None

    proto.document_change.document = DummyDocument()
    inst._firestore._database_string = "abc://foo"
    inst.on_snapshot(proto)
    assert inst.change_map["abc://foo/documents/fred"].data == {}


def test_watch_on_snapshot_document_change_neither_changed_nor_removed():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change.target_ids = []

    inst.on_snapshot(proto)
    assert not inst.change_map


def test_watch_on_snapshot_document_removed():
    from google.cloud.firestore_v1.watch import ChangeType

    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change = ""

    class DummyRemove(object):
        document = "fred"

    remove = DummyRemove()
    proto.document_remove = remove
    proto.document_delete = ""
    inst.on_snapshot(proto)
    assert inst.change_map["fred"] is ChangeType.REMOVED


def test_watch_on_snapshot_filter_update():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change = ""
    proto.document_remove = ""
    proto.document_delete = ""

    class DummyFilter(object):
        count = 999

    proto.filter = DummyFilter()

    def reset():
        inst._docs_reset = True

    inst._reset_docs = reset
    inst.on_snapshot(proto)
    assert inst._docs_reset


def test_watch_on_snapshot_filter_update_no_size_change():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change = ""
    proto.document_remove = ""
    proto.document_delete = ""

    class DummyFilter(object):
        count = 0

    proto.filter = DummyFilter()
    inst._docs_reset = False

    inst.on_snapshot(proto)
    assert not inst._docs_reset


def test_watch_on_snapshot_unknown_listen_type():
    inst = _make_watch()
    proto = DummyProto()
    proto.target_change = ""
    proto.document_change = ""
    proto.document_remove = ""
    proto.document_delete = ""
    proto.filter = ""

    with pytest.raises(Exception) as exc:
        inst.on_snapshot(proto)

    assert str(exc.value).startswith("Unknown listen response type")


def test_watch_push_callback_called_no_changes(snapshots):
    dummy_time = (datetime.datetime.fromtimestamp(1534858278, datetime.timezone.utc),)

    inst = _make_watch(snapshots=snapshots)
    inst.push(dummy_time, "token")
    assert snapshots == [([], [], dummy_time)]
    assert inst.has_pushed
    assert inst.resume_token == "token"


def test_watch_push_already_pushed(snapshots):
    class DummyReadTime(object):
        seconds = 1534858278

    inst = _make_watch(snapshots=snapshots)
    inst.has_pushed = True
    inst.push(DummyReadTime, "token")
    assert snapshots == []
    assert inst.has_pushed
    assert inst.resume_token == "token"


def test_watch__current_size_empty():
    inst = _make_watch()
    result = inst._current_size()
    assert result == 0


def test_watch__current_size_docmap_has_one():
    inst = _make_watch()
    inst.doc_map["a"] = 1
    result = inst._current_size()
    assert result == 1


def test_watch__affects_target_target_id_None():
    inst = _make_watch()
    assert inst._affects_target(None, [])


def test_watch__affects_target_current_id_in_target_ids():
    inst = _make_watch()
    assert inst._affects_target([1], 1)


def test_watch__affects_target_current_id_not_in_target_ids():
    inst = _make_watch()
    assert not inst._affects_target([1], 2)


def test_watch__extract_changes_doc_removed():
    from google.cloud.firestore_v1.watch import ChangeType

    inst = _make_watch()
    changes = {"name": ChangeType.REMOVED}
    doc_map = {"name": True}
    results = inst._extract_changes(doc_map, changes, None)
    assert results == (["name"], [], [])


def test_watch__extract_changes_doc_removed_docname_not_in_docmap():
    from google.cloud.firestore_v1.watch import ChangeType

    inst = _make_watch()
    changes = {"name": ChangeType.REMOVED}
    doc_map = {}
    results = inst._extract_changes(doc_map, changes, None)
    assert results == ([], [], [])


def test_watch__extract_changes_doc_updated():
    inst = _make_watch()

    class Dummy(object):
        pass

    doc = Dummy()
    snapshot = Dummy()
    changes = {"name": snapshot}
    doc_map = {"name": doc}
    results = inst._extract_changes(doc_map, changes, 1)
    assert results == ([], [], [snapshot])
    assert snapshot.read_time == 1


def test_watch__extract_changes_doc_updated_read_time_is_None():
    inst = _make_watch()

    class Dummy(object):
        pass

    doc = Dummy()
    snapshot = Dummy()
    snapshot.read_time = None
    changes = {"name": snapshot}
    doc_map = {"name": doc}
    results = inst._extract_changes(doc_map, changes, None)
    assert results == ([], [], [snapshot])
    assert snapshot.read_time is None


def test_watch__extract_changes_doc_added():
    inst = _make_watch()

    class Dummy(object):
        pass

    snapshot = Dummy()
    changes = {"name": snapshot}
    doc_map = {}
    results = inst._extract_changes(doc_map, changes, 1)
    assert results == ([], [snapshot], [])
    assert snapshot.read_time == 1


def test_watch__extract_changes_doc_added_read_time_is_None():
    inst = _make_watch()

    class Dummy(object):
        pass

    snapshot = Dummy()
    snapshot.read_time = None
    changes = {"name": snapshot}
    doc_map = {}
    results = inst._extract_changes(doc_map, changes, None)
    assert results == ([], [snapshot], [])
    assert snapshot.read_time is None


def test_watch__compute_snapshot_doctree_and_docmap_disagree_about_length():
    inst = _make_watch()
    doc_tree = {}
    doc_map = {None: None}

    with pytest.raises(AssertionError):
        inst._compute_snapshot(doc_tree, doc_map, None, None, None)


def test_watch__compute_snapshot_operation_relative_ordering():
    from google.cloud.firestore_v1.watch import WatchDocTree

    doc_tree = WatchDocTree()

    class DummyDoc(object):
        update_time = mock.sentinel

    deleted_doc = DummyDoc()
    added_doc = DummyDoc()
    added_doc._document_path = "/added"
    updated_doc = DummyDoc()
    updated_doc._document_path = "/updated"
    doc_tree = doc_tree.insert(deleted_doc, None)
    doc_tree = doc_tree.insert(updated_doc, None)
    doc_map = {"/deleted": deleted_doc, "/updated": updated_doc}
    added_snapshot = DummyDocumentSnapshot(added_doc, None, True, None, None, None)
    added_snapshot.reference = added_doc
    updated_snapshot = DummyDocumentSnapshot(updated_doc, None, True, None, None, None)
    updated_snapshot.reference = updated_doc
    delete_changes = ["/deleted"]
    add_changes = [added_snapshot]
    update_changes = [updated_snapshot]
    inst = _make_watch()
    updated_tree, updated_map, applied_changes = inst._compute_snapshot(
        doc_tree, doc_map, delete_changes, add_changes, update_changes
    )
    # TODO: Verify that the assertion here is correct.
    assert updated_map == {"/updated": updated_snapshot, "/added": added_snapshot}


def test_watch__compute_snapshot_modify_docs_updated_doc_no_timechange():
    from google.cloud.firestore_v1.watch import WatchDocTree

    doc_tree = WatchDocTree()

    class DummyDoc(object):
        pass

    updated_doc_v1 = DummyDoc()
    updated_doc_v1.update_time = 1
    updated_doc_v1._document_path = "/updated"
    updated_doc_v2 = DummyDoc()
    updated_doc_v2.update_time = 1
    updated_doc_v2._document_path = "/updated"
    doc_tree = doc_tree.insert("/updated", updated_doc_v1)
    doc_map = {"/updated": updated_doc_v1}
    updated_snapshot = DummyDocumentSnapshot(updated_doc_v2, None, True, None, None, 1)
    delete_changes = []
    add_changes = []
    update_changes = [updated_snapshot]
    inst = _make_watch()
    updated_tree, updated_map, applied_changes = inst._compute_snapshot(
        doc_tree, doc_map, delete_changes, add_changes, update_changes
    )
    assert updated_map == doc_map  # no change


def test_watch__compute_snapshot_deletes_w_real_comparator():
    from google.cloud.firestore_v1.watch import WatchDocTree

    doc_tree = WatchDocTree()

    class DummyDoc(object):
        update_time = mock.sentinel

    deleted_doc_1 = DummyDoc()
    deleted_doc_2 = DummyDoc()
    doc_tree = doc_tree.insert(deleted_doc_1, None)
    doc_tree = doc_tree.insert(deleted_doc_2, None)
    doc_map = {"/deleted_1": deleted_doc_1, "/deleted_2": deleted_doc_2}
    delete_changes = ["/deleted_1", "/deleted_2"]
    add_changes = []
    update_changes = []
    inst = _make_watch(comparator=object())
    updated_tree, updated_map, applied_changes = inst._compute_snapshot(
        doc_tree, doc_map, delete_changes, add_changes, update_changes
    )
    assert updated_map == {}


def test_watch__reset_docs():
    from google.cloud.firestore_v1.watch import ChangeType

    inst = _make_watch()
    inst.change_map = {None: None}
    from google.cloud.firestore_v1.watch import WatchDocTree

    doc = DummyDocumentReference("doc")
    doc_tree = WatchDocTree()
    snapshot = DummyDocumentSnapshot(doc, None, True, None, None, None)
    snapshot.reference = doc
    doc_tree = doc_tree.insert(snapshot, None)
    inst.doc_tree = doc_tree
    inst._reset_docs()
    assert inst.change_map == {"/doc": ChangeType.REMOVED}
    assert inst.resume_token is None
    assert not inst.current


def test_watch_resume_token_sent_on_recovery():
    inst = _make_watch()
    inst.resume_token = b"ABCD0123"
    request = inst._get_rpc_request()
    assert request.add_target.resume_token == b"ABCD0123"


class DummyFirestoreStub(object):
    def Listen(self):  # pragma: NO COVER
        pass


class DummyFirestoreClient(object):
    def __init__(self):
        self._transport = mock.Mock(_stubs={"firestore_stub": DummyFirestoreStub()})


class DummyDocumentReference(object):
    def __init__(self, *document_path, **kw):
        if "client" not in kw:
            self._client = DummyFirestore()
        else:
            self._client = kw["client"]

        self._path = document_path
        self._document_path = "/" + "/".join(document_path)
        self.__dict__.update(kw)


class DummyDocument(object):
    def __init__(self, name, parent):
        self._name = name
        self._parent = parent

    @property
    def _document_path(self):
        return "{}/documents/{}".format(
            self._parent._client._database_string, self._name
        )


class DummyCollection(object):
    def __init__(self, client, parent=None):
        self._client = client
        self._parent = parent

    def _parent_info(self):
        if self._parent is None:
            return "{}/documents".format(self._client._database_string), None
        return self._parent._document_path, None


def _compare(x, y):  # pragma: NO COVER
    return 1


class DummyQuery(object):
    def __init__(self, parent):
        self._comparator = _compare
        self._parent = parent

    @property
    def _client(self):
        return self._parent._client

    def _to_protobuf(self):
        return ""


class DummyFirestore(object):
    _firestore_api = DummyFirestoreClient()
    _database_string = "abc://bar/"
    _rpc_metadata = None

    def ListenRequest(self, **kw):  # pragma: NO COVER
        pass

    def document(self, *document_path):  # pragma: NO COVER
        if len(document_path) == 1:
            path = document_path[0].split("/")
        else:
            path = document_path

        return DummyDocumentReference(*path, client=self)


class DummyDocumentSnapshot(object):
    # def __init__(self, **kw):
    #     self.__dict__.update(kw)
    def __init__(self, reference, data, exists, read_time, create_time, update_time):
        self.reference = reference
        self.data = data
        self.exists = exists
        self.read_time = read_time
        self.create_time = create_time
        self.update_time = update_time

    def __str__(self):
        return "%s-%s" % (self.reference._document_path, self.read_time)

    def __hash__(self):
        return hash(str(self))


class DummyBackgroundConsumer(object):
    started = False
    stopped = False
    is_active = True

    def __init__(self, rpc, on_snapshot):
        self._rpc = rpc
        self.on_snapshot = on_snapshot

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True
        self.is_active = False


class DummyThread(object):
    started = False

    def __init__(self, name, target, kwargs):
        self.name = name
        self.target = target
        self.kwargs = kwargs

    def start(self):
        self.started = True


class DummyThreading(object):
    def __init__(self):
        self.threads = {}

    def Thread(self, name, target, kwargs):
        thread = DummyThread(name, target, kwargs)
        self.threads[name] = thread
        return thread


class DummyRpc(object):
    def __init__(
        self,
        start_rpc,
        should_recover,
        should_terminate=None,
        initial_request=None,
        metadata=None,
    ):
        self.start_rpc = start_rpc
        self.should_recover = should_recover
        self.should_terminate = should_terminate
        self.initial_request = initial_request()
        self.metadata = metadata
        self.closed = False
        self.callbacks = []

    def add_done_callback(self, callback):
        self.callbacks.append(callback)

    def close(self):
        self.closed = True


class DummyCause(object):
    code = 1
    message = "hi"


class DummyChange(object):
    def __init__(self):
        from google.cloud.firestore_v1.types import firestore

        self.target_ids = []
        self.removed_target_ids = []
        self.read_time = 0
        self.target_change_type = firestore.TargetChange.TargetChangeType.NO_CHANGE
        self.resume_token = None
        self.cause = DummyCause()


class DummyProto(object):
    def __init__(self):
        self.target_change = DummyChange()
        self.document_change = DummyChange()


class DummyTarget(object):
    def QueryTarget(self, **kw):
        self.kw = kw
        return DummyQueryTarget()


class DummyQueryTarget(object):
    @property
    def _pb(self):
        return "dummy query target"


class DummyPb2(object):

    Target = DummyTarget()

    def ListenRequest(self, **kw):
        pass
