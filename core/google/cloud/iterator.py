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

"""Iterators for paging through API responses.

These iterators simplify the process of paging through API responses
where the response is a list of results with a ``nextPageToken``.

To make an iterator work, you'll need to provide a way to convert a JSON
item returned from the API into the object of your choice (via
``item_to_value``). You also may need to specify a custom ``items_key`` so
that a given response (containing a page of results) can be parsed into an
iterable page of the actual objects you want. You then can use this to get
**all** the results from a resource::

    >>> def item_to_value(iterator, item):
    ...     my_item = MyItemClass(iterator.client, other_arg=True)
    ...     my_item._set_properties(item)
    ...     return my_item
    ...
    >>> iterator = Iterator(..., items_key='blocks',
    ...                     item_to_value=item_to_value)
    >>> list(iterator)  # Convert to a list (consumes all values).

Or you can walk your way through items and call off the search early if
you find what you're looking for (resulting in possibly fewer
requests)::

    >>> for my_item in Iterator(...):
    ...     print(my_item.name)
    ...     if not my_item.is_valid:
    ...         break

At any point, you may check the number of items consumed by referencing the
``num_results`` property of the iterator::

    >>> my_iterator = Iterator(...)
    >>> for my_item in my_iterator:
    ...     if my_iterator.num_results >= 10:
    ...         break

When iterating, not every new item will send a request to the server.
To iterate based on each page of items (where a page corresponds to
a request)::

    >>> iterator = Iterator(...)
    >>> for page in iterator.pages:
    ...     print('=' * 20)
    ...     print('    Page number: %d' % (iterator.page_number,))
    ...     print('  Items in page: %d' % (page.num_items,))
    ...     print('     First item: %r' % (next(page),))
    ...     print('Items remaining: %d' % (page.remaining,))
    ...     print('Next page token: %s' % (iterator.next_page_token,))
    ====================
        Page number: 1
      Items in page: 1
         First item: <MyItemClass at 0x7f1d3cccf690>
    Items remaining: 0
    Next page token: eav1OzQB0OM8rLdGXOEsyQWSG
    ====================
        Page number: 2
      Items in page: 19
         First item: <MyItemClass at 0x7f1d3cccffd0>
    Items remaining: 18
    Next page token: None

To consume an entire page::

    >>> list(page)
    [
        <MyItemClass at 0x7fd64a098ad0>,
        <MyItemClass at 0x7fd64a098ed0>,
        <MyItemClass at 0x7fd64a098e90>,
    ]
"""


import six


DEFAULT_ITEMS_KEY = 'items'
"""The dictionary key used to retrieve items from each response."""


# pylint: disable=unused-argument
def _do_nothing_page_start(iterator, page, response):
    """Helper to provide custom behavior after a :class:`Page` is started.

    This is a do-nothing stand-in as the default value.

    :type iterator: :class:`Iterator`
    :param iterator: An iterator that holds some request info.

    :type page: :class:`Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page.
    """
# pylint: enable=unused-argument


class Page(object):
    """Single page of results in an iterator.

    :type parent: :class:`Iterator`
    :param parent: The iterator that owns the current page.

    :type items: iterable
    :param items: An iterable (that also defines __len__) of items
                  from a raw API response.

    :type item_to_value: callable
    :param item_to_value: Callable to convert an item from the type in the
                          raw API response into the native object.
                          Assumed signature takes an :class:`Iterator` and a
                          raw API response with a single item.
    """

    def __init__(self, parent, items, item_to_value):
        self._parent = parent
        self._num_items = len(items)
        self._remaining = self._num_items
        self._item_iter = iter(items)
        self._item_to_value = item_to_value

    @property
    def num_items(self):
        """Total items in the page.

        :rtype: int
        :returns: The number of items in this page.
        """
        return self._num_items

    @property
    def remaining(self):
        """Remaining items in the page.

        :rtype: int
        :returns: The number of items remaining in this page.
        """
        return self._remaining

    def __iter__(self):
        """The :class:`Page` is an iterator."""
        return self

    def next(self):
        """Get the next value in the page."""
        item = six.next(self._item_iter)
        result = self._item_to_value(self._parent, item)
        # Since we've successfully got the next value from the
        # iterator, we update the number of remaining.
        self._remaining -= 1
        return result

    # Alias needed for Python 2/3 support.
    __next__ = next


class Iterator(object):
    """A generic class for iterating through API list responses.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client used to identify the application.

    :type item_to_value: callable
    :param item_to_value: Callable to convert an item from the type in the
                          raw API response into the native object.
                          Assumed signature takes an :class:`Iterator` and a
                          raw API response with a single item.

    :type page_token: str
    :param page_token: (Optional) A token identifying a page in a result set.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.
    """

    def __init__(self, client, item_to_value,
                 page_token=None, max_results=None):
        self._started = False
        self.client = client
        self._item_to_value = item_to_value
        self.max_results = max_results
        # The attributes below will change over the life of the iterator.
        self.page_number = 0
        self.next_page_token = page_token
        self.num_results = 0

    @property
    def pages(self):
        """Iterator of pages in the response.

        :rtype: :class:`~types.GeneratorType`
        :returns: A generator of :class:`Page` instances.
        :raises ValueError: If the iterator has already been started.
        """
        if self._started:
            raise ValueError('Iterator has already started', self)
        self._started = True
        return self._page_iter(increment=True)

    def _items_iter(self):
        """Iterator for each item returned."""
        for page in self._page_iter(increment=False):
            for item in page:
                self.num_results += 1
                yield item

    def __iter__(self):
        """Iterator for each item returned.

        :rtype: :class:`~types.GeneratorType`
        :returns: A generator of items from the API.
        :raises ValueError: If the iterator has already been started.
        """
        if self._started:
            raise ValueError('Iterator has already started', self)
        self._started = True
        return self._items_iter()

    def _page_iter(self, increment):
        """Generator of pages of API responses.

        :type increment: bool
        :param increment: Flag indicating if the total number of results
                          should be incremented on each page. This is useful
                          since a page iterator will want to increment by
                          results per page while an items iterator will want
                          to increment per item.

        Yields :class:`Page` instances.
        """
        page = self._next_page()
        while page is not None:
            self.page_number += 1
            if increment:
                self.num_results += page.num_items
            yield page
            page = self._next_page()

    @staticmethod
    def _next_page():
        """Get the next page in the iterator.

        This does nothing and is intended to be over-ridden by subclasses
        to return the next :class:`Page`.

        :raises NotImplementedError: Always.
        """
        raise NotImplementedError


class HTTPIterator(Iterator):
    """A generic class for iterating through Cloud JSON APIs list responses.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client used to identify the application.

    :type path: str
    :param path: The path to query for the list of items.

    :type item_to_value: callable
    :param item_to_value: Callable to convert an item from JSON
                          into the native object. Assumed signature
                          takes an :class:`Iterator` and a dictionary
                          holding a single item.

    :type items_key: str
    :param items_key: (Optional) The key used to grab retrieved items from an
                      API response. Defaults to :data:`DEFAULT_ITEMS_KEY`.

    :type page_token: str
    :param page_token: (Optional) A token identifying a page in a result set.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.

    :type extra_params: dict
    :param extra_params: (Optional) Extra query string parameters for the
                         API call.

    :type page_start: callable
    :param page_start: (Optional) Callable to provide any special behavior
                       after a new page has been created. Assumed signature
                       takes the :class:`Iterator` that started the page,
                       the :class:`Page` that was started and the dictionary
                       containing the page response.

    .. autoattribute:: pages
    """

    _PAGE_TOKEN = 'pageToken'
    _MAX_RESULTS = 'maxResults'
    _NEXT_TOKEN = 'nextPageToken'
    _RESERVED_PARAMS = frozenset([_PAGE_TOKEN, _MAX_RESULTS])
    _HTTP_METHOD = 'GET'

    def __init__(self, client, path, item_to_value,
                 items_key=DEFAULT_ITEMS_KEY,
                 page_token=None, max_results=None, extra_params=None,
                 page_start=_do_nothing_page_start):
        super(HTTPIterator, self).__init__(
            client, item_to_value, page_token=page_token,
            max_results=max_results)
        self.path = path
        self._items_key = items_key
        self.extra_params = extra_params
        self._page_start = page_start
        # Verify inputs / provide defaults.
        if self.extra_params is None:
            self.extra_params = {}
        self._verify_params()

    def _verify_params(self):
        """Verifies the parameters don't use any reserved parameter.

        :raises ValueError: If a reserved parameter is used.
        """
        reserved_in_use = self._RESERVED_PARAMS.intersection(
            self.extra_params)
        if reserved_in_use:
            raise ValueError('Using a reserved parameter',
                             reserved_in_use)

    def _next_page(self):
        """Get the next page in the iterator.

        :rtype: :class:`Page`
        :returns: The next page in the iterator (or :data:`None` if
                  there are no pages left).
        """
        if self._has_next_page():
            response = self._get_next_page_response()
            items = response.get(self._items_key, ())
            page = Page(self, items, self._item_to_value)
            self._page_start(self, page, response)
            self.next_page_token = response.get(self._NEXT_TOKEN)
            return page
        else:
            return None

    def _has_next_page(self):
        """Determines whether or not there are more pages with results.

        :rtype: bool
        :returns: Whether the iterator has more pages.
        """
        if self.page_number == 0:
            return True

        if self.max_results is not None:
            if self.num_results >= self.max_results:
                return False

        return self.next_page_token is not None

    def _get_query_params(self):
        """Getter for query parameters for the next request.

        :rtype: dict
        :returns: A dictionary of query parameters.
        """
        result = {}
        if self.next_page_token is not None:
            result[self._PAGE_TOKEN] = self.next_page_token
        if self.max_results is not None:
            result[self._MAX_RESULTS] = self.max_results - self.num_results
        result.update(self.extra_params)
        return result

    def _get_next_page_response(self):
        """Requests the next page from the path provided.

        :rtype: dict
        :returns: The parsed JSON response of the next page's contents.
        """
        params = self._get_query_params()
        if self._HTTP_METHOD == 'GET':
            return self.client._connection.api_request(
                method=self._HTTP_METHOD,
                path=self.path,
                query_params=params)
        elif self._HTTP_METHOD == 'POST':
            return self.client._connection.api_request(
                method=self._HTTP_METHOD,
                path=self.path,
                data=params)
        else:
            raise ValueError('Unexpected HTTP method', self._HTTP_METHOD)


class GAXIterator(Iterator):
    """A generic class for iterating through Cloud gRPC APIs list responses.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client used to identify the application.

    :type page_iter: :class:`~google.gax.PageIterator`
    :param page_iter: A GAX page iterator to be wrapped and conform to the
                      :class:`~google.cloud.iterator.Iterator` surface.

    :type item_to_value: callable
    :param item_to_value: Callable to convert an item from a protobuf
                          into the native object. Assumed signature
                          takes an :class:`Iterator` and a single item
                          from the API response as a protobuf.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.

    .. autoattribute:: pages
    """

    def __init__(self, client, page_iter, item_to_value, max_results=None):
        super(GAXIterator, self).__init__(
            client, item_to_value, page_token=page_iter.page_token,
            max_results=max_results)
        self._gax_page_iter = page_iter

    def _next_page(self):
        """Get the next page in the iterator.

        Wraps the response from the :class:`~google.gax.PageIterator` in a
        :class:`Page` instance and captures some state at each page.

        :rtype: :class:`Page`
        :returns: The next page in the iterator (or :data:`None` if
                  there are no pages left).
        """
        try:
            items = six.next(self._gax_page_iter)
            page = Page(self, items, self._item_to_value)
            self.next_page_token = self._gax_page_iter.page_token or None
            return page
        except StopIteration:
            return None
