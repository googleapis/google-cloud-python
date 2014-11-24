"""Create / interact with gcloud storage buckets."""

import os

from gcloud.storage._helpers import _PropertyMixin
from gcloud.storage._helpers import _scalar_property
from gcloud.storage import exceptions
from gcloud.storage.acl import BucketACL
from gcloud.storage.acl import DefaultObjectACL
from gcloud.storage.iterator import Iterator
from gcloud.storage.key import Key
import six


class _KeyIterator(Iterator):
    """An iterator listing keys in a bucket

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.key.Bucket` objects.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket from which to list keys.
    """
    def __init__(self, bucket, extra_params=None):
        self.bucket = bucket
        self.prefixes = ()
        super(_KeyIterator, self).__init__(
            connection=bucket.connection, path=bucket.path + '/o',
            extra_params=extra_params)

    def get_items_from_response(self, response):
        """Yield :class:`.storage.key.Key` items from response.

        :type response: dict
        :param response: The JSON API response for a page of keys.
        """
        self.prefixes = tuple(response.get('prefixes', ()))
        for item in response.get('items', []):
            yield Key.from_dict(item, bucket=self.bucket)


class Bucket(_PropertyMixin):
    """A class representing a Bucket on Cloud Storage.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use when sending requests.

    :type name: string
    :param name: The name of the bucket.
    """
    _iterator_class = _KeyIterator

    CUSTOM_PROPERTY_ACCESSORS = {
        'acl': 'acl',
        'cors': 'get_cors()',
        'defaultObjectAcl': 'get_default_object_acl()',
        'etag': 'etag',
        'id': 'id',
        'lifecycle': 'get_lifecycle()',
        'location': 'location',
        'logging': 'get_logging()',
        'metageneration': 'metageneration',
        'name': 'name',
        'owner': 'owner',
        'projectNumber': 'project_number',
        'selfLink': 'self_link',
        'storageClass': 'storage_class',
        'timeCreated': 'time_created',
        'versioning': 'versioning_enabled',
    }
    """Map field name -> accessor for fields w/ custom accessors."""

    # ACL rules are lazily retrieved.
    _acl = _default_object_acl = None

    def __init__(self, connection=None, name=None, properties=None):
        super(Bucket, self).__init__(name=name, properties=properties)
        self._connection = connection

    @classmethod
    def from_dict(cls, bucket_dict, connection=None):
        """Construct a new bucket from a dictionary of data from Cloud Storage.

        :type bucket_dict: dict
        :param bucket_dict: The dictionary of data to construct a bucket from.

        :rtype: :class:`Bucket`
        :returns: A bucket constructed from the data provided.
        """
        return cls(connection=connection, name=bucket_dict['name'],
                   properties=bucket_dict)

    def __repr__(self):
        return '<Bucket: %s>' % self.name

    def __iter__(self):
        return iter(self._iterator_class(bucket=self))

    def __contains__(self, key):
        return self.get_key(key) is not None

    @property
    def acl(self):
        """Create our ACL on demand."""
        if self._acl is None:
            self._acl = BucketACL(self)
        return self._acl

    @property
    def default_object_acl(self):
        """Create our defaultObjectACL on demand."""
        if self._default_object_acl is None:
            self._default_object_acl = DefaultObjectACL(self)
        return self._default_object_acl

    @property
    def connection(self):
        """Getter property for the connection to use with this Bucket.

        :rtype: :class:`gcloud.storage.connection.Connection`
        :returns: The connection to use.
        """
        return self._connection

    @property
    def path(self):
        """The URL path to this bucket."""
        if not self.name:
            raise ValueError('Cannot determine path without bucket name.')

        return '/b/' + self.name

    def get_key(self, key):
        """Get a key object by name.

        This will return None if the key doesn't exist::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> print bucket.get_key('/path/to/key.txt')
          <Key: my-bucket, /path/to/key.txt>
          >>> print bucket.get_key('/does-not-exist.txt')
          None

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The name of the key to retrieve.

        :rtype: :class:`gcloud.storage.key.Key` or None
        :returns: The key object if it exists, otherwise None.
        """
        # Coerce this to a key object (either from a Key or a string).
        key = self.new_key(key)

        try:
            response = self.connection.api_request(method='GET', path=key.path)
            return Key.from_dict(response, bucket=self)
        except exceptions.NotFound:
            return None

    def get_all_keys(self):
        """List all the keys in this bucket.

        This will **not** retrieve all the data for all the keys, it
        will only retrieve the keys.

        This is equivalent to::

          keys = [key for key in bucket]

        :rtype: list of :class:`gcloud.storage.key.Key`
        :returns: A list of all the Key objects in this bucket.
        """
        return list(self)

    def iterator(self, prefix=None, delimiter=None, max_results=None,
                 versions=None):
        """Return an iterator used to find keys in the bucket.

        :type prefix: string or None
        :param prefix: optional prefix used to filter keys.

        :type delimiter: string or None
        :param delimiter: optional delimter, used with ``prefix`` to
                          emulate hierarchy.

        :type max_results: integer or None
        :param max_results: maximum number of keys to return.

        :type versions: boolean or None
        :param versions: whether object versions should be returned as
                         separate keys.

        :rtype: :class:`_KeyIterator`
        """
        extra_params = {}

        if prefix is not None:
            extra_params['prefix'] = prefix

        if delimiter is not None:
            extra_params['delimiter'] = delimiter

        if max_results is not None:
            extra_params['maxResults'] = max_results

        if versions is not None:
            extra_params['versions'] = versions

        return self._iterator_class(self, extra_params=extra_params)

    def new_key(self, key):
        """Given path name (or Key), return a :class:`.storage.key.Key` object.

        This is really useful when you're not sure if you have a Key
        object or a string path name.  Given either of those types, this
        returns the corresponding Key object.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: A path name or actual key object.

        :rtype: :class:`gcloud.storage.key.Key`
        :returns: A Key object with the path provided.
        """
        if isinstance(key, Key):
            return key

        if isinstance(key, six.string_types):
            return Key(bucket=self, name=key)

        raise TypeError('Invalid key: %s' % key)

    def delete(self, force=False):
        """Delete this bucket.

        The bucket **must** be empty in order to delete it.  If the
        bucket doesn't exist, this will raise a
        :class:`gcloud.storage.exceptions.NotFound`.  If the bucket
        is not empty, this will raise an Exception.

        If you want to delete a non-empty bucket you can pass in a force
        parameter set to true.  This will iterate through the bucket's
        keys and delete the related objects, before deleting the bucket.

        :type force: bool
        :param full: If True, empties the bucket's objects then deletes it.

        :raises: :class:`gcloud.storage.exceptions.NotFound` if the
                 bucket does not exist, or
                 :class:`gcloud.storage.exceptions.Conflict` if the
                 bucket has keys and `force` is not passed.
        """
        return self.connection.delete_bucket(self.name, force=force)

    def delete_key(self, key):
        """Deletes a key from the current bucket.

        If the key isn't found,
        this will throw a :class:`gcloud.storage.exceptions.NotFound`.

        For example::

          >>> from gcloud import storage
          >>> from gcloud.storage import exceptions
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, my-file.txt>]
          >>> bucket.delete_key('my-file.txt')
          >>> try:
          ...   bucket.delete_key('doesnt-exist')
          ... except exceptions.NotFound:
          ...   pass


        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: A key name or Key object to delete.

        :rtype: :class:`gcloud.storage.key.Key`
        :returns: The key that was just deleted.
        :raises: :class:`gcloud.storage.exceptions.NotFound` (to suppress
                 the exception, call ``delete_keys``, passing a no-op
                 ``on_error`` callback, e.g.::

                 >>> bucket.delete_keys([key], on_error=lambda key: pass)
        """
        key = self.new_key(key)
        self.connection.api_request(method='DELETE', path=key.path)
        return key

    def delete_keys(self, keys, on_error=None):
        """Deletes a list of keys from the current bucket.

        Uses :func:`Bucket.delete_key` to delete each individual key.

        :type keys: list of string or :class:`gcloud.storage.key.Key`
        :param keys: A list of key names or Key objects to delete.

        :type on_error: a callable taking (key)
        :param on_error: If not ``None``, called once for each key raising
                         :class:`gcloud.storage.exceptions.NotFound`;
                         otherwise, the exception is propagated.

        :raises: :class:`gcloud.storage.exceptions.NotFound` (if
                 `on_error` is not passed).
        """
        for key in keys:
            try:
                self.delete_key(key)
            except exceptions.NotFound:
                if on_error is not None:
                    on_error(key)
                else:
                    raise

    def copy_key(self, key, destination_bucket, new_name=None):
        """Copy the given key to the given bucket, optionally with a new name.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The key to be copied.

        :type destination_bucket: :class:`gcloud.storage.bucket.Bucket`
        :param destination_bucket: The bucket into which the key should be
                                   copied.

        :type new_name: string
        :param new_name: (optional) the new name for the copied file.

        :rtype: :class:`gcloud.storage.key.Key`
        :returns: The new Key.
        """
        if new_name is None:
            new_name = key.name
        new_key = destination_bucket.new_key(new_name)
        api_path = key.path + '/copyTo' + new_key.path
        self.connection.api_request(method='POST', path=api_path)
        return new_key

    def upload_file(self, filename, key=None):
        """Shortcut method to upload a file into this bucket.

        Use this method to quickly put a local file in Cloud Storage.

        For example::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file('~/my-file.txt', 'remote-text-file.txt')
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, remote-text-file.txt>]

        If you don't provide a key value, we will try to upload the file
        using the local filename as the key (**not** the complete
        path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file('~/my-file.txt')
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, my-file.txt>]

        :type filename: string
        :param filename: Local path to the file you want to upload.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The key (either an object or a remote path) of where
                    to put the file.  If this is blank, we will try to
                    upload the file to the root of the bucket with the
                    same name as on your local file system.
        """
        if key is None:
            key = os.path.basename(filename)
        key = self.new_key(key)
        key.upload_from_filename(filename)
        return key

    def upload_file_object(self, file_obj, key=None):
        """Shortcut method to upload a file object into this bucket.

        Use this method to quickly put a local file in Cloud Storage.

        For example::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file(open('~/my-file.txt'), 'remote-text-file.txt')
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, remote-text-file.txt>]

        If you don't provide a key value, we will try to upload the file
        using the local filename as the key (**not** the complete
        path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file(open('~/my-file.txt'))
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, my-file.txt>]

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The key (either an object or a remote path) of where
                    to put the file.  If this is blank, we will try to
                    upload the file to the root of the bucket with the
                    same name as on your local file system.
        """
        if key:
            key = self.new_key(key)
        else:
            key = self.new_key(os.path.basename(file_obj.name))
        return key.upload_from_file(file_obj)

    def get_cors(self):
        """Retrieve CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each CORS policy.
        """
        return [policy.copy() for policy in self.properties.get('cors', ())]

    def update_cors(self, entries):
        """Update CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list(dict)
        :param entries: A sequence of mappings describing each CORS policy.
        """
        self._patch_properties({'cors': entries})

    def get_default_object_acl(self):
        """Get the current Default Object ACL rules.

        If the acl isn't available locally, this method will reload it from
        Cloud Storage.

        :rtype: :class:`gcloud.storage.acl.DefaultObjectACL`
        :returns: A DefaultObjectACL object for this bucket.
        """
        if not self.default_object_acl.loaded:
            self.default_object_acl.reload()
        return self.default_object_acl

    @property
    def etag(self):
        """Retrieve the ETag for the bucket.

        See: http://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string
        """
        return self.properties['etag']

    @property
    def id(self):
        """Retrieve the ID for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string
        """
        return self.properties['id']

    def get_lifecycle(self):
        """Retrieve lifecycle rules configured for this bucket.

        See: https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each lifecycle rule.
        """
        info = self.properties.get('lifecycle', {})
        return [rule.copy() for rule in info.get('rule', ())]

    def update_lifecycle(self, rules):
        """Update CORS policies configured for this bucket.

        See: https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type rules: list(dict)
        :param rules: A sequence of mappings describing each lifecycle rule.
        """
        self._patch_properties({'lifecycle': {'rule': rules}})

    location = _scalar_property('location')
    """Retrieve location configured for this bucket.

    See: https://cloud.google.com/storage/docs/json_api/v1/buckets and
    https://cloud.google.com/storage/docs/concepts-techniques#specifyinglocations

    :rtype: string
    """

    def get_logging(self):
        """Return info about access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#status

        :rtype: dict or None
        :returns: a dict w/ keys, ``logBucket`` and ``logObjectPrefix``
                  (if logging is enabled), or None (if not).
        """
        info = self.properties.get('logging')
        if info is not None:
            return info.copy()

    def enable_logging(self, bucket_name, object_prefix=''):
        """Enable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#delivery

        :type bucket_name: string
        :param bucket_name: name of bucket in which to store access logs

        :type object_prefix: string
        :param object_prefix: prefix for access log filenames
        """
        info = {'logBucket': bucket_name, 'logObjectPrefix': object_prefix}
        self._patch_properties({'logging': info})

    def disable_logging(self):
        """Disable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/accesslogs#disabling
        """
        self._patch_properties({'logging': None})

    @property
    def metageneration(self):
        """Retrieve the metageneration for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: integer
        """
        return self.properties['metageneration']

    @property
    def owner(self):
        """Retrieve info about the owner of the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: dict
        :returns: mapping of owner's role/ID.
        """
        return self.properties['owner'].copy()

    @property
    def project_number(self):
        """Retrieve the number of the project to which the bucket is assigned.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: integer
        """
        return self.properties['projectNumber']

    @property
    def self_link(self):
        """Retrieve the URI for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string
        """
        return self.properties['selfLink']

    @property
    def storage_class(self):
        """Retrieve the storage class for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets and
        https://cloud.google.com/storage/docs/durable-reduced-availability

        :rtype: string
        :returns: Currently one of "STANDARD", "DURABLE_REDUCED_AVAILABILITY"
        """
        return self.properties['storageClass']

    @property
    def time_created(self):
        """Retrieve the timestamp at which the bucket was created.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: string
        :returns: timestamp in RFC 3339 format.
        """
        return self.properties['timeCreated']

    @property
    def versioning_enabled(self):
        """Is versioning enabled for this bucket?

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :rtype: boolean
        :returns: True if enabled, else False.
        """
        versioning = self.properties.get('versioning', {})
        return versioning.get('enabled', False)

    @versioning_enabled.setter
    def versioning_enabled(self, value):
        """Enable versioning for this bucket.

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :type value: convertible to bool
        :param value: should versioning be anabled for the bucket?
        """
        self._patch_properties({'versioning': {'enabled': bool(value)}})

    def configure_website(self, main_page_suffix=None, not_found_page=None):
        """Configure website-related properties.

        See: https://developers.google.com/storage/docs/website-configuration

        .. note::
          This (apparently) only works
          if your bucket name is a domain name
          (and to do that, you need to get approved somehow...).

        If you want this bucket to host a website, just provide the name
        of an index page and a page to use when a key isn't found::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email,
                                                  private_key_path)
          >>> bucket = connection.get_bucket(bucket_name)
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
            'website': {
                'mainPageSuffix': main_page_suffix,
                'notFoundPage': not_found_page,
            },
        }
        return self._patch_properties(data)

    def disable_website(self):
        """Disable the website configuration for this bucket.

        This is really just a shortcut for setting the website-related
        attributes to ``None``.
        """
        return self.configure_website(None, None)

    def make_public(self, recursive=False, future=False):
        """Make a bucket public.

        :type recursive: bool
        :param recursive: If True, this will make all keys inside the bucket
                          public as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future public as well.
        """
        self.acl.all().grant_read()
        self.acl.save()

        if future:
            doa = self.get_default_object_acl()
            doa.all().grant_read()
            doa.save()

        if recursive:
            for key in self:
                key.acl.all().grant_read()
                key.save_acl()
