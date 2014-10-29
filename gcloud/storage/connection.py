"""Create / interact with gcloud storage connections."""

import base64
import calendar
import datetime
import json
import urllib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from OpenSSL import crypto
import pytz

from gcloud import connection
from gcloud.storage import exceptions
from gcloud.storage.bucket import Bucket
from gcloud.storage.bucket import BucketIterator


def _utcnow():  # pragma: NO COVER testing replaces
    """Returns current time as UTC datetime.

    NOTE: on the module namespace so tests can replace it.
    """
    return datetime.datetime.utcnow()


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
      >>> connection = storage.get_connection(project, email, key_path)
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

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/storage/{api_version}{path}'
    """A template for the URL of a particular API call."""

    API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'

    def __init__(self, project, *args, **kwargs):
        """:type project: string
        :param project: The project name to connect to.

        """

        super(Connection, self).__init__(*args, **kwargs)

        self.project = project

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
        query_params.update({'project': self.project})
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

        headers['User-Agent'] = self.USER_AGENT

        return self.http.request(uri=url, method=method, headers=headers,
                                 body=data)

    def api_request(self, method, path, query_params=None,
                    data=None, content_type=None,
                    api_base_url=None, api_version=None,
                    expect_json=True):
        """Make a request over the HTTP transport to the Cloud Storage API.

        You shouldn't need to use this method,
        but if you plan to interact with the API using these primitives,
        this is the correct one to use...

        :type method: string
        :param method: The HTTP method name (ie, ``GET``, ``POST``, etc).
                       Required.

        :type path: string
        :param path: The path to the resource (ie, ``'/b/bucket-name'``).
                     Required.

        :type query_params: dict
        :param query_params: A dictionary of keys and values to insert into
                             the query string of the URL.
                             Default is empty dict.

        :type data: string
        :param data: The data to send as the body of the request. Default is
                     the empty string.

        :type content_type: string
        :param content_type: The proper MIME type of the data provided. Default
                             is None.

        :type api_base_url: string
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.
                             Default is the standard API base URL.

        :type api_version: string
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.
                            Default is the latest API version supported by
                            gcloud-python.

        :type expect_json: bool
        :param expect_json: If True, this method will try to parse the response
                            as JSON and raise an exception if that cannot
                            be done.  Default is True.

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

        if response.status == 404:
            raise exceptions.NotFoundError(response)
        elif not 200 <= response.status < 300:
            raise exceptions.ConnectionError(response, content)

        if content and expect_json:
            content_type = response.get('content-type', '')
            if not content_type.startswith('application/json'):
                raise TypeError('Expected JSON, got %s' % content_type)
            return json.loads(content)

        return content

    def get_all_buckets(self):
        """Get all buckets in the project.

        This will not populate the list of keys available
        in each bucket.

        You can also iterate over the connection object,
        so these two operations are identical::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> for bucket in connection.get_all_buckets():
          >>>   print bucket
          >>> # ... is the same as ...
          >>> for bucket in connection:
          >>>   print bucket

        :rtype: list of :class:`gcloud.storage.bucket.Bucket` objects.
        :returns: All buckets belonging to this project.
        """

        return list(self)

    def get_bucket(self, bucket_name):
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
          >>> connection = storage.get_connection(project, email, key_path)
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
        bucket = self.new_bucket(bucket_name)
        response = self.api_request(method='GET', path=bucket.path)
        return Bucket.from_dict(response, connection=self)

    def lookup(self, bucket_name):
        """Get a bucket by name, returning None if not found.

        You can use this if you would rather
        checking for a None value
        than catching an exception::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
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

    def create_bucket(self, bucket):
        """Create a new bucket.

        For example::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, client, key_path)
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

    def delete_bucket(self, bucket, force=False):
        """Delete a bucket.

        You can use this method to delete a bucket by name,
        or to delete a bucket object::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
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

        :type force: bool
        :param full: If True, empties the bucket's objects then deletes it.

        :rtype: bool
        :returns: True if the bucket was deleted.
        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """

        bucket = self.new_bucket(bucket)

        # This force delete operation is slow.
        if force:
            for key in bucket:
                key.delete()

        self.api_request(method='DELETE', path=bucket.path)
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
        except NameError:  # pragma: NO COVER PY3k
            string_type = str

        if isinstance(bucket, string_type):
            return Bucket(connection=self, name=bucket)

        raise TypeError('Invalid bucket: %s' % bucket)

    def generate_signed_url(self, resource, expiration,
                            method='GET', content_md5=None,
                            content_type=None):
        """Generate signed URL to provide query-string auth'n to a resource.

        :type resource: string
        :param resource: A pointer to a specific resource
                         (typically, ``/bucket-name/path/to/key.txt``).

        :type expiration: int, long, datetime.datetime, datetime.timedelta
        :param expiration: When the signed URL should expire.

        :type method: string
        :param method: The HTTP verb that will be used when requesting the URL.

        :type content_md5: string
        :param content_md5: The MD5 hash of the object referenced by
                            ``resource``.

        :type content_type: string
        :param content_type: The content type of the object referenced by
                             ``resource``.

        :rtype: string
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """

        expiration = _get_expiration_seconds(expiration)

        # Generate the string to sign.
        signature_string = '\n'.join([
            method,
            content_md5 or '',
            content_type or '',
            str(expiration),
            resource])

        # Take our PKCS12 (.p12) key and make it into a RSA key we can use...
        pkcs12 = crypto.load_pkcs12(
            base64.b64decode(self.credentials.private_key),
            'notasecret')
        pem = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, pkcs12.get_privatekey())
        pem_key = RSA.importKey(pem)

        # Sign the string with the RSA key.
        signer = PKCS1_v1_5.new(pem_key)
        signature_hash = SHA256.new(signature_string)
        signature_bytes = signer.sign(signature_hash)
        signature = base64.b64encode(signature_bytes)

        # Set the right query parameters.
        query_params = {
            'GoogleAccessId': self.credentials.service_account_name,
            'Expires': str(expiration),
            'Signature': signature,
        }

        # Return the built URL.
        return '{endpoint}{resource}?{querystring}'.format(
            endpoint=self.API_ACCESS_ENDPOINT, resource=resource,
            querystring=urllib.urlencode(query_params))


def _get_expiration_seconds(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """

    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = _utcnow().replace(tzinfo=pytz.utc)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        # Make sure the timezone on the value is UTC
        # (either by converting or replacing the value).
        if expiration.tzinfo:
            expiration = expiration.astimezone(pytz.utc)
        else:
            expiration = expiration.replace(tzinfo=pytz.utc)

        # Turn the datetime into a timestamp (seconds, not microseconds).
        expiration = int(calendar.timegm(expiration.timetuple()))

    if not isinstance(expiration, (int, long)):
        raise TypeError('Expected an integer timestamp, datetime, or '
                        'timedelta. Got %s' % type(expiration))
    return expiration
