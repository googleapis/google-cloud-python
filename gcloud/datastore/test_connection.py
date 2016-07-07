# Copyright 2014 Google Inc. All rights reserved.
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

import unittest2


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.connection import Connection

        return Connection

    def _make_key_pb(self, project, id_=1234):
        from gcloud.datastore.key import Key
        path_args = ('Kind',)
        if id_ is not None:
            path_args += (id_,)
        return Key(*path_args, project=project).to_protobuf()

    def _make_query_pb(self, kind):
        from gcloud.datastore._generated import query_pb2
        pb = query_pb2.Query()
        pb.kind.add().name = kind
        return pb

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _verifyProtobufCall(self, called_with, URI, conn):
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)

    def test_default_url(self):
        klass = self._getTargetClass()
        conn = self._makeOne()
        self.assertEqual(conn.api_base_url, klass.API_BASE_URL)

    def test_custom_url_from_env(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.connection import API_BASE_URL
        from gcloud.environment_vars import GCD_HOST

        HOST = 'CURR_HOST'
        fake_environ = {GCD_HOST: HOST}

        with _Monkey(os, environ=fake_environ):
            conn = self._makeOne()

        self.assertNotEqual(conn.api_base_url, API_BASE_URL)
        self.assertEqual(conn.api_base_url, HOST + '/datastore')

    def test_custom_url_from_constructor(self):
        from gcloud.connection import API_BASE_URL

        HOST = object()
        conn = self._makeOne(api_base_url=HOST)
        self.assertNotEqual(conn.api_base_url, API_BASE_URL)
        self.assertEqual(conn.api_base_url, HOST)

    def test_custom_url_constructor_and_env(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.connection import API_BASE_URL
        from gcloud.environment_vars import GCD_HOST

        HOST1 = object()
        HOST2 = object()
        fake_environ = {GCD_HOST: HOST1}

        with _Monkey(os, environ=fake_environ):
            conn = self._makeOne(api_base_url=HOST2)

        self.assertNotEqual(conn.api_base_url, API_BASE_URL)
        self.assertNotEqual(conn.api_base_url, HOST1)
        self.assertEqual(conn.api_base_url, HOST2)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        class Creds(object):

            def create_scoped_required(self):
                return False

        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.credentials is creds)

    def test_http_w_existing(self):
        conn = self._makeOne()
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        import httplib2

        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, httplib2.Http))

    def test_http_w_creds(self):
        import httplib2

        authorized = object()

        class Creds(object):

            def authorize(self, http):
                self._called_with = http
                return authorized

            def create_scoped_required(self):
                return False

        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, httplib2.Http))

    def test__request_w_200(self):
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = b'DATA'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        http = conn._http = Http({'status': '200'}, 'CONTENT')
        self.assertEqual(conn._request(PROJECT, METHOD, DATA), 'CONTENT')
        self._verifyProtobufCall(http._called_with, URI, conn)
        self.assertEqual(http._called_with['body'], DATA)

    def test__request_not_200(self):
        from gcloud.exceptions import BadRequest
        from google.rpc import status_pb2

        error = status_pb2.Status()
        error.message = 'Entity value is indexed.'
        error.code = 9  # FAILED_PRECONDITION

        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        DATA = 'DATA'
        conn = self._makeOne()
        conn._http = Http({'status': '400'}, error.SerializeToString())
        with self.assertRaises(BadRequest) as e:
            conn._request(PROJECT, METHOD, DATA)
        expected_message = '400 Entity value is indexed.'
        self.assertEqual(str(e.exception), expected_message)

    def test__rpc(self):

        class ReqPB(object):

            def SerializeToString(self):
                return REQPB

        class RspPB(object):

            def __init__(self, pb):
                self._pb = pb

            @classmethod
            def FromString(cls, pb):
                return cls(pb)

        REQPB = b'REQPB'
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        http = conn._http = Http({'status': '200'}, 'CONTENT')
        response = conn._rpc(PROJECT, METHOD, ReqPB(), RspPB)
        self.assertTrue(isinstance(response, RspPB))
        self.assertEqual(response._pb, 'CONTENT')
        self._verifyProtobufCall(http._called_with, URI, conn)
        self.assertEqual(http._called_with['body'], REQPB)

    def test_build_api_url_w_default_base_version(self):
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        self.assertEqual(conn.build_api_url(PROJECT, METHOD), URI)

    def test_build_api_url_w_explicit_base_version(self):
        BASE = 'http://example.com/'
        VER = '3.1415926'
        PROJECT = 'PROJECT'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            BASE,
            VER,
            'projects',
            PROJECT + ':' + METHOD,
        ])
        self.assertEqual(conn.build_api_url(PROJECT, METHOD, BASE, VER),
                         URI)

    def test_lookup_single_key_empty_response(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_single_key_empty_response_w_eventual(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb],
                                               eventual=True)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb2.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_lookup_single_key_empty_response_w_eventual_and_transaction(self):
        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        key_pb = self._make_key_pb(PROJECT)
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.lookup, PROJECT, key_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb],
                                               transaction_id=TRANSACTION)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_lookup_single_key_nonempty_response(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import entity_pb2

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.LookupResponse()
        entity = entity_pb2.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        (found,), missing, deferred = conn.lookup(PROJECT, [key_pb])
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        self.assertEqual(found.key.path[0].kind, 'Kind')
        self.assertEqual(found.key.path[0].id, 1234)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(key_pb, keys[0])

    def test_lookup_multiple_keys_empty_response(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_missing(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        er_1 = rsp_pb.missing.add()
        er_1.entity.key.CopyFrom(key_pb1)
        er_2 = rsp_pb.missing.add()
        er_2.entity.key.CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(result, [])
        self.assertEqual(len(deferred), 0)
        self.assertEqual([missed.key for missed in missing],
                         [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_lookup_multiple_keys_w_deferred(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        key_pb1 = self._make_key_pb(PROJECT)
        key_pb2 = self._make_key_pb(PROJECT, id_=2345)
        rsp_pb = datastore_pb2.LookupResponse()
        rsp_pb.deferred.add().CopyFrom(key_pb1)
        rsp_pb.deferred.add().CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(PROJECT, [key_pb1, key_pb2])
        self.assertEqual(result, [])
        self.assertEqual(len(missing), 0)
        self.assertEqual([def_key for def_key in deferred], [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(cw['headers']['User-Agent'], conn.USER_AGENT)
        rq_class = datastore_pb2.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.keys)
        self.assertEqual(len(keys), 2)
        self.assertEqual(key_pb1, keys[0])
        self.assertEqual(key_pb2, keys[1])

    def test_run_query_w_eventual_no_transaction(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(PROJECT, q_pb,
                                                 eventual=True)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb2.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_run_query_wo_eventual_w_transaction(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = b'TRANSACTION'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(
            PROJECT, q_pb, transaction_id=TRANSACTION)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(
            request.read_options.read_consistency,
            datastore_pb2.ReadOptions.READ_CONSISTENCY_UNSPECIFIED)
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_run_query_w_eventual_and_transaction(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = b'TRANSACTION'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.run_query, PROJECT, q_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_run_query_wo_namespace_empty_result(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import query_pb2

        PROJECT = 'PROJECT'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = query_pb2.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(PROJECT, q_pb)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, '')
        self.assertEqual(request.query, q_pb)

    def test_run_query_w_namespace_nonempty_result(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import entity_pb2

        PROJECT = 'PROJECT'
        KIND = 'Kind'
        entity = entity_pb2.Entity()
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb2.RunQueryResponse()
        rsp_pb.batch.entity_results.add(entity=entity)
        rsp_pb.batch.entity_result_type = 1  # FULL
        rsp_pb.batch.more_results = 3  # NO_MORE_RESULTS
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs = conn.run_query(PROJECT, q_pb, 'NS')[0]
        self.assertEqual(len(pbs), 1)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace_id, 'NS')
        self.assertEqual(request.query, q_pb)

    def test_begin_transaction(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        TRANSACTION = b'TRANSACTION'
        rsp_pb = datastore_pb2.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':beginTransaction',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(PROJECT), TRANSACTION)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.BeginTransactionRequest
        request = rq_class()
        request.ParseFromString(cw['body'])

    def test_commit_wo_transaction(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore import connection as MUT
        from gcloud.datastore.helpers import _new_value_pb

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())

        # Set up mock for parsing the response.
        expected_result = object()
        _parsed = []

        def mock_parse(response):
            _parsed.append(response)
            return expected_result

        with _Monkey(MUT, _parse_commit_response=mock_parse):
            result = conn.commit(PROJECT, req_pb, None)

        self.assertTrue(result is expected_result)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)
        self.assertEqual(_parsed, [rsp_pb])

    def test_commit_w_transaction(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore import connection as MUT
        from gcloud.datastore.helpers import _new_value_pb

        PROJECT = 'PROJECT'
        key_pb = self._make_key_pb(PROJECT)
        rsp_pb = datastore_pb2.CommitResponse()
        req_pb = datastore_pb2.CommitRequest()
        mutation = req_pb.mutations.add()
        insert = mutation.upsert
        insert.key.CopyFrom(key_pb)
        value_pb = _new_value_pb(insert, 'foo')
        value_pb.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())

        # Set up mock for parsing the response.
        expected_result = object()
        _parsed = []

        def mock_parse(response):
            _parsed.append(response)
            return expected_result

        with _Monkey(MUT, _parse_commit_response=mock_parse):
            result = conn.commit(PROJECT, req_pb, b'xact')

        self.assertTrue(result is expected_result)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'xact')
        self.assertEqual(list(request.mutations), [mutation])
        self.assertEqual(request.mode, rq_class.TRANSACTIONAL)
        self.assertEqual(_parsed, [rsp_pb])

    def test_rollback_ok(self):
        from gcloud.datastore._generated import datastore_pb2
        PROJECT = 'PROJECT'
        TRANSACTION = b'xact'

        rsp_pb = datastore_pb2.RollbackResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':rollback',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.rollback(PROJECT, TRANSACTION), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.RollbackRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, TRANSACTION)

    def test_allocate_ids_empty(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(PROJECT, []), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(list(request.keys), [])

    def test_allocate_ids_non_empty(self):
        from gcloud.datastore._generated import datastore_pb2

        PROJECT = 'PROJECT'
        before_key_pbs = [
            self._make_key_pb(PROJECT, id_=None),
            self._make_key_pb(PROJECT, id_=None),
            ]
        after_key_pbs = [
            self._make_key_pb(PROJECT),
            self._make_key_pb(PROJECT, id_=2345),
            ]
        rsp_pb = datastore_pb2.AllocateIdsResponse()
        rsp_pb.keys.add().CopyFrom(after_key_pbs[0])
        rsp_pb.keys.add().CopyFrom(after_key_pbs[1])
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            conn.API_VERSION,
            'projects',
            PROJECT + ':allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(PROJECT, before_key_pbs),
                         after_key_pbs)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb2.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(len(request.keys), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.keys):
            self.assertEqual(key_before, key_after)


class Test__parse_commit_response(unittest2.TestCase):

    def _callFUT(self, commit_response_pb):
        from gcloud.datastore.connection import _parse_commit_response
        return _parse_commit_response(commit_response_pb)

    def test_it(self):
        from gcloud.datastore._generated import datastore_pb2
        from gcloud.datastore._generated import entity_pb2

        index_updates = 1337
        keys = [
            entity_pb2.Key(
                path=[
                    entity_pb2.Key.PathElement(
                        kind='Foo',
                        id=1234,
                    ),
                ],
            ),
            entity_pb2.Key(
                path=[
                    entity_pb2.Key.PathElement(
                        kind='Bar',
                        name='baz',
                    ),
                ],
            ),
        ]
        response = datastore_pb2.CommitResponse(
            mutation_results=[
                datastore_pb2.MutationResult(key=key) for key in keys
            ],
            index_updates=index_updates,
        )
        result = self._callFUT(response)
        self.assertEqual(result, (index_updates, keys))


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content


class _PathElementProto(object):

    def __init__(self, _id):
        self.id = _id


class _KeyProto(object):

    def __init__(self, id_):
        self.path = [_PathElementProto(id_)]
