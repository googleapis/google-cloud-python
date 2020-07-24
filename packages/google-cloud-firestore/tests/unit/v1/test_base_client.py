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

import datetime
import unittest

import mock


class TestBaseClient(unittest.TestCase):

    PROJECT = "my-prahjekt"

    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.client import Client

        return Client

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def _make_default_one(self):
        credentials = _make_credentials()
        return self._make_one(project=self.PROJECT, credentials=credentials)

    @mock.patch(
        "google.cloud.firestore_v1.services.firestore.client.FirestoreClient",
        autospec=True,
        return_value=mock.sentinel.firestore_api,
    )
    @mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.grpc.FirestoreGrpcTransport",
        autospec=True,
    )
    def test__firestore_api_property(self, mock_channel, mock_client):
        mock_client.DEFAULT_ENDPOINT = "endpoint"
        client = self._make_default_one()
        client_options = client._client_options = mock.Mock()
        self.assertIsNone(client._firestore_api_internal)
        firestore_api = client._firestore_api
        self.assertIs(firestore_api, mock_client.return_value)
        self.assertIs(firestore_api, client._firestore_api_internal)
        mock_client.assert_called_once_with(
            transport=client._transport, client_options=client_options
        )

        # Call again to show that it is cached, but call count is still 1.
        self.assertIs(client._firestore_api, mock_client.return_value)
        self.assertEqual(mock_client.call_count, 1)

    @mock.patch(
        "google.cloud.firestore_v1.services.firestore.client.FirestoreClient",
        autospec=True,
        return_value=mock.sentinel.firestore_api,
    )
    @mock.patch(
        "google.cloud.firestore_v1.services.firestore.transports.grpc.FirestoreGrpcTransport.create_channel",
        autospec=True,
    )
    def test__firestore_api_property_with_emulator(
        self, mock_insecure_channel, mock_client
    ):
        emulator_host = "localhost:8081"
        with mock.patch("os.getenv") as getenv:
            getenv.return_value = emulator_host
            client = self._make_default_one()

        self.assertIsNone(client._firestore_api_internal)
        firestore_api = client._firestore_api
        self.assertIs(firestore_api, mock_client.return_value)
        self.assertIs(firestore_api, client._firestore_api_internal)

        mock_insecure_channel.assert_called_once_with(host=emulator_host)

        # Call again to show that it is cached, but call count is still 1.
        self.assertIs(client._firestore_api, mock_client.return_value)
        self.assertEqual(mock_client.call_count, 1)

    def test___database_string_property(self):
        credentials = _make_credentials()
        database = "cheeeeez"
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, database=database
        )
        self.assertIsNone(client._database_string_internal)
        database_string = client._database_string
        expected = "projects/{}/databases/{}".format(client.project, client._database)
        self.assertEqual(database_string, expected)
        self.assertIs(database_string, client._database_string_internal)

        # Swap it out with a unique value to verify it is cached.
        client._database_string_internal = mock.sentinel.cached
        self.assertIs(client._database_string, mock.sentinel.cached)

    def test___rpc_metadata_property(self):
        credentials = _make_credentials()
        database = "quanta"
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, database=database
        )

        self.assertEqual(
            client._rpc_metadata,
            [("google-cloud-resource-prefix", client._database_string)],
        )

    def test__rpc_metadata_property_with_emulator(self):
        emulator_host = "localhost:8081"
        with mock.patch("os.getenv") as getenv:
            getenv.return_value = emulator_host

            credentials = _make_credentials()
            database = "quanta"
            client = self._make_one(
                project=self.PROJECT, credentials=credentials, database=database
            )

        self.assertEqual(
            client._rpc_metadata,
            [
                ("google-cloud-resource-prefix", client._database_string),
                ("authorization", "Bearer owner"),
            ],
        )

    def test_field_path(self):
        klass = self._get_target_class()
        self.assertEqual(klass.field_path("a", "b", "c"), "a.b.c")

    def test_write_option_last_update(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1._helpers import LastUpdateOption

        timestamp = timestamp_pb2.Timestamp(seconds=1299767599, nanos=811111097)

        klass = self._get_target_class()
        option = klass.write_option(last_update_time=timestamp)
        self.assertIsInstance(option, LastUpdateOption)
        self.assertEqual(option._last_update_time, timestamp)

    def test_write_option_exists(self):
        from google.cloud.firestore_v1._helpers import ExistsOption

        klass = self._get_target_class()

        option1 = klass.write_option(exists=False)
        self.assertIsInstance(option1, ExistsOption)
        self.assertFalse(option1._exists)

        option2 = klass.write_option(exists=True)
        self.assertIsInstance(option2, ExistsOption)
        self.assertTrue(option2._exists)

    def test_write_open_neither_arg(self):
        from google.cloud.firestore_v1.base_client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option()

        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR,))

    def test_write_multiple_args(self):
        from google.cloud.firestore_v1.base_client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option(exists=False, last_update_time=mock.sentinel.timestamp)

        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR,))

    def test_write_bad_arg(self):
        from google.cloud.firestore_v1.base_client import _BAD_OPTION_ERR

        klass = self._get_target_class()
        with self.assertRaises(TypeError) as exc_info:
            klass.write_option(spinach="popeye")

        extra = "{!r} was provided".format("spinach")
        self.assertEqual(exc_info.exception.args, (_BAD_OPTION_ERR, extra))


class Test__reference_info(unittest.TestCase):
    @staticmethod
    def _call_fut(references):
        from google.cloud.firestore_v1.base_client import _reference_info

        return _reference_info(references)

    def test_it(self):
        from google.cloud.firestore_v1.client import Client

        credentials = _make_credentials()
        client = Client(project="hi-projject", credentials=credentials)

        reference1 = client.document("a", "b")
        reference2 = client.document("a", "b", "c", "d")
        reference3 = client.document("a", "b")
        reference4 = client.document("f", "g")

        doc_path1 = reference1._document_path
        doc_path2 = reference2._document_path
        doc_path3 = reference3._document_path
        doc_path4 = reference4._document_path
        self.assertEqual(doc_path1, doc_path3)

        document_paths, reference_map = self._call_fut(
            [reference1, reference2, reference3, reference4]
        )
        self.assertEqual(document_paths, [doc_path1, doc_path2, doc_path3, doc_path4])
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
        from google.cloud.firestore_v1.base_client import _get_reference

        return _get_reference(document_path, reference_map)

    def test_success(self):
        doc_path = "a/b/c"
        reference_map = {doc_path: mock.sentinel.reference}
        self.assertIs(self._call_fut(doc_path, reference_map), mock.sentinel.reference)

    def test_failure(self):
        from google.cloud.firestore_v1.base_client import _BAD_DOC_TEMPLATE

        doc_path = "1/888/call-now"
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(doc_path, {})

        err_msg = _BAD_DOC_TEMPLATE.format(doc_path)
        self.assertEqual(exc_info.exception.args, (err_msg,))


class Test__parse_batch_get(unittest.TestCase):
    @staticmethod
    def _call_fut(get_doc_response, reference_map, client=mock.sentinel.client):
        from google.cloud.firestore_v1.base_client import _parse_batch_get

        return _parse_batch_get(get_doc_response, reference_map, client)

    @staticmethod
    def _dummy_ref_string():
        from google.cloud.firestore_v1.base_client import DEFAULT_DATABASE

        project = u"bazzzz"
        collection_id = u"fizz"
        document_id = u"buzz"
        return u"projects/{}/databases/{}/documents/{}/{}".format(
            project, DEFAULT_DATABASE, collection_id, document_id
        )

    def test_found(self):
        from google.cloud.firestore_v1.types import document
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.firestore_v1.document import DocumentSnapshot

        now = datetime.datetime.utcnow()
        read_time = _datetime_to_pb_timestamp(now)
        delta = datetime.timedelta(seconds=100)
        update_time = _datetime_to_pb_timestamp(now - delta)
        create_time = _datetime_to_pb_timestamp(now - 2 * delta)

        ref_string = self._dummy_ref_string()
        document_pb = document.Document(
            name=ref_string,
            fields={
                "foo": document.Value(double_value=1.5),
                "bar": document.Value(string_value=u"skillz"),
            },
            create_time=create_time,
            update_time=update_time,
        )
        response_pb = _make_batch_response(found=document_pb, read_time=read_time)

        reference_map = {ref_string: mock.sentinel.reference}
        snapshot = self._call_fut(response_pb, reference_map)
        self.assertIsInstance(snapshot, DocumentSnapshot)
        self.assertIs(snapshot._reference, mock.sentinel.reference)
        self.assertEqual(snapshot._data, {"foo": 1.5, "bar": u"skillz"})
        self.assertTrue(snapshot._exists)
        self.assertEqual(snapshot.read_time.timestamp_pb(), read_time)
        self.assertEqual(snapshot.create_time.timestamp_pb(), create_time)
        self.assertEqual(snapshot.update_time.timestamp_pb(), update_time)

    def test_missing(self):
        from google.cloud.firestore_v1.document import DocumentReference

        ref_string = self._dummy_ref_string()
        response_pb = _make_batch_response(missing=ref_string)
        document = DocumentReference("fizz", "bazz", client=mock.sentinel.client)
        reference_map = {ref_string: document}
        snapshot = self._call_fut(response_pb, reference_map)
        self.assertFalse(snapshot.exists)
        self.assertEqual(snapshot.id, "bazz")
        self.assertIsNone(snapshot._data)

    def test_unset_result_type(self):
        response_pb = _make_batch_response()
        with self.assertRaises(ValueError):
            self._call_fut(response_pb, {})

    def test_unknown_result_type(self):
        response_pb = mock.Mock()
        response_pb._pb.mock_add_spec(spec=["WhichOneof"])
        response_pb._pb.WhichOneof.return_value = "zoob_value"

        with self.assertRaises(ValueError):
            self._call_fut(response_pb, {})

        response_pb._pb.WhichOneof.assert_called_once_with("result")


class Test__get_doc_mask(unittest.TestCase):
    @staticmethod
    def _call_fut(field_paths):
        from google.cloud.firestore_v1.base_client import _get_doc_mask

        return _get_doc_mask(field_paths)

    def test_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_paths(self):
        from google.cloud.firestore_v1.types import common

        field_paths = ["a.b", "c"]
        result = self._call_fut(field_paths)
        expected = common.DocumentMask(field_paths=field_paths)
        self.assertEqual(result, expected)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_batch_response(**kwargs):
    from google.cloud.firestore_v1.types import firestore

    return firestore.BatchGetDocumentsResponse(**kwargs)
