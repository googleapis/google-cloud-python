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


class Test__do_nothing_page_start(unittest.TestCase):

    def _call_fut(self, iterator, page, response):
        from google.cloud.iterator import _do_nothing_page_start

        return _do_nothing_page_start(iterator, page, response)

    def test_do_nothing(self):
        result = self._call_fut(None, None, None)
        self.assertIsNone(result)


class TestPage(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.iterator import Page

        return Page

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        parent = object()
        item_to_value = object()
        page = self._make_one(parent, (1, 2, 3), item_to_value)
        self.assertIs(page._parent, parent)
        self.assertEqual(page._num_items, 3)
        self.assertEqual(page._remaining, 3)
        self.assertIs(page._item_to_value, item_to_value)

    def test_num_items_property(self):
        page = self._make_one(None, (), None)
        num_items = 42
        page._num_items = num_items
        self.assertEqual(page.num_items, num_items)

    def test_remaining_property(self):
        page = self._make_one(None, (), None)
        remaining = 1337
        page._remaining = remaining
        self.assertEqual(page.remaining, remaining)

    def test___iter__(self):
        page = self._make_one(None, (), None)
        self.assertIs(iter(page), page)

    def test_iterator_calls__item_to_value(self):
        import six

        class Parent(object):

            calls = 0

            def item_to_value(self, item):
                self.calls += 1
                return item

        parent = Parent()
        page = self._make_one(parent, (10, 11, 12),
                              Parent.item_to_value)
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

    @staticmethod
    def _get_target_class():
        from google.cloud.iterator import Iterator

        return Iterator

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        connection = _Connection()
        client = _Client(connection)
        item_to_value = object()
        token = 'ab13nceor03'
        max_results = 1337
        iterator = self._make_one(client, item_to_value, page_token=token,
                                  max_results=max_results)

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertIs(iterator._item_to_value, item_to_value)
        self.assertEqual(iterator.max_results, max_results)
        # Changing attributes.
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, token)
        self.assertEqual(iterator.num_results, 0)

    def test_pages_property(self):
        iterator = self._make_one(None, None)
        self.assertFalse(iterator._started)
        mock_iter = object()
        incremented = []

        def page_iter(increment):
            incremented.append(increment)
            return mock_iter

        iterator._page_iter = page_iter
        self.assertIs(iterator.pages, mock_iter)
        self.assertEqual(incremented, [True])
        # Check the side-effect.
        self.assertTrue(iterator._started)

    def test_pages_property_started(self):
        import types

        iterator = self._make_one(None, None)
        self.assertIsInstance(iterator.pages, types.GeneratorType)
        # Make sure we cannot restart.
        with self.assertRaises(ValueError):
            getattr(iterator, 'pages')

    def test_pages_property_items_started(self):
        import types

        iterator = self._make_one(None, None)
        self.assertIsInstance(iter(iterator), types.GeneratorType)
        with self.assertRaises(ValueError):
            getattr(iterator, 'pages')

    @staticmethod
    def _do_nothing(parent, value):
        return parent, value

    def test__items_iter(self):
        import types
        import six
        from google.cloud.iterator import Page

        # Items to be returned.
        item1 = 17
        item2 = 100
        item3 = 211

        # Make pages from mock responses
        parent = object()
        page1 = Page(parent, (item1, item2), self._do_nothing)
        page2 = Page(parent, (item3,), self._do_nothing)

        iterator = self._make_one(None, None)
        # Fake the page iterator on the object.
        incremented = []

        def page_iter(increment):
            incremented.append(increment)
            return iter((page1, page2))

        iterator._page_iter = page_iter
        items_iter = iterator._items_iter()
        # Make sure it is a generator.
        self.assertIsInstance(items_iter, types.GeneratorType)

        # Consume items and check the state of the iterator.
        self.assertEqual(iterator.num_results, 0)
        self.assertEqual(six.next(items_iter), (parent, item1))
        self.assertEqual(iterator.num_results, 1)
        self.assertEqual(six.next(items_iter), (parent, item2))
        self.assertEqual(iterator.num_results, 2)
        self.assertEqual(six.next(items_iter), (parent, item3))
        self.assertEqual(iterator.num_results, 3)
        with self.assertRaises(StopIteration):
            six.next(items_iter)

        # Make sure our page_iter() was called correctly.
        self.assertEqual(incremented, [False])

    def test___iter__(self):
        iterator = self._make_one(None, None)
        self.assertFalse(iterator._started)
        incremented = []

        def page_iter(increment):
            incremented.append(increment)
            return iter(())

        iterator._page_iter = page_iter
        self.assertEqual(list(iterator), [])
        # Check the side-effect.
        self.assertTrue(iterator._started)

    def test___iter___started(self):
        import types

        iterator = self._make_one(None, None)
        self.assertIsInstance(iter(iterator), types.GeneratorType)
        with self.assertRaises(ValueError):
            iter(iterator)

    def test___iter___pages_started(self):
        import types

        iterator = self._make_one(None, None)
        self.assertIsInstance(iterator.pages, types.GeneratorType)
        with self.assertRaises(ValueError):
            iter(iterator)

    def test__next_page_virtual(self):
        iterator = self._make_one(None, None)
        with self.assertRaises(NotImplementedError):
            iterator._next_page()


class TestHTTPIterator(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.iterator import HTTPIterator

        return HTTPIterator

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        from google.cloud.iterator import _do_nothing_page_start

        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._make_one(client, path, None)
        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertEqual(iterator.path, path)
        self.assertIsNone(iterator._item_to_value)
        self.assertEqual(iterator._items_key, 'items')
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator.extra_params, {})
        self.assertIs(iterator._page_start, _do_nothing_page_start)
        # Changing attributes.
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.num_results, 0)

    def test_constructor_w_extra_param_collision(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        extra_params = {'pageToken': 'val'}
        with self.assertRaises(ValueError):
            self._make_one(client, path, None, extra_params=extra_params)

    def test_pages_iter_empty_then_another(self):
        import six
        from google.cloud._testing import _Monkey
        from google.cloud import iterator as MUT

        items_key = 'its-key'
        iterator = self._make_one(None, None, None, items_key=items_key)
        # Fake the next page class.
        fake_page = MUT.Page(None, (), None)
        page_args = []

        def dummy_response():
            return {}

        def dummy_page_class(*args):
            page_args.append(args)
            return fake_page

        iterator._get_next_page_response = dummy_response
        pages_iter = iterator.pages
        with _Monkey(MUT, Page=dummy_page_class):
            page = six.next(pages_iter)
        self.assertIs(page, fake_page)
        self.assertEqual(
            page_args, [(iterator, (), iterator._item_to_value)])

    def test_iterate(self):
        import six

        path = '/foo'
        key1 = 'key1'
        key2 = 'key2'
        item1, item2 = object(), object()
        ITEMS = {key1: item1, key2: item2}

        def item_to_value(iterator, item):  # pylint: disable=unused-argument
            return ITEMS[item['name']]

        connection = _Connection(
            {'items': [{'name': key1}, {'name': key2}]})
        client = _Client(connection)
        iterator = self._make_one(client, path=path,
                                  item_to_value=item_to_value)
        self.assertEqual(iterator.num_results, 0)

        items_iter = iter(iterator)
        val1 = six.next(items_iter)
        self.assertEqual(val1, item1)
        self.assertEqual(iterator.num_results, 1)

        val2 = six.next(items_iter)
        self.assertEqual(val2, item2)
        self.assertEqual(iterator.num_results, 2)

        with self.assertRaises(StopIteration):
            six.next(items_iter)

        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], path)
        self.assertEqual(kw['query_params'], {})

    def test__has_next_page_new(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._make_one(client, path, None)
        self.assertTrue(iterator._has_next_page())

    def test__has_next_page_w_number_no_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._make_one(client, path, None)
        iterator.page_number = 1
        self.assertFalse(iterator._has_next_page())

    def test__has_next_page_w_number_w_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        iterator = self._make_one(client, path, None)
        iterator.page_number = 1
        iterator.next_page_token = token
        self.assertTrue(iterator._has_next_page())

    def test__has_next_page_w_max_results_not_done(self):
        iterator = self._make_one(None, None, None, max_results=3,
                                  page_token='definitely-not-none')
        iterator.page_number = 1
        self.assertLess(iterator.num_results, iterator.max_results)
        self.assertTrue(iterator._has_next_page())

    def test__has_next_page_w_max_results_done(self):
        iterator = self._make_one(None, None, None, max_results=3)
        iterator.page_number = 1
        iterator.num_results = iterator.max_results
        self.assertFalse(iterator._has_next_page())

    def test__get_query_params_no_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        iterator = self._make_one(client, path, None)
        self.assertEqual(iterator._get_query_params(), {})

    def test__get_query_params_w_token(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        iterator = self._make_one(client, path, None)
        iterator.next_page_token = token
        self.assertEqual(iterator._get_query_params(),
                         {'pageToken': token})

    def test__get_query_params_w_max_results(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        max_results = 3
        iterator = self._make_one(client, path, None,
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
        iterator = self._make_one(client, path, None,
                                  extra_params=extra_params)
        self.assertEqual(iterator._get_query_params(), extra_params)

    def test__get_query_params_w_token_and_extra_params(self):
        connection = _Connection()
        client = _Client(connection)
        path = '/foo'
        token = 'token'
        extra_params = {'key': 'val'}
        iterator = self._make_one(client, path, None,
                                  extra_params=extra_params)
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
        iterator = self._make_one(client, path, None)
        response = iterator._get_next_page_response()
        self.assertEqual(response['items'], [{'name': key1}, {'name': key2}])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], path)
        self.assertEqual(kw['query_params'], {})

    def test__get_next_page_response_with_post(self):
        path = '/foo'
        returned = {'green': 'eggs', 'ham': 55}
        connection = _Connection(returned)
        client = _Client(connection)
        iterator = self._make_one(client, path, None)
        iterator._HTTP_METHOD = 'POST'
        response = iterator._get_next_page_response()
        self.assertEqual(response, returned)

        self.assertEqual(len(connection._requested), 1)
        called_kwargs = connection._requested[0]
        self.assertEqual(called_kwargs, {
            'method': iterator._HTTP_METHOD,
            'path': path,
            'data': {},
        })

    def test__get_next_page_bad_http_method(self):
        path = '/foo'
        client = _Client(None)
        iterator = self._make_one(client, path, None)
        iterator._HTTP_METHOD = 'NOT-A-VERB'
        with self.assertRaises(ValueError):
            iterator._get_next_page_response()


class TestGAXIterator(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.iterator import GAXIterator

        return GAXIterator

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        client = _Client(None)
        token = 'zzzyy78kl'
        page_iter = SimpleIter(token)
        item_to_value = object()
        max_results = 1337
        iterator = self._make_one(client, page_iter, item_to_value,
                                  max_results=max_results)

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertIs(iterator._item_to_value, item_to_value)
        self.assertEqual(iterator.max_results, max_results)
        self.assertIs(iterator._gax_page_iter, page_iter)
        # Changing attributes.
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, token)
        self.assertEqual(iterator.num_results, 0)

    @staticmethod
    def _do_nothing(parent, value):
        return parent, value

    def test__next_page(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.iterator import Page

        # Make a mock ``google.gax.PageIterator``
        page_items = (29, 31)  # Items for just one page.
        page_token = '2sde98ds2s0hh'
        page_iter = _GAXPageIterator(page_items, page_token=page_token)
        # Wrap the GAX iterator.
        iterator = self._make_one(None, page_iter, self._do_nothing)

        page = iterator._next_page()
        # First check the page token.
        self.assertEqual(iterator.next_page_token, page_token)
        # Then check the page.
        self.assertIsInstance(page, Page)
        # _do_nothing will throw the iterator in front.
        expected = zip((iterator, iterator), page_items)
        self.assertEqual(list(page), list(expected))

    def test__next_page_empty(self):
        from google.cloud._testing import _GAXPageIterator

        # Make a mock ``google.gax.PageIterator``
        page_iter = _GAXPageIterator()
        # Wrap the GAX iterator.
        iterator = self._make_one(None, page_iter, self._do_nothing)

        page = iterator._next_page()
        self.assertIsNone(page)
        self.assertIsNone(iterator.next_page_token)

    def test_iterate(self):
        import six
        from google.cloud._testing import _GAXPageIterator

        item1 = object()
        item2 = object()
        item3 = object()
        token1 = 'smkdme30e2e32r'
        token2 = '39cm9csl123dck'

        # Make a mock ``google.gax.PageIterator``
        page1 = (item1,)
        page2 = (item2, item3)
        page_iter = _GAXPageIterator(page1, page2, page_token=token1)
        iterator = self._make_one(None, page_iter, self._do_nothing)

        self.assertEqual(iterator.num_results, 0)

        items_iter = iter(iterator)
        val1 = six.next(items_iter)
        self.assertEqual(val1, (iterator, item1))
        self.assertEqual(iterator.num_results, 1)
        self.assertEqual(iterator.next_page_token, token1)

        # Before grabbing the next page, hot-swap the token
        # on the ``page_iter``.
        page_iter.page_token = token2

        # Grab the next item (which will cause the next page).
        val2 = six.next(items_iter)
        self.assertEqual(val2, (iterator, item2))
        self.assertEqual(iterator.num_results, 2)
        self.assertEqual(iterator.next_page_token, token2)

        # Grab the final item from the final / current page.
        val3 = six.next(items_iter)
        self.assertEqual(val3, (iterator, item3))
        self.assertEqual(iterator.num_results, 3)
        # Make sure the token did not change.
        self.assertEqual(iterator.next_page_token, token2)

        with self.assertRaises(StopIteration):
            six.next(items_iter)


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
        self._connection = connection


class SimpleIter(object):

    def __init__(self, page_token=None):
        self.page_token = page_token
