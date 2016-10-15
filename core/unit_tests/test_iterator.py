# Copyright 2015 Google Inc.
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


class TestPage(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.iterator import Page
        return Page

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        parent = object()
        items_key = 'potatoes'
        response = {items_key: (1, 2, 3)}
        page = self._makeOne(parent, response, items_key)
        self.assertIs(page._parent, parent)
        self.assertEqual(page._num_items, 3)
        self.assertEqual(page._remaining, 3)

    def test_num_items_property(self):
        page = self._makeOne(None, {}, '')
        num_items = 42
        page._num_items = num_items
        self.assertEqual(page.num_items, num_items)

    def test_remaining_property(self):
        page = self._makeOne(None, {}, '')
        remaining = 1337
        page._remaining = remaining
        self.assertEqual(page.remaining, remaining)

    def test___iter__(self):
        page = self._makeOne(None, {}, '')
        self.assertIs(iter(page), page)

    def test_iterator_calls__item_to_value(self):
        import six

        class Parent(object):

            calls = 0
            values = None

            def _item_to_value(self, item):
                self.calls += 1
                return item

        items_key = 'turkeys'
        response = {items_key: [10, 11, 12]}
        parent = Parent()
        page = self._makeOne(parent, response, items_key)
        page._remaining = 100

        self.assertEqual(parent.calls, 0)
        self.assertEqual(page.remaining, 100)
        self.assertEqual(six.next(page), 10)
        self.assertEqual(parent.calls, 1)
        self.assertEqual(page.remaining, 99)
        self.assertEqual(six.next(page), 11)
        self.assertEqual(parent.calls, 2)
        self.assertEqual(page.remaining, 98)
        self.assertEqual(six.next(page), 12)
        self.assertEqual(parent.calls, 3)
        self.assertEqual(page.remaining, 97)


class TestIterator(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.iterator import Iterator
        return Iterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._makeOne(client, path=path)
        self.assertIs(iterator.client, client)
        self.assertEqual(iterator.path, path)
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)

    def test_constructor_default_path(self):
        klass = self._getTargetClass()

        class WithPath(klass):
            PATH = '/path'

        connection = _Connection()
        client = _Client(connection)
        iterator = WithPath(client)
        self.assertIs(iterator.client, client)
        self.assertEqual(iterator.path, WithPath.PATH)
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)

    def test_constructor_w_extra_param_collision(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        extra_params = {'pageToken': 'val'}
        with self.assertRaises(ValueError):
            self._makeOne(client, path=path, extra_params=extra_params)

    def test_next_page_no_more(self):
        from google.cloud.iterator import NO_MORE_PAGES

        iterator = self._makeOne(None)
        iterator._page = NO_MORE_PAGES
        with self.assertRaises(ValueError):
            iterator.next_page()

    def test_next_page_not_empty_success(self):
        from google.cloud.iterator import Page

        iterator = self._makeOne(None)
        iterator._page = Page(None, {}, '')
        iterator._page._remaining = 1
        updated = iterator.next_page(require_empty=False)
        self.assertFalse(updated)

    def test_next_page_not_empty_fail(self):
        from google.cloud.iterator import Page

        iterator = self._makeOne(None)
        iterator._page = Page(None, {}, '')
        iterator._page._remaining = 1
        with self.assertRaises(ValueError):
            iterator.next_page(require_empty=True)

    def test_next_page_empty_then_no_more(self):
        from google.cloud.iterator import NO_MORE_PAGES

        iterator = self._makeOne(None)
        # Fake that there are no more pages.
        iterator.page_number = 1
        iterator.next_page_token = None
        updated = iterator.next_page()
        self.assertTrue(updated)
        self.assertIs(iterator.page, NO_MORE_PAGES)

    def test_next_page_empty_then_another(self):
        iterator = self._makeOne(None)
        # Fake the next page class.
        fake_page = object()
        page_args = []

        def dummy_response():
            return {}

        def dummy_page_class(*args):
            page_args.append(args)
            return fake_page

        iterator._get_next_page_response = dummy_response
        iterator._PAGE_CLASS = dummy_page_class
        updated = iterator.next_page()
        self.assertTrue(updated)
        self.assertIs(iterator.page, fake_page)
        self.assertEqual(page_args, [(iterator, {}, iterator.ITEMS_KEY)])

    def test___iter__(self):
        iterator = self._makeOne(None, None)
        self.assertIs(iter(iterator), iterator)

    def test_iterate(self):
        import six

        path = '/foo'
        key1 = 'key1'
        key2 = 'key2'
        item1, item2 = object(), object()
        ITEMS = {key1: item1, key2: item2}

        klass = self._getTargetClass()

        class WithItemToValue(klass):

            def _item_to_value(self, item):
                return ITEMS[item['name']]

        connection = _Connection(
            {'items': [{'name': key1}, {'name': key2}]})
        client = _Client(connection)
        iterator = WithItemToValue(client, path=path)
        self.assertEqual(iterator.num_results, 0)

        val1 = six.next(iterator)
        self.assertEqual(val1, item1)
        self.assertEqual(iterator.num_results, 1)

        val2 = six.next(iterator)
        self.assertEqual(val2, item2)
        self.assertEqual(iterator.num_results, 2)

        with self.assertRaises(StopIteration):
            six.next(iterator)

        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], path)
        self.assertEqual(kw['query_params'], {})

    def test_has_next_page_new(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._makeOne(client, path=path)
        self.assertTrue(iterator.has_next_page())

    def test_has_next_page_w_number_no_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._makeOne(client, path=path)
        iterator.page_number = 1
        self.assertFalse(iterator.has_next_page())

    def test_has_next_page_w_number_w_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        iterator = self._makeOne(client, path=path)
        iterator.page_number = 1
        iterator.next_page_token = token
        self.assertTrue(iterator.has_next_page())

    def test_has_next_page_w_max_results_not_done(self):
        iterator = self._makeOne(None, path=None, max_results=3,
                                 page_token='definitely-not-none')
        iterator.page_number = 1
        self.assertLess(iterator.num_results, iterator.max_results)
        self.assertTrue(iterator.has_next_page())

    def test_has_next_page_w_max_results_done(self):
        iterator = self._makeOne(None, None, max_results=3)
        iterator.page_number = 1
        iterator.num_results = iterator.max_results
        self.assertFalse(iterator.has_next_page())

    def test__get_query_params_no_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._makeOne(client, path=path)
        self.assertEqual(iterator._get_query_params(), {})

    def test__get_query_params_w_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        iterator = self._makeOne(client, path=path)
        iterator.next_page_token = token
        self.assertEqual(iterator._get_query_params(),
                         {'pageToken': token})

    def test__get_query_params_w_max_results(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        max_results = 3
        iterator = self._makeOne(client, path=path,
                                 max_results=max_results)
        iterator.num_results = 1
        local_max = max_results - iterator.num_results
        self.assertEqual(iterator._get_query_params(),
                         {'maxResults': local_max})

    def test__get_query_params_extra_params(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        extra_params = {'key': 'val'}
        iterator = self._makeOne(client, path=path, extra_params=extra_params)
        self.assertEqual(iterator._get_query_params(), extra_params)

    def test__get_query_params_w_token_and_extra_params(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        extra_params = {'key': 'val'}
        iterator = self._makeOne(client, path=path, extra_params=extra_params)
        iterator.next_page_token = token

        expected_query = extra_params.copy()
        expected_query.update({'pageToken': token})
        self.assertEqual(iterator._get_query_params(), expected_query)

    def test__get_next_page_response_new_no_token_in_response(self):
        path = '/foo'
        token = 'token'
        key1 = 'key1'
        key2 = 'key2'
        connection = _Connection({'items': [{'name': key1}, {'name': key2}],
                                  'nextPageToken': token})
        client = _Client(connection)
        iterator = self._makeOne(client, path=path)
        response = iterator._get_next_page_response()
        self.assertEqual(response['items'], [{'name': key1}, {'name': key2}])
        self.assertEqual(iterator.page_number, 1)
        self.assertEqual(iterator.next_page_token, token)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], path)
        self.assertEqual(kw['query_params'], {})

    def test__item_to_value_virtual(self):
        iterator = self._makeOne(None)
        with self.assertRaises(NotImplementedError):
            iterator._item_to_value({})

    def test_reset(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        iterator = self._makeOne(client, path=path)
        iterator.page_number = 1
        iterator.next_page_token = token
        iterator._page = object()
        iterator.reset()
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.num_results, 0)
        self.assertIsNone(iterator.next_page_token)
        self.assertIsNone(iterator._page)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Client(object):

    def __init__(self, connection):
        self.connection = connection
