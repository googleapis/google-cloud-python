import httplib2
import json
import urllib


from gcloud import connection
from gcloud.storage import exceptions
from gcloud.storage.bucket import Bucket
from gcloud.storage.iterator import BucketIterator


class Connection(connection.Connection):
  """A connection to Google Cloud Storage via the JSON REST API.

  This class should understand only the basic types (and protobufs)
  in method arguments, however should be capable of returning advanced types.

  See :class:`gcloud.connection.Connection` for a full list of parameters.
  :class:`Connection` differs only in needing a project name
  (which you specify when creating a project in the Cloud Console).

  A typical use of this is to operate on
  :class:`gcloud.storage.bucket.Bucket` objects::

    >>> from gcloud import storage
    >>> connection = storage.get_connection(project_name, email, key_path)
    >>> bucket = connection.create_bucket('my-bucket-name')

  You can then delete this bucket::

    >>> bucket.delete()
    >>> # or
    >>> connection.delete_bucket(bucket)

  If you want to access an existing bucket::

    >>> bucket = connection.get_bucket('my-bucket-name')

  A :class:`Connection` is actually iterable
  and will return the :class:`gcloud.storage.bucket.Bucket` objects
  inside the project::

    >>> for bucket in connection:
    >>>   print bucket
    <Bucket: my-bucket-name>

  In that same way, you can check for whether a bucket exists
  inside the project using Python's ``in`` operator::

    >>> print 'my-bucket-name' in connection
    True
  """

  API_VERSION = 'v1beta2'
  """The version of the API, used in building the API call's URL."""

  API_URL_TEMPLATE = '{api_base_url}/storage/{api_version}{path}'
  """A template used to craft the URL pointing toward a particular API call."""

  def __init__(self, project_name, *args, **kwargs):
    """
    :type project_name: string
    :param project_name: The project name to connect to.
    """

    super(Connection, self).__init__(*args, **kwargs)

    self.project_name = project_name

  def __iter__(self):
    return iter(BucketIterator(connection=self))

  def __contains__(self, bucket_name):
    return self.lookup(bucket_name) is not None

  def build_api_url(self, path, query_params=None, api_base_url=None,
                    api_version=None):
    """Construct an API url given a few components, some optional.

    Typically, you shouldn't need to use this method.

    :type path: string
    :param path: The path to the resource (ie, ``'/b/bucket-name'``).

    :type query_params: dict
    :param query_params: A dictionary of keys and values to insert into
                         the query string of the URL.

    :type api_base_url: string
    :param api_base_url: The base URL for the API endpoint.
                         Typically you won't have to provide this.

    :type api_version: string
    :param api_version: The version of the API to call.
                        Typically you shouldn't provide this and instead
                        use the default for the library.

    :rtype: string
    :returns: The URL assembled from the pieces provided.
    """

    url = self.API_URL_TEMPLATE.format(
        api_base_url=(api_base_url or self.API_BASE_URL),
        api_version=(api_version or self.API_VERSION),
        path=path)

    query_params = query_params or {}
    query_params.update({'project': self.project_name})
    url += '?' + urllib.urlencode(query_params)

    return url

  def make_request(self, method, url, data=None, content_type=None,
                   headers=None):
    """A low level method to send a request to the API.

    Typically, you shouldn't need to use this method.

    :type method: string
    :param method: The HTTP method to use in the request.

    :type url: string
    :param url: The URL to send the request to.

    :type data: string
    :param data: The data to send as the body of the request.

    :type content_type: string
    :param content_type: The proper MIME type of the data provided.

    :type headers: dict
    :param headers: A dictionary of HTTP headers to send with the request.

    :rtype: tuple of ``response`` (a dictionary of sorts)
            and ``content`` (a string).
    :returns: The HTTP response object and the content of the response.
    """

    headers = headers or {}
    headers['Accept-Encoding'] = 'gzip'

    if data:
      content_length = len(str(data))
    else:
      content_length = 0

    headers['Content-Length'] = content_length

    if content_type:
      headers['Content-Type'] = content_type

    return self.http.request(uri=url, method=method, headers=headers,
                               body=data)

  def api_request(self, method, path=None, query_params=None,
                  data=None, content_type=None,
                  api_base_url=None, api_version=None,
                  expect_json=True):
    """Make a request over the HTTP transport to the Cloud Storage API.

    You shouldn't need to use this method,
    but if you plan to interact with the API using these primitives,
    this is the correct one to use...

    :type method: string
    :param method: The HTTP method name (ie, ``GET``, ``POST``, etc).

    :type path: string
    :param path: The path to the resource (ie, ``'/b/bucket-name'``).

    :type query_params: dict
    :param query_params: A dictionary of keys and values to insert into
                         the query string of the URL.

    :type data: string
    :param data: The data to send as the body of the request.

    :type content_type: string
    :param content_type: The proper MIME type of the data provided.

    :type api_base_url: string
    :param api_base_url: The base URL for the API endpoint.
                         Typically you won't have to provide this.

    :type api_version: string
    :param api_version: The version of the API to call.
                        Typically you shouldn't provide this and instead
                        use the default for the library.

    :type expect_json: bool
    :param expect_json: If True, this method will try to parse the response
                        as JSON and raise an exception if that cannot be done.

    :raises: Exception if the response code is not 200 OK.
    """

    url = self.build_api_url(path=path, query_params=query_params,
                             api_base_url=api_base_url,
                             api_version=api_version)

    # Making the executive decision that any dictionary
    # data will be sent properly as JSON.
    if data and isinstance(data, dict):
      data = json.dumps(data)
      content_type = 'application/json'

    response, content = self.make_request(
        method=method, url=url, data=data, content_type=content_type)

    # TODO: Add better error handling.
    if response.status == 404:
      raise exceptions.NotFoundError(response, content)
    elif not 200 <= response.status < 300:
      raise exceptions.ConnectionError(response, content)

    if content and expect_json:
      # TODO: Better checking on this header for JSON.
      content_type = response.get('content-type', '')
      if not content_type.startswith('application/json'):
        raise TypeError('Expected JSON, got %s' % content_type)
      return json.loads(content)

    return content

  def get_all_buckets(self, *args, **kwargs):
    """Get all buckets in the project.

    This will not populate the list of keys available
    in each bucket.

    You can also iterate over the connection object,
    so these two operations are identical::

      >>> from gcloud import storage
      >>> connection = storage.get_connection(project_name, email, key_path)
      >>> for bucket in connection.get_all_buckets():
      >>>   print bucket
      >>> # ... is the same as ...
      >>> for bucket in connection:
      >>>   print bucket

    :rtype: list of :class:`gcloud.storage.bucket.Bucket` objects.
    :returns: All buckets belonging to this project.
    """

    return list(self)

  def get_bucket(self, bucket_name, *args, **kwargs):
    """Get a bucket by name.

    If the bucket isn't found,
    this will raise a :class:`gcloud.storage.exceptions.NotFoundError`.
    If you would rather get a bucket by name,
    and return ``None`` if the bucket isn't found
    (like ``{}.get('...')``)
    then use :func:`Connection.lookup`.

    For example::

      >>> from gcloud import storage
      >>> from gcloud.storage import exceptions
      >>> connection = storage.get_connection(project_name, email, key_path)
      >>> try:
      >>>   bucket = connection.get_bucket('my-bucket')
      >>> except exceptions.NotFoundError:
      >>>   print 'Sorry, that bucket does not exist!'

    :type bucket_name: string
    :param bucket_name: The name of the bucket to get.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The bucket matching the name provided.
    :raises: :class:`gcloud.storage.exceptions.NotFoundError`
    """

    # TODO: URL-encode the bucket name to be safe?
    bucket = self.new_bucket(bucket_name)
    response = self.api_request(method='GET', path=bucket.path)
    return Bucket.from_dict(response, connection=self)

  def lookup(self, bucket_name):
    """Get a bucket by name, returning None if not found.

    You can use this if you would rather
    checking for a None value
    than catching an exception::

      >>> from gcloud import storage
      >>> connection = storage.get_connection(project_name, email, key_path)
      >>> bucket = connection.get_bucket('doesnt-exist')
      >>> print bucket
      None
      >>> bucket = connection.get_bucket('my-bucket')
      >>> print bucket
      <Bucket: my-bucket>

    :type bucket_name: string
    :param bucket_name: The name of the bucket to get.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The bucket matching the name provided or None if not found.
    """

    try:
      return self.get_bucket(bucket_name)
    except exceptions.NotFoundError:
      return None

  def create_bucket(self, bucket, *args, **kwargs):
    # TODO: Which exceptions will this raise?
    """Create a new bucket.

    For example::

      >>> from gcloud import storage
      >>> connection = storage.get_connection(project_name, client, key_path)
      >>> bucket = connection.create_bucket('my-bucket')
      >>> print bucket
      <Bucket: my-bucket>

    :type bucket: string or :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket name (or bucket object) to create.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The newly created bucket.
    """

    bucket = self.new_bucket(bucket)
    response = self.api_request(method='POST', path='/b',
                                data={'name': bucket.name})
    return Bucket.from_dict(response, connection=self)

  def delete_bucket(self, bucket, *args, **kwargs):
    """Delete a bucket.

    You can use this method to delete a bucket by name,
    or to delete a bucket object::

      >>> from gcloud import storage
      >>> connection = storage.get_connection(project_name, email, key_path)
      >>> connection.delete_bucket('my-bucket')
      True

    You can also delete pass in the bucket object::

      >>> bucket = connection.get_bucket('other-bucket')
      >>> connection.delete_bucket(bucket)
      True

    If the bucket doesn't exist,
    this will raise a :class:`gcloud.storage.exceptions.NotFoundError`::

      >>> from gcloud.storage import exceptions
      >>> try:
      >>>   connection.delete_bucket('my-bucket')
      >>> except exceptions.NotFoundError:
      >>>   print 'That bucket does not exist!'

    :type bucket: string or :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket name (or bucket object) to create.

    :rtype: bool
    :returns: True if the bucket was deleted.
    :raises: :class:`gcloud.storage.exceptions.NotFoundError`
    """

    bucket = self.new_bucket(bucket)
    response = self.api_request(method='DELETE', path=bucket.path)
    return True

  def new_bucket(self, bucket):
    """Factory method for creating a new (unsaved) bucket object.

    This method is really useful when you're not sure whether
    you have an actual :class:`gcloud.storage.bucket.Bucket` object
    or just a name of a bucket.
    It always returns the object::

       >>> bucket = connection.new_bucket('bucket')
       >>> print bucket
       <Bucket: bucket>
       >>> bucket = connection.new_bucket(bucket)
       >>> print bucket
       <Bucket: bucket>

    :type bucket: string or :class:`gcloud.storage.bucket.Bucket`
    :param bucket: A name of a bucket or an existing Bucket object.
    """

    if isinstance(bucket, Bucket):
      return bucket

    # Support Python 2 and 3.
    try:
      string_type = basestring
    except NameError:
      string_type = str

    if isinstance(bucket, string_type):
      return Bucket(connection=self, name=bucket)

    raise TypeError('Invalid bucket: %s' % bucket)
