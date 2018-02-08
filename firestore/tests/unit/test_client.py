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

import datetime
import types
import unittest

import mock


class TestClient(unittest.TestCase):

    PROJECT = 'my-prahjekt'

    @staticmethod
    def _get_target_class():
        from google.cloud import firestore

        return firestore.Client

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def _make_default_one(self):
        credentials = _make_credentials()
        return self._make_one(project=self.PROJECT, credentials=credentials)

    def test_constructor(self):
        from google.cloud.firestore_v1beta1.client import DEFAULT_DATABASE

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client._credentials, credentials)
        self.assertEqual(client._database, DEFAULT_DATABASE)

    def test_constructor_explicit(self):
        credentials = _make_credentials()
        database = 'now-db'
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, database=database)
        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client._credentials, credentials)
        self.assertEqual(client._database, database)

    @mock.patch(
        'google.cloud.firestore_v1beta1.client._make_firestore_api',
        return_value=mock.sentinel.firestore_api)
    def test__firestore_api_property(self, mock_make_api):
        client = self._make_default_one()
        self.assertIsNone(client._firestore_api_internal)
        firestore_api = client._firestore_api
        self.assertIs(firestore_api, mock_make_api.return_value)
        self.assertIs(firestore_api, client._firestore_api_internal)
        mock_make_api.assert_called_once_with(client)

        # Call again to show that it is cached, but call count is still 1.
        self.assertIs(client._firestore_api, mock_make_api.return_value)
        self.assertEqual(mock_make_api.call_count, 1)

    def test___database_string_property(self):
        credentials = _make_credentials()
        database = 'cheeeeez'
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, database=database)
        self.assertIsNone(client._database_string_internal)
        database_string = client._database_string
        expected = 'projects/{}/databases/{}'.format(
            client.project, client._database)
        self.assertEqual(database_string, expected)
        self.assertIs(database_string, client._database_string_internal)

        # Swap it out with a unique value to verify it is cached.
        client._database_string_internal = mock.sentinel.cached
        self.assertIs(client._database_string, mock.sentinel.cached)

    def test___call_options_property(self):
        import google.gax

        credentials = _make_credentials()
        database = 'quanta'
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, database=database)
        self.assertIsNone(client._call_options_internal)

        call_options = client._call_options
        self.assertIsInstance(call_options, google.gax.CallOptions)
        expected_kwargs = {
            'metadata': [
                ('google-cloud-resource-prefix', client._database_string),
            ],
        }
        self.assertEqual(call_options.kwargs, expected_kwargs)

        self.assertIs(call_options, client._call_options_internal)

        # Swap it out with a unique value to verify it is cached.
        client._call_options_internal = mock.sentinel.cached
        self.assertIs(client._call_options, mock.sentinel.cached)

    def test_collection_factory(self):
        from google.cloud.firestore_v1beta1.collection import CollectionReference

        collection_id = 'users'
        client = self._make_default_one()
        collection = client.collection(collection_id)

        self.assertEqual(collection._path, (collection_id,))
        self.assertIs(collection._client, client)
        self.assertIsInstance(collection, CollectionReference)

    def test_collection_factory_nested(self):
        from google.cloud.firestore_v1beta1.collection import CollectionReference

        client = self._make_default_one()
        parts = ('users', 'alovelace', 'beep')
        collection_path = '/'.join(parts)
        collection1 = client.collection(collection_path)

        self.assertEqual(collection1._path, parts)
        self.assertIs(collection1._client, client)
        self.assertIsInstance(collection1, CollectionReference)

        # Make sure using segments gives the same result.
        collection2 = client.collection(*parts)
        self.assertEqual(collection2._path, parts)
        self.assertIs(collection2._client, client)
        self.assertIsInstance(collection2, CollectionReference)

    def test_document_factory(self):
        from google.cloud.firestore_v1beta1.document import DocumentReference

        parts = ('rooms', 'roomA')
        client = self._make_default_one()
        doc_path = '/'.join(parts)
        document1 = client.document(doc_path)

        self.assertEqual(document1._path, parts)
        self.assertIs(document1._client, client)
        self.assertIsInstance(document1, DocumentReference)

        # Make sure using segments gives the same result.
        document2 = client.document(*parts)
        self.assertEqual(document2._path, parts)
        self.assertIs(document2._client, client)
        self.assertIsInstance(document2, DocumentReference)

    def test_document_factory_nested(self):
        from google.cloud.firestore_v1beta1.document import DocumentReference

        client = self._make_default_one()
        parts = ('rooms', 'roomA', 'shoes', 'dressy')
        doc_path = '/'.join(parts)
        document1 = client.document(doc_path)

        self.assertEqual(document1._path, parts)
        self.assertIs(document1._client, client)
        self.assertIsInstance(document1, DocumentReference)

        # Make sure using segments gives the same result.
        document2 = client.document(*parts)
        self.assertEqual(document2._path, parts)
        self.assertIs(document2._client, client)
        self.assertIsInstance(document2, DocumentReference)

    def test_field_path(self):
        klass = self._get_target_class()
        self.assertEqual(klass.field_path('a', 'b', 'c'), 'a.b.c')

    def test_write_option_create(self):
        from google.cloud.firestore_v1beta1.client import CreateIfMissingOption

        klass = self._get_target_class()

        option1 = klass.write_option(create_if_missing=False)
        self.assertIsInstance(option1, CreateIfMissingOption)
        self.assertFalse(option1._create_if_missing)

        option2 = klass.write_option(create_if_missing=True)
        self.assertIsInstance(option2, CreateIfMissingOption)
        self.assertTrue(option2._create_if_missing)

    def test_write_option_last_update(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1beta1.client import LastUpdateOption

        timestamp = timestamp_pb2.Timestamp(
            seconds=1299767599,
            nanos=811111097,
        )

        klass = self._get_target_class()
        option = klass.write_option(last_update_time=timestamp)
        self.assertIsInstance(option, LastUpdateOption)
        self.assertEqual(option._last_update_time, timestamp)

    def test_write_option_exists(self):
        from google.cloud.firestore_v1beta1.client import ExistsOption

        klass = self._get_target_class()

        option1 = klass.write_option(exists=False)
        self.assertIsInstance(option1, ExistsOption)
        self.assertFalse(option1._exists)

        option2 = klass.write_option(exists=True)
        self.assertIsInstance(option2, ExistsOption)
        self.assertTrue(option2._exists)

    def test_write_open_neither_arg(self):
        from google.cloud.firestore_v1beta1.client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option()

        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR,))

    def test_write_multiple_args(self):
        from google.cloud.firestore_v1beta1.client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option(
                create_if_missing=False,
                last_update_time=mock.sentinel.timestamp)

        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR,))

    def test_write_bad_arg(self):
        from google.cloud.firestore_v1beta1.client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option(spinach='popeye')

        extra = '{!r} was provided'.format('spinach')
        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR, extra))

    def _get_all_helper(self, client, references, document_pbs, **kwargs):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=['batch_get_documents'])
        response_iterator = iter(document_pbs)
        firestore_api.batch_get_documents.return_value = response_iterator

        # Attach the fake GAPIC to a real client.
        client._firestore_api_internal = firestore_api

        # Actually call get_all().
        snapshots = client.get_all(references, **kwargs)
        self.assertIsInstance(snapshots, types.GeneratorType)

        return list(snapshots)

    def _info_for_get_all(self, data1, data2):
        client = self._make_default_one()
        document1 = client.document('pineapple', 'lamp1')
        document2 = client.document('pineapple', 'lamp2')

        # Make response protobufs.
        document_pb1, read_time = _doc_get_info(
            document1._document_path, data1)
        response1 = _make_batch_response(
            found=document_pb1, read_time=read_time)

        document_pb2, read_time = _doc_get_info(
            document2._document_path, data2)
        response2 = _make_batch_response(
            found=document_pb2, read_time=read_time)

        return client, document1, document2, response1, response2

    def test_get_all(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        data1 = {'a': u'cheese'}
        data2 = {'b': True, 'c': 18}
        info = self._info_for_get_all(data1, data2)
        client, document1, document2, response1, response2 = info

        # Exercise the mocked ``batch_get_documents``.
        field_paths = ['a', 'b']
        snapshots = self._get_all_helper(
            client, [document1, document2], [response1, response2],
            field_paths=field_paths)
        self.assertEqual(len(snapshots), 2)

        snapshot1 = snapshots[0]
        self.assertIsInstance(snapshot1, DocumentSnapshot)
        self.assertIs(snapshot1._reference, document1)
        self.assertEqual(snapshot1._data, data1)

        snapshot2 = snapshots[1]
        self.assertIsInstance(snapshot2, DocumentSnapshot)
        self.assertIs(snapshot2._reference, document2)
        self.assertEqual(snapshot2._data, data2)

        # Verify the call to the mock.
        doc_paths = [document1._document_path, document2._document_path]
        mask = common_pb2.DocumentMask(field_paths=field_paths)
        client._firestore_api.batch_get_documents.assert_called_once_with(
            client._database_string, doc_paths, mask, transaction=None,
            options=client._call_options)

    def test_get_all_with_transaction(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        data = {'so-much': 484}
        info = self._info_for_get_all(data, {})
        client, document, _, response, _ = info
        transaction = client.transaction()
        txn_id = b'the-man-is-non-stop'
        transaction._id = txn_id

        # Exercise the mocked ``batch_get_documents``.
        snapshots = self._get_all_helper(
            client, [document], [response], transaction=transaction)
        self.assertEqual(len(snapshots), 1)

        snapshot = snapshots[0]
        self.assertIsInstance(snapshot, DocumentSnapshot)
        self.assertIs(snapshot._reference, document)
        self.assertEqual(snapshot._data, data)

        # Verify the call to the mock.
        doc_paths = [document._document_path]
        client._firestore_api.batch_get_documents.assert_called_once_with(
            client._database_string, doc_paths, None, transaction=txn_id,
            options=client._call_options)

    def test_get_all_unknown_result(self):
        from google.cloud.firestore_v1beta1.client import _BAD_DOC_TEMPLATE

        info = self._info_for_get_all({'z': 28.5}, {})
        client, document, _, _, response = info

        # Exercise the mocked ``batch_get_documents``.
        with self.assertRaises(ValueError) as exc_info:
            self._get_all_helper(
                client, [document], [response])

        err_msg = _BAD_DOC_TEMPLATE.format(response.found.name)
        self.assertEqual(exc_info.exception.args, (err_msg,))

        # Verify the call to the mock.
        doc_paths = [document._document_path]
        client._firestore_api.batch_get_documents.assert_called_once_with(
            client._database_string, doc_paths, None, transaction=None,
            options=client._call_options)

    def test_get_all_wrong_order(self):
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        data1 = {'up': 10}
        data2 = {'down': -10}
        info = self._info_for_get_all(data1, data2)
        client, document1, document2, response1, response2 = info
        document3 = client.document('pineapple', 'lamp3')
        response3 = _make_batch_response(missing=document3._document_path)

        # Exercise the mocked ``batch_get_documents``.
        snapshots = self._get_all_helper(
            client, [document1, document2, document3],
            [response2, response1, response3])

        self.assertEqual(len(snapshots), 3)

        snapshot1 = snapshots[0]
        self.assertIsInstance(snapshot1, DocumentSnapshot)
        self.assertIs(snapshot1._reference, document2)
        self.assertEqual(snapshot1._data, data2)

        snapshot2 = snapshots[1]
        self.assertIsInstance(snapshot2, DocumentSnapshot)
        self.assertIs(snapshot2._reference, document1)
        self.assertEqual(snapshot2._data, data1)

        self.assertIsNone(snapshots[2])

        # Verify the call to the mock.
        doc_paths = [
            document1._document_path,
            document2._document_path,
            document3._document_path,
        ]
        client._firestore_api.batch_get_documents.assert_called_once_with(
            client._database_string, doc_paths, None, transaction=None,
            options=client._call_options)

    def test_batch(self):
        from google.cloud.firestore_v1beta1.batch import WriteBatch

        client = self._make_default_one()
        batch = client.batch()
        self.assertIsInstance(batch, WriteBatch)
        self.assertIs(batch._client, client)
        self.assertEqual(batch._write_pbs, [])

    def test_transaction(self):
        from google.cloud.firestore_v1beta1.transaction import Transaction

        client = self._make_default_one()
        transaction = client.transaction(max_attempts=3, read_only=True)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction._write_pbs, [])
        self.assertEqual(transaction._max_attempts, 3)
        self.assertTrue(transaction._read_only)
        self.assertIsNone(transaction._id)


class TestWriteOption(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.client import WriteOption

        return WriteOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_modify_write(self):
        option = self._make_one()
        with self.assertRaises(NotImplementedError):
            option.modify_write(None)


class TestLastUpdateOption(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.client import LastUpdateOption

        return LastUpdateOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        option = self._make_one(mock.sentinel.timestamp)
        self.assertIs(option._last_update_time, mock.sentinel.timestamp)

    def test_modify_write_update_time(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        timestamp_pb = timestamp_pb2.Timestamp(
            seconds=683893592,
            nanos=229362000,
        )
        option = self._make_one(timestamp_pb)
        write_pb = write_pb2.Write()
        ret_val = option.modify_write(write_pb)

        self.assertIsNone(ret_val)
        expected_doc = common_pb2.Precondition(update_time=timestamp_pb)
        self.assertEqual(write_pb.current_document, expected_doc)


class TestCreateIfMissingOption(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.client import CreateIfMissingOption

        return CreateIfMissingOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        option = self._make_one(mock.sentinel.totes_bool)
        self.assertIs(option._create_if_missing, mock.sentinel.totes_bool)

    def test_modify_write_dont_create(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        option = self._make_one(False)
        write_pb = write_pb2.Write()
        ret_val = option.modify_write(write_pb)

        self.assertIsNone(ret_val)
        expected_doc = common_pb2.Precondition(exists=True)
        self.assertEqual(write_pb.current_document, expected_doc)

    def test_modify_write_do_create(self):
        from google.cloud.firestore_v1beta1.proto import write_pb2

        option = self._make_one(True)
        write_pb = write_pb2.Write()
        ret_val = option.modify_write(write_pb)

        self.assertIsNone(ret_val)
        # No precondition is set here.
        self.assertFalse(write_pb.HasField('current_document'))

    def test_modify_write_create_not_allowed(self):
        no_create_msg = mock.sentinel.message
        option1 = self._make_one(True)
        option2 = self._make_one(False)

        with self.assertRaises(ValueError) as exc_info:
            option1.modify_write(None, no_create_msg=no_create_msg)
        self.assertEqual(exc_info.exception.args, (no_create_msg,))

        with self.assertRaises(ValueError) as exc_info:
            option2.modify_write(None, no_create_msg=no_create_msg)
        self.assertEqual(exc_info.exception.args, (no_create_msg,))


class TestExistsOption(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.client import ExistsOption

        return ExistsOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        option = self._make_one(mock.sentinel.totes_bool)
        self.assertIs(option._exists, mock.sentinel.totes_bool)

    def test_modify_write(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        for exists in (True, False):
            option = self._make_one(exists)
            write_pb = write_pb2.Write()
            ret_val = option.modify_write(write_pb)

            self.assertIsNone(ret_val)
            expected_doc = common_pb2.Precondition(exists=exists)
            self.assertEqual(write_pb.current_document, expected_doc)


class Test__make_firestore_api(unittest.TestCase):

    CLIENT_PATH = (
        'google.cloud.firestore_v1beta1.gapic.'
        'firestore_client.FirestoreClient')

    @staticmethod
    def _call_fut(client):
        from google.cloud.firestore_v1beta1.client import _make_firestore_api

        return _make_firestore_api(client)

    @mock.patch(CLIENT_PATH, return_value=mock.sentinel.firestore_client)
    @mock.patch('google.cloud.firestore_v1beta1.client.make_secure_channel',
                return_value=mock.sentinel.channel)
    def test_it(self, make_chan, mock_klass):
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.firestore_v1beta1 import __version__

        client = mock.Mock(
            _credentials=mock.sentinel.credentials,
            spec=['_credentials'])
        firestore_client = self._call_fut(client)
        self.assertIs(firestore_client, mock.sentinel.firestore_client)

        host = mock_klass.SERVICE_ADDRESS
        make_chan.assert_called_once_with(
            mock.sentinel.credentials, DEFAULT_USER_AGENT, host)
        mock_klass.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)


class Test__reference_info(unittest.TestCase):

    @staticmethod
    def _call_fut(references):
        from google.cloud.firestore_v1beta1.client import _reference_info

        return _reference_info(references)

    def test_it(self):
        from google.cloud.firestore_v1beta1.client import Client

        credentials = _make_credentials()
        client = Client(project='hi-projject', credentials=credentials)

        reference1 = client.document('a', 'b')
        reference2 = client.document('a', 'b', 'c', 'd')
        reference3 = client.document('a', 'b')
        reference4 = client.document('f', 'g')

        doc_path1 = reference1._document_path
        doc_path2 = reference2._document_path
        doc_path3 = reference3._document_path
        doc_path4 = reference4._document_path
        self.assertEqual(doc_path1, doc_path3)

        document_paths, reference_map = self._call_fut(
            [reference1, reference2, reference3, reference4])
        self.assertEqual(
            document_paths, [doc_path1, doc_path2, doc_path3, doc_path4])
        # reference3 over-rides reference1.
        expected_map = {
            doc_path2: reference2,
            doc_path3: reference3,
            doc_path4: reference4,
        }
        self.assertEqual(reference_map, expected_map)


class Test__get_reference(unittest.TestCase):

    @staticmethod
    def _call_fut(document_path, reference_map):
        from google.cloud.firestore_v1beta1.client import _get_reference

        return _get_reference(document_path, reference_map)

    def test_success(self):
        doc_path = 'a/b/c'
        reference_map = {doc_path: mock.sentinel.reference}
        self.assertIs(
            self._call_fut(doc_path, reference_map), mock.sentinel.reference)

    def test_failure(self):
        from google.cloud.firestore_v1beta1.client import _BAD_DOC_TEMPLATE

        doc_path = '1/888/call-now'
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(doc_path, {})

        err_msg = _BAD_DOC_TEMPLATE.format(doc_path)
        self.assertEqual(exc_info.exception.args, (err_msg,))


class Test__parse_batch_get(unittest.TestCase):

    @staticmethod
    def _call_fut(
            get_doc_response, reference_map, client=mock.sentinel.client):
        from google.cloud.firestore_v1beta1.client import _parse_batch_get

        return _parse_batch_get(get_doc_response, reference_map, client)

    @staticmethod
    def _dummy_ref_string():
        from google.cloud.firestore_v1beta1.client import DEFAULT_DATABASE

        project = u'bazzzz'
        collection_id = u'fizz'
        document_id = u'buzz'
        return u'projects/{}/databases/{}/documents/{}/{}'.format(
            project, DEFAULT_DATABASE, collection_id, document_id)

    def test_found(self):
        from google.cloud.firestore_v1beta1.proto import document_pb2
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.firestore_v1beta1.document import DocumentSnapshot

        now = datetime.datetime.utcnow()
        read_time = _datetime_to_pb_timestamp(now)
        delta = datetime.timedelta(seconds=100)
        update_time = _datetime_to_pb_timestamp(now - delta)
        create_time = _datetime_to_pb_timestamp(now - 2 * delta)

        ref_string = self._dummy_ref_string()
        document_pb = document_pb2.Document(
            name=ref_string,
            fields={
                'foo': document_pb2.Value(double_value=1.5),
                'bar': document_pb2.Value(string_value=u'skillz'),
            },
            create_time=create_time,
            update_time=update_time,
        )
        response_pb = _make_batch_response(
            found=document_pb,
            read_time=read_time,
        )

        reference_map = {ref_string: mock.sentinel.reference}
        snapshot = self._call_fut(response_pb, reference_map)
        self.assertIsInstance(snapshot, DocumentSnapshot)
        self.assertIs(snapshot._reference, mock.sentinel.reference)
        self.assertEqual(snapshot._data, {'foo': 1.5, 'bar': u'skillz'})
        self.assertTrue(snapshot._exists)
        self.assertEqual(snapshot.read_time, read_time)
        self.assertEqual(snapshot.create_time, create_time)
        self.assertEqual(snapshot.update_time, update_time)

    def test_missing(self):
        ref_string = self._dummy_ref_string()
        response_pb = _make_batch_response(missing=ref_string)

        snapshot = self._call_fut(response_pb, {})
        self.assertIsNone(snapshot)

    def test_unset_result_type(self):
        response_pb = _make_batch_response()
        with self.assertRaises(ValueError):
            self._call_fut(response_pb, {})

    def test_unknown_result_type(self):
        response_pb = mock.Mock(spec=['WhichOneof'])
        response_pb.WhichOneof.return_value = 'zoob_value'

        with self.assertRaises(ValueError):
            self._call_fut(response_pb, {})

        response_pb.WhichOneof.assert_called_once_with('result')


class Test__get_doc_mask(unittest.TestCase):

    @staticmethod
    def _call_fut(field_paths):
        from google.cloud.firestore_v1beta1.client import _get_doc_mask

        return _get_doc_mask(field_paths)

    def test_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_paths(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2

        field_paths = ['a.b', 'c']
        result = self._call_fut(field_paths)
        expected = common_pb2.DocumentMask(field_paths=field_paths)
        self.assertEqual(result, expected)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_batch_response(**kwargs):
    from google.cloud.firestore_v1beta1.proto import firestore_pb2

    return firestore_pb2.BatchGetDocumentsResponse(**kwargs)


def _doc_get_info(ref_string, values):
    from google.cloud.firestore_v1beta1.proto import document_pb2
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.firestore_v1beta1 import _helpers

    now = datetime.datetime.utcnow()
    read_time = _datetime_to_pb_timestamp(now)
    delta = datetime.timedelta(seconds=100)
    update_time = _datetime_to_pb_timestamp(now - delta)
    create_time = _datetime_to_pb_timestamp(now - 2 * delta)

    document_pb = document_pb2.Document(
        name=ref_string,
        fields=_helpers.encode_dict(values),
        create_time=create_time,
        update_time=update_time,
    )

    return document_pb, read_time


class TestMergeOption(unittest.TestCase):
    
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1 import client

        return client.MergeOption()
    
    def test__convert_simple_field_paths_with_leading_digits(self):
        klass = self._get_target_class()
        field_paths = ["0abc", "abc", "321"]
        convert = klass._convert_simple_fields_with_leading_digits(field_paths)
        self.assertListEqual(convert, ["`0abc`", "abc", "`321`"])
