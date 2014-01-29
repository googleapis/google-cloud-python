"""Iterators for paging through API responses.

These iterators
simplify the process
of paging through API responses
where the response
is a list of results
with a ``nextPageToken``.

To make an iterator work,
just override the ``get_items_from_response`` method
so that given a response
(containing a page of results)
it parses those results
into an iterable
of the actual objects you want::

  class MyIterator(Iterator):
    def get_items_from_response(self, response):
      items = response.get('items', [])
      for item in items:
        yield MyItemClass.from_dict(item, other_arg=True)

You then can use this
to get **all** the results
from a resource::

  >>> iterator = MyIterator(...)
  >>> list(iterator)  # Convert to a list (consumes all values).

Or you can walk your way through items
and call off the search early
if you find what you're looking for
(resulting in possibly fewer requests)::

  >>> for item in MyIterator(...):
  >>>   print item.name
  >>>   if not item.is_valid:
  >>>     break
"""


class Iterator(object):
  """A generic class for iterating through Cloud Storage list responses.

  :type connection: :class:`gcloud.storage.connection.Connection`
  :param connection: The connection to use to make requests.

  :type path: string
  :param path: The path to query for the list of items.
  """

  def __init__(self, connection, path):
    self.connection = connection
    self.path = path
    self.page_number = 0
    self.next_page_token = None

  def __iter__(self):
    """Iterate through the list of items."""

    while self.has_next_page():
      response = self.get_next_page_response()
      for item in self.get_items_from_response(response):
        yield item

  def has_next_page(self):
    """Determines whether or not this iterator has more pages.

    :rtype: bool
    :returns: Whether the iterator has more pages or not.
    """

    if self.page_number == 0:
      return True

    return self.next_page_token is not None

  def get_query_params(self):
    """Getter for query parameters for the next request.

    :rtype: dict or None
    :returns: A dictionary of query parameters or None if there are none.
    """

    if self.next_page_token:
      return {'pageToken': self.next_page_token}

  def get_next_page_response(self):
    """Requests the next page from the path provided.

    :rtype: dict
    :returns: The parsed JSON response of the next page's contents.
    """

    if not self.has_next_page():
      raise RuntimeError('No more pages. Try resetting the iterator.')

    response = self.connection.api_request(
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

    This method should be overridden by a subclass.
    It should accept the API response
    of a request for the next page of items,
    and return a list (or other iterable)
    of items.

    Typically this method will construct
    a Bucket or a Key
    from the page of results in the response.

    :type response: dict
    :param response: The response of asking for the next page of items.

    :rtype: iterable
    :returns: Items that the iterator should yield.
    """
    raise NotImplementedError


class BucketIterator(Iterator):
  """An iterator listing all buckets.

  You shouldn't have to use this directly,
  but instead should use the helper methods
  on :class:`gcloud.storage.connection.Connection` objects.

  :type connection: :class:`gcloud.storage.connection.Connection`
  :param connection: The connection to use for querying the list of buckets.
  """

  def __init__(self, connection):
    super(BucketIterator, self).__init__(connection=connection, path='/b')

  def get_items_from_response(self, response):
    """Factory method which yields :class:`gcloud.storage.bucket.Bucket` items from a response.

    :type response: dict
    :param response: The JSON API response for a page of buckets.
    """

    from gcloud.storage.bucket import Bucket
    for item in response.get('items', []):
      yield Bucket.from_dict(item, connection=self.connection)


class KeyIterator(Iterator):
  """An iterator listing keys.

  You shouldn't have to use this directly,
  but instead should use the helper methods
  on :class:`gcloud.storage.key.Key` objects.

  :type bucket: :class:`gcloud.storage.bucket.Bucket`
  :param bucket: The bucket from which to list keys.
  """

  def __init__(self, bucket):
    self.bucket = bucket
    super(KeyIterator, self).__init__(
        connection=bucket.connection, path=bucket.path + '/o')

  def get_items_from_response(self, response):
    """Factory method which yields :class:`gcloud.storage.key.Key` items from a response.

    :type response: dict
    :param response: The JSON API response for a page of keys.
    """

    from gcloud.storage.key import Key
    for item in response.get('items', []):
      yield Key.from_dict(item, bucket=self.bucket)


class KeyDataIterator(object):
  # TODO: Use an actual HTTP streaming library,
  #       not multiple requests and the range header.

  def __init__(self, key):
    self.key = key
    self.reset()

  def __iter__(self):
    while self.has_more_data():
      yield self.get_next_chunk()

  def reset(self):
    self._bytes_written = 0
    self._total_bytes = None

  def has_more_data(self):
    if self._bytes_written == 0:
      return True
    elif not self._total_bytes:
      # self._total_bytes **should** be set by this point.
      # If it isn't, something is wrong.
      raise ValueError('Size of object is unknown... This is bad.')
    else:
      return (self._bytes_written < self._total_bytes)

  def get_headers(self):
    start = self._bytes_written
    end = self._bytes_written + self.key.CHUNK_SIZE

    if self._total_bytes and end > self._total_bytes:
      end = ''

    return {'Range': 'bytes=%s-%s' % (start, end)}

  def get_url(self):
    return self.key.connection.build_api_url(
        path=self.key.path, query_params={'alt': 'media'})

  def get_next_chunk(self):
    if not self.has_more_data():
      raise RuntimeError('No more data in this iterator. Try resetting.')

    response, content = self.key.connection.make_request(
        method='GET', url=self.get_url(), headers=self.get_headers())

    if response.status in (200, 206):
      self._bytes_written += len(content)

      if 'content-range' in response:
        content_range = response['content-range']
        self._total_bytes = int(content_range.rsplit('/', 1)[1])

      return content

    # Expected a 200 or a 206... Got something else, which is bad.
    raise Exception(response)
