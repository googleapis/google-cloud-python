import datetime
import unittest
import mock
from google.cloud.firestore_v1.proto import firestore_pb2


class TestWatchDocTree(unittest.TestCase):
    def _makeOne(self):
        from google.cloud.firestore_v1.watch import WatchDocTree

        return WatchDocTree()

    def test_insert_and_keys(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        inst = inst.insert("a", 2)
        self.assertEqual(sorted(inst.keys()), ["a", "b"])

    def test_remove_and_keys(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        inst = inst.insert("a", 2)
        inst = inst.remove("a")
        self.assertEqual(sorted(inst.keys()), ["b"])

    def test_insert_and_find(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        inst = inst.insert("a", 2)
        val = inst.find("a")
        self.assertEqual(val.value, 2)

    def test___len__(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        inst = inst.insert("a", 2)
        self.assertEqual(len(inst), 2)

    def test___iter__(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        inst = inst.insert("a", 2)
        self.assertEqual(sorted(list(inst)), ["a", "b"])

    def test___contains__(self):
        inst = self._makeOne()
        inst = inst.insert("b", 1)
        self.assertTrue("b" in inst)
        self.assertFalse("a" in inst)


class TestDocumentChange(unittest.TestCase):
    def _makeOne(self, type, document, old_index, new_index):
        from google.cloud.firestore_v1.watch import DocumentChange

        return DocumentChange(type, document, old_index, new_index)

    def test_ctor(self):
        inst = self._makeOne("type", "document", "old_index", "new_index")
        self.assertEqual(inst.type, "type")
        self.assertEqual(inst.document, "document")
        self.assertEqual(inst.old_index, "old_index")
        self.assertEqual(inst.new_index, "new_index")


class TestWatchResult(unittest.TestCase):
    def _makeOne(self, snapshot, name, change_type):
        from google.cloud.firestore_v1.watch import WatchResult

        return WatchResult(snapshot, name, change_type)

    def test_ctor(self):
        inst = self._makeOne("snapshot", "name", "change_type")
        self.assertEqual(inst.snapshot, "snapshot")
        self.assertEqual(inst.name, "name")
        self.assertEqual(inst.change_type, "change_type")


class Test_maybe_wrap_exception(unittest.TestCase):
    def _callFUT(self, exc):
        from google.cloud.firestore_v1.watch import _maybe_wrap_exception

        return _maybe_wrap_exception(exc)

    def test_is_grpc_error(self):
        import grpc
        from google.api_core.exceptions import GoogleAPICallError

        exc = grpc.RpcError()
        result = self._callFUT(exc)
        self.assertEqual(result.__class__, GoogleAPICallError)

    def test_is_not_grpc_error(self):
        exc = ValueError()
        result = self._callFUT(exc)
        self.assertEqual(result.__class__, ValueError)


class Test_document_watch_comparator(unittest.TestCase):
    def _callFUT(self, doc1, doc2):
        from google.cloud.firestore_v1.watch import document_watch_comparator

        return document_watch_comparator(doc1, doc2)

    def test_same_doc(self):
        result = self._callFUT(1, 1)
        self.assertEqual(result, 0)

    def test_diff_doc(self):
        self.assertRaises(AssertionError, self._callFUT, 1, 2)


class Test_should_recover(unittest.TestCase):
    def _callFUT(self, exception):
        from google.cloud.firestore_v1.watch import _should_recover

        return _should_recover(exception)

    def test_w_unavailable(self):
        from google.api_core.exceptions import ServiceUnavailable

        exception = ServiceUnavailable("testing")

        self.assertTrue(self._callFUT(exception))

    def test_w_non_recoverable(self):
        exception = ValueError("testing")

        self.assertFalse(self._callFUT(exception))


class Test_should_terminate(unittest.TestCase):
    def _callFUT(self, exception):
        from google.cloud.firestore_v1.watch import _should_terminate

        return _should_terminate(exception)

    def test_w_unavailable(self):
        from google.api_core.exceptions import Cancelled

        exception = Cancelled("testing")

        self.assertTrue(self._callFUT(exception))

    def test_w_non_recoverable(self):
        exception = ValueError("testing")

        self.assertFalse(self._callFUT(exception))


class TestWatch(unittest.TestCase):
    def _makeOne(
        self,
        document_reference=None,
        firestore=None,
        target=None,
        comparator=None,
        snapshot_callback=None,
        snapshot_class=None,
        reference_class=None,
    ):  # pragma: NO COVER
        from google.cloud.firestore_v1.watch import Watch

        if document_reference is None:
            document_reference = DummyDocumentReference()
        if firestore is None:
            firestore = DummyFirestore()
        if target is None:
            WATCH_TARGET_ID = 0x5079  # "Py"
            target = {"documents": {"documents": ["/"]}, "target_id": WATCH_TARGET_ID}
        if comparator is None:
            comparator = self._document_watch_comparator
        if snapshot_callback is None:
            snapshot_callback = self._snapshot_callback
        if snapshot_class is None:
            snapshot_class = DummyDocumentSnapshot
        if reference_class is None:
            reference_class = DummyDocumentReference
        inst = Watch(
            document_reference,
            firestore,
            target,
            comparator,
            snapshot_callback,
            snapshot_class,
            reference_class,
            BackgroundConsumer=DummyBackgroundConsumer,
            ResumableBidiRpc=DummyRpc,
        )
        return inst

    def setUp(self):
        self.snapshotted = None

    def _document_watch_comparator(self, doc1, doc2):  # pragma: NO COVER
        return 0

    def _snapshot_callback(self, docs, changes, read_time):
        self.snapshotted = (docs, changes, read_time)

    def test_ctor(self):
        from google.cloud.firestore_v1.proto import firestore_pb2
        from google.cloud.firestore_v1.watch import _should_recover
        from google.cloud.firestore_v1.watch import _should_terminate

        inst = self._makeOne()
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst._rpc.callbacks, [inst._on_rpc_done])
        self.assertIs(inst._rpc.start_rpc, inst._api.transport.listen)
        self.assertIs(inst._rpc.should_recover, _should_recover)
        self.assertIs(inst._rpc.should_terminate, _should_terminate)
        self.assertIsInstance(inst._rpc.initial_request, firestore_pb2.ListenRequest)
        self.assertEqual(inst._rpc.metadata, DummyFirestore._rpc_metadata)

    def test__on_rpc_done(self):
        from google.cloud.firestore_v1.watch import _RPC_ERROR_THREAD_NAME

        inst = self._makeOne()
        threading = DummyThreading()
        with mock.patch("google.cloud.firestore_v1.watch.threading", threading):
            inst._on_rpc_done(True)
        self.assertTrue(threading.threads[_RPC_ERROR_THREAD_NAME].started)

    def test_close(self):
        inst = self._makeOne()
        inst.close()
        self.assertEqual(inst._consumer, None)
        self.assertEqual(inst._rpc, None)
        self.assertTrue(inst._closed)

    def test_close_already_closed(self):
        inst = self._makeOne()
        inst._closed = True
        old_consumer = inst._consumer
        inst.close()
        self.assertEqual(inst._consumer, old_consumer)

    def test_close_inactive(self):
        inst = self._makeOne()
        old_consumer = inst._consumer
        old_consumer.is_active = False
        inst.close()
        self.assertEqual(old_consumer.stopped, False)

    def test_unsubscribe(self):
        inst = self._makeOne()
        inst.unsubscribe()
        self.assertTrue(inst._rpc is None)

    def test_for_document(self):
        from google.cloud.firestore_v1.watch import Watch

        docref = DummyDocumentReference()
        snapshot_callback = self._snapshot_callback
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
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst._rpc.callbacks, [inst._on_rpc_done])

    def test_for_query(self):
        from google.cloud.firestore_v1.watch import Watch

        snapshot_callback = self._snapshot_callback
        snapshot_class_instance = DummyDocumentSnapshot
        document_reference_class_instance = DummyDocumentReference
        client = DummyFirestore()
        parent = DummyCollection(client)
        modulename = "google.cloud.firestore_v1.watch"
        pb2 = DummyPb2()
        with mock.patch("%s.firestore_pb2" % modulename, pb2):
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
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst._rpc.callbacks, [inst._on_rpc_done])
        self.assertEqual(inst._targets["query"], "dummy query target")

    def test_for_query_nested(self):
        from google.cloud.firestore_v1.watch import Watch

        snapshot_callback = self._snapshot_callback
        snapshot_class_instance = DummyDocumentSnapshot
        document_reference_class_instance = DummyDocumentReference
        client = DummyFirestore()
        root = DummyCollection(client)
        grandparent = DummyDocument("document", parent=root)
        parent = DummyCollection(client, parent=grandparent)
        modulename = "google.cloud.firestore_v1.watch"
        pb2 = DummyPb2()
        with mock.patch("%s.firestore_pb2" % modulename, pb2):
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
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst._rpc.callbacks, [inst._on_rpc_done])
        self.assertEqual(inst._targets["query"], "dummy query target")

    def test_on_snapshot_target_w_none(self):
        inst = self._makeOne()
        proto = None
        inst.on_snapshot(proto)  # nothing to assert, no mutations, no rtnval
        self.assertTrue(inst._consumer is None)
        self.assertTrue(inst._rpc is None)

    def test_on_snapshot_target_no_change_no_target_ids_not_current(self):
        inst = self._makeOne()
        proto = DummyProto()
        inst.on_snapshot(proto)  # nothing to assert, no mutations, no rtnval

    def test_on_snapshot_target_no_change_no_target_ids_current(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.read_time = 1
        inst.current = True

        def push(read_time, next_resume_token):
            inst._read_time = read_time
            inst._next_resume_token = next_resume_token

        inst.push = push
        inst.on_snapshot(proto)
        self.assertEqual(inst._read_time, 1)
        self.assertEqual(inst._next_resume_token, None)

    def test_on_snapshot_target_add(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.target_change_type = firestore_pb2.TargetChange.ADD
        proto.target_change.target_ids = [1]  # not "Py"
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertEqual(str(exc.exception), "Unexpected target ID 1 sent by server")

    def test_on_snapshot_target_remove(self):
        inst = self._makeOne()
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.REMOVE
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertEqual(str(exc.exception), "Error 1:  hi")

    def test_on_snapshot_target_remove_nocause(self):
        inst = self._makeOne()
        proto = DummyProto()
        target_change = proto.target_change
        target_change.cause = None
        target_change.target_change_type = firestore_pb2.TargetChange.REMOVE
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertEqual(str(exc.exception), "Error 13:  internal error")

    def test_on_snapshot_target_reset(self):
        inst = self._makeOne()

        def reset():
            inst._docs_reset = True

        inst._reset_docs = reset
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.RESET
        inst.on_snapshot(proto)
        self.assertTrue(inst._docs_reset)

    def test_on_snapshot_target_current(self):
        inst = self._makeOne()
        inst.current = False
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.CURRENT
        inst.on_snapshot(proto)
        self.assertTrue(inst.current)

    def test_on_snapshot_target_unknown(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.target_change_type = "unknown"
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertTrue(inst._consumer is None)
        self.assertTrue(inst._rpc is None)
        self.assertEqual(str(exc.exception), "Unknown target change type: unknown ")

    def test_on_snapshot_document_change_removed(self):
        from google.cloud.firestore_v1.watch import WATCH_TARGET_ID, ChangeType

        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ""
        proto.document_change.removed_target_ids = [WATCH_TARGET_ID]

        class DummyDocument:
            name = "fred"

        proto.document_change.document = DummyDocument()
        inst.on_snapshot(proto)
        self.assertTrue(inst.change_map["fred"] is ChangeType.REMOVED)

    def test_on_snapshot_document_change_changed(self):
        from google.cloud.firestore_v1.watch import WATCH_TARGET_ID

        inst = self._makeOne()

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
        self.assertEqual(inst.change_map["fred"].data, {})

    def test_on_snapshot_document_change_changed_docname_db_prefix(self):
        # TODO: Verify the current behavior. The change map currently contains
        # the db-prefixed document name and not the bare document name.
        from google.cloud.firestore_v1.watch import WATCH_TARGET_ID

        inst = self._makeOne()

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
        self.assertEqual(inst.change_map["abc://foo/documents/fred"].data, {})

    def test_on_snapshot_document_change_neither_changed_nor_removed(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ""
        proto.document_change.target_ids = []

        inst.on_snapshot(proto)
        self.assertTrue(not inst.change_map)

    def test_on_snapshot_document_removed(self):
        from google.cloud.firestore_v1.watch import ChangeType

        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ""
        proto.document_change = ""

        class DummyRemove(object):
            document = "fred"

        remove = DummyRemove()
        proto.document_remove = remove
        proto.document_delete = ""
        inst.on_snapshot(proto)
        self.assertTrue(inst.change_map["fred"] is ChangeType.REMOVED)

    def test_on_snapshot_filter_update(self):
        inst = self._makeOne()
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
        self.assertTrue(inst._docs_reset)

    def test_on_snapshot_filter_update_no_size_change(self):
        inst = self._makeOne()
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
        self.assertFalse(inst._docs_reset)

    def test_on_snapshot_unknown_listen_type(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ""
        proto.document_change = ""
        proto.document_remove = ""
        proto.document_delete = ""
        proto.filter = ""
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertTrue(
            str(exc.exception).startswith("Unknown listen response type"),
            str(exc.exception),
        )

    def test_push_callback_called_no_changes(self):
        import pytz

        class DummyReadTime(object):
            seconds = 1534858278

        inst = self._makeOne()
        inst.push(DummyReadTime, "token")
        self.assertEqual(
            self.snapshotted,
            ([], [], datetime.datetime.fromtimestamp(DummyReadTime.seconds, pytz.utc)),
        )
        self.assertTrue(inst.has_pushed)
        self.assertEqual(inst.resume_token, "token")

    def test_push_already_pushed(self):
        class DummyReadTime(object):
            seconds = 1534858278

        inst = self._makeOne()
        inst.has_pushed = True
        inst.push(DummyReadTime, "token")
        self.assertEqual(self.snapshotted, None)
        self.assertTrue(inst.has_pushed)
        self.assertEqual(inst.resume_token, "token")

    def test__current_size_empty(self):
        inst = self._makeOne()
        result = inst._current_size()
        self.assertEqual(result, 0)

    def test__current_size_docmap_has_one(self):
        inst = self._makeOne()
        inst.doc_map["a"] = 1
        result = inst._current_size()
        self.assertEqual(result, 1)

    def test__affects_target_target_id_None(self):
        inst = self._makeOne()
        self.assertTrue(inst._affects_target(None, []))

    def test__affects_target_current_id_in_target_ids(self):
        inst = self._makeOne()
        self.assertTrue(inst._affects_target([1], 1))

    def test__affects_target_current_id_not_in_target_ids(self):
        inst = self._makeOne()
        self.assertFalse(inst._affects_target([1], 2))

    def test__extract_changes_doc_removed(self):
        from google.cloud.firestore_v1.watch import ChangeType

        inst = self._makeOne()
        changes = {"name": ChangeType.REMOVED}
        doc_map = {"name": True}
        results = inst._extract_changes(doc_map, changes, None)
        self.assertEqual(results, (["name"], [], []))

    def test__extract_changes_doc_removed_docname_not_in_docmap(self):
        from google.cloud.firestore_v1.watch import ChangeType

        inst = self._makeOne()
        changes = {"name": ChangeType.REMOVED}
        doc_map = {}
        results = inst._extract_changes(doc_map, changes, None)
        self.assertEqual(results, ([], [], []))

    def test__extract_changes_doc_updated(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        doc = Dummy()
        snapshot = Dummy()
        changes = {"name": snapshot}
        doc_map = {"name": doc}
        results = inst._extract_changes(doc_map, changes, 1)
        self.assertEqual(results, ([], [], [snapshot]))
        self.assertEqual(snapshot.read_time, 1)

    def test__extract_changes_doc_updated_read_time_is_None(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        doc = Dummy()
        snapshot = Dummy()
        snapshot.read_time = None
        changes = {"name": snapshot}
        doc_map = {"name": doc}
        results = inst._extract_changes(doc_map, changes, None)
        self.assertEqual(results, ([], [], [snapshot]))
        self.assertEqual(snapshot.read_time, None)

    def test__extract_changes_doc_added(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        snapshot = Dummy()
        changes = {"name": snapshot}
        doc_map = {}
        results = inst._extract_changes(doc_map, changes, 1)
        self.assertEqual(results, ([], [snapshot], []))
        self.assertEqual(snapshot.read_time, 1)

    def test__extract_changes_doc_added_read_time_is_None(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        snapshot = Dummy()
        snapshot.read_time = None
        changes = {"name": snapshot}
        doc_map = {}
        results = inst._extract_changes(doc_map, changes, None)
        self.assertEqual(results, ([], [snapshot], []))
        self.assertEqual(snapshot.read_time, None)

    def test__compute_snapshot_doctree_and_docmap_disagree_about_length(self):
        inst = self._makeOne()
        doc_tree = {}
        doc_map = {None: None}
        self.assertRaises(
            AssertionError, inst._compute_snapshot, doc_tree, doc_map, None, None, None
        )

    def test__compute_snapshot_operation_relative_ordering(self):
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
        updated_snapshot = DummyDocumentSnapshot(
            updated_doc, None, True, None, None, None
        )
        updated_snapshot.reference = updated_doc
        delete_changes = ["/deleted"]
        add_changes = [added_snapshot]
        update_changes = [updated_snapshot]
        inst = self._makeOne()
        updated_tree, updated_map, applied_changes = inst._compute_snapshot(
            doc_tree, doc_map, delete_changes, add_changes, update_changes
        )
        # TODO: Verify that the assertion here is correct.
        self.assertEqual(
            updated_map, {"/updated": updated_snapshot, "/added": added_snapshot}
        )

    def test__compute_snapshot_modify_docs_updated_doc_no_timechange(self):
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
        updated_snapshot = DummyDocumentSnapshot(
            updated_doc_v2, None, True, None, None, 1
        )
        delete_changes = []
        add_changes = []
        update_changes = [updated_snapshot]
        inst = self._makeOne()
        updated_tree, updated_map, applied_changes = inst._compute_snapshot(
            doc_tree, doc_map, delete_changes, add_changes, update_changes
        )
        self.assertEqual(updated_map, doc_map)  # no change

    def test__compute_snapshot_deletes_w_real_comparator(self):
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
        inst = self._makeOne(comparator=object())
        updated_tree, updated_map, applied_changes = inst._compute_snapshot(
            doc_tree, doc_map, delete_changes, add_changes, update_changes
        )
        self.assertEqual(updated_map, {})

    def test__reset_docs(self):
        from google.cloud.firestore_v1.watch import ChangeType

        inst = self._makeOne()
        inst.change_map = {None: None}
        from google.cloud.firestore_v1.watch import WatchDocTree

        doc = DummyDocumentReference("doc")
        doc_tree = WatchDocTree()
        snapshot = DummyDocumentSnapshot(doc, None, True, None, None, None)
        snapshot.reference = doc
        doc_tree = doc_tree.insert(snapshot, None)
        inst.doc_tree = doc_tree
        inst._reset_docs()
        self.assertEqual(inst.change_map, {"/doc": ChangeType.REMOVED})
        self.assertEqual(inst.resume_token, None)
        self.assertFalse(inst.current)

    def test_resume_token_sent_on_recovery(self):
        inst = self._makeOne()
        inst.resume_token = b"ABCD0123"
        request = inst._get_rpc_request()
        self.assertEqual(request.add_target.resume_token, b"ABCD0123")


class DummyFirestoreStub(object):
    def Listen(self):  # pragma: NO COVER
        pass


class DummyFirestoreClient(object):
    def __init__(self):
        self.transport = mock.Mock(_stubs={"firestore_stub": DummyFirestoreStub()})


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
        self.target_ids = []
        self.removed_target_ids = []
        self.read_time = 0
        self.target_change_type = firestore_pb2.TargetChange.NO_CHANGE
        self.resume_token = None
        self.cause = DummyCause()


class DummyProto(object):
    def __init__(self):
        self.target_change = DummyChange()
        self.document_change = DummyChange()


class DummyTarget(object):
    def QueryTarget(self, **kw):
        self.kw = kw
        return "dummy query target"


class DummyPb2(object):

    Target = DummyTarget()

    def ListenRequest(self, **kw):
        pass
