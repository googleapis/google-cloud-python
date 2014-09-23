import unittest2


class TestIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.iterator import Iterator
        return Iterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        PATH = '/foo'
        iterator = self._makeOne(connection, PATH)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, PATH)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)

    def test___iter__(self):
        PATH = '/foo'
        KEY1 = 'key1'
        KEY2 = 'key2'
        ITEM1, ITEM2 = object(), object()
        ITEMS = {KEY1: ITEM1, KEY2: ITEM2}
        def _get_items(response):
            for item in response.get('items', []):
                yield ITEMS[item['name']]
        connection = _Connection({'items': [{'name': KEY1}, {'name': KEY2}]})
        iterator = self._makeOne(connection, PATH)
        iterator.get_items_from_response = _get_items
        self.assertEqual(list(iterator), [ITEM1, ITEM2])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], PATH)
        self.assertEqual(kw['query_params'], None)

    def test_has_next_page_new(self):
        connection = _Connection()
        PATH = '/foo'
        iterator = self._makeOne(connection, PATH)
        self.assertTrue(iterator.has_next_page())

    def test_has_next_page_w_number_no_token(self):
        connection = _Connection()
        PATH = '/foo'
        iterator = self._makeOne(connection, PATH)
        iterator.page_number = 1
        self.assertFalse(iterator.has_next_page())

    def test_has_next_page_w_number_w_token(self):
        connection = _Connection()
        PATH = '/foo'
        TOKEN = 'token'
        iterator = self._makeOne(connection, PATH)
        iterator.page_number = 1
        iterator.next_page_token = TOKEN
        self.assertTrue(iterator.has_next_page())

    def test_get_query_params_no_token(self):
        connection = _Connection()
        PATH = '/foo'
        iterator = self._makeOne(connection, PATH)
        self.assertEqual(iterator.get_query_params(), None)

    def test_get_query_params_w_token(self):
        connection = _Connection()
        PATH = '/foo'
        TOKEN = 'token'
        iterator = self._makeOne(connection, PATH)
        iterator.next_page_token = TOKEN
        self.assertEqual(iterator.get_query_params(),
                         {'pageToken': TOKEN,
                         })

    def test_get_next_page_response_new_no_token_in_response(self):
        PATH = '/foo'
        TOKEN = 'token'
        KEY1 = 'key1'
        KEY2 = 'key2'
        connection = _Connection({'items': [{'name': KEY1}, {'name': KEY2}],
                                  'nextPageToken': TOKEN})
        iterator = self._makeOne(connection, PATH)
        response = iterator.get_next_page_response()
        self.assertEqual(response['items'], [{'name': KEY1}, {'name': KEY2}])
        self.assertEqual(iterator.page_number, 1)
        self.assertEqual(iterator.next_page_token, TOKEN)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], PATH)
        self.assertEqual(kw['query_params'], None)

    def test_get_next_page_response_no_token(self):
        connection = _Connection()
        PATH = '/foo'
        iterator = self._makeOne(connection, PATH)
        iterator.page_number = 1
        self.assertRaises(RuntimeError, iterator.get_next_page_response)

    def test_reset(self):
        connection = _Connection()
        PATH = '/foo'
        TOKEN = 'token'
        iterator = self._makeOne(connection, PATH)
        iterator.page_number = 1
        iterator.next_page_token = TOKEN
        iterator.reset()
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)


class TestBucketIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.iterator import BucketIterator
        return BucketIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        iterator = self._makeOne(connection)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, '/b')
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        iterator = self._makeOne(connection)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.bucket import Bucket
        KEY = 'key'
        response = {'items': [{'name': KEY}]}
        connection = _Connection()
        iterator = self._makeOne(connection)
        buckets = list(iterator.get_items_from_response(response))
        self.assertEqual(len(buckets), 1)
        bucket = buckets[0]
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, KEY)


class TestKeyIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.iterator import KeyIterator
        return KeyIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        self.assertTrue(iterator.bucket is bucket)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, '%s/o' % bucket.path)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.key import Key
        KEY = 'key'
        response = {'items': [{'name': KEY}]}
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual(len(keys), 1)
        key = keys[0]
        self.assertTrue(isinstance(key, Key))
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)


class TestKeyDataIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.iterator import KeyDataIterator
        return KeyDataIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertTrue(iterator.key is key)
        self.assertEqual(iterator._bytes_written, 0)
        self.assertEqual(iterator._total_bytes, None)

    def test__iter__(self):
        response1 = _Response(status=200)
        response1['content-range'] = '0-10/15'
        response2 = _Response(status=200)
        response2['content-range'] = '11-14/15'
        connection = _Connection((response1, '01234567890'),
                                 (response2, '1234'),
                                )
        key = _Key(connection)
        iterator = self._makeOne(key)
        chunks = list(iterator)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], '01234567890')
        self.assertEqual(chunks[1], '1234')
        self.assertEqual(iterator._bytes_written, 15)
        self.assertEqual(iterator._total_bytes, 15)
        kws = connection._requested
        self.assertEqual(kws[0]['method'], 'GET')
        self.assertEqual(kws[0]['url'], 
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kws[0]['headers'], {'Range': 'bytes=0-10'})
        self.assertEqual(kws[1]['method'], 'GET')
        self.assertEqual(kws[1]['url'], 
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kws[1]['headers'], {'Range': 'bytes=11-'})

    def test_reset(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        iterator.reset()
        self.assertEqual(iterator._bytes_written, 0)
        self.assertEqual(iterator._total_bytes, None)

    def test_has_more_data_new(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertTrue(iterator.has_more_data())

    def test_has_more_data_invalid(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10 # no _total_bytes
        self.assertRaises(ValueError, iterator.has_more_data)

    def test_has_more_data_true(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        self.assertTrue(iterator.has_more_data())

    def test_has_more_data_false(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 1000
        iterator._total_bytes = 1000
        self.assertFalse(iterator.has_more_data())

    def test_get_headers_new(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=0-10')

    def test_get_headers_ok(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=10-20')

    def test_get_headers_off_end(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 95
        iterator._total_bytes = 100
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=95-')

    def test_get_url(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertEqual(iterator.get_url(),
                         'http://example.com/b/name/o/key?alt=media')

    def test_get_next_chunk_underflow(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = iterator._total_bytes = 10
        self.assertRaises(RuntimeError, iterator.get_next_chunk)

    def test_get_next_chunk_200(self):
        response = _Response(status=200)
        response['content-range'] = '0-10/100'
        connection = _Connection((response, 'CHUNK'))
        key = _Key(connection)
        iterator = self._makeOne(key)
        chunk = iterator.get_next_chunk()
        self.assertEqual(chunk, 'CHUNK')
        self.assertEqual(iterator._bytes_written, len(chunk))
        self.assertEqual(iterator._total_bytes, 100)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['url'], 
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kw['headers'], {'Range': 'bytes=0-10'})

    def test_get_next_chunk_206(self):
        response = _Response(status=206)
        connection = _Connection((response, 'CHUNK'))
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._total_bytes = 1000
        chunk = iterator.get_next_chunk()
        self.assertEqual(chunk, 'CHUNK')
        self.assertEqual(iterator._bytes_written, len(chunk))
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['url'], 
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kw['headers'], {'Range': 'bytes=0-10'})

    def test_get_next_chunk_416(self):
        response = _Response(status=416)
        connection = _Connection((response, ''))
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._total_bytes = 1000
        self.assertRaises(Exception, iterator.get_next_chunk)


class _Response(dict):
    @property
    def status(self):
        return self['status']

class _Connection(object):
    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
    def make_request(self, **kw):
        from gcloud.storage.exceptions import NotFoundError
        self._requested.append(kw)
        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFoundError('miss', None)
        else:
            return response
    def api_request(self, **kw):
        from gcloud.storage.exceptions import NotFoundError
        self._requested.append(kw)
        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFoundError('miss', None)
        else:
            return response
    def build_api_url(self, path, query_params=None):
        from urllib import urlencode
        from urlparse import urlunsplit
        qs = urlencode(query_params or {})
        return urlunsplit(('http', 'example.com', path, qs, ''))

class _Bucket(object):
    path = '/b/name'
    def __init__(self, connection):
        self.connection = connection

class _Key(object):
    CHUNK_SIZE = 10
    path = '/b/name/o/key'
    def __init__(self, connection):
        self.connection = connection
