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

  class MyPage(Page):

      def _item_to_value(self, item):
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

    def _item_to_value(self, item):
        """Get the next item in the page.

        This method (along with the constructor) is the workhorse
        of this class. Subclasses will need to implement this method.

        :type item: dict
        :param item: An item to be converted to a native object.

        :raises NotImplementedError: Always
        """
        raise NotImplementedError

    def next(self):
        """Get the next value in the iterator."""
        item = six.next(self._item_iter)
        result = self._item_to_value(item)
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

    :type page_token: str
    :param page_token: (Optional) A token identifying a page in a result set.

    :type max_results: int
    :param max_results: (Optional) The maximum number of results to fetch.

    :type extra_params: dict or None
    :param extra_params: Extra query string parameters for the API call.

    :type path: str
    :param path: The path to query for the list of items.
    """

    PAGE_TOKEN = 'pageToken'
    MAX_RESULTS = 'maxResults'
    RESERVED_PARAMS = frozenset([PAGE_TOKEN, MAX_RESULTS])
    PAGE_CLASS = Page
    PATH = None

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

    def _update_page(self):
        """Replace the current page.

        Does nothing if the current page is non-null and has items
        remaining.

        :raises: :class:`~exceptions.StopIteration` if there is no next page.
        """
        if self.page is not None and self.page.remaining > 0:
            return
        if self.has_next_page():
            response = self._get_next_page_response()
            self._page = self.PAGE_CLASS(self, response)
        else:
            raise StopIteration

    def next(self):
        """Get the next value in the iterator."""
        self._update_page()
        item = six.next(self.page)
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
