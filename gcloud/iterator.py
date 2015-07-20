# Copyright 2015 Google Inc. All rights reserved.
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

To make an iterator work, just override the ``get_items_from_response``
method so that given a response (containing a page of results) it parses
those results into an iterable of the actual objects you want::

  class MyIterator(Iterator):
      def get_items_from_response(self, response):
          items = response.get('items', [])
          for item in items:
              my_item = MyItemClass(other_arg=True)
              my_item._set_properties(item)
              yield my_item

You then can use this to get **all** the results from a resource::

    >>> iterator = MyIterator(...)
    >>> list(iterator)  # Convert to a list (consumes all values).

Or you can walk your way through items and call off the search early if
you find what you're looking for (resulting in possibly fewer
requests)::

    >>> for item in MyIterator(...):
    >>>     print item.name
    >>>     if not item.is_valid:
    >>>         break
"""


class Iterator(object):
    """A generic class for iterating through Cloud JSON APIs list responses.

    :type client: :class:`gcloud.client.Client`
    :param client: The client, which owns a connection to make requests.

    :type path: string
    :param path: The path to query for the list of items.

    :type extra_params: dict or None
    :param extra_params: Extra query string parameters for the API call.
    """

    PAGE_TOKEN = 'pageToken'
    RESERVED_PARAMS = frozenset([PAGE_TOKEN])

    def __init__(self, client, path, extra_params=None):
        self.client = client
        self.path = path
        self.page_number = 0
        self.next_page_token = None
        self.extra_params = extra_params or {}
        reserved_in_use = self.RESERVED_PARAMS.intersection(
            self.extra_params)
        if reserved_in_use:
            raise ValueError(('Using a reserved parameter',
                              reserved_in_use))

    def __iter__(self):
        """Iterate through the list of items."""
        while self.has_next_page():
            response = self.get_next_page_response()
            for item in self.get_items_from_response(response):
                yield item

    def has_next_page(self):
        """Determines whether or not this iterator has more pages.

        :rtype: boolean
        :returns: Whether the iterator has more pages or not.
        """
        if self.page_number == 0:
            return True

        return self.next_page_token is not None

    def get_query_params(self):
        """Getter for query parameters for the next request.

        :rtype: dict
        :returns: A dictionary of query parameters.
        """
        result = ({self.PAGE_TOKEN: self.next_page_token}
                  if self.next_page_token else {})
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

    def get_items_from_response(self, response):
        """Factory method called while iterating. This should be overriden.

        This method should be overridden by a subclass.  It should
        accept the API response of a request for the next page of items,
        and return a list (or other iterable) of items.

        Typically this method will construct a Bucket or a Blob from the
        page of results in the response.

        :type response: dict
        :param response: The response of asking for the next page of items.

        :rtype: iterable
        :returns: Items that the iterator should yield.
        """
        raise NotImplementedError
