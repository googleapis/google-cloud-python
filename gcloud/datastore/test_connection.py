import unittest2

class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

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
        from httplib2 import Http
        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, Http))

    def test_http_w_creds(self):
        from httplib2 import Http
        authorized = object()
        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, Http))

    def test__request_w_200(self):
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        DATA = b'DATA'
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        METHOD,
                       ])
        http = conn._http = Http({'status': '200'}, 'CONTENT')
        self.assertEqual(conn._request(DATASET_ID, METHOD, DATA), 'CONTENT')
        self.assertEqual(http._called_with,
                         {'uri': URI,
                          'method': 'POST',
                          'headers':
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '4',
                            },
                          'body': DATA,
                         })

    def test__request_not_200(self):
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        DATA = 'DATA'
        conn = self._makeOne()
        http = conn._http = Http({'status': '400'}, 'Bad Request')
        with self.assertRaises(Exception) as e:
            conn._request(DATASET_ID, METHOD, DATA)
        self.assertEqual(str(e.exception),
                         'Request failed. Error was: Bad Request')

    def test__rpc(self):

        class ReqPB(object):
            def SerializeToString(self):
                return b'REQPB'

        class RspPB(object):
            def __init__(self, pb):
                self._pb = pb
            @classmethod
            def FromString(cls, pb):
                return cls(pb)

        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
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
        self.assertEqual(http._called_with,
                         {'uri': URI,
                          'method': 'POST',
                          'headers':
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '5',
                            },
                          'body': b'REQPB',
                         })

    def test_build_api_url_w_default_base_version(self):
        DATASET_ID = 'DATASET'
        METHOD = 'METHOD'
        klass = self._getTargetClass()
        URI = '/'.join([klass.API_BASE_URL,
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
        URI = '/'.join([BASE,
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

    def test_begin_transaction_w_existing_transaction(self):
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        conn.transaction(object())
        self.assertRaises(ValueError, conn.begin_transaction, DATASET_ID)

    def test_begin_transaction_default_serialize(self):
        from gcloud.datastore.connection import datastore_pb
        xact = object()
        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'beginTransaction',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(DATASET_ID), TRANSACTION)
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '2',
                            })
        self.assertEqual(cw['body'], b'\x08\x00') # SNAPSHOT

    def test_begin_transaction_explicit_serialize(self):
        from gcloud.datastore.connection import datastore_pb
        xact = object()
        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        rsp_pb = datastore_pb.BeginTransactionResponse()
        rsp_pb.transaction = TRANSACTION
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'beginTransaction',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.begin_transaction(DATASET_ID, True), TRANSACTION)
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '2',
                            })
        self.assertEqual(cw['body'], b'\x08\x01') # SERIALIZABLE

    def test_rollback_transaction_wo_existing_transaction(self):
        DATASET_ID = 'DATASET'
        TRANSACTION_ID = 'TRANSACTION'
        conn = self._makeOne()
        self.assertRaises(ValueError,
                          conn.rollback_transaction, DATASET_ID, TRANSACTION_ID)

    def test_rollback_transaction_w_existing_transaction_no_id(self):
        class Xact(object):
            def id(self):
                return None
        DATASET_ID = 'DATASET'
        TRANSACTION_ID = 'TRANSACTION'
        conn = self._makeOne()
        conn.transaction(Xact())
        self.assertRaises(ValueError,
                          conn.rollback_transaction, DATASET_ID, TRANSACTION_ID)

    def test_rollback_transaction_ok(self):
        from gcloud.datastore.connection import datastore_pb
        class Xact(object):
            def id(self):
                return 'xact'
        xact = object()

        DATASET_ID = 'DATASET'
        TRANSACTION = 'TRANSACTION'
        rsp_pb = datastore_pb.RollbackResponse()
        conn = self._makeOne()
        conn.transaction(Xact())
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'rollback',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.rollback_transaction(DATASET_ID, TRANSACTION),
                         None)
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '13',
                            })
        self.assertEqual(cw['body'], b'\n\x0bTRANSACTION')

    def test_run_query_wo_namespace_empty_result(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.query import Query
        DATASET_ID = 'DATASET'
        KIND = 'Nonesuch'
        q_pb = Query(KIND, DATASET_ID).to_protobuf()
        rsp_pb = datastore_pb.RunQueryResponse()
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'runQuery',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.run_query(DATASET_ID, q_pb), [])
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '14',
                            })
        self.assertEqual(cw['body'], b'\x1a\x0c\x1a\n\n\x08Nonesuch')

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
        rsp_pb.batch.more_results = 3 # NO_MORE_RESULTS
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'runQuery',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        result = conn.run_query(DATASET_ID, q_pb, 'NS')
        returned, = result # one entity
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '16',
                            })
        self.assertEqual(cw['body'],
                         b'\x12\x04"\x02NS\x1a\x08\x1a\x06\n\x04Kind')

    def test_lookup_single_key_empty_response(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        key_pb = Key(dataset=Dataset(DATASET_ID),
                     path=[{'kind': 'Kind', 'id': 1234}]).to_protobuf()
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'lookup',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, key_pb), None)
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '26',
                            })
        self.assertEqual(cw['body'],
                         b'\x1a\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xd2\t')

    def test_lookup_single_key_nonempty_response(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        key_pb = Key(dataset=Dataset(DATASET_ID),
                     path=[{'kind': 'Kind', 'id': 1234}]).to_protobuf()
        rsp_pb = datastore_pb.LookupResponse()
        entity = datastore_pb.Entity()
        entity.key.CopyFrom(key_pb)
        rsp_pb.found.add(entity=entity)
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
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
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '26',
                            })
        self.assertEqual(cw['body'],
                         b'\x1a\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xd2\t')

    def test_lookup_multiple_keys_empty_response(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        key_pb1 = Key(dataset=Dataset(DATASET_ID),
                      path=[{'kind': 'Kind', 'id': 1234}]).to_protobuf()
        key_pb2 = Key(dataset=Dataset(DATASET_ID),
                      path=[{'kind': 'Kind', 'id': 2345}]).to_protobuf()
        rsp_pb = datastore_pb.LookupResponse()
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
                        'datastore',
                        conn.API_VERSION,
                        'datasets',
                        DATASET_ID,
                        'lookup',
                       ])
        http = conn._http = Http({'status': '200'}, rsp_pb.SerializeToString())
        self.assertEqual(conn.lookup(DATASET_ID, [key_pb1, key_pb2]), [])
        cw = http._called_with
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '52',
                            })
        self.assertEqual(cw['body'],
                         b'\x1a\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xd2\t'
                         b'\x1a\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xa9\x12')

    def test_commit_wo_transaction(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        key_pb = Key(dataset=Dataset(DATASET_ID),
                      path=[{'kind': 'Kind', 'id': 1234}]).to_protobuf()
        rsp_pb = datastore_pb.CommitResponse()
        mutation = datastore_pb.Mutation()
        insert = mutation.upsert.add()
        insert.key.CopyFrom(key_pb)
        prop = insert.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        conn = self._makeOne()
        URI = '/'.join([conn.API_BASE_URL,
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
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '47',
                            })
        self.assertEqual(cw['body'],
                         b'\x12+\n)\n\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xd2\t'
                         b'\x12\r\n\x03foo"\x06\x8a\x01\x03Foo(\x02'
                         )

    def test_commit_w_transaction(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        class Xact(object):
            def id(self):
                return 'xact'
        DATASET_ID = 'DATASET'
        key_pb = Key(dataset=Dataset(DATASET_ID),
                      path=[{'kind': 'Kind', 'id': 1234}]).to_protobuf()
        rsp_pb = datastore_pb.CommitResponse()
        mutation = datastore_pb.Mutation()
        insert = mutation.upsert.add()
        insert.key.CopyFrom(key_pb)
        prop = insert.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        conn = self._makeOne()
        conn.transaction(Xact())
        URI = '/'.join([conn.API_BASE_URL,
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
        self.assertEqual(cw['uri'], URI)
        self.assertEqual(cw['method'], 'POST')
        self.assertEqual(cw['headers'],
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '53',
                            })
        self.assertEqual(cw['body'],
                         b'\n\x04xact'
                         b'\x12+\n)\n\x18\n\x0b\x1a\ts~DATASET'
                         b'\x12\t\n\x04Kind\x10\xd2\t'
                         b'\x12\r\n\x03foo"\x06\x8a\x01\x03Foo(\x01'
                         )

class Http(object):

    def __init__(self, headers, content):
        self._headers = headers
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._headers, self._content


class _Monkey(object):
    # context-manager for replacing module names in the scope of a test.
    def __init__(self, module, **kw):
        self.module = module
        self.to_restore = dict([(key, getattr(module, key)) for key in kw])
        for key, value in kw.items():
            setattr(module, key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self.to_restore.items():
            setattr(self.module, key, value)
