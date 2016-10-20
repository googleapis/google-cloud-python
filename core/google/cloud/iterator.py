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

When iterating, not every new item will send a request to the server.
To monitor these requests, track the current page of the iterator::

    >>> iterator = Iterator(...)
    >>> iterator.page_number
    0
    >>> next(iterator)
    <MyItemClass at 0x7f1d3cccf690>
    >>> iterator.page_number
    1
    >>> iterator.page.remaining
    1
    >>> next(iterator)
    <MyItemClass at 0x7f1d3cccfe90>
    >>> iterator.page_number
    1
    >>> iterator.page.remaining
    0
    >>> next(iterator)
    <MyItemClass at 0x7f1d3cccffd0>
    >>> iterator.page_number
    2
    >>> iterator.page.remaining
    19

It's also possible to consume an entire page and handle the paging process
manually::

    >>> iterator = Iterator(...)
    >>> # Manually pull down the first page.
    >>> iterator.update_page()
    >>> items = list(iterator.page)
    >>> items
    [
        <MyItemClass at 0x7fd64a098ad0>,
        <MyItemClass at 0x7fd64a098ed0>,
        <MyItemClass at 0x7fd64a098e90>,
    ]
    >>> iterator.page.remaining
    0
    >>> iterator.page.num_items
    3
    >>> iterator.next_page_token
    'eav1OzQB0OM8rLdGXOEsyQWSG'
    >>>
    >>> # Ask for the next page to be grabbed.
    >>> iterator.update_page()
    >>> list(iterator.page)
    [
        <MyItemClass at 0x7fea740abdd0>,
        <MyItemClass at 0x7fea740abe50>,
    ]
    >>>
    >>> # When there are no more results
    >>> iterator.next_page_token is None
    True
    >>> iterator.update_page()
    >>> iterator.page is None
    True
"""


import six


_UNSET = object()
_NO_MORE_PAGES_ERR = 'Iterator has no more pages.'
_UNSTARTED_ERR = (
    'Iterator has not been started. Either begin iterating, '
    'call next(my_iter) or call my_iter.update_page().')
_PAGE_ERR_TEMPLATE = (
    'Tried to update the page while current page (%r) still has %d '
    'items remaining.')
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

    :type response: dict
    :param response: The JSON API response for a page.

    :type items_key: str
    :param items_key: The dictionary key used to retrieve items
                      from the response.

    :type item_to_value: callable
    :param item_to_value: Callable to convert an item from JSON
                          into the native object. Assumed signature
                          takes an :class:`Iterator` and a dictionary
                          holding a single item.
    """

    def __init__(self, parent, response, items_key, item_to_value):
        self._parent = parent
        items = response.get(items_key, ())
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
    """A generic class for iterating through Cloud JSON APIs list responses.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client, which owns a connection to make requests.

    :type path: str
    :param path: The path to query for the list of items. Defaults
                 to :attr:`PATH` on the current iterator class.

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
    """

    _PAGE_TOKEN = 'pageToken'
    _MAX_RESULTS = 'maxResults'
    _RESERVED_PARAMS = frozenset([_PAGE_TOKEN, _MAX_RESULTS])

    def __init__(self, client, path, item_to_value,
                 items_key=DEFAULT_ITEMS_KEY,
                 page_token=None, max_results=None, extra_params=None,
                 page_start=_do_nothing_page_start):
        self.client = client
        self.path = path
        self._items_key = items_key
        self._item_to_value = item_to_value
        self.max_results = max_results
        self.extra_params = extra_params
        self._page_start = page_start
        if self.extra_params is None:
            self.extra_params = {}
        self._verify_params()
        # The attributes below will change over the life of the iterator.
        self.page_number = 0
        self.next_page_token = page_token
        self.num_results = 0
        self._page = _UNSET

    def _verify_params(self):
        """Verifies the parameters don't use any reserved parameter.

        :raises ValueError: If a reserved parameter is used.
        """
        reserved_in_use = self._RESERVED_PARAMS.intersection(
            self.extra_params)
        if reserved_in_use:
            raise ValueError('Using a reserved parameter',
                             reserved_in_use)

    @property
    def page(self):
        """The current page of results that has been retrieved.

        If there are no more results, will return :data:`None`.

        :rtype: :class:`Page`
        :returns: The page of items that has been retrieved.
        :raises AttributeError: If the page has not been set.
        """
        if self._page is _UNSET:
            raise AttributeError(_UNSTARTED_ERR)
        return self._page

    def __iter__(self):
        """The :class:`Iterator` is an iterator."""
        return self

    def update_page(self, require_empty=True):
        """Move to the next page in the result set.

        If the current page is not empty and ``require_empty`` is :data:`True`
        then an exception will be raised. If the current page is not empty
        and ``require_empty`` is :data:`False`, then this will return
        without updating the current page.

        If the current page **is** empty, but there are no more results,
        sets the current page to :data:`None`.

        If there are no more pages, throws an exception.

        :type require_empty: bool
        :param require_empty: (Optional) Flag to indicate if the current page
                              must be empty before updating.

        :raises ValueError: If ``require_empty`` is :data:`True` but the
                            current page is not empty.
        :raises ValueError: If there are no more pages.
        """
        if self._page is None:
            raise ValueError(_NO_MORE_PAGES_ERR)

        # NOTE: This assumes Page.remaining can never go below 0.
        page_empty = self._page is _UNSET or self._page.remaining == 0
        if page_empty:
            if self._has_next_page():
                response = self._get_next_page_response()
                self._page = Page(self, response, self._items_key,
                                  self._item_to_value)
                self._page_start(self, self._page, response)
            else:
                self._page = None
        else:
            if require_empty:
                msg = _PAGE_ERR_TEMPLATE % (self._page, self.page.remaining)
                raise ValueError(msg)

    def next(self):
        """Get the next item from the request."""
        self.update_page(require_empty=False)
        if self.page is None:
            raise StopIteration
        item = six.next(self.page)
        self.num_results += 1
        return item

    # Alias needed for Python 2/3 support.
    __next__ = next

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
        response = self.client.connection.api_request(
            method='GET', path=self.path,
            query_params=self._get_query_params())

        self.page_number += 1
        self.next_page_token = response.get('nextPageToken')

        return response

    def reset(self):
        """Resets the iterator to the beginning."""
        self.page_number = 0
        self.next_page_token = None
        self.num_results = 0
        self._page = _UNSET
