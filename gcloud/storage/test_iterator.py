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
                         {'pageToken': TOKEN})

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

    def test_get_items_from_response_raises_NotImplementedError(self):
        PATH = '/foo'
        connection = _Connection()
        iterator = self._makeOne(connection, PATH)
        self.assertRaises(NotImplementedError,
                          iterator.get_items_from_response, object())


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
