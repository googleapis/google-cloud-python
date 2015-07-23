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

    def _make_key_pb(self, dataset_id, id=1234):
        from gcloud.datastore.key import Key
        path_args = ('Kind',)
        if id is not None:
            path_args += (id,)
        return Key(*path_args, dataset_id=dataset_id).to_protobuf()

    def _make_query_pb(self, kind):
        from gcloud.datastore.connection import datastore_pb
        pb = datastore_pb.Query()
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
        from gcloud.connection import API_BASE_URL

        conn = self._makeOne()
        self.assertEqual(conn.api_base_url, API_BASE_URL)

    def test_custom_url_from_env(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.connection import API_BASE_URL
        from gcloud.datastore.connection import GCD_HOST

        HOST = object()
        fake_environ = {GCD_HOST: HOST}

        with _Monkey(os, getenv=fake_environ.get):
            conn = self._makeOne()

        self.assertNotEqual(conn.api_base_url, API_BASE_URL)
        self.assertEqual(conn.api_base_url, HOST)

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
        from gcloud.datastore.connection import GCD_HOST

        HOST1 = object()
        HOST2 = object()
        fake_environ = {GCD_HOST: HOST1}

        with _Monkey(os, getenv=fake_environ.get):
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
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        DATA = b'DATA'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        http = conn._http = Http({'status': '200'}, 'CONTENT')
        self.assertEqual(conn._request(DATASET_ID, METHOD, DATA), 'CONTENT')
        self._verifyProtobufCall(http._called_with, URI, conn)
        self.assertEqual(http._called_with['body'], DATA)

    def test__request_not_200(self):
        from gcloud.exceptions import BadRequest

        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        DATA = 'DATA'
        conn = self._makeOne()
        conn._http = Http({'status': '400'}, b'Entity value is indexed.')
        with self.assertRaises(BadRequest) as e:
            conn._request(DATASET_ID, METHOD, DATA)
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
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        http = conn._http = Http({'status': '200'}, 'CONTENT')
        response = conn._rpc(DATASET_ID, METHOD, ReqPB(), RspPB)
        self.assertTrue(isinstance(response, RspPB))
        self.assertEqual(response._pb, 'CONTENT')
        self._verifyProtobufCall(http._called_with, URI, conn)
        self.assertEqual(http._called_with['body'], REQPB)

    def test_build_api_url_w_default_base_version(self):
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        self.assertEqual(conn.build_api_url(DATASET_ID, METHOD), URI)

    def test_build_api_url_w_explicit_base_version(self):
        BASE = 'http://example.com/'
        VER = '3.1415926'
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([
            BASE,
            'datastore',
            VER,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        self.assertEqual(conn.build_api_url(DATASET_ID, METHOD, BASE, VER),
                         URI)

    def test_lookup_single_key_empty_response(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(DATASET_ID, [key_pb])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        _compare_key_pb_after_request(self, key_pb, keys[0])

    def test_lookup_single_key_empty_response_w_eventual(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(DATASET_ID, [key_pb],
                                               eventual=True)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        _compare_key_pb_after_request(self, key_pb, keys[0])
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_lookup_single_key_empty_response_w_eventual_and_transaction(self):
        DATASET_ID = 'DATASET'
        TRANSACTION = b'TRANSACTION'
        key_pb = self._make_key_pb(DATASET_ID)
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.lookup, DATASET_ID, key_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = b'TRANSACTION'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(DATASET_ID, [key_pb],
                                               transaction_id=TRANSACTION)
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        _compare_key_pb_after_request(self, key_pb, keys[0])
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_lookup_single_key_nonempty_response(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        entity = datastore_pb.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        (found,), missing, deferred = conn.lookup(DATASET_ID, [key_pb])
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        self.assertEqual(found.key.path_element[0].kind, 'Kind')
        self.assertEqual(found.key.path_element[0].id, 1234)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        _compare_key_pb_after_request(self, key_pb, keys[0])

    def test_lookup_multiple_keys_empty_response(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found, missing, deferred = conn.lookup(DATASET_ID, [key_pb1, key_pb2])
        self.assertEqual(len(found), 0)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(deferred), 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        _compare_key_pb_after_request(self, key_pb1, keys[0])
        _compare_key_pb_after_request(self, key_pb2, keys[1])

    def test_lookup_multiple_keys_w_missing(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb = datastore_pb.LookupResponse()
        er_1 = rsp_pb.missing.add()
        er_1.entity.key.CopyFrom(key_pb1)
        er_2 = rsp_pb.missing.add()
        er_2.entity.key.CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(DATASET_ID, [key_pb1, key_pb2])
        self.assertEqual(result, [])
        self.assertEqual(len(deferred), 0)
        self.assertEqual([missed.key for missed in missing],
                         [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        _compare_key_pb_after_request(self, key_pb1, keys[0])
        _compare_key_pb_after_request(self, key_pb2, keys[1])

    def test_lookup_multiple_keys_w_deferred(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb = datastore_pb.LookupResponse()
        rsp_pb.deferred.add().CopyFrom(key_pb1)
        rsp_pb.deferred.add().CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result, missing, deferred = conn.lookup(DATASET_ID, [key_pb1, key_pb2])
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
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        _compare_key_pb_after_request(self, key_pb1, keys[0])
        _compare_key_pb_after_request(self, key_pb2, keys[1])

    def test_run_query_w_eventual_no_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(DATASET_ID, q_pb,
                                                 eventual=True)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, b'')

    def test_run_query_wo_eventual_w_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = b'TRANSACTION'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(
            DATASET_ID, q_pb, transaction_id=TRANSACTION)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace, '')
        self.assertEqual(request.query, q_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb.ReadOptions.DEFAULT)
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_run_query_w_eventual_and_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = b'TRANSACTION'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        self.assertRaises(ValueError, conn.run_query, DATASET_ID, q_pb,
                          eventual=True, transaction_id=TRANSACTION)

    def test_run_query_wo_namespace_empty_result(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs, end, more, skipped = conn.run_query(DATASET_ID, q_pb)
        self.assertEqual(pbs, [])
        self.assertEqual(end, CURSOR)
        self.assertTrue(more)
        self.assertEqual(skipped, 0)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace, '')
        self.assertEqual(request.query, q_pb)

    def test_run_query_w_namespace_nonempty_result(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        entity = datastore_pb.Entity()
        q_pb = self._make_query_pb(KIND)
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.entity_result.add(entity=entity)
        rsp_pb.batch.entity_result_type = 1  # FULL
        rsp_pb.batch.more_results = 3  # NO_MORE_RESULTS
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'runQuery',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        pbs = conn.run_query(DATASET_ID, q_pb, 'NS')[0]
        self.assertEqual(len(pbs), 1)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RunQueryRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.partition_id.namespace, 'NS')
        self.assertEqual(request.query, q_pb)

    def test_begin_transaction_default_serialize(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = b'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'beginTransaction',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(DATASET_ID), TRANSACTION)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.BeginTransactionRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.isolation_level, rq_class.SNAPSHOT)

    def test_begin_transaction_explicit_serialize(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = b'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'beginTransaction',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(DATASET_ID, True), TRANSACTION)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.BeginTransactionRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.isolation_level, rq_class.SERIALIZABLE)

    def test_commit_wo_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        mutation = datastore_pb.Mutation()
        insert = mutation.upsert.add()
        insert.key.CopyFrom(key_pb)
        prop = insert.property.add()
        prop.name = 'foo'
        prop.value.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.commit(DATASET_ID, mutation, None)
        self.assertEqual(result.index_updates, 0)
        self.assertEqual(list(result.insert_auto_id_key), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'')
        self.assertEqual(request.mutation, mutation)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_commit_w_transaction(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        mutation = datastore_pb.Mutation()
        insert = mutation.upsert.add()
        insert.key.CopyFrom(key_pb)
        prop = insert.property.add()
        prop.name = 'foo'
        prop.value.string_value = u'Foo'
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.commit(DATASET_ID, mutation, b'xact')
        self.assertEqual(result.index_updates, 0)
        self.assertEqual(list(result.insert_auto_id_key), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, b'xact')
        self.assertEqual(request.mutation, mutation)
        self.assertEqual(request.mode, rq_class.TRANSACTIONAL)

    def test_rollback_ok(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        DATASET_ID = 'DATASET'
        TRANSACTION = b'xact'

        rsp_pb = datastore_pb.RollbackResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'rollback',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.rollback(DATASET_ID, TRANSACTION), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RollbackRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, TRANSACTION)

    def test_allocate_ids_empty(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        rsp_pb = datastore_pb.AllocateIdsResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(DATASET_ID, []), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(list(request.key), [])

    def test_allocate_ids_non_empty(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 'DATASET'
        before_key_pbs = [
            self._make_key_pb(DATASET_ID, id=None),
            self._make_key_pb(DATASET_ID, id=None),
            ]
        after_key_pbs = [
            self._make_key_pb(DATASET_ID),
            self._make_key_pb(DATASET_ID, id=2345),
            ]
        rsp_pb = datastore_pb.AllocateIdsResponse()
        rsp_pb.key.add().CopyFrom(after_key_pbs[0])
        rsp_pb.key.add().CopyFrom(after_key_pbs[1])
        conn = self._makeOne()
        URI = '/'.join([
            conn.api_base_url,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'allocateIds',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.allocate_ids(DATASET_ID, before_key_pbs),
                         after_key_pbs)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.AllocateIdsRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(len(request.key), len(before_key_pbs))
        for key_before, key_after in zip(before_key_pbs, request.key):
            _compare_key_pb_after_request(self, key_before, key_after)


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content


def _compare_key_pb_after_request(test, key_before, key_after):
    test.assertFalse(key_after.partition_id.HasField('dataset_id'))
    test.assertEqual(key_before.partition_id.namespace,
                     key_after.partition_id.namespace)
    test.assertEqual(len(key_before.path_element),
                     len(key_after.path_element))
    for elt1, elt2 in zip(key_before.path_element, key_after.path_element):
        test.assertEqual(elt1, elt2)


class _PathElementProto(object):

    def __init__(self, _id):
        self.id = _id


class _KeyProto(object):

    def __init__(self, id_):
        self.path_element = [_PathElementProto(id_)]
