import unittest2


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        self.assertEqual(conn.project, PROJECT)
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        PROJECT = 'project'
        creds = object()
        conn = self._makeOne(PROJECT, creds)
        self.assertEqual(conn.project, PROJECT)
        self.assertTrue(conn.credentials is creds)

    def test_http_w_existing(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        from httplib2 import Http
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        self.assertTrue(isinstance(conn.http, Http))

    def test_http_w_creds(self):
        from httplib2 import Http
        PROJECT = 'project'
        authorized = object()
        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(PROJECT, creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, Http))

    def test___iter___empty(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        keys = list(conn)
        self.assertEqual(len(keys), 0)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test___iter___non_empty(self):
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"items": [{"name": "%s"}]}' % KEY)
        keys = list(conn)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0].name, KEY)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test___contains___miss(self):
        PROJECT = 'project'
        NONESUCH = 'nonesuch'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'nonesuch?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '404',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertFalse(NONESUCH in conn)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test___contains___hit(self):
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'key?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"name": "%s"}' % KEY)
        self.assertTrue(KEY in conn)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_build_api_url_no_extra_query_params(self):
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'foo?project=%s' % PROJECT,
                       ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from urlparse import parse_qsl
        from urlparse import urlsplit
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'foo'
                       ])
        uri = conn.build_api_url('/foo', {'bar': 'baz'})
        scheme, netloc, path, qs, frag = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', 'storage', conn.API_VERSION, 'foo']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['project'], PROJECT)
        self.assertEqual(parms['bar'], 'baz')

    def test_make_request_no_data_no_content_type_no_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http({'status': '200',
                                  'content-type': 'text/plain',
                                 }, '')
        headers, content = conn.make_request('GET', URI)
        self.assertEqual(headers['status'], '200')
        self.assertEqual(headers['content-type'], 'text/plain')
        self.assertEqual(content, '')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                         })

    def test_make_request_w_data_no_extra_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http({'status': '200',
                                  'content-type': 'text/plain',
                                 }, '')
        headers, content = conn.make_request('GET', URI, {}, 'application/json')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], {})
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                          'Content-Type': 'application/json',
                         })

    def test_make_request_w_extra_headers(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = 'http://example.com/test'
        http = conn._http = Http({'status': '200',
                                  'content-type': 'text/plain',
                                 }, '')
        headers, content = conn.make_request('GET', URI,
                                             headers={'X-Foo': 'foo'})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                          'X-Foo': 'foo',
                         })

    def test_api_request_defaults(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        # see https://github.com/GoogleCloudPlatform/
                        #          gcloud-python/issues/140
                        #'?project=%s' % PROJECT,
                       ]) + 'None?project=%s' % PROJECT # XXX
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertEqual(conn.api_request('GET'), {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                         })

    def test_api_request_w_path(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertEqual(conn.api_request('GET', '/'), {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                         })

    def test_api_request_w_non_json_response(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'text/plain',
                                 }, 'CONTENT')
        self.assertRaises(TypeError, conn.api_request, 'GET', '/')

    def test_api_request_wo_json_expected(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'text/plain',
                                 }, 'CONTENT')
        self.assertEqual(conn.api_request('GET', '/', expect_json=False),
                         'CONTENT')

    def test_api_request_w_query_params(self):
        from urlparse import parse_qsl
        from urlparse import urlsplit
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s&foo=bar' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertEqual(conn.api_request('GET', '/', {'foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, frag = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', 'storage', conn.API_VERSION, '']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['project'], PROJECT)
        self.assertEqual(parms['foo'], 'bar')
        self.assertEqual(http._called_with['body'], None)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  0,
                         })

    def test_api_request_w_data(self):
        import json
        PROJECT = 'project'
        DATA = {'foo': 'bar'}
        DATAJ = json.dumps(DATA)
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertEqual(conn.api_request('POST', '/', data=DATA), {})
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], DATAJ)
        self.assertEqual(http._called_with['headers'],
                         {'Accept-Encoding': 'gzip',
                          'Content-Length':  len(DATAJ),
                          'Content-Type': 'application/json',
                         })

    def test_api_request_w_404(self):
        from gcloud.storage.exceptions import NotFoundError
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '404',
                                  'content-type': 'text/plain',
                                 }, '')
        self.assertRaises(NotFoundError, conn.api_request, 'GET', '/')

    def test_api_request_w_500(self):
        from gcloud.storage.exceptions import ConnectionError
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        '?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '500',
                                  'content-type': 'text/plain',
                                 }, '')
        self.assertRaises(ConnectionError, conn.api_request, 'GET', '/')

    def test_get_all_buckets_empty(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        keys = conn.get_all_buckets()
        self.assertEqual(len(keys), 0)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_all_buckets_non_empty(self):
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"items": [{"name": "%s"}]}' % KEY)
        keys = conn.get_all_buckets()
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0].name, KEY)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_bucket_miss(self):
        from gcloud.storage.exceptions import NotFoundError
        PROJECT = 'project'
        NONESUCH = 'nonesuch'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'nonesuch?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '404',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertRaises(NotFoundError, conn.get_bucket, NONESUCH)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_bucket_hit(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'key?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"name": "%s"}' % KEY)
        bucket = conn.get_bucket(KEY)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, KEY)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_lookup_miss(self):
        PROJECT = 'project'
        NONESUCH = 'nonesuch'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'nonesuch?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '404',
                                  'content-type': 'application/json',
                                 }, '{}')
        self.assertEqual(conn.lookup(NONESUCH), None)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_lookup_hit(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'key?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"name": "%s"}' % KEY)
        bucket = conn.lookup(KEY)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, KEY)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_create_bucket_ok(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{"name": "%s"}' % KEY)
        bucket = conn.create_bucket(KEY)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, KEY)
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)

    def test_delete_bucket_defaults_miss(self):
        _deleted_keys = []
        class _Key(object):
            def __init__(self, name):
                self._name = name
            def delete(self):
                _deleted_keys.append(self._name)
        class _Bucket(object):
            def __init__(self, name):
                self._name = name
                self.path = '/b/' + name
            def __iter__(self):
                return iter([_Key(x) for x in ('foo', 'bar')])
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        URI = '/'.join([conn.API_BASE_URL,
                        'storage',
                        conn.API_VERSION,
                        'b',
                        'key?project=%s' % PROJECT,
                       ])
        http = conn._http = Http({'status': '200',
                                  'content-type': 'application/json',
                                 }, '{}')
        def _new_bucket(name):
            return _Bucket(name)
        conn.new_bucket = _new_bucket
        self.assertEqual(conn.delete_bucket(KEY, True), True)
        self.assertEqual(_deleted_keys, ['foo', 'bar'])
        self.assertEqual(http._called_with['method'], 'DELETE')
        self.assertEqual(http._called_with['uri'], URI)

    def test_new_bucket_w_existing(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        existing = Bucket(self, KEY)
        self.assertTrue(conn.new_bucket(existing) is existing)

    def test_new_bucket_w_key(self):
        from gcloud.storage.bucket import Bucket
        PROJECT = 'project'
        KEY = 'key'
        conn = self._makeOne(PROJECT)
        bucket = conn.new_bucket(KEY)
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is conn)
        self.assertEqual(bucket.name, KEY)

    def test_new_bucket_w_invalid(self):
        PROJECT = 'project'
        conn = self._makeOne(PROJECT)
        self.assertRaises(TypeError, conn.new_bucket, object())


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
