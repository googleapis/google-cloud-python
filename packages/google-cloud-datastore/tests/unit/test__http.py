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
from http import client

import requests


class Test__make_retry_timeout_kwargs(unittest.TestCase):
    @staticmethod
    def _call_fut(retry, timeout):
        from google.cloud.datastore._http import _make_retry_timeout_kwargs

        return _make_retry_timeout_kwargs(retry, timeout)

    def test_empty(self):
        expected = {}
        self.assertEqual(self._call_fut(None, None), expected)

    def test_w_retry(self):
        retry = object()
        expected = {"retry": retry}
        self.assertEqual(self._call_fut(retry, None), expected)

    def test_w_timeout(self):
        timeout = 5.0
        expected = {"timeout": timeout}
        self.assertEqual(self._call_fut(None, timeout), expected)

    def test_w_retry_w_timeout(self):
        retry = object()
        timeout = 5.0
        expected = {"retry": retry, "timeout": timeout}
        self.assertEqual(self._call_fut(retry, timeout), expected)


class Foo:
    def __init__(self, bar=None, baz=None):
        self.bar = bar
        self.baz = baz


class Test__make_request_pb(unittest.TestCase):
    @staticmethod
    def _call_fut(request, request_pb_type):
        from google.cloud.datastore._http import _make_request_pb

        return _make_request_pb(request, request_pb_type)

    def test_w_empty_dict(self):
        request = {}

        foo = self._call_fut(request, Foo)

        self.assertIsInstance(foo, Foo)
        self.assertIsNone(foo.bar)
        self.assertIsNone(foo.baz)

    def test_w_partial_dict(self):
        request = {"bar": "Bar"}

        foo = self._call_fut(request, Foo)

        self.assertIsInstance(foo, Foo)
        self.assertEqual(foo.bar, "Bar")
        self.assertIsNone(foo.baz)

    def test_w_complete_dict(self):
        request = {"bar": "Bar", "baz": "Baz"}

        foo = self._call_fut(request, Foo)

        self.assertIsInstance(foo, Foo)
        self.assertEqual(foo.bar, "Bar")
        self.assertEqual(foo.baz, "Baz")

    def test_w_instance(self):
        passed = Foo()

        foo = self._call_fut(passed, Foo)

        self.assertIs(foo, passed)


class Test__request(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.datastore._http import _request

        return _request(*args, **kwargs)

    def _helper(self, retry=None, timeout=None):
        from google.cloud import _http as connection_module

        project = "PROJECT"
        method = "METHOD"
        data = b"DATA"
        base_url = "http://api-url"
        user_agent = "USER AGENT"
        client_info = _make_client_info(user_agent)
        response_data = "CONTENT"

        http = _make_requests_session([_make_response(content=response_data)])

        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = self._call_fut(
            http, project, method, data, base_url, client_info, **kwargs
        )
        self.assertEqual(response, response_data)

        # Check that the mocks were called as expected.
        expected_url = _build_expected_url(base_url, project, method)
        expected_headers = {
            "Content-Type": "application/x-protobuf",
            "User-Agent": user_agent,
            connection_module.CLIENT_INFO_HEADER: user_agent,
        }

        if retry is not None:
            retry.assert_called_once_with(http.request)

        kwargs.pop("retry", None)
        http.request.assert_called_once_with(
            method="POST",
            url=expected_url,
            headers=expected_headers,
            data=data,
            **kwargs
        )

    def test_ok(self):
        self._helper()

    def test_w_retry(self):
        retry = mock.MagicMock()
        self._helper(retry=retry)

    def test_w_timeout(self):
        timeout = 5.0
        self._helper(timeout=timeout)

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
            [_make_response(client.BAD_REQUEST, content=error.SerializeToString())]
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

    def _helper(self, retry=None, timeout=None):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        http = object()
        project = "projectOK"
        method = "beginTransaction"
        base_url = "test.invalid"
        client_info = _make_client_info()
        request_pb = datastore_pb2.BeginTransactionRequest(project_id=project)

        response_pb = datastore_pb2.BeginTransactionResponse(transaction=b"7830rmc")

        kwargs = _make_retry_timeout_kwargs(retry, timeout)

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
                **kwargs
            )

        self.assertEqual(result, response_pb._pb)

        mock_request.assert_called_once_with(
            http,
            project,
            method,
            request_pb._pb.SerializeToString(),
            base_url,
            client_info,
            **kwargs
        )

    def test_defaults(self):
        self._helper()

    def test_w_retry(self):
        retry = mock.MagicMock()
        self._helper(retry=retry)

    def test_w_timeout(self):
        timeout = 5.0
        self._helper(timeout=timeout)


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

    def _lookup_single_helper(
        self,
        read_consistency=None,
        transaction=None,
        empty=True,
        retry=None,
        timeout=None,
    ):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2

        project = "PROJECT"
        key_pb = _make_key_pb(project)

        options_kw = {}
        if read_consistency is not None:
            options_kw["read_consistency"] = read_consistency
        if transaction is not None:
            options_kw["transaction"] = transaction

        read_options = datastore_pb2.ReadOptions(**options_kw)

        rsp_pb = datastore_pb2.LookupResponse()

        if not empty:
            entity = entity_pb2.Entity()
            entity.key._pb.CopyFrom(key_pb._pb)
            rsp_pb._pb.found.add(entity=entity._pb)

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
        ds_api = self._make_one(client)
        request = {
            "project_id": project,
            "keys": [key_pb],
            "read_options": read_options,
        }
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.lookup(request=request, **kwargs)

        self.assertEqual(response, rsp_pb._pb)

        if empty:
            self.assertEqual(len(response.found), 0)
        else:
            self.assertEqual(len(response.found), 1)

        self.assertEqual(len(response.missing), 0)
        self.assertEqual(len(response.deferred), 0)

        uri = _build_expected_url(client._base_url, project, "lookup")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.LookupRequest(), retry=retry, timeout=timeout,
        )

        if retry is not None:
            retry.assert_called_once_with(http.request)

        self.assertEqual(list(request.keys), [key_pb._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_single_key_miss(self):
        self._lookup_single_helper()

    def test_lookup_single_key_miss_w_read_consistency(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        read_consistency = datastore_pb2.ReadOptions.ReadConsistency.EVENTUAL
        self._lookup_single_helper(read_consistency=read_consistency)

    def test_lookup_single_key_miss_w_transaction(self):
        transaction = b"TRANSACTION"
        self._lookup_single_helper(transaction=transaction)

    def test_lookup_single_key_hit(self):
        self._lookup_single_helper(empty=False)

    def test_lookup_single_key_hit_w_retry(self):
        retry = mock.MagicMock()
        self._lookup_single_helper(empty=False, retry=retry)

    def test_lookup_single_key_hit_w_timeout(self):
        timeout = 5.0
        self._lookup_single_helper(empty=False, timeout=timeout)

    def _lookup_multiple_helper(
        self, found=0, missing=0, deferred=0, retry=None, timeout=None,
    ):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2

        project = "PROJECT"
        key_pb1 = _make_key_pb(project)
        key_pb2 = _make_key_pb(project, id_=2345)
        keys = [key_pb1, key_pb2]
        read_options = datastore_pb2.ReadOptions()

        rsp_pb = datastore_pb2.LookupResponse()

        found_keys = []
        for i_found in range(found):
            key = keys[i_found]
            found_keys.append(key._pb)
            entity = entity_pb2.Entity()
            entity.key._pb.CopyFrom(key._pb)
            rsp_pb._pb.found.add(entity=entity._pb)

        missing_keys = []
        for i_missing in range(missing):
            key = keys[i_missing]
            missing_keys.append(key._pb)
            entity = entity_pb2.Entity()
            entity.key._pb.CopyFrom(key._pb)
            rsp_pb._pb.missing.add(entity=entity._pb)

        deferred_keys = []
        for i_deferred in range(deferred):
            key = keys[i_deferred]
            deferred_keys.append(key._pb)
            rsp_pb._pb.deferred.append(key._pb)

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
        ds_api = self._make_one(client)
        request = {
            "project_id": project,
            "keys": keys,
            "read_options": read_options,
        }
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.lookup(request=request, **kwargs)

        self.assertEqual(response, rsp_pb._pb)

        self.assertEqual([found.entity.key for found in response.found], found_keys)
        self.assertEqual(
            [missing.entity.key for missing in response.missing], missing_keys
        )
        self.assertEqual(list(response.deferred), deferred_keys)

        uri = _build_expected_url(client._base_url, project, "lookup")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.LookupRequest(), retry=retry, timeout=timeout,
        )
        self.assertEqual(list(request.keys), [key_pb1._pb, key_pb2._pb])
        self.assertEqual(request.read_options, read_options._pb)

    def test_lookup_multiple_keys_w_empty_response(self):
        self._lookup_multiple_helper()

    def test_lookup_multiple_keys_w_retry(self):
        retry = mock.MagicMock()
        self._lookup_multiple_helper(retry=retry)

    def test_lookup_multiple_keys_w_timeout(self):
        timeout = 5.0
        self._lookup_multiple_helper(timeout=timeout)

    def test_lookup_multiple_keys_w_found(self):
        self._lookup_multiple_helper(found=2)

    def test_lookup_multiple_keys_w_missing(self):
        self._lookup_multiple_helper(missing=2)

    def test_lookup_multiple_keys_w_deferred(self):
        self._lookup_multiple_helper(deferred=2)

    def _run_query_helper(
        self,
        read_consistency=None,
        transaction=None,
        namespace=None,
        found=0,
        retry=None,
        timeout=None,
    ):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2
        from google.cloud.datastore_v1.types import entity as entity_pb2
        from google.cloud.datastore_v1.types import query as query_pb2

        project = "PROJECT"
        kind = "Nonesuch"
        query_pb = self._make_query_pb(kind)

        partition_kw = {"project_id": project}
        if namespace is not None:
            partition_kw["namespace_id"] = namespace

        partition_id = entity_pb2.PartitionId(**partition_kw)

        options_kw = {}
        if read_consistency is not None:
            options_kw["read_consistency"] = read_consistency
        if transaction is not None:
            options_kw["transaction"] = transaction
        read_options = datastore_pb2.ReadOptions(**options_kw)

        cursor = b"\x00"
        batch_kw = {
            "entity_result_type": query_pb2.EntityResult.ResultType.FULL,
            "end_cursor": cursor,
            "more_results": query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS,
        }
        if found:
            batch_kw["entity_results"] = [
                query_pb2.EntityResult(entity=entity_pb2.Entity())
            ] * found
        rsp_pb = datastore_pb2.RunQueryResponse(
            batch=query_pb2.QueryResultBatch(**batch_kw)
        )

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
        ds_api = self._make_one(client)
        request = {
            "project_id": project,
            "partition_id": partition_id,
            "read_options": read_options,
            "query": query_pb,
        }
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.run_query(request=request, **kwargs)

        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "runQuery")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.RunQueryRequest(), retry=retry, timeout=timeout,
        )
        self.assertEqual(request.partition_id, partition_id._pb)
        self.assertEqual(request.query, query_pb._pb)
        self.assertEqual(request.read_options, read_options._pb)

    def test_run_query_simple(self):
        self._run_query_helper()

    def test_run_query_w_retry(self):
        retry = mock.MagicMock()
        self._run_query_helper(retry=retry)

    def test_run_query_w_timeout(self):
        timeout = 5.0
        self._run_query_helper(timeout=timeout)

    def test_run_query_w_read_consistency(self):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        read_consistency = datastore_pb2.ReadOptions.ReadConsistency.EVENTUAL
        self._run_query_helper(read_consistency=read_consistency)

    def test_run_query_w_transaction(self):
        transaction = b"TRANSACTION"
        self._run_query_helper(transaction=transaction)

    def test_run_query_w_namespace_nonempty_result(self):
        namespace = "NS"
        self._run_query_helper(namespace=namespace, found=1)

    def _begin_transaction_helper(self, options=None, retry=None, timeout=None):
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
        request = {"project_id": project}

        if options is not None:
            request["transaction_options"] = options

        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.begin_transaction(request=request, **kwargs)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "beginTransaction")
        request = _verify_protobuf_call(
            http,
            uri,
            datastore_pb2.BeginTransactionRequest(),
            retry=retry,
            timeout=timeout,
        )

    def test_begin_transaction_wo_options(self):
        self._begin_transaction_helper()

    def test_begin_transaction_w_options(self):
        from google.cloud.datastore_v1.types import TransactionOptions

        read_only = TransactionOptions.ReadOnly._meta.pb()
        options = TransactionOptions(read_only=read_only)
        self._begin_transaction_helper(options=options)

    def test_begin_transaction_w_retry(self):
        retry = mock.MagicMock()
        self._begin_transaction_helper(retry=retry)

    def test_begin_transaction_w_timeout(self):
        timeout = 5.0
        self._begin_transaction_helper(timeout=timeout)

    def _commit_helper(self, transaction=None, retry=None, timeout=None):
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

        rq_class = datastore_pb2.CommitRequest
        ds_api = self._make_one(client)

        request = {"project_id": project, "mutations": [mutation]}

        if transaction is not None:
            request["transaction"] = transaction
            mode = request["mode"] = rq_class.Mode.TRANSACTIONAL
        else:
            mode = request["mode"] = rq_class.Mode.NON_TRANSACTIONAL

        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        result = ds_api.commit(request=request, **kwargs)

        self.assertEqual(result, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "commit")
        request = _verify_protobuf_call(
            http, uri, rq_class(), retry=retry, timeout=timeout,
        )
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, mode)

        if transaction is not None:
            self.assertEqual(request.transaction, transaction)
        else:
            self.assertEqual(request.transaction, b"")

    def test_commit_wo_transaction(self):
        self._commit_helper()

    def test_commit_w_transaction(self):
        transaction = b"xact"

        self._commit_helper(transaction=transaction)

    def test_commit_w_retry(self):
        retry = mock.MagicMock()
        self._commit_helper(retry=retry)

    def test_commit_w_timeout(self):
        timeout = 5.0
        self._commit_helper(timeout=timeout)

    def _rollback_helper(self, retry=None, timeout=None):
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
        request = {"project_id": project, "transaction": transaction}
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.rollback(request=request, **kwargs)

        # Check the result and verify the callers.
        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "rollback")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.RollbackRequest(), retry=retry, timeout=timeout,
        )
        self.assertEqual(request.transaction, transaction)

    def test_rollback_ok(self):
        self._rollback_helper()

    def test_rollback_w_retry(self):
        retry = mock.MagicMock()
        self._rollback_helper(retry=retry)

    def test_rollback_w_timeout(self):
        timeout = 5.0
        self._rollback_helper(timeout=timeout)

    def _allocate_ids_helper(self, count=0, retry=None, timeout=None):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        before_key_pbs = []
        after_key_pbs = []
        rsp_pb = datastore_pb2.AllocateIdsResponse()

        for i_count in range(count):
            requested = _make_key_pb(project, id_=None)
            before_key_pbs.append(requested)
            allocated = _make_key_pb(project, id_=i_count)
            after_key_pbs.append(allocated)
            rsp_pb._pb.keys.add().CopyFrom(allocated._pb)

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
        ds_api = self._make_one(client)

        request = {"project_id": project, "keys": before_key_pbs}
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.allocate_ids(request=request, **kwargs)

        self.assertEqual(response, rsp_pb._pb)
        self.assertEqual(list(response.keys), [i._pb for i in after_key_pbs])

        uri = _build_expected_url(client._base_url, project, "allocateIds")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.AllocateIdsRequest(), retry=retry, timeout=timeout,
        )
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)

    def test_allocate_ids_empty(self):
        self._allocate_ids_helper()

    def test_allocate_ids_non_empty(self):
        self._allocate_ids_helper(count=2)

    def test_allocate_ids_w_retry(self):
        retry = mock.MagicMock()
        self._allocate_ids_helper(retry=retry)

    def test_allocate_ids_w_timeout(self):
        timeout = 5.0
        self._allocate_ids_helper(timeout=timeout)

    def _reserve_ids_helper(self, count=0, retry=None, timeout=None):
        from google.cloud.datastore_v1.types import datastore as datastore_pb2

        project = "PROJECT"
        before_key_pbs = []
        rsp_pb = datastore_pb2.ReserveIdsResponse()

        for i_count in range(count):
            requested = _make_key_pb(project, id_=i_count)
            before_key_pbs.append(requested)

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
        ds_api = self._make_one(client)

        request = {"project_id": project, "keys": before_key_pbs}
        kwargs = _make_retry_timeout_kwargs(retry, timeout, http)

        response = ds_api.reserve_ids(request=request, **kwargs)

        self.assertEqual(response, rsp_pb._pb)

        uri = _build_expected_url(client._base_url, project, "reserveIds")
        request = _verify_protobuf_call(
            http, uri, datastore_pb2.AllocateIdsRequest(), retry=retry, timeout=timeout,
        )
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)

    def test_reserve_ids_empty(self):
        self._reserve_ids_helper()

    def test_reserve_ids_non_empty(self):
        self._reserve_ids_helper(count=2)

    def test_reserve_ids_w_retry(self):
        retry = mock.MagicMock()
        self._reserve_ids_helper(retry=retry)

    def test_reserve_ids_w_timeout(self):
        timeout = 5.0
        self._reserve_ids_helper(timeout=timeout)


def _make_response(status=client.OK, content=b"", headers={}):
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


def _verify_protobuf_call(http, expected_url, pb, retry=None, timeout=None):
    from google.cloud import _http as connection_module

    expected_headers = {
        "Content-Type": "application/x-protobuf",
        "User-Agent": _USER_AGENT,
        connection_module.CLIENT_INFO_HEADER: _USER_AGENT,
    }

    if retry is not None:
        retry.assert_called_once_with(http.request)

    if timeout is not None:
        http.request.assert_called_once_with(
            method="POST",
            url=expected_url,
            headers=expected_headers,
            data=mock.ANY,
            timeout=timeout,
        )
    else:
        http.request.assert_called_once_with(
            method="POST", url=expected_url, headers=expected_headers, data=mock.ANY
        )

    data = http.request.mock_calls[0][2]["data"]
    pb._pb.ParseFromString(data)
    return pb


def _make_retry_timeout_kwargs(retry, timeout, http=None):
    kwargs = {}

    if retry is not None:
        kwargs["retry"] = retry
        if http is not None:
            retry.return_value = http.request

    if timeout is not None:
        kwargs["timeout"] = timeout

    return kwargs
