# Copyright 2014 Google LLC
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
from six.moves import http_client

import requests


class Test__request(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.datastore._http import _request

        return _request(*args, **kwargs)

    def test_success(self):
        from google.cloud import _http as connection_module

        project = "PROJECT"
        method = "METHOD"
        data = b"DATA"
        base_url = "http://api-url"
        user_agent = "USER AGENT"
        client_info = _make_client_info(user_agent)
        response_data = "CONTENT"

        http = _make_requests_session([_make_response(content=response_data)])

        # Call actual function under test.
        response = self._call_fut(http, project, method, data, base_url, client_info)
        self.assertEqual(response, response_data)

        # Check that the mocks were called as expected.
        expected_url = _build_expected_url(base_url, project, method)
        expected_headers = {
            "Content-Type": "application/x-protobuf",
            "User-Agent": user_agent,
            connection_module.CLIENT_INFO_HEADER: user_agent,
        }
        http.request.assert_called_once_with(
            method="POST", url=expected_url, headers=expected_headers, data=data
        )

    def test_failure(self):
        from google.cloud.exceptions import BadRequest
        from google.rpc import code_pb2
        from google.rpc import status_pb2

        project = "PROJECT"
        method = "METHOD"
        data = "DATA"
        uri = "http://api-url"
        user_agent = "USER AGENT"
        client_info = _make_client_info(user_agent)

        error = status_pb2.Status()
        error.message = "Entity value is indexed."
        error.code = code_pb2.FAILED_PRECONDITION

        http = _make_requests_session(
            [_make_response(http_client.BAD_REQUEST, content=error.SerializeToString())]
        )

        with self.assertRaises(BadRequest) as exc:
            self._call_fut(http, project, method, data, uri, client_info)

        expected_message = "400 Entity value is indexed."
        self.assertEqual(str(exc.exception), expected_message)


class Test__rpc(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.datastore._http import _rpc

        return _rpc(*args, **kwargs)

    def test_it(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        http = object()
        project = "projectOK"
        method = "beginTransaction"
        base_url = "test.invalid"
        client_info = _make_client_info()
        request_pb = datastore_pb2.BeginTransactionRequest(project_id=project)

        response_pb = datastore_pb2.BeginTransactionResponse(transaction=b"7830rmc")
        patch = mock.patch(
            "google.cloud.datastore._http._request",
            return_value=response_pb._pb.SerializeToString(),
        )
        with patch as mock_request:
            result = self._call_fut(
                http,
                project,
                method,
                base_url,
                client_info,
                request_pb,
                datastore_pb2.BeginTransactionResponse,
            )
            self.assertEqual(result, response_pb._pb)

            mock_request.assert_called_once_with(
                http,
                project,
                method,
                request_pb._pb.SerializeToString(),
                base_url,
                client_info,
            )


class TestHTTPDatastoreAPI(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.datastore._http import HTTPDatastoreAPI

        return HTTPDatastoreAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _make_query_pb(kind):
        from google.cloud.datastore_v1.types import query as query_pb2

        return query_pb2.Query(kind=[query_pb2.KindExpression(name=kind)])

    def test_constructor(self):
        client = object()
        ds_api = self._make_one(client)
        self.assertIs(ds_api.client, client)

    def test_lookup_single_key_empty_response(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()
        read_options = datastore_pb2.ReadOptions()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_single_key_empty_response_w_eventual(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()
        read_options = datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.ReadConsistency.EVENTUAL
        )

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        transaction = b"TRANSACTION"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()
        read_options = datastore_pb2.ReadOptions(transaction=transaction)

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_single_key_nonempty_response(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2

        project = "PROJECT"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.LookupResponse()
        entity = entity_pb2.Entity()
        entity.key._pb.CopyFrom(key_pb._pb)
        rsp_pb._pb.found.add(entity=entity._pb)
        read_options = datastore_pb2.ReadOptions()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 1)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)
        found = response.found[0].entity
        self.assertEqual(found.key.path[0].kind, "Kind")
        self.assertEqual(found.key.path[0].id, 1234)

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_multiple_keys_empty_response(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        read_options = datastore_pb2.ReadOptions()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb1, key_pb2], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb1._pb, key_pb2._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_multiple_keys_w_missing(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        er_1 = rsp_pb._pb.missing.add()
        er_1.entity.key.CopyFrom(key_pb1._pb)
        er_2 = rsp_pb._pb.missing.add()
        er_2.entity.key.CopyFrom(key_pb2._pb)
        read_options = datastore_pb2.ReadOptions()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb1, key_pb2], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.deferred), 0)
        missing_keys = [result.entity.key for result in response.missing]
        self.assertEqual(missing_keys, [key_pb1._pb, key_pb2._pb])

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb1._pb, key_pb2._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_multiple_keys_w_deferred(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        rsp_pb._pb.deferred.add().CopyFrom(key_pb1._pb)
        rsp_pb._pb.deferred.add().CopyFrom(key_pb2._pb)
        read_options = datastore_pb2.ReadOptions()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.lookup(project, [key_pb1, key_pb2], read_options=read_options)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        uri = _build_expected_url(client._base_url, project, "lookup")
        self.assertEqual(len(response.found), 0)
        self.assertEqual(len(response.missing), 0)
        self.assertEqual(list(response.deferred), [key_pb1._pb, key_pb2._pb])

        request = _verify_protobuf_call(http, uri, datastore_pb2.LookupRequest())
        self.assertEqual(list(request.keys), [key_pb1._pb, key_pb2._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_run_query_w_eventual_no_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore_v1.types import query as query_pb2

        project = "PROJECT"
        kind = "Nonesuch"
        cursor = b"\x00"
        query_pb = self._make_query_pb(kind)
        partition_id = entity_pb2.PartitionId(project_id=project)
        read_options = datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.ReadConsistency.EVENTUAL
        )
        rsp_pb = datastore_pb2.RunQueryResponse(
            batch=query_pb2.QueryResultBatch(
                entity_result_type=query_pb2.EntityResult.ResultType.FULL,
                end_cursor=cursor,
                more_results=query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS,
            )
        )

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.run_query(project, partition_id, read_options, query=query_pb)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "runQuery")
        request = _verify_protobuf_call(http, uri, datastore_pb2.RunQueryRequest())
        self.assertEqual(request.partition_id, partition_id._pb)
        self.assertEqual(request.query, query_pb._pb)
        self.assertEqual(request.read_options, read_options._pb)

    def test_run_query_wo_eventual_w_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore_v1.types import query as query_pb2

        project = "PROJECT"
        kind = "Nonesuch"
        cursor = b"\x00"
        transaction = b"TRANSACTION"
        query_pb = self._make_query_pb(kind)
        partition_id = entity_pb2.PartitionId(project_id=project)
        read_options = datastore_pb2.ReadOptions(transaction=transaction)
        rsp_pb = datastore_pb2.RunQueryResponse(
            batch=query_pb2.QueryResultBatch(
                entity_result_type=query_pb2.EntityResult.ResultType.FULL,
                end_cursor=cursor,
                more_results=query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS,
            )
        )

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.run_query(project, partition_id, read_options, query=query_pb)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "runQuery")
        request = _verify_protobuf_call(http, uri, datastore_pb2.RunQueryRequest())
        self.assertEqual(request.partition_id, partition_id._pb)
        self.assertEqual(request.query, query_pb._pb)
        self.assertEqual(request.read_options, read_options._pb)

    def test_run_query_wo_namespace_empty_result(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore_v1.types import query as query_pb2

        project = "PROJECT"
        kind = "Nonesuch"
        cursor = b"\x00"
        query_pb = self._make_query_pb(kind)
        partition_id = entity_pb2.PartitionId(project_id=project)
        read_options = datastore_pb2.ReadOptions()
        rsp_pb = datastore_pb2.RunQueryResponse(
            batch=query_pb2.QueryResultBatch(
                entity_result_type=query_pb2.EntityResult.ResultType.FULL,
                end_cursor=cursor,
                more_results=query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS,
            )
        )

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.run_query(project, partition_id, read_options, query=query_pb)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "runQuery")
        request = _verify_protobuf_call(http, uri, datastore_pb2.RunQueryRequest())
        self.assertEqual(request.partition_id, partition_id._pb)
        self.assertEqual(request.query, query_pb._pb)
        self.assertEqual(request.read_options, read_options._pb)

    def test_run_query_w_namespace_nonempty_result(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore_v1.types import query as query_pb2

        project = "PROJECT"
        kind = "Kind"
        namespace = "NS"
        query_pb = self._make_query_pb(kind)
        partition_id = entity_pb2.PartitionId(
            project_id=project, namespace_id=namespace
        )
        read_options = datastore_pb2.ReadOptions()
        rsp_pb = datastore_pb2.RunQueryResponse(
            batch=query_pb2.QueryResultBatch(
                entity_result_type=query_pb2.EntityResult.ResultType.FULL,
                entity_results=[query_pb2.EntityResult(entity=entity_pb2.Entity())],
                more_results=query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS,
            )
        )

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.run_query(project, partition_id, read_options, query=query_pb)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "runQuery")
        request = _verify_protobuf_call(http, uri, datastore_pb2.RunQueryRequest())
        self.assertEqual(request.partition_id, partition_id._pb)
        self.assertEqual(request.query, query_pb._pb)

    def test_begin_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        transaction = b"TRANSACTION"
        rsp_pb = datastore_pb2.BeginTransactionResponse()
        rsp_pb.transaction = transaction

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.begin_transaction(project)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "beginTransaction")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.BeginTransactionRequest()
        )
        # The RPC-over-HTTP request does not set the project in the request.
        self.assertEqual(request.project_id, u"")

    def test_commit_wo_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        project = "PROJECT"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb._pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb._pb)
        value_pb = _new_value_pb(insert, "foo")
        value_pb.string_value = u"Foo"

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        rq_class = datastore_pb2.CommitRequest
        ds_api = self._make_one(client)
        mode = rq_class.Mode.NON_TRANSACTIONAL
        result = ds_api.commit(project, mode, [mutation])

        # Check the result and verify the callers.
        self.assertEqual(result, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "commit")
        request = _verify_protobuf_call(http, uri, rq_class())
        self.assertEqual(request.transaction, b"")
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.Mode.NON_TRANSACTIONAL)

    def test_commit_w_transaction(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        project = "PROJECT"
        key_pb = _make_key_pb(project)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb._pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb._pb)
        value_pb = _new_value_pb(insert, "foo")
        value_pb.string_value = u"Foo"

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        rq_class = datastore_pb2.CommitRequest
        ds_api = self._make_one(client)
        mode = rq_class.Mode.TRANSACTIONAL
        result = ds_api.commit(project, mode, [mutation], transaction=b"xact")

        # Check the result and verify the callers.
        self.assertEqual(result, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "commit")
        request = _verify_protobuf_call(http, uri, rq_class())
        self.assertEqual(request.transaction, b"xact")
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.Mode.TRANSACTIONAL)

    def test_rollback_ok(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        transaction = b"xact"
        rsp_pb = datastore_pb2.RollbackResponse()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.rollback(project, transaction)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "rollback")
        request = _verify_protobuf_call(http, uri, datastore_pb2.RollbackRequest())
        self.assertEqual(request.transaction, transaction)

    def test_allocate_ids_empty(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        rsp_pb = datastore_pb2.AllocateIdsResponse()

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.allocate_ids(project, [])

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)
        self.assertEqual(list(response.keys), [])

        uri = _build_expected_url(client._base_url, project, "allocateIds")
        request = _verify_protobuf_call(http, uri, datastore_pb2.AllocateIdsRequest())
        self.assertEqual(list(request.keys), [])

    def test_allocate_ids_non_empty(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        before_key_pbs = [
            _make_key_pb(project, id_=None),
            _make_key_pb(project, id_=None),
        ]
        after_key_pbs = [_make_key_pb(project), _make_key_pb(project, id_=2345)]
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        rsp_pb._pb.keys.add().CopyFrom(after_key_pbs[0]._pb)
        rsp_pb._pb.keys.add().CopyFrom(after_key_pbs[1]._pb)

        # Create mock HTTP and client with response.
        http = _make_requests_session(
            [_make_response(content=rsp_pb._pb.SerializeToString())]
        )
        client_info = _make_client_info()
        client = mock.Mock(
            _http=http,
            _base_url="test.invalid",
            _client_info=client_info,
            spec=["_http", "_base_url", "_client_info"],
        )

        # Make request.
        ds_api = self._make_one(client)
        response = ds_api.allocate_ids(project, before_key_pbs)

        # Check the result and verify the callers.
        self.assertEqual(list(response.keys), [i._pb for i in after_key_pbs])
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "allocateIds")
        request = _verify_protobuf_call(http, uri, datastore_pb2.AllocateIdsRequest())
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)


def _make_response(status=http_client.OK, content=b"", headers={}):
    response = requests.Response()
    response.status_code = status
    response._content = content
    response.headers = headers
    response.request = requests.Request()
    return response


def _make_requests_session(responses):
    session = mock.create_autospec(requests.Session, instance=True)
    session.request.side_effect = responses
    return session


def _build_expected_url(api_base_url, project, method):
    from google.cloud.datastore._http import API_VERSION

    return "/".join([api_base_url, API_VERSION, "projects", project + ":" + method])


def _make_key_pb(project, id_=1234):
    from google.cloud.datastore.key import Key

    path_args = ("Kind",)
    if id_ is not None:
        path_args += (id_,)
    return Key(*path_args, project=project).to_protobuf()


_USER_AGENT = "TESTING USER AGENT"


def _make_client_info(user_agent=_USER_AGENT):
    from google.api_core.client_info import ClientInfo

    client_info = mock.create_autospec(ClientInfo)
    client_info.to_user_agent.return_value = user_agent
    return client_info


def _verify_protobuf_call(http, expected_url, pb):
    from google.cloud import _http as connection_module

    expected_headers = {
        "Content-Type": "application/x-protobuf",
        "User-Agent": _USER_AGENT,
        connection_module.CLIENT_INFO_HEADER: _USER_AGENT,
    }

    http.request.assert_called_once_with(
        method="POST", url=expected_url, headers=expected_headers, data=mock.ANY
    )

    data = http.request.mock_calls[0][2]["data"]
    pb._pb.ParseFromString(data)
    return pb
