# Copyright 2014 Google Inc. All rights reserved.
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

"""Create / interact with gcloud storage buckets.

If you want to check whether a blob exists, you can use the ``in`` operator
in Python::

  >>> print 'kitten.jpg' in bucket
  True
  >>> print 'does-not-exist' in bucket
  False

If you want to get all the blobs in the bucket, you can use
:func:`list_blobs <gcloud.storage.bucket.Bucket.list_blobs>`::

  >>> blobs = bucket.list_blobs()

You can also use the bucket as an iterator::

  >>> for blob in bucket:
  ...   print blob
"""

import datetime
import copy
import os

import pytz
import six

from gcloud._helpers import get_default_project
from gcloud.exceptions import NotFound
from gcloud.storage._helpers import _PropertyMixin
from gcloud.storage._helpers import _require_connection
from gcloud.storage._helpers import _scalar_property
from gcloud.storage.acl import BucketACL
from gcloud.storage.acl import DefaultObjectACL
from gcloud.storage.iterator import Iterator
from gcloud.storage.blob import Blob
from gcloud._helpers import _RFC3339_MICROS


class _BlobIterator(Iterator):
    """An iterator listing blobs in a bucket

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.blob.Bucket` objects.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket from which to list blobs.
    """
    def __init__(self, bucket, extra_params=None):
        self.bucket = bucket
        self.prefixes = ()
        super(_BlobIterator, self).__init__(
            connection=bucket.connection, path=bucket.path + '/o',
            extra_params=extra_params)

    def get_items_from_response(self, response):
        """Yield :class:`.storage.blob.Blob` items from response.

        :type response: dict
        :param response: The JSON API response for a page of blobs.
        """
        self.prefixes = tuple(response.get('prefixes', ()))
        for item in response.get('items', []):
            name = item.get('name')
            blob = Blob(name, bucket=self.bucket)
            blob._set_properties(item)
            yield blob


class Bucket(_PropertyMixin):
    """A class representing a Bucket on Cloud Storage.

    :type name: string
    :param name: The name of the bucket.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use when sending requests.

    :type properties: dictionary or ``NoneType``
    :param properties: The properties associated with the bucket.
    """
    _iterator_class = _BlobIterator

    _MAX_OBJECTS_FOR_BUCKET_DELETE = 256
    """Maximum number of existing objects allowed in Bucket.delete()."""

    def __init__(self, name=None, connection=None):
        super(Bucket, self).__init__(name=name)
        self._connection = connection
        self._acl = BucketACL(self)
        self._default_object_acl = DefaultObjectACL(self)

    def __repr__(self):
        return '<Bucket: %s>' % self.name

    def __iter__(self):
        return iter(self.list_blobs())

    def __contains__(self, blob_name):
        blob = Blob(blob_name, bucket=self)
        return blob.exists()

    def exists(self, connection=None):
        """Determines whether or not this bucket exists.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: boolean
        :returns: True if the bucket exists in Cloud Storage.
        """
        connection = _require_connection(connection)
        try:
            # We only need the status code (200 or not) so we seek to
            # minimize the returned payload.
            query_params = {'fields': 'name'}
            connection.api_request(method='GET', path=self.path,
                                   query_params=query_params)
            return True
        except NotFound:
            return False

    def create(self, project=None, connection=None):
        """Creates current bucket.

        If the bucket already exists, will raise
        :class:`gcloud.exceptions.Conflict`.

        This implements "storage.buckets.insert".

        :type project: string
        :param project: Optional. The project to use when creating bucket.
                        If not provided, falls back to default.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: :class:`gcloud.storage.bucket.Bucket`
        :returns: The newly created bucket.
        :raises: :class:`EnvironmentError` if the project is not given and
                 can't be inferred.
        """
        connection = _require_connection(connection)
        if project is None:
            project = get_default_project()
        if project is None:
            raise EnvironmentError('Project could not be inferred '
                                   'from environment.')

        query_params = {'project': project}
        api_response = connection.api_request(
            method='POST', path='/b', query_params=query_params,
            data={'name': self.name})
        self._set_properties(api_response)

    @property
    def acl(self):
        """Create our ACL on demand."""
        return self._acl

    @property
    def default_object_acl(self):
        """Create our defaultObjectACL on demand."""
        return self._default_object_acl

    @property
    def connection(self):
        """Getter property for the connection to use with this Bucket.

        :rtype: :class:`gcloud.storage.connection.Connection`
        :returns: The connection to use.
        """
        return self._connection

    @staticmethod
    def path_helper(bucket_name):
        """Relative URL path for a bucket.

        :type bucket_name: string
        :param bucket_name: The bucket name in the path.

        :rtype: string
        :returns: The relative URL path for ``bucket_name``.
        """
        return '/b/' + bucket_name

    @property
    def path(self):
        """The URL path to this bucket."""
        if not self.name:
            raise ValueError('Cannot determine path without bucket name.')

        return self.path_helper(self.name)

    def get_blob(self, blob_name, connection=None):
        """Get a blob object by name.

        This will return None if the blob doesn't exist::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> print bucket.get_blob('/path/to/blob.txt')
          <Blob: my-bucket, /path/to/blob.txt>
          >>> print bucket.get_blob('/does-not-exist.txt')
          None

        :type blob_name: string
        :param blob_name: The name of the blob to retrieve.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: :class:`gcloud.storage.blob.Blob` or None
        :returns: The blob object if it exists, otherwise None.
        """
        connection = _require_connection(connection)
        blob = Blob(bucket=self, name=blob_name)
        try:
            response = connection.api_request(method='GET',
                                              path=blob.path)
            name = response.get('name')  # Expect this to be blob_name
            blob = Blob(name, bucket=self)
            blob._set_properties(response)
            return blob
        except NotFound:
            return None

    def list_blobs(self, max_results=None, page_token=None, prefix=None,
                   delimiter=None, versions=None,
                   projection='noAcl', fields=None):
        """Return an iterator used to find blobs in the bucket.

        :type max_results: integer or ``NoneType``
        :param max_results: maximum number of blobs to return.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of blobs. If not
                           passed, will return the first page of blobs.

        :type prefix: string or ``NoneType``
        :param prefix: optional prefix used to filter blobs.

        :type delimiter: string or ``NoneType``
        :param delimiter: optional delimter, used with ``prefix`` to
                          emulate hierarchy.

        :type versions: boolean or ``NoneType``
        :param versions: whether object versions should be returned as
                         separate blobs.

        :type projection: string or ``NoneType``
        :param projection: If used, must be 'full' or 'noAcl'. Defaults to
                           'noAcl'. Specifies the set of properties to return.

        :type fields: string or ``NoneType``
        :param fields: Selector specifying which fields to include in a
                       partial response. Must be a list of fields. For example
                       to get a partial response with just the next page token
                       and the language of each blob returned:
                       'items/contentLanguage,nextPageToken'

        :rtype: :class:`_BlobIterator`.
        :returns: An iterator of blobs.
        """
        extra_params = {}

        if max_results is not None:
            extra_params['maxResults'] = max_results

        if prefix is not None:
            extra_params['prefix'] = prefix

        if delimiter is not None:
            extra_params['delimiter'] = delimiter

        if versions is not None:
            extra_params['versions'] = versions

        extra_params['projection'] = projection

        if fields is not None:
            extra_params['fields'] = fields

        result = self._iterator_class(self, extra_params=extra_params)
        # Page token must be handled specially since the base `Iterator`
        # class has it as a reserved property.
        if page_token is not None:
            result.next_page_token = page_token
        return result

    def delete(self, force=False, connection=None):
        """Delete this bucket.

        The bucket **must** be empty in order to submit a delete request. If
        ``force=True`` is passed, this will first attempt to delete all the
        objects / blobs in the bucket (i.e. try to empty the bucket).

        If the bucket doesn't exist, this will raise
        :class:`gcloud.exceptions.NotFound`.  If the bucket is not empty
        (and ``force=False``), will raise :class:`gcloud.exceptions.Conflict`.

        If ``force=True`` and the bucket contains more than 256 objects / blobs
        this will cowardly refuse to delete the objects (or the bucket). This
        is to prevent accidental bucket deletion and to prevent extremely long
        runtime of this method.

        :type force: boolean
        :param force: If True, empties the bucket's objects then deletes it.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :raises: :class:`ValueError` if ``force`` is ``True`` and the bucket
                 contains more than 256 objects / blobs.
        """
        connection = _require_connection(connection)
        if force:
            blobs = list(self.list_blobs(
                max_results=self._MAX_OBJECTS_FOR_BUCKET_DELETE + 1))
            if len(blobs) > self._MAX_OBJECTS_FOR_BUCKET_DELETE:
                message = (
                    'Refusing to delete bucket with more than '
                    '%d objects. If you actually want to delete '
                    'this bucket, please delete the objects '
                    'yourself before calling Bucket.delete().'
                ) % (self._MAX_OBJECTS_FOR_BUCKET_DELETE,)
                raise ValueError(message)

            # Ignore 404 errors on delete.
            self.delete_blobs(blobs, on_error=lambda blob: None,
                              connection=connection)

        connection.api_request(method='DELETE', path=self.path)

    def delete_blob(self, blob_name, connection=None):
        """Deletes a blob from the current bucket.

        If the blob isn't found (backend 404), raises a
        :class:`gcloud.exceptions.NotFound`.

        For example::

          >>> from gcloud.exceptions import NotFound
          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> print bucket.list_blobs()
          [<Blob: my-bucket, my-file.txt>]
          >>> bucket.delete_blob('my-file.txt')
          >>> try:
          ...   bucket.delete_blob('doesnt-exist')
          ... except NotFound:
          ...   pass

        :type blob_name: string
        :param blob_name: A blob name to delete.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :raises: :class:`gcloud.exceptions.NotFound` (to suppress
                 the exception, call ``delete_blobs``, passing a no-op
                 ``on_error`` callback, e.g.::

                 >>> bucket.delete_blobs([blob], on_error=lambda blob: None)
        """
        connection = _require_connection(connection)
        blob_path = Blob.path_helper(self.path, blob_name)
        connection.api_request(method='DELETE', path=blob_path)

    def delete_blobs(self, blobs, on_error=None, connection=None):
        """Deletes a list of blobs from the current bucket.

        Uses :func:`Bucket.delete_blob` to delete each individual blob.

        :type blobs: list of string or :class:`gcloud.storage.blob.Blob`
        :param blobs: A list of blob names or Blob objects to delete.

        :type on_error: a callable taking (blob)
        :param on_error: If not ``None``, called once for each blob raising
                         :class:`gcloud.exceptions.NotFound`;
                         otherwise, the exception is propagated.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :raises: :class:`gcloud.exceptions.NotFound` (if
                 `on_error` is not passed).
        """
        connection = _require_connection(connection)
        for blob in blobs:
            try:
                blob_name = blob
                if not isinstance(blob_name, six.string_types):
                    blob_name = blob.name
                self.delete_blob(blob_name, connection=connection)
            except NotFound:
                if on_error is not None:
                    on_error(blob)
                else:
                    raise

    @staticmethod
    def copy_blob(blob, destination_bucket, new_name=None,
                  connection=None):
        """Copy the given blob to the given bucket, optionally with a new name.

        :type blob: string or :class:`gcloud.storage.blob.Blob`
        :param blob: The blob to be copied.

        :type destination_bucket: :class:`gcloud.storage.bucket.Bucket`
        :param destination_bucket: The bucket into which the blob should be
                                   copied.

        :type new_name: string
        :param new_name: (optional) the new name for the copied file.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: :class:`gcloud.storage.blob.Blob`
        :returns: The new Blob.
        """
        connection = _require_connection(connection)
        if new_name is None:
            new_name = blob.name
        new_blob = Blob(bucket=destination_bucket, name=new_name)
        api_path = blob.path + '/copyTo' + new_blob.path
        copy_result = connection.api_request(method='POST', path=api_path)
        new_blob._set_properties(copy_result)
        return new_blob

    def upload_file(self, filename, blob_name=None, connection=None):
        """Shortcut method to upload a file into this bucket.

        Use this method to quickly put a local file in Cloud Storage.

        For example::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> bucket.upload_file('~/my-file.txt', 'remote-text-file.txt')
          >>> print bucket.list_blobs()
          [<Blob: my-bucket, remote-text-file.txt>]

        If you don't provide a blob name, we will try to upload the file
        using the local filename (**not** the complete path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> bucket.upload_file('~/my-file.txt')
          >>> print bucket.list_blobs()
          [<Blob: my-bucket, my-file.txt>]

        :type filename: string
        :param filename: Local path to the file you want to upload.

        :type blob_name: string
        :param blob_name: The name of the blob to upload the file to. If this
                          is blank, we will try to upload the file to the root
                          of the bucket with the same name as on your local
                          file system.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: :class:`Blob`
        :returns: The updated Blob object.
        """
        if blob_name is None:
            blob_name = os.path.basename(filename)
        blob = Blob(bucket=self, name=blob_name)
        blob.upload_from_filename(filename, connection=connection)
        return blob

    def upload_file_object(self, file_obj, blob_name=None, connection=None):
        """Shortcut method to upload a file object into this bucket.

        Use this method to quickly put a local file in Cloud Storage.

        For example::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> bucket.upload_file(open('~/my-file.txt'), 'remote-text-file.txt')
          >>> print bucket.list_blobs()
          [<Blob: my-bucket, remote-text-file.txt>]

        If you don't provide a blob name, we will try to upload the file
        using the local filename (**not** the complete path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket('my-bucket', connection=connection)
          >>> bucket.upload_file(open('~/my-file.txt'))
          >>> print bucket.list_blobs()
          [<Blob: my-bucket, my-file.txt>]

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type blob_name: string
        :param blob_name: The name of the blob to upload the file to. If this
                          is blank, we will try to upload the file to the root
                          of the bucket with the same name as on your local
                          file system.

        :type connection: :class:`gcloud.storage.connection.Connection` or
                          ``NoneType``
        :param connection: Optional. The connection to use when sending
                           requests. If not provided, falls back to default.

        :rtype: :class:`Blob`
        :returns: The updated Blob object.
        """
        if blob_name is None:
            blob_name = os.path.basename(file_obj.name)
        blob = Blob(bucket=self, name=blob_name)
        blob.upload_from_file(file_obj, connection=connection)
        return blob

    @property
    def cors(self):
        """Retrieve CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list of dictionaries
        :returns: A sequence of mappings describing each CORS policy.
        """
        return [copy.deepcopy(policy)
                for policy in self._properties.get('cors', ())]

    @cors.setter
    def cors(self, entries):
        """Set CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list of dictionaries
        :param entries: A sequence of mappings describing each CORS policy.
        """
        self._patch_property('cors', entries)

    @property
    def etag(self):
        """Retrieve the ETag for the bucket.

        See: http://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string or ``NoneType``
        :returns: The bucket etag or ``None`` if the property is not
                  set locally.
        """
        return self._properties.get('etag')

    @property
    def id(self):
        """Retrieve the ID for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string or ``NoneType``
        :returns: The ID of the bucket or ``None`` if the property is not
                  set locally.
        """
        return self._properties.get('id')

    @property
    def lifecycle_rules(self):
        """Lifecycle rules configured for this bucket.

        See: https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each lifecycle rule.
        """
        info = self._properties.get('lifecycle', {})
        return [copy.deepcopy(rule) for rule in info.get('rule', ())]

    @lifecycle_rules.setter
    def lifecycle_rules(self, rules):
        """Update the lifecycle rules configured for this bucket.

        See: https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each lifecycle rule.
        """
        self._patch_property('lifecycle', {'rule': rules})

    location = _scalar_property('location')
    """Retrieve location configured for this bucket.

    See: https://cloud.google.com/storage/docs/json_api/v1/buckets and
    https://cloud.google.com/storage/docs/concepts-techniques#specifyinglocations

    If the property is not set locally, returns ``None``.

    :rtype: string or ``NoneType``
    """

    def get_logging(self):
        """Return info about access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#status

        :rtype: dict or None
        :returns: a dict w/ keys, ``logBucket`` and ``logObjectPrefix``
                  (if logging is enabled), or None (if not).
        """
        info = self._properties.get('logging')
        return copy.deepcopy(info)

    def enable_logging(self, bucket_name, object_prefix=''):
        """Enable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#delivery

        :type bucket_name: string
        :param bucket_name: name of bucket in which to store access logs

        :type object_prefix: string
        :param object_prefix: prefix for access log filenames
        """
        info = {'logBucket': bucket_name, 'logObjectPrefix': object_prefix}
        self._patch_property('logging', info)

    def disable_logging(self):
        """Disable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#disabling
        """
        self._patch_property('logging', None)

    @property
    def metageneration(self):
        """Retrieve the metageneration for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: integer or ``NoneType``
        :returns: The metageneration of the bucket or ``None`` if the property
                  is not set locally.
        """
        metageneration = self._properties.get('metageneration')
        if metageneration is not None:
            return int(metageneration)

    @property
    def owner(self):
        """Retrieve info about the owner of the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: dict or ``NoneType``
        :returns: Mapping of owner's role/ID. If the property is not set
                  locally, returns ``None``.
        """
        return copy.deepcopy(self._properties.get('owner'))

    @property
    def project_number(self):
        """Retrieve the number of the project to which the bucket is assigned.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: integer or ``NoneType``
        :returns: The project number that owns the bucket or ``None`` if the
                  property is not set locally.
        """
        project_number = self._properties.get('projectNumber')
        if project_number is not None:
            return int(project_number)

    @property
    def self_link(self):
        """Retrieve the URI for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string or ``NoneType``
        :returns: The self link for the bucket or ``None`` if the property is
                  not set locally.
        """
        return self._properties.get('selfLink')

    @property
    def storage_class(self):
        """Retrieve the storage class for the bucket.

        See: https://cloud.google.com/storage/docs/storage-classes
        https://cloud.google.com/storage/docs/nearline-storage
        https://cloud.google.com/storage/docs/durable-reduced-availability

        :rtype: string or ``NoneType``
        :returns: If set, one of "STANDARD", "NEARLINE", or
                  "DURABLE_REDUCED_AVAILABILITY", else ``None``.
        """
        return self._properties.get('storageClass')

    @property
    def time_created(self):
        """Retrieve the timestamp at which the bucket was created.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get('timeCreated')
        if value is not None:
            naive = datetime.datetime.strptime(value, _RFC3339_MICROS)
            return naive.replace(tzinfo=pytz.utc)

    @property
    def versioning_enabled(self):
        """Is versioning enabled for this bucket?

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :rtype: boolean
        :returns: True if enabled, else False.
        """
        versioning = self._properties.get('versioning', {})
        return versioning.get('enabled', False)

    @versioning_enabled.setter
    def versioning_enabled(self, value):
        """Enable versioning for this bucket.

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :type value: convertible to boolean
        :param value: should versioning be anabled for the bucket?
        """
        self._patch_property('versioning', {'enabled': bool(value)})

    def configure_website(self, main_page_suffix=None, not_found_page=None):
        """Configure website-related properties.

        See: https://developers.google.com/storage/docs/website-configuration

        .. note::
          This (apparently) only works
          if your bucket name is a domain name
          (and to do that, you need to get approved somehow...).

        If you want this bucket to host a website, just provide the name
        of an index page and a page to use when a blob isn't found::

          >>> from gcloud import storage
          >>> connection = storage.get_connection()
          >>> bucket = storage.get_bucket(bucket_name, connection=connection)
          >>> bucket.configure_website('index.html', '404.html')

        You probably should also make the whole bucket public::

          >>> bucket.make_public(recursive=True, future=True)

        This says: "Make the bucket public, and all the stuff already in
        the bucket, and anything else I add to the bucket.  Just make it
        all public."

        :type main_page_suffix: string
        :param main_page_suffix: The page to use as the main page
                                 of a directory.
                                 Typically something like index.html.

        :type not_found_page: string
        :param not_found_page: The file to use when a page isn't found.
        """
        data = {
            'mainPageSuffix': main_page_suffix,
            'notFoundPage': not_found_page,
        }
        self._patch_property('website', data)

    def disable_website(self):
        """Disable the website configuration for this bucket.

        This is really just a shortcut for setting the website-related
        attributes to ``None``.
        """
        return self.configure_website(None, None)

    def make_public(self, recursive=False, future=False):
        """Make a bucket public.

        :type recursive: boolean
        :param recursive: If True, this will make all blobs inside the bucket
                          public as well.

        :type future: boolean
        :param future: If True, this will make all objects created in the
                       future public as well.
        """
        self.acl.all().grant_read()
        self.acl.save()

        if future:
            doa = self.default_object_acl
            if not doa.loaded:
                doa.reload()
            doa.all().grant_read()
            doa.save()

        if recursive:
            for blob in self:
                blob.acl.all().grant_read()
                blob.save_acl()
