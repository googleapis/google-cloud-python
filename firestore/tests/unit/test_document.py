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

import collections
import unittest

import mock


class TestDocumentReference(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.document import DocumentReference

        return DocumentReference

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        collection_id1 = 'users'
        document_id1 = 'alovelace'
        collection_id2 = 'platform'
        document_id2 = '*nix'
        client = mock.sentinel.client

        document = self._make_one(
            collection_id1, document_id1,
            collection_id2, document_id2, client=client)
        self.assertIs(document._client, client)
        expected_path = (
            collection_id1, document_id1, collection_id2, document_id2)
        self.assertEqual(document._path, expected_path)

    def test_constructor_invalid_path(self):
        with self.assertRaises(ValueError):
            self._make_one()
        with self.assertRaises(ValueError):
            self._make_one(None, 'before', 'bad-collection-id', 'fifteen')
        with self.assertRaises(ValueError):
            self._make_one('bad-document-ID', None)
        with self.assertRaises(ValueError):
            self._make_one('Just', 'A-Collection', 'Sub')

    def test_constructor_invalid_kwarg(self):
        with self.assertRaises(TypeError):
            self._make_one('Coh-lek-shun', 'Dahk-yu-mehnt', burger=18.75)

    def test___copy__(self):
        client = _make_client('rain')
        document = self._make_one('a', 'b', client=client)
        # Access the document path so it is copied.
        doc_path = document._document_path
        self.assertEqual(doc_path, document._document_path_internal)

        new_document = document.__copy__()
        self.assertIsNot(new_document, document)
        self.assertIs(new_document._client, document._client)
        self.assertEqual(new_document._path, document._path)
        self.assertEqual(
            new_document._document_path_internal,
            document._document_path_internal)

    def test___deepcopy__calls_copy(self):
        client = mock.sentinel.client
        document = self._make_one('a', 'b', client=client)
        document.__copy__ = mock.Mock(
            return_value=mock.sentinel.new_doc, spec=[])

        unused_memo = {}
        new_document = document.__deepcopy__(unused_memo)
        self.assertIs(new_document, mock.sentinel.new_doc)
        document.__copy__.assert_called_once_with()

    def test__eq__same_type(self):
        document1 = self._make_one('X', 'YY', client=mock.sentinel.client)
        document2 = self._make_one('X', 'ZZ', client=mock.sentinel.client)
        document3 = self._make_one('X', 'YY', client=mock.sentinel.client2)
        document4 = self._make_one('X', 'YY', client=mock.sentinel.client)

        pairs = (
            (document1, document2),
            (document1, document3),
            (document2, document3),
        )
        for candidate1, candidate2 in pairs:
            # We use == explicitly since assertNotEqual would use !=.
            equality_val = candidate1 == candidate2
            self.assertFalse(equality_val)

        # Check the only equal one.
        self.assertEqual(document1, document4)
        self.assertIsNot(document1, document4)

    def test__eq__other_type(self):
        document = self._make_one('X', 'YY', client=mock.sentinel.client)
        other = object()
        equality_val = document == other
        self.assertFalse(equality_val)
        self.assertIs(document.__eq__(other), NotImplemented)

    def test__ne__same_type(self):
        document1 = self._make_one('X', 'YY', client=mock.sentinel.client)
        document2 = self._make_one('X', 'ZZ', client=mock.sentinel.client)
        document3 = self._make_one('X', 'YY', client=mock.sentinel.client2)
        document4 = self._make_one('X', 'YY', client=mock.sentinel.client)

        self.assertNotEqual(document1, document2)
        self.assertNotEqual(document1, document3)
        self.assertNotEqual(document2, document3)

        # We use != explicitly since assertEqual would use ==.
        inequality_val = document1 != document4
        self.assertFalse(inequality_val)
        self.assertIsNot(document1, document4)

    def test__ne__other_type(self):
        document = self._make_one('X', 'YY', client=mock.sentinel.client)
        other = object()
        self.assertNotEqual(document, other)
        self.assertIs(document.__ne__(other), NotImplemented)

    def test__document_path_property(self):
        project = 'hi-its-me-ok-bye'
        client = _make_client(project=project)

        collection_id = 'then'
        document_id = '090909iii'
        document = self._make_one(collection_id, document_id, client=client)
        doc_path = document._document_path
        expected = 'projects/{}/databases/{}/documents/{}/{}'.format(
            project, client._database, collection_id, document_id)
        self.assertEqual(doc_path, expected)
        self.assertIs(document._document_path_internal, doc_path)

        # Make sure value is cached.
        document._document_path_internal = mock.sentinel.cached
        self.assertIs(document._document_path, mock.sentinel.cached)

    def test__document_path_property_no_client(self):
        document = self._make_one('hi', 'bye')
        self.assertIsNone(document._client)
        with self.assertRaises(ValueError):
            getattr(document, '_document_path')

        self.assertIsNone(document._document_path_internal)

    def test_id_property(self):
        document_id = '867-5309'
        document = self._make_one('Co-lek-shun', document_id)
        self.assertEqual(document.id, document_id)

    def test_parent_property(self):
        from google.cloud.firestore_v1beta1.collection import CollectionReference

        collection_id = 'grocery-store'
        document_id = 'market'
        client = _make_client()
        document = self._make_one(collection_id, document_id, client=client)

        parent = document.parent
        self.assertIsInstance(parent, CollectionReference)
        self.assertIs(parent._client, client)
        self.assertEqual(parent._path, (collection_id,))

    def test_collection_factory(self):
        from google.cloud.firestore_v1beta1.collection import CollectionReference

        collection_id = 'grocery-store'
        document_id = 'market'
        new_collection = 'fruits'
        client = _make_client()
        document = self._make_one(
            collection_id, document_id, client=client)

        child = document.collection(new_collection)
        self.assertIsInstance(child, CollectionReference)
        self.assertIs(child._client, client)
        self.assertEqual(
            child._path, (collection_id, document_id, new_collection))

    @staticmethod
    def _write_pb_for_create(document_path, document_data):
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2
        from google.cloud.firestore_v1beta1 import _helpers

        return write_pb2.Write(
            update=document_pb2.Document(
                name=document_path,
                fields=_helpers.encode_dict(document_data),
            ),
            current_document=common_pb2.Precondition(exists=False),
        )

    def test_create(self):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['commit'])
        commit_response = mock.Mock(
            write_results=[mock.sentinel.write_result],
            spec=['write_results'])
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client('dignity')
        client._firestore_api_internal = firestore_api

        # Actually make a document and call create().
        document = self._make_one('foo', 'twelve', client=client)
        document_data = {
            'hello': 'goodbye',
            'count': 99,
        }
        write_result = document.create(document_data)

        # Verify the response and the mocks.
        self.assertIs(write_result, mock.sentinel.write_result)
        write_pb = self._write_pb_for_create(
            document._document_path, document_data)
        firestore_api.commit.assert_called_once_with(
            client._database_string, [write_pb], transaction=None,
            options=client._call_options)

    @staticmethod
    def _write_pb_for_set(document_path, document_data):
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2
        from google.cloud.firestore_v1beta1 import _helpers

        return write_pb2.Write(
            update=document_pb2.Document(
                name=document_path,
                fields=_helpers.encode_dict(document_data),
            ),
        )

    def _set_helper(self, **option_kwargs):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['commit'])
        commit_response = mock.Mock(
            write_results=[mock.sentinel.write_result],
            spec=['write_results'])
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client('db-dee-bee')
        client._firestore_api_internal = firestore_api

        # Actually make a document and call create().
        document = self._make_one('User', 'Interface', client=client)
        document_data = {
            'And': 500,
            'Now': b'\xba\xaa\xaa \xba\xaa\xaa',
        }
        if option_kwargs:
            option = client.write_option(**option_kwargs)
            write_result = document.set(document_data, option=option)
        else:
            option = None
            write_result = document.set(document_data)

        # Verify the response and the mocks.
        self.assertIs(write_result, mock.sentinel.write_result)
        write_pb = self._write_pb_for_set(
            document._document_path, document_data)
        if option is not None:
            option.modify_write(write_pb)
        firestore_api.commit.assert_called_once_with(
            client._database_string, [write_pb], transaction=None,
            options=client._call_options)

    def test_set(self):
        self._set_helper()

    def test_set_with_option(self):
        self._set_helper(create_if_missing=False)

    @staticmethod
    def _write_pb_for_update(document_path, update_values, field_paths):
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2
        from google.cloud.firestore_v1beta1 import _helpers

        return write_pb2.Write(
            update=document_pb2.Document(
                name=document_path,
                fields=_helpers.encode_dict(update_values),
            ),
            update_mask=common_pb2.DocumentMask(field_paths=field_paths),
            current_document=common_pb2.Precondition(exists=True),
        )

    def _update_helper(self, **option_kwargs):
        from google.cloud.firestore_v1beta1.constants import DELETE_FIELD

        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['commit'])
        commit_response = mock.Mock(
            write_results=[mock.sentinel.write_result],
            spec=['write_results'])
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client('potato-chip')
        client._firestore_api_internal = firestore_api

        # Actually make a document and call create().
        document = self._make_one('baked', 'Alaska', client=client)
        # "Cheat" and use OrderedDict-s so that iteritems() is deterministic.
        field_updates = collections.OrderedDict((
            ('hello', 1),
            ('then.do', False),
            ('goodbye', DELETE_FIELD),
        ))
        if option_kwargs:
            option = client.write_option(**option_kwargs)
            write_result = document.update(field_updates, option=option)
        else:
            option = None
            write_result = document.update(field_updates)

        # Verify the response and the mocks.
        self.assertIs(write_result, mock.sentinel.write_result)
        update_values = {
            'hello': field_updates['hello'],
            'then': {
                'do': field_updates['then.do'],
            }
        }
        field_paths = list(field_updates.keys())
        write_pb = self._write_pb_for_update(
            document._document_path, update_values, field_paths)
        if option is not None:
            option.modify_write(write_pb)
        firestore_api.commit.assert_called_once_with(
            client._database_string, [write_pb], transaction=None,
            options=client._call_options)

    def test_update(self):
        self._update_helper()

    def test_update_with_option(self):
        self._update_helper(create_if_missing=False)

    def _delete_helper(self, **option_kwargs):
        from google.cloud.firestore_v1beta1.proto import write_pb2

        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['commit'])
        commit_response = mock.Mock(
            commit_time=mock.sentinel.commit_time, spec=['commit_time'])
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client('donut-base')
        client._firestore_api_internal = firestore_api

        # Actually make a document and call delete().
        document = self._make_one('where', 'we-are', client=client)
        if option_kwargs:
            option = client.write_option(**option_kwargs)
            delete_time = document.delete(option=option)
        else:
            option = None
            delete_time = document.delete()

        # Verify the response and the mocks.
        self.assertIs(delete_time, mock.sentinel.commit_time)
        write_pb = write_pb2.Write(delete=document._document_path)
        if option is not None:
            option.modify_write(write_pb)
        firestore_api.commit.assert_called_once_with(
            client._database_string, [write_pb], transaction=None,
            options=client._call_options)

    def test_delete(self):
        self._delete_helper()

    def test_delete_with_option(self):
        from google.protobuf import timestamp_pb2

        timestamp_pb = timestamp_pb2.Timestamp(
            seconds=1058655101,
            nanos=100022244,
        )
        self._delete_helper(last_update_time=timestamp_pb)

    def test_delete_with_bad_option(self):
        from google.cloud.firestore_v1beta1._helpers import NO_CREATE_ON_DELETE

        with self.assertRaises(ValueError) as exc_info:
            self._delete_helper(create_if_missing=True)
        self.assertEqual(exc_info.exception.args, (NO_CREATE_ON_DELETE,))

    def test_get_success(self):
        # Create a minimal fake client with a dummy response.
        response_iterator = iter([mock.sentinel.snapshot])
        client = mock.Mock(spec=['get_all'])
        client.get_all.return_value = response_iterator

        # Actually make a document and call get().
        document = self._make_one('yellow', 'mellow', client=client)
        snapshot = document.get()

        # Verify the response and the mocks.
        self.assertIs(snapshot, mock.sentinel.snapshot)
        client.get_all.assert_called_once_with(
            [document], field_paths=None, transaction=None)

    def test_get_with_transaction(self):
        from google.cloud.firestore_v1beta1.client import Client
        from google.cloud.firestore_v1beta1.transaction import Transaction

        # Create a minimal fake client with a dummy response.
        response_iterator = iter([mock.sentinel.snapshot])
        client = mock.create_autospec(Client, instance=True)
        client.get_all.return_value = response_iterator

        # Actually make a document and call get().
        document = self._make_one('yellow', 'mellow', client=client)
        transaction = Transaction(client)
        transaction._id = b'asking-me-2'
        snapshot = document.get(transaction=transaction)

        # Verify the response and the mocks.
        self.assertIs(snapshot, mock.sentinel.snapshot)
        client.get_all.assert_called_once_with(
            [document], field_paths=None, transaction=transaction)

    def test_get_not_found(self):
        from google.cloud.exceptions import NotFound

        # Create a minimal fake client with a dummy response.
        response_iterator = iter([None])
        client = mock.Mock(
            _database_string='sprinklez',
            spec=['_database_string', 'get_all'])
        client.get_all.return_value = response_iterator

        # Actually make a document and call get().
        document = self._make_one('house', 'cowse', client=client)
        field_paths = ['x.y', 'x.z', 't']
        with self.assertRaises(NotFound):
            document.get(field_paths=field_paths)

        # Verify the response and the mocks.
        client.get_all.assert_called_once_with(
            [document], field_paths=field_paths, transaction=None)


class TestDocumentSnapshot(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        return DocumentSnapshot

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def _make_reference(self, *args, **kwargs):
        from google.cloud.firestore_v1beta1.document import DocumentReference

        return DocumentReference(*args, **kwargs)

    def test_constructor(self):
        reference = self._make_reference(
            'hi', 'bye', client=mock.sentinel.client)
        data = {'zoop': 83}
        snapshot = self._make_one(
            reference, data, True, mock.sentinel.read_time,
            mock.sentinel.create_time, mock.sentinel.update_time)
        self.assertIs(snapshot._reference, reference)
        self.assertEqual(snapshot._data, data)
        self.assertIsNot(snapshot._data, data)  # Make sure copied.
        self.assertTrue(snapshot._exists)
        self.assertIs(snapshot.read_time, mock.sentinel.read_time)
        self.assertIs(snapshot.create_time, mock.sentinel.create_time)
        self.assertIs(snapshot.update_time, mock.sentinel.update_time)

    def test__client_property(self):
        reference = self._make_reference(
            'ok', 'fine', 'now', 'fore', client=mock.sentinel.client)
        snapshot = self._make_one(reference, {}, False, None, None, None)
        self.assertIs(snapshot._client, mock.sentinel.client)

    def test_exists_property(self):
        reference = mock.sentinel.reference

        snapshot1 = self._make_one(reference, {}, False, None, None, None)
        self.assertFalse(snapshot1.exists)
        snapshot2 = self._make_one(reference, {}, True, None, None, None)
        self.assertTrue(snapshot2.exists)

    def test_id_property(self):
        document_id = 'around'
        reference = self._make_reference(
            'look', document_id, client=mock.sentinel.client)
        snapshot = self._make_one(reference, {}, True, None, None, None)
        self.assertEqual(snapshot.id, document_id)
        self.assertEqual(reference.id, document_id)

    def test_reference_property(self):
        snapshot = self._make_one(
            mock.sentinel.reference, {}, True, None, None, None)
        self.assertIs(snapshot.reference, mock.sentinel.reference)

    def test_get(self):
        data = {'one': {'bold': 'move'}}
        snapshot = self._make_one(None, data, True, None, None, None)

        first_read = snapshot.get('one')
        second_read = snapshot.get('one')
        self.assertEqual(first_read, data.get('one'))
        self.assertIsNot(first_read, data.get('one'))
        self.assertEqual(first_read, second_read)
        self.assertIsNot(first_read, second_read)

        with self.assertRaises(KeyError):
            snapshot.get('two')

    def test_to_dict(self):
        data = {
            'a': 10,
            'b': ['definitely', 'mutable'],
            'c': {'45': 50},
        }
        snapshot = self._make_one(None, data, True, None, None, None)
        as_dict = snapshot.to_dict()
        self.assertEqual(as_dict, data)
        self.assertIsNot(as_dict, data)
        # Check that the data remains unchanged.
        as_dict['b'].append('hi')
        self.assertEqual(data, snapshot.to_dict())
        self.assertNotEqual(data, as_dict)


class Test__get_document_path(unittest.TestCase):

    @staticmethod
    def _call_fut(client, path):
        from google.cloud.firestore_v1beta1.document import _get_document_path

        return _get_document_path(client, path)

    def test_it(self):
        project = 'prah-jekt'
        client = _make_client(project=project)
        path = ('Some', 'Document', 'Child', 'Shockument')
        document_path = self._call_fut(client, path)

        expected = 'projects/{}/databases/{}/documents/{}'.format(
            project, client._database, '/'.join(path))
        self.assertEqual(document_path, expected)


class Test__consume_single_get(unittest.TestCase):

    @staticmethod
    def _call_fut(response_iterator):
        from google.cloud.firestore_v1beta1.document import _consume_single_get

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
        from google.cloud.firestore_v1beta1.document import _first_write_result

        return _first_write_result(write_results)

    def test_success(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        single_result = write_pb2.WriteResult(
            update_time=timestamp_pb2.Timestamp(
                seconds=1368767504,
                nanos=458000123,
            ),
        )
        write_results = [single_result]
        result = self._call_fut(write_results)
        self.assertIs(result, single_result)

    def test_failure_not_enough(self):
        write_results = []
        with self.assertRaises(ValueError):
            self._call_fut(write_results)

    def test_more_than_one(self):
        from google.cloud.firestore_v1beta1.proto import write_pb2

        result1 = write_pb2.WriteResult()
        result2 = write_pb2.WriteResult()
        write_results = [result1, result2]
        result = self._call_fut(write_results)
        self.assertIs(result, result1)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project='project-project'):
    from google.cloud.firestore_v1beta1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
