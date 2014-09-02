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
        DATA = 'DATA'
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
                return 'REQPB'

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
                          'body': 'REQPB',
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

    def test_begin_transaction_already(self):
        DATASET_ID = 'DATASET'
        conn = self._makeOne()
        conn.transaction(object())
        self.assertRaises(ValueError, conn.begin_transaction, DATASET_ID)

    def test_begin_transaction_default_serialize(self):
        from gcloud.datastore.connection import datastore_pb
        xact = object()
        class RspPB(object):
            def __init__(self, pb):
                self._pb = pb
                self.transaction = xact
            @classmethod
            def FromString(cls, pb):
                return cls(pb)

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
        self.assertEqual(http._called_with,
                         {'uri': URI,
                          'method': 'POST',
                          'headers': 
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '2',
                            },
                          'body': b'\x08\x00', # SNAPSHOT
                         })

    def test_begin_transaction_explicit_serialize(self):
        from gcloud.datastore.connection import datastore_pb
        xact = object()
        class RspPB(object):
            def __init__(self, pb):
                self._pb = pb
                self.transaction = xact
            @classmethod
            def FromString(cls, pb):
                return cls(pb)

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
        self.assertEqual(http._called_with,
                         {'uri': URI,
                          'method': 'POST',
                          'headers': 
                            {'Content-Type': 'application/x-protobuf',
                             'Content-Length': '2',
                            },
                          'body': b'\x08\x01', # SERIALIZABLE
                         })

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
