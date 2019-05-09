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

import unittest

import mock


class TestWriteBatch(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.batch import WriteBatch

        return WriteBatch

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        batch = self._make_one(mock.sentinel.client)
        self.assertIs(batch._client, mock.sentinel.client)
        self.assertEqual(batch._write_pbs, [])
        self.assertIsNone(batch.write_results)
        self.assertIsNone(batch.commit_time)

    def test__add_write_pbs(self):
        batch = self._make_one(mock.sentinel.client)
        self.assertEqual(batch._write_pbs, [])
        batch._add_write_pbs([mock.sentinel.write1, mock.sentinel.write2])
        self.assertEqual(batch._write_pbs, [mock.sentinel.write1, mock.sentinel.write2])

    def test_create(self):
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        client = _make_client()
        batch = self._make_one(client)
        self.assertEqual(batch._write_pbs, [])

        reference = client.document("this", "one")
        document_data = {"a": 10, "b": 2.5}
        ret_val = batch.create(reference, document_data)
        self.assertIsNone(ret_val)
        new_write_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=reference._document_path,
                fields={
                    "a": _value_pb(integer_value=document_data["a"]),
                    "b": _value_pb(double_value=document_data["b"]),
                },
            ),
            current_document=common_pb2.Precondition(exists=False),
        )
        self.assertEqual(batch._write_pbs, [new_write_pb])

    def test_set(self):
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        client = _make_client()
        batch = self._make_one(client)
        self.assertEqual(batch._write_pbs, [])

        reference = client.document("another", "one")
        field = "zapzap"
        value = u"meadows and flowers"
        document_data = {field: value}
        ret_val = batch.set(reference, document_data)
        self.assertIsNone(ret_val)
        new_write_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=reference._document_path,
                fields={field: _value_pb(string_value=value)},
            )
        )
        self.assertEqual(batch._write_pbs, [new_write_pb])

    def test_set_merge(self):
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        client = _make_client()
        batch = self._make_one(client)
        self.assertEqual(batch._write_pbs, [])

        reference = client.document("another", "one")
        field = "zapzap"
        value = u"meadows and flowers"
        document_data = {field: value}
        ret_val = batch.set(reference, document_data, merge=True)
        self.assertIsNone(ret_val)
        new_write_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=reference._document_path,
                fields={field: _value_pb(string_value=value)},
            ),
            update_mask={"field_paths": [field]},
        )
        self.assertEqual(batch._write_pbs, [new_write_pb])

    def test_update(self):
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        client = _make_client()
        batch = self._make_one(client)
        self.assertEqual(batch._write_pbs, [])

        reference = client.document("cats", "cradle")
        field_path = "head.foot"
        value = u"knees toes shoulders"
        field_updates = {field_path: value}

        ret_val = batch.update(reference, field_updates)
        self.assertIsNone(ret_val)

        map_pb = document_pb2.MapValue(fields={"foot": _value_pb(string_value=value)})
        new_write_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=reference._document_path,
                fields={"head": _value_pb(map_value=map_pb)},
            ),
            update_mask=common_pb2.DocumentMask(field_paths=[field_path]),
            current_document=common_pb2.Precondition(exists=True),
        )
        self.assertEqual(batch._write_pbs, [new_write_pb])

    def test_delete(self):
        from google.cloud.firestore_v1.proto import write_pb2

        client = _make_client()
        batch = self._make_one(client)
        self.assertEqual(batch._write_pbs, [])

        reference = client.document("early", "mornin", "dawn", "now")
        ret_val = batch.delete(reference)
        self.assertIsNone(ret_val)
        new_write_pb = write_pb2.Write(delete=reference._document_path)
        self.assertEqual(batch._write_pbs, [new_write_pb])

    def test_commit(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto import firestore_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.Mock(spec=["commit"])
        timestamp = timestamp_pb2.Timestamp(seconds=1234567, nanos=123456798)
        commit_response = firestore_pb2.CommitResponse(
            write_results=[write_pb2.WriteResult(), write_pb2.WriteResult()],
            commit_time=timestamp,
        )
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client("grand")
        client._firestore_api_internal = firestore_api

        # Actually make a batch with some mutations and call commit().
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        batch.create(document1, {"ten": 10, "buck": u"ets"})
        document2 = client.document("c", "d", "e", "f")
        batch.delete(document2)
        write_pbs = batch._write_pbs[::]

        write_results = batch.commit()
        self.assertEqual(write_results, list(commit_response.write_results))
        self.assertEqual(batch.write_results, write_results)
        self.assertEqual(batch.commit_time, timestamp)
        # Make sure batch has no more "changes".
        self.assertEqual(batch._write_pbs, [])

        # Verify the mocks.
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            write_pbs,
            transaction=None,
            metadata=client._rpc_metadata,
        )

    def test_as_context_mgr_wo_error(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto import firestore_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        firestore_api = mock.Mock(spec=["commit"])
        timestamp = timestamp_pb2.Timestamp(seconds=1234567, nanos=123456798)
        commit_response = firestore_pb2.CommitResponse(
            write_results=[write_pb2.WriteResult(), write_pb2.WriteResult()],
            commit_time=timestamp,
        )
        firestore_api.commit.return_value = commit_response
        client = _make_client()
        client._firestore_api_internal = firestore_api
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        document2 = client.document("c", "d", "e", "f")

        with batch as ctx_mgr:
            self.assertIs(ctx_mgr, batch)
            ctx_mgr.create(document1, {"ten": 10, "buck": u"ets"})
            ctx_mgr.delete(document2)
            write_pbs = batch._write_pbs[::]

        self.assertEqual(batch.write_results, list(commit_response.write_results))
        self.assertEqual(batch.commit_time, timestamp)
        # Make sure batch has no more "changes".
        self.assertEqual(batch._write_pbs, [])

        # Verify the mocks.
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            write_pbs,
            transaction=None,
            metadata=client._rpc_metadata,
        )

    def test_as_context_mgr_w_error(self):
        firestore_api = mock.Mock(spec=["commit"])
        client = _make_client()
        client._firestore_api_internal = firestore_api
        batch = self._make_one(client)
        document1 = client.document("a", "b")
        document2 = client.document("c", "d", "e", "f")

        with self.assertRaises(RuntimeError):
            with batch as ctx_mgr:
                ctx_mgr.create(document1, {"ten": 10, "buck": u"ets"})
                ctx_mgr.delete(document2)
                raise RuntimeError("testing")

        self.assertIsNone(batch.write_results)
        self.assertIsNone(batch.commit_time)
        # batch still has its changes
        self.assertEqual(len(batch._write_pbs), 2)

        firestore_api.commit.assert_not_called()


def _value_pb(**kwargs):
    from google.cloud.firestore_v1.proto.document_pb2 import Value

    return Value(**kwargs)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="seventy-nine"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
