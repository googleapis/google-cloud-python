# Copyright 2020 Google LLC All rights reserved.
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

import unittest

import mock
from proto.datetime_helpers import DatetimeWithNanoseconds
from google.protobuf import timestamp_pb2


class TestBaseDocumentReference(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.document import DocumentReference

        return DocumentReference

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        collection_id1 = "users"
        document_id1 = "alovelace"
        collection_id2 = "platform"
        document_id2 = "*nix"
        client = mock.MagicMock()
        client.__hash__.return_value = 1234

        document = self._make_one(
            collection_id1, document_id1, collection_id2, document_id2, client=client
        )
        self.assertIs(document._client, client)
        expected_path = "/".join(
            (collection_id1, document_id1, collection_id2, document_id2)
        )
        self.assertEqual(document.path, expected_path)

    def test_constructor_invalid_path_empty(self):
        with self.assertRaises(ValueError):
            self._make_one()

    def test_constructor_invalid_path_bad_collection_id(self):
        with self.assertRaises(ValueError):
            self._make_one(None, "before", "bad-collection-id", "fifteen")

    def test_constructor_invalid_path_bad_document_id(self):
        with self.assertRaises(ValueError):
            self._make_one("bad-document-ID", None)

    def test_constructor_invalid_path_bad_number_args(self):
        with self.assertRaises(ValueError):
            self._make_one("Just", "A-Collection", "Sub")

    def test_constructor_invalid_kwarg(self):
        with self.assertRaises(TypeError):
            self._make_one("Coh-lek-shun", "Dahk-yu-mehnt", burger=18.75)

    def test___copy__(self):
        client = _make_client("rain")
        document = self._make_one("a", "b", client=client)
        # Access the document path so it is copied.
        doc_path = document._document_path
        self.assertEqual(doc_path, document._document_path_internal)

        new_document = document.__copy__()
        self.assertIsNot(new_document, document)
        self.assertIs(new_document._client, document._client)
        self.assertEqual(new_document._path, document._path)
        self.assertEqual(
            new_document._document_path_internal, document._document_path_internal
        )

    def test___deepcopy__calls_copy(self):
        client = mock.sentinel.client
        document = self._make_one("a", "b", client=client)
        document.__copy__ = mock.Mock(return_value=mock.sentinel.new_doc, spec=[])

        unused_memo = {}
        new_document = document.__deepcopy__(unused_memo)
        self.assertIs(new_document, mock.sentinel.new_doc)
        document.__copy__.assert_called_once_with()

    def test__eq__same_type(self):
        document1 = self._make_one("X", "YY", client=mock.sentinel.client)
        document2 = self._make_one("X", "ZZ", client=mock.sentinel.client)
        document3 = self._make_one("X", "YY", client=mock.sentinel.client2)
        document4 = self._make_one("X", "YY", client=mock.sentinel.client)

        pairs = ((document1, document2), (document1, document3), (document2, document3))
        for candidate1, candidate2 in pairs:
            # We use == explicitly since assertNotEqual would use !=.
            equality_val = candidate1 == candidate2
            self.assertFalse(equality_val)

        # Check the only equal one.
        self.assertEqual(document1, document4)
        self.assertIsNot(document1, document4)

    def test__eq__other_type(self):
        document = self._make_one("X", "YY", client=mock.sentinel.client)
        other = object()
        equality_val = document == other
        self.assertFalse(equality_val)
        self.assertIs(document.__eq__(other), NotImplemented)

    def test___hash__(self):
        client = mock.MagicMock()
        client.__hash__.return_value = 234566789
        document = self._make_one("X", "YY", client=client)
        self.assertEqual(hash(document), hash(("X", "YY")) + hash(client))

    def test__ne__same_type(self):
        document1 = self._make_one("X", "YY", client=mock.sentinel.client)
        document2 = self._make_one("X", "ZZ", client=mock.sentinel.client)
        document3 = self._make_one("X", "YY", client=mock.sentinel.client2)
        document4 = self._make_one("X", "YY", client=mock.sentinel.client)

        self.assertNotEqual(document1, document2)
        self.assertNotEqual(document1, document3)
        self.assertNotEqual(document2, document3)

        # We use != explicitly since assertEqual would use ==.
        inequality_val = document1 != document4
        self.assertFalse(inequality_val)
        self.assertIsNot(document1, document4)

    def test__ne__other_type(self):
        document = self._make_one("X", "YY", client=mock.sentinel.client)
        other = object()
        self.assertNotEqual(document, other)
        self.assertIs(document.__ne__(other), NotImplemented)

    def test__document_path_property(self):
        project = "hi-its-me-ok-bye"
        client = _make_client(project=project)

        collection_id = "then"
        document_id = "090909iii"
        document = self._make_one(collection_id, document_id, client=client)
        doc_path = document._document_path
        expected = "projects/{}/databases/{}/documents/{}/{}".format(
            project, client._database, collection_id, document_id
        )
        self.assertEqual(doc_path, expected)
        self.assertIs(document._document_path_internal, doc_path)

        # Make sure value is cached.
        document._document_path_internal = mock.sentinel.cached
        self.assertIs(document._document_path, mock.sentinel.cached)

    def test__document_path_property_no_client(self):
        document = self._make_one("hi", "bye")
        self.assertIsNone(document._client)
        with self.assertRaises(ValueError):
            getattr(document, "_document_path")

        self.assertIsNone(document._document_path_internal)

    def test_id_property(self):
        document_id = "867-5309"
        document = self._make_one("Co-lek-shun", document_id)
        self.assertEqual(document.id, document_id)

    def test_parent_property(self):
        from google.cloud.firestore_v1.collection import CollectionReference

        collection_id = "grocery-store"
        document_id = "market"
        client = _make_client()
        document = self._make_one(collection_id, document_id, client=client)

        parent = document.parent
        self.assertIsInstance(parent, CollectionReference)
        self.assertIs(parent._client, client)
        self.assertEqual(parent._path, (collection_id,))

    def test_collection_factory(self):
        from google.cloud.firestore_v1.collection import CollectionReference

        collection_id = "grocery-store"
        document_id = "market"
        new_collection = "fruits"
        client = _make_client()
        document = self._make_one(collection_id, document_id, client=client)

        child = document.collection(new_collection)
        self.assertIsInstance(child, CollectionReference)
        self.assertIs(child._client, client)
        self.assertEqual(child._path, (collection_id, document_id, new_collection))


class TestDocumentSnapshot(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.document import DocumentSnapshot

        return DocumentSnapshot

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def _make_reference(self, *args, **kwargs):
        from google.cloud.firestore_v1.document import DocumentReference

        return DocumentReference(*args, **kwargs)

    def _make_w_ref(self, ref_path=("a", "b"), data={}, exists=True):
        client = mock.sentinel.client
        reference = self._make_reference(*ref_path, client=client)
        return self._make_one(
            reference,
            data,
            exists,
            mock.sentinel.read_time,
            mock.sentinel.create_time,
            mock.sentinel.update_time,
        )

    def test_constructor(self):
        client = mock.sentinel.client
        reference = self._make_reference("hi", "bye", client=client)
        data = {"zoop": 83}
        snapshot = self._make_one(
            reference,
            data,
            True,
            mock.sentinel.read_time,
            mock.sentinel.create_time,
            mock.sentinel.update_time,
        )
        self.assertIs(snapshot._reference, reference)
        self.assertEqual(snapshot._data, data)
        self.assertIsNot(snapshot._data, data)  # Make sure copied.
        self.assertTrue(snapshot._exists)
        self.assertIs(snapshot.read_time, mock.sentinel.read_time)
        self.assertIs(snapshot.create_time, mock.sentinel.create_time)
        self.assertIs(snapshot.update_time, mock.sentinel.update_time)

    def test___eq___other_type(self):
        snapshot = self._make_w_ref()
        other = object()
        self.assertFalse(snapshot == other)

    def test___eq___different_reference_same_data(self):
        snapshot = self._make_w_ref(("a", "b"))
        other = self._make_w_ref(("c", "d"))
        self.assertFalse(snapshot == other)

    def test___eq___same_reference_different_data(self):
        snapshot = self._make_w_ref(("a", "b"))
        other = self._make_w_ref(("a", "b"), {"foo": "bar"})
        self.assertFalse(snapshot == other)

    def test___eq___same_reference_same_data(self):
        snapshot = self._make_w_ref(("a", "b"), {"foo": "bar"})
        other = self._make_w_ref(("a", "b"), {"foo": "bar"})
        self.assertTrue(snapshot == other)

    def test___hash__(self):
        client = mock.MagicMock()
        client.__hash__.return_value = 234566789
        reference = self._make_reference("hi", "bye", client=client)
        data = {"zoop": 83}
        update_time = DatetimeWithNanoseconds.from_timestamp_pb(
            timestamp_pb2.Timestamp(seconds=123456, nanos=123456789)
        )
        snapshot = self._make_one(
            reference, data, True, None, mock.sentinel.create_time, update_time
        )
        self.assertEqual(
            hash(snapshot), hash(reference) + hash(123456) + hash(123456789)
        )

    def test__client_property(self):
        reference = self._make_reference(
            "ok", "fine", "now", "fore", client=mock.sentinel.client
        )
        snapshot = self._make_one(reference, {}, False, None, None, None)
        self.assertIs(snapshot._client, mock.sentinel.client)

    def test_exists_property(self):
        reference = mock.sentinel.reference

        snapshot1 = self._make_one(reference, {}, False, None, None, None)
        self.assertFalse(snapshot1.exists)
        snapshot2 = self._make_one(reference, {}, True, None, None, None)
        self.assertTrue(snapshot2.exists)

    def test_id_property(self):
        document_id = "around"
        reference = self._make_reference(
            "look", document_id, client=mock.sentinel.client
        )
        snapshot = self._make_one(reference, {}, True, None, None, None)
        self.assertEqual(snapshot.id, document_id)
        self.assertEqual(reference.id, document_id)

    def test_reference_property(self):
        snapshot = self._make_one(mock.sentinel.reference, {}, True, None, None, None)
        self.assertIs(snapshot.reference, mock.sentinel.reference)

    def test_get(self):
        data = {"one": {"bold": "move"}}
        snapshot = self._make_one(None, data, True, None, None, None)

        first_read = snapshot.get("one")
        second_read = snapshot.get("one")
        self.assertEqual(first_read, data.get("one"))
        self.assertIsNot(first_read, data.get("one"))
        self.assertEqual(first_read, second_read)
        self.assertIsNot(first_read, second_read)

        with self.assertRaises(KeyError):
            snapshot.get("two")

    def test_nonexistent_snapshot(self):
        snapshot = self._make_one(None, None, False, None, None, None)
        self.assertIsNone(snapshot.get("one"))

    def test_to_dict(self):
        data = {"a": 10, "b": ["definitely", "mutable"], "c": {"45": 50}}
        snapshot = self._make_one(None, data, True, None, None, None)
        as_dict = snapshot.to_dict()
        self.assertEqual(as_dict, data)
        self.assertIsNot(as_dict, data)
        # Check that the data remains unchanged.
        as_dict["b"].append("hi")
        self.assertEqual(data, snapshot.to_dict())
        self.assertNotEqual(data, as_dict)

    def test_non_existent(self):
        snapshot = self._make_one(None, None, False, None, None, None)
        as_dict = snapshot.to_dict()
        self.assertIsNone(as_dict)


class Test__get_document_path(unittest.TestCase):
    @staticmethod
    def _call_fut(client, path):
        from google.cloud.firestore_v1.base_document import _get_document_path

        return _get_document_path(client, path)

    def test_it(self):
        project = "prah-jekt"
        client = _make_client(project=project)
        path = ("Some", "Document", "Child", "Shockument")
        document_path = self._call_fut(client, path)

        expected = "projects/{}/databases/{}/documents/{}".format(
            project, client._database, "/".join(path)
        )
        self.assertEqual(document_path, expected)


class Test__consume_single_get(unittest.TestCase):
    @staticmethod
    def _call_fut(response_iterator):
        from google.cloud.firestore_v1.base_document import _consume_single_get

        return _consume_single_get(response_iterator)

    def test_success(self):
        response_iterator = iter([mock.sentinel.result])
        result = self._call_fut(response_iterator)
        self.assertIs(result, mock.sentinel.result)

    def test_failure_not_enough(self):
        response_iterator = iter([])
        with self.assertRaises(ValueError):
            self._call_fut(response_iterator)

    def test_failure_too_many(self):
        response_iterator = iter([None, None])
        with self.assertRaises(ValueError):
            self._call_fut(response_iterator)


class Test__first_write_result(unittest.TestCase):
    @staticmethod
    def _call_fut(write_results):
        from google.cloud.firestore_v1.base_document import _first_write_result

        return _first_write_result(write_results)

    def test_success(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.types import write

        single_result = write.WriteResult(
            update_time=timestamp_pb2.Timestamp(seconds=1368767504, nanos=458000123)
        )
        write_results = [single_result]
        result = self._call_fut(write_results)
        self.assertIs(result, single_result)

    def test_failure_not_enough(self):
        write_results = []
        with self.assertRaises(ValueError):
            self._call_fut(write_results)

    def test_more_than_one(self):
        from google.cloud.firestore_v1.types import write

        result1 = write.WriteResult()
        result2 = write.WriteResult()
        write_results = [result1, result2]
        result = self._call_fut(write_results)
        self.assertIs(result, result1)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="project-project"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
