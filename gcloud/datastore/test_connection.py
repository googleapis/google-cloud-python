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

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _verifyProtobufCall(self, called_with, URI, conn):
        self.assertEqual(called_with['uri'], URI)
        self.assertEqual(called_with['method'], 'POST')
        self.assertEqual(called_with['headers']['Content-Type'],
                         'application/x-protobuf')
        self.assertEqual(called_with['headers']['User-Agent'],
                         conn.USER_AGENT)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        creds = object()
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
            conn.API_BASE_URL,
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
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        DATA = 'DATA'
        conn = self._makeOne()
        conn._http = Http({'status': '400'}, 'Bad Request')
        with self.assertRaises(Exception) as e:
            conn._request(DATASET_ID, METHOD, DATA)
        self.assertEqual(str(e.exception),
                         'Request failed. Error was: Bad Request')

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
            conn.API_BASE_URL,
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
        klass = self._getTargetClass()
        URI = '/'.join([
            klass.API_BASE_URL,
            'datastore',
            klass.API_VERSION,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        self.assertEqual(klass.build_api_url(DATASET_ID, METHOD), URI)

    def test_build_api_url_w_explicit_base_version(self):
        BASE = 'http://example.com/'
        VER = '3.1415926'
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        klass = self._getTargetClass()
        URI = '/'.join([
            BASE,
            'datastore',
            VER,
            'datasets',
            DATASET_ID,
            METHOD,
        ])
        self.assertEqual(klass.build_api_url(DATASET_ID, METHOD, BASE, VER),
                         URI)

    def test_transaction_getter_unset(self):
        conn = self._makeOne()
        self.assertTrue(conn.transaction() is None)

    def test_transaction_setter(self):
        xact = object()
        conn = self._makeOne()
        self.assertTrue(conn.transaction(xact) is conn)
        self.assertTrue(conn.transaction() is xact)

    def test_mutation_wo_transaction(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore.connection import datastore_pb

        class Mutation(object):
            pass
        conn = self._makeOne()
        with _Monkey(datastore_pb, Mutation=Mutation):
            found = conn.mutation()
        self.assertTrue(isinstance(found, Mutation))

    def test_mutation_w_transaction(self):

        class Mutation(object):
            pass

        class Xact(object):
            def mutation(self):
                return Mutation()
        conn = self._makeOne()
        conn.transaction(Xact())
        found = conn.mutation()
        self.assertTrue(isinstance(found, Mutation))

    def test_dataset(self):
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        dataset = conn.dataset(DATASET_ID)
        self.assertTrue(dataset.connection() is conn)
        self.assertEqual(dataset.id(), DATASET_ID)

    def test_lookup_single_key_empty_response(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, key_pb), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], key_pb)

    def test_lookup_single_key_empty_response_w_eventual(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, key_pb, eventual=True), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], key_pb)
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb.ReadOptions.EVENTUAL)
        self.assertEqual(request.read_options.transaction, '')

    def test_lookup_single_key_empty_response_w_eventual_and_transaction(self):
        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        key_pb = self._make_key_pb(DATASET_ID)
        conn = self._makeOne()
        conn.transaction(Transaction(TRANSACTION))
        self.assertRaises(
            ValueError, conn.lookup, DATASET_ID, key_pb, eventual=True)

    def test_lookup_single_key_empty_response_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        conn.transaction(Transaction(TRANSACTION))
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, key_pb), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], key_pb)
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_lookup_single_key_nonempty_response(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.LookupResponse()
        entity = datastore_pb.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        found = conn.lookup(DATASET_ID, key_pb)
        self.assertEqual(found.key.path_element[0].kind, 'Kind')
        self.assertEqual(found.key.path_element[0].id, 1234)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], key_pb)

    def test_lookup_multiple_keys_empty_response(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, [key_pb1, key_pb2]), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        self.assertEqual(keys[0], key_pb1)
        self.assertEqual(keys[1], key_pb2)

    def test_lookup_multiple_keys_w_missing(self):
        from gcloud.datastore.connection import datastore_pb

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
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        missing = []
        result = conn.lookup(DATASET_ID, [key_pb1, key_pb2], missing=missing)
        self.assertEqual(result, [])
        self.assertEqual([missed.key for missed in missing],
                         [key_pb1, key_pb2])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        self.assertEqual(keys[0], key_pb1)
        self.assertEqual(keys[1], key_pb2)

    def test_lookup_multiple_keys_w_missing_non_empty(self):
        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        conn = self._makeOne()
        missing = ['this', 'list', 'is', 'not', 'empty']
        self.assertRaises(
            ValueError,
            conn.lookup, DATASET_ID, [key_pb1, key_pb2], missing=missing)

    def test_lookup_multiple_keys_w_deferred(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb = datastore_pb.LookupResponse()
        rsp_pb.deferred.add().CopyFrom(key_pb1)
        rsp_pb.deferred.add().CopyFrom(key_pb2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        deferred = []
        result = conn.lookup(DATASET_ID, [key_pb1, key_pb2], deferred=deferred)
        self.assertEqual(result, [])
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
        self.assertEqual(keys[0], key_pb1)
        self.assertEqual(keys[1], key_pb2)

    def test_lookup_multiple_keys_w_deferred_non_empty(self):
        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        conn = self._makeOne()
        deferred = ['this', 'list', 'is', 'not', 'empty']
        self.assertRaises(
            ValueError,
            conn.lookup, DATASET_ID, [key_pb1, key_pb2], deferred=deferred)

    def test_lookup_multiple_keys_w_deferred_from_backend_but_not_passed(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb1 = self._make_key_pb(DATASET_ID)
        key_pb2 = self._make_key_pb(DATASET_ID, id=2345)
        rsp_pb1 = datastore_pb.LookupResponse()
        entity1 = datastore_pb.Entity()
        entity1.key.CopyFrom(key_pb1)
        rsp_pb1.found.add(entity=entity1)
        rsp_pb1.deferred.add().CopyFrom(key_pb2)
        rsp_pb2 = datastore_pb.LookupResponse()
        entity2 = datastore_pb.Entity()
        entity2.key.CopyFrom(key_pb2)
        rsp_pb2.found.add(entity=entity2)
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'lookup',
        ])
        http = conn._http = HttpMultiple(
            ({'status': '200'}, rsp_pb1.SerializeToString()),
            ({'status': '200'}, rsp_pb2.SerializeToString()),
            )
        found = conn.lookup(DATASET_ID, [key_pb1, key_pb2])
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0].key.path_element[0].kind, 'Kind')
        self.assertEqual(found[0].key.path_element[0].id, 1234)
        self.assertEqual(found[1].key.path_element[0].kind, 'Kind')
        self.assertEqual(found[1].key.path_element[0].id, 2345)
        cw = http._called_with
        rq_class = datastore_pb.LookupRequest
        request = rq_class()
        self.assertEqual(len(cw), 2)

        self._verifyProtobufCall(cw[0], URI, conn)
        request.ParseFromString(cw[0]['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 2)
        self.assertEqual(keys[0], key_pb1)
        self.assertEqual(keys[1], key_pb2)

        self._verifyProtobufCall(cw[1], URI, conn)
        request.ParseFromString(cw[1]['body'])
        keys = list(request.key)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], key_pb2)

    def test_run_query_w_eventual_no_transaction(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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
        self.assertEqual(request.read_options.transaction, '')

    def test_run_query_wo_eventual_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = 'TRANSACTION'
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        conn.transaction(Transaction(TRANSACTION))
        URI = '/'.join([
            conn.API_BASE_URL,
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
        self.assertEqual(request.read_options.read_consistency,
                         datastore_pb.ReadOptions.DEFAULT)
        self.assertEqual(request.read_options.transaction, TRANSACTION)

    def test_run_query_w_eventual_and_transaction(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        TRANSACTION = 'TRANSACTION'
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        conn.transaction(Transaction(TRANSACTION))
        self.assertRaises(
            ValueError, conn.run_query, DATASET_ID, q_pb, eventual=True)

    def test_run_query_wo_namespace_empty_result(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query

        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        CURSOR = b'\x00'
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.end_cursor = CURSOR
        no_more = datastore_pb.QueryResultBatch.NO_MORE_RESULTS
        rsp_pb.batch.more_results = no_more
        rsp_pb.batch.entity_result_type = datastore_pb.EntityResult.FULL
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query

        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        entity = datastore_pb.Entity()
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        rsp_pb.batch.entity_result.add(entity=entity)
        rsp_pb.batch.entity_result_type = 1  # FULL
        rsp_pb.batch.more_results = 3  # NO_MORE_RESULTS
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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

    def test_begin_transaction_w_existing_transaction(self):
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        conn.transaction(object())
        self.assertRaises(ValueError, conn.begin_transaction, DATASET_ID)

    def test_begin_transaction_default_serialize(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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
        from gcloud.datastore.connection import datastore_pb

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
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.commit(DATASET_ID, mutation)
        self.assertEqual(result.index_updates, 0)
        self.assertEqual(list(result.insert_auto_id_key), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, '')
        self.assertEqual(request.mutation, mutation)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_commit_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb

        class Xact(object):
            def id(self):
                return 'xact'
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
        conn.transaction(Xact())
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.commit(DATASET_ID, mutation)
        self.assertEqual(result.index_updates, 0)
        self.assertEqual(list(result.insert_auto_id_key), [])
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, 'xact')
        self.assertEqual(request.mutation, mutation)
        self.assertEqual(request.mode, rq_class.TRANSACTIONAL)

    def test_rollback_wo_existing_transaction(self):
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        self.assertRaises(ValueError,
                          conn.rollback, DATASET_ID)

    def test_rollback_w_existing_transaction_no_id(self):

        class Xact(object):

            def id(self):
                return None
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        conn.transaction(Xact())
        self.assertRaises(ValueError,
                          conn.rollback, DATASET_ID)

    def test_rollback_ok(self):
        from gcloud.datastore.connection import datastore_pb
        DATASET_ID = 'DATASET'
        TRANSACTION = 'xact'

        class Xact(object):

            def id(self):
                return TRANSACTION
        rsp_pb = datastore_pb.RollbackResponse()
        conn = self._makeOne()
        conn.transaction(Xact())
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'rollback',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.rollback(DATASET_ID), None)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.RollbackRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, TRANSACTION)

    def test_allocate_ids_empty(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        rsp_pb = datastore_pb.AllocateIdsResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
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
        from gcloud.datastore.connection import datastore_pb

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
            conn.API_BASE_URL,
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
        self.assertEqual(list(request.key), before_key_pbs)

    def test_save_entity_wo_transaction_w_upsert(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.save_entity(DATASET_ID, key_pb, {'foo': u'Foo'})
        self.assertEqual(result, (False, None))
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, '')
        mutation = request.mutation
        self.assertEqual(len(mutation.insert_auto_id), 0)
        upserts = list(mutation.upsert)
        self.assertEqual(len(upserts), 1)
        upsert = upserts[0]
        self.assertEqual(upsert.key, key_pb)
        props = list(upsert.property)
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0].name, 'foo')
        self.assertEqual(props[0].value.string_value, u'Foo')
        self.assertEqual(props[0].value.indexed, True)
        self.assertEqual(len(mutation.delete), 0)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_save_entity_w_exclude_from_indexes(self):
        from gcloud.datastore.connection import datastore_pb
        import operator

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.save_entity(DATASET_ID, key_pb,
                                  {'foo': u'Foo', 'bar': [u'bar1', u'bar2']},
                                  exclude_from_indexes=['foo', 'bar'])
        self.assertEqual(result, (False, None))
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, '')
        mutation = request.mutation
        self.assertEqual(len(mutation.insert_auto_id), 0)
        upserts = list(mutation.upsert)
        self.assertEqual(len(upserts), 1)
        upsert = upserts[0]
        self.assertEqual(upsert.key, key_pb)
        props = sorted(upsert.property,
                       key=operator.attrgetter('name'),
                       reverse=True)
        self.assertEqual(len(props), 2)
        self.assertEqual(props[0].name, 'foo')
        self.assertEqual(props[0].value.string_value, u'Foo')
        self.assertEqual(props[0].value.indexed, False)
        self.assertEqual(props[1].name, 'bar')
        self.assertEqual(props[1].value.list_value[0].string_value, 'bar1')
        self.assertEqual(props[1].value.list_value[1].string_value, 'bar2')
        self.assertEqual(props[1].value.HasField('indexed'), False)
        self.assertEqual(props[1].value.list_value[0].indexed, False)
        self.assertEqual(props[1].value.list_value[1].indexed, False)
        self.assertEqual(len(mutation.delete), 0)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_save_entity_wo_transaction_w_auto_id(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID, id=None)
        updated_key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        mr_pb = rsp_pb.mutation_result
        mr_pb.index_updates = 0
        iaik_pb = mr_pb.insert_auto_id_key.add()
        iaik_pb.CopyFrom(updated_key_pb)
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.save_entity(DATASET_ID, key_pb, {'foo': u'Foo'})
        self.assertEqual(result, (True, 1234))
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, '')
        mutation = request.mutation
        inserts = list(mutation.insert_auto_id)
        insert = inserts[0]
        self.assertEqual(insert.key, key_pb)
        props = list(insert.property)
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0].name, 'foo')
        self.assertEqual(props[0].value.string_value, u'Foo')
        self.assertEqual(len(inserts), 1)
        upserts = list(mutation.upsert)
        self.assertEqual(len(upserts), 0)
        self.assertEqual(len(mutation.delete), 0)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_save_entity_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb

        mutation = datastore_pb.Mutation()

        class Xact(object):
            def mutation(self):
                return mutation
        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        conn.transaction(Xact())
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.save_entity(DATASET_ID, key_pb, {'foo': u'Foo'})
        self.assertEqual(result, (False, None))
        self.assertEqual(http._called_with, None)
        mutation = conn.mutation()
        self.assertEqual(len(mutation.upsert), 1)

    def test_save_entity_w_transaction_nested_entity(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.entity import Entity

        mutation = datastore_pb.Mutation()

        class Xact(object):
            def mutation(self):
                return mutation
        DATASET_ID = 'DATASET'
        nested = Entity()
        nested['bar'] = u'Bar'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        conn.transaction(Xact())
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.save_entity(DATASET_ID, key_pb, {'foo': nested})
        self.assertEqual(result, (False, None))
        self.assertEqual(http._called_with, None)
        mutation = conn.mutation()
        self.assertEqual(len(mutation.upsert), 1)

    def test_delete_entities_wo_transaction(self):
        from gcloud.datastore.connection import datastore_pb

        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            'datastore',
            conn.API_VERSION,
            'datasets',
            DATASET_ID,
            'commit',
        ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.delete_entities(DATASET_ID, [key_pb])
        self.assertEqual(result, True)
        cw = http._called_with
        self._verifyProtobufCall(cw, URI, conn)
        rq_class = datastore_pb.CommitRequest
        request = rq_class()
        request.ParseFromString(cw['body'])
        self.assertEqual(request.transaction, '')
        mutation = request.mutation
        self.assertEqual(len(mutation.insert_auto_id), 0)
        self.assertEqual(len(mutation.upsert), 0)
        deletes = list(mutation.delete)
        self.assertEqual(len(deletes), 1)
        delete = deletes[0]
        self.assertEqual(delete, key_pb)
        self.assertEqual(request.mode, rq_class.NON_TRANSACTIONAL)

    def test_delete_entities_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb

        mutation = datastore_pb.Mutation()

        class Xact(object):
            def mutation(self):
                return mutation
        DATASET_ID = 'DATASET'
        key_pb = self._make_key_pb(DATASET_ID)
        rsp_pb = datastore_pb.CommitResponse()
        conn = self._makeOne()
        conn.transaction(Xact())
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.delete_entities(DATASET_ID, [key_pb])
        self.assertEqual(result, True)
        self.assertEqual(http._called_with, None)
        mutation = conn.mutation()
        self.assertEqual(len(mutation.delete), 1)


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        self._headers = headers
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._headers, self._content


class HttpMultiple(object):

    def __init__(self, *responses):
        self._called_with = []
        self._responses = list(responses)

    def request(self, **kw):
        self._called_with.append(kw)
        result, self._responses = self._responses[0], self._responses[1:]
        return result


class Transaction(object):

    def __init__(self, id):
        self._id = id

    def id(self):
        return self._id
