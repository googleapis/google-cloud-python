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

To make an iterator work, you may need to override the
``ITEMS_KEY`` class attribute so that a given response (containing a page of
results) can be parsed into an iterable page of the actual objects you want::

  class MyIterator(Iterator):

      ITEMS_KEY = 'blocks'

      def _item_to_value(self, item):
          my_item = MyItemClass(other_arg=True)
          my_item._set_properties(item)
          return my_item

You then can use this to get **all** the results from a resource::

    >>> iterator = MyIterator(...)
    >>> list(iterator)  # Convert to a list (consumes all values).

Or you can walk your way through items and call off the search early if
you find what you're looking for (resulting in possibly fewer
requests)::

    >>> for my_item in MyIterator(...):
    ...     print(my_item.name)
    ...     if not my_item.is_valid:
    ...         break

When iterating, not every new item will send a request to the server.
To monitor these requests, track the current page of the iterator::

    >>> iterator = MyIterator(...)
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

    >>> iterator = MyIterator(...)
    >>> # No page of results before the iterator has started.
    >>> iterator.page is None
    True
    >>>
    >>> # Manually pull down the next page.
    >>> iterator.next_page()  # Returns "updated" status of page
    True
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
    >>> iterator.next_page()
    True
    >>> list(iterator.page)
    [
        <MyItemClass at 0x7fea740abdd0>,
        <MyItemClass at 0x7fea740abe50>,
    ]
    >>>
    >>> # When there are no more results
    >>> iterator.next_page()
    True
    >>> iterator.page is google.cloud.iterator.NO_MORE_PAGES
    True
"""


import six


NO_MORE_PAGES = object()
"""Sentinel object indicating an iterator has no more pages."""
_NO_MORE_PAGES_ERR = 'Iterator has no more pages.'
_PAGE_ERR_TEMPLATE = (
    'Tried to get next_page() while current page (%r) still has %d '
    'items remaining.')


class Page(object):
    """Single page of results in an iterator.

    :type parent: :class:`Iterator`
    :param parent: The iterator that owns the current page.

    :type response: dict
    :param response: The JSON API response for a page.

    :type items_key: str
    :param items_key: The dictionary key used to retrieve items
                      from the response.
    """

    def __init__(self, parent, response, items_key):
        self._parent = parent
        items = response.get(items_key, ())
        self._num_items = len(items)
        self._remaining = self._num_items
        self._item_iter = iter(items)
        self.response = response

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
        result = self._parent._item_to_value(item)
        # Since we've successfully got the next value from the
        # iterator, we update the number of remaining.
        self._remaining -= 1
        return result

    # Alias needed for Python 2/3 support.
    __next__ = next


class Iterator(object):
    """A generic class for iterating through Cloud JSON APIs list responses.

    Sub-classes need to over-write :attr:`ITEMS_KEY` and to define
    :meth:`_item_to_value`.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client, which owns a connection to make requests.

    :type page_token: str
    :param page_token: (Optional) A token identifying a page in a result set.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.

    :type extra_params: :class:`dict` or :data:`None`
    :param extra_params: Extra query string parameters for the API call.

    :type path: str
    :param path: The path to query for the list of items.
    """

    PAGE_TOKEN = 'pageToken'
    MAX_RESULTS = 'maxResults'
    RESERVED_PARAMS = frozenset([PAGE_TOKEN, MAX_RESULTS])
    PATH = None
    ITEMS_KEY = 'items'
    """The dictionary key used to retrieve items from each response."""
    _PAGE_CLASS = Page

    def __init__(self, client, page_token=None, max_results=None,
                 extra_params=None, path=None):
        self.extra_params = extra_params or {}
        self._verify_params()
        self.max_results = max_results
        self.client = client
        self.path = path or self.PATH
        # The attributes below will change over the life of the iterator.
        self.page_number = 0
        self.next_page_token = page_token
        self.num_results = 0
        self._page = None

    def _verify_params(self):
        """Verifies the parameters don't use any reserved parameter.

        :raises ValueError: If a reserved parameter is used.
        """
        reserved_in_use = self.RESERVED_PARAMS.intersection(
            self.extra_params)
        if reserved_in_use:
            raise ValueError('Using a reserved parameter',
                             reserved_in_use)

    @property
    def page(self):
        """The current page of results that has been retrieved.

        :rtype: :class:`Page`
        :returns: The page of items that has been retrieved.
        """
        return self._page

    def __iter__(self):
        """The :class:`Iterator` is an iterator."""
        return self

    def next_page(self, require_empty=True):
        """Move to the next page in the result set.

        If the current page is not empty and ``require_empty`` is :data:`True`
        then an exception will be raised. If the current page is not empty
        and ``require_empty`` is :data:`False`, then this will return
        without updating the current page (and will return an ``updated``
        value of :data:`False`).

        If the current page **is** empty, but there are no more results,
        sets the current page to :attr:`NO_MORE_PAGES`.

        If the current page is :attr:`NO_MORE_PAGES`, throws an exception.

        :type require_empty: bool
        :param require_empty: (Optional) Flag to indicate if the current page
                              must be empty before updating.

        :rtype: bool
        :returns: Flag indicated if the page was updated.
        :raises ValueError: If ``require_empty`` is :data:`True` but the
                            current page is not empty.
        :raises ValueError: If the current page is :attr:`NO_MORE_PAGES`.
        """
        if self._page is NO_MORE_PAGES:
            raise ValueError(_NO_MORE_PAGES_ERR)

        # NOTE: This assumes Page.remaining can never go below 0.
        page_empty = self._page is None or self._page.remaining == 0
        if page_empty:
            if self.has_next_page():
                response = self._get_next_page_response()
                self._page = self._PAGE_CLASS(self, response, self.ITEMS_KEY)
            else:
                self._page = NO_MORE_PAGES

            return True
        else:
            if require_empty:
                msg = _PAGE_ERR_TEMPLATE % (self._page, self.page.remaining)
                raise ValueError(msg)
            return False

    def _item_to_value(self, item):
        """Get the next item in the page.

        Subclasses will need to implement this method.

        :type item: dict
        :param item: An item to be converted to a native object.

        :raises NotImplementedError: Always
        """
        raise NotImplementedError

    def next(self):
        """Get the next item from the request."""
        self.next_page(require_empty=False)
        if self.page is NO_MORE_PAGES:
            raise StopIteration
        item = six.next(self.page)
        self.num_results += 1
        return item

    # Alias needed for Python 2/3 support.
    __next__ = next

    def has_next_page(self):
        """Determines whether or not there are more pages with results.

        :rtype: boolean
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
            result[self.PAGE_TOKEN] = self.next_page_token
        if self.max_results is not None:
            result[self.MAX_RESULTS] = self.max_results - self.num_results
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
        self._page = None
