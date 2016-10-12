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

To make an iterator work, just override the ``PAGE_CLASS`` class
attribute so that given a response (containing a page of results) can
be parsed into an iterable page of the actual objects you want::
those results into an iterable of the actual

  class MyPage(Page):

      def _next_item(self):
          item = six.next(self._item_iter)
          my_item = MyItemClass(other_arg=True)
          my_item._set_properties(item)
          return my_item


  class MyIterator(Iterator):

      PAGE_CLASS = MyPage

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
"""


import six


class Page(object):
    """Single page of results in an iterator.

    :type parent: :class:`Iterator`
    :param parent: The iterator that owns the current page.

    :type response: dict
    :param response: The JSON API response for a page.
    """

    ITEMS_KEY = 'items'

    def __init__(self, parent, response):
        self._parent = parent
        items = response.get(self.ITEMS_KEY, ())
        self._num_items = len(items)
        self._remaining = self._num_items
        self._item_iter = iter(items)

    @property
    def num_items(self):
        """Total items in the page.

        :rtype: int
        :returns: The number of items in this page of items.
        """
        return self._num_items

    @property
    def remaining(self):
        """Remaining items in the page.

        :rtype: int
        :returns: The number of items remaining this page.
        """
        return self._remaining

    def __iter__(self):
        """The :class:`Page` is an iterator."""
        return self

    def _next_item(self):
        """Get the next item in the page.

        This method (along with the constructor) is the workhorse
        of this class. Subclasses will need to implement this method.

        It is separate from :meth:`next` since that method needs
        to be aliased as ``__next__`` in Python 3.

        :raises NotImplementedError: Always
        """
        raise NotImplementedError

    def next(self):
        """Get the next value in the iterator."""
        result = self._next_item()
        # Since we've successfully got the next value from the
        # iterator, we update the number of remaining.
        self._remaining -= 1
        return result

    # Alias needed for Python 2/3 support.
    __next__ = next


class Iterator(object):
    """A generic class for iterating through Cloud JSON APIs list responses.

    Sub-classes need to over-write ``PAGE_CLASS``.

    :type client: :class:`google.cloud.client.Client`
    :param client: The client, which owns a connection to make requests.

    :type path: str
    :param path: The path to query for the list of items.

    :type page_token: str
    :param page_token: (Optional) A token identifying a page in a result set.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.

    :type extra_params: dict or None
    :param extra_params: Extra query string parameters for the API call.
    """

    PAGE_TOKEN = 'pageToken'
    MAX_RESULTS = 'maxResults'
    RESERVED_PARAMS = frozenset([PAGE_TOKEN, MAX_RESULTS])
    PAGE_CLASS = Page

    def __init__(self, client, path, page_token=None,
                 max_results=None, extra_params=None):
        self.client = client
        self.path = path
        self.page_number = 0
        self.next_page_token = page_token
        self.max_results = max_results
        self.num_results = 0
        self.extra_params = extra_params or {}
        reserved_in_use = self.RESERVED_PARAMS.intersection(
            self.extra_params)
        if reserved_in_use:
            raise ValueError(('Using a reserved parameter',
                              reserved_in_use))
        self._curr_items = iter(())

    def __iter__(self):
        """The :class:`Iterator` is an iterator."""
        return self

    def _update_items(self):
        """Replace the current items iterator.

        Intended to be used when the current items iterator is exhausted.

        After replacing the iterator, consumes the first value to make sure
        it is valid.

        :rtype: object
        :returns: The first item in the next iterator.
        :raises: :class:`~exceptions.StopIteration` if there is no next page.
        """
        if self.has_next_page():
            response = self.get_next_page_response()
            self._curr_items = self.PAGE_CLASS(self, response)
            return six.next(self._curr_items)
        else:
            raise StopIteration

    def next(self):
        """Get the next value in the iterator."""
        try:
            item = six.next(self._curr_items)
        except StopIteration:
            item = self._update_items()

        self.num_results += 1
        return item

    # Alias needed for Python 2/3 support.
    __next__ = next

    def has_next_page(self):
        """Determines whether or not this iterator has more pages.

        :rtype: boolean
        :returns: Whether the iterator has more pages or not.
        """
        if self.page_number == 0:
            return True

        if self.max_results is not None:
            if self.num_results >= self.max_results:
                return False

        return self.next_page_token is not None

    def get_query_params(self):
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

    def get_next_page_response(self):
        """Requests the next page from the path provided.

        :rtype: dict
        :returns: The parsed JSON response of the next page's contents.
        """
        if not self.has_next_page():
            raise RuntimeError('No more pages. Try resetting the iterator.')

        response = self.client.connection.api_request(
            method='GET', path=self.path, query_params=self.get_query_params())

        self.page_number += 1
        self.next_page_token = response.get('nextPageToken')

        return response

    def reset(self):
        """Resets the iterator to the beginning."""
        self.page_number = 0
        self.next_page_token = None
        self.num_results = 0


class MethodIterator(object):
    """Method-based iterator iterating through Cloud JSON APIs list responses.

    :type method: instance method
    :param method: ``list_foo`` method of a domain object, taking as arguments
                   ``page_token``, ``page_size``, and optional additional
                   keyword arguments.

    :type page_token: string or ``NoneType``
    :param page_token: Initial page token to pass.  if ``None``, fetch the
                       first page from the ``method`` API call.

    :type page_size: integer or ``NoneType``
    :param page_size: Maximum number of items to return from the ``method``
                      API call; if ``None``, uses the default for the API.

    :type max_calls: integer or ``NoneType``
    :param max_calls: Maximum number of times to make the ``method``
                      API call; if ``None``, applies no limit.

    :type kw: dict
    :param kw: optional keyword arguments to be passed to ``method``.
    """
    def __init__(self, method, page_token=None, page_size=None,
                 max_calls=None, **kw):
        self._method = method
        self._token = page_token
        self._page_size = page_size
        self._kw = kw
        self._max_calls = max_calls
        self._page_num = 0

    def __iter__(self):
        while self._max_calls is None or self._page_num < self._max_calls:
            items, new_token = self._method(
                page_token=self._token, page_size=self._page_size, **self._kw)
            for item in items:
                yield item
            if new_token is None:
                return
            self._page_num += 1
            self._token = new_token
