"""Create / interact with gcloud storage buckets."""

import os

from gcloud.storage._helpers import _MetadataMixin
from gcloud.storage import exceptions
from gcloud.storage.acl import BucketACL
from gcloud.storage.acl import DefaultObjectACL
from gcloud.storage.iterator import Iterator
from gcloud.storage.key import Key
from gcloud.storage.key import _KeyIterator


class Bucket(_MetadataMixin):
    """A class representing a Bucket on Cloud Storage.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use when sending requests.

    :type name: string
    :param name: The name of the bucket.
    """

    CUSTOM_METADATA_FIELDS = {
        'acl': 'get_acl',
        'defaultObjectAcl': 'get_default_object_acl',
        'cors': 'get_cors',
    }
    """Mapping of field name -> accessor for fields w/ custom accessors."""

    # ACL rules are lazily retrieved.
    _acl = _default_object_acl = None

    def __init__(self, connection=None, name=None, metadata=None):
        super(Bucket, self).__init__(name=name, metadata=metadata)
        self._connection = connection

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

    @classmethod
    def from_dict(cls, bucket_dict, connection=None):
        """Construct a new bucket from a dictionary of data from Cloud Storage.

        :type bucket_dict: dict
        :param bucket_dict: The dictionary of data to construct a bucket from.

        :rtype: :class:`Bucket`
        :returns: A bucket constructed from the data provided.
        """
        return cls(connection=connection, name=bucket_dict['name'],
                   metadata=bucket_dict)

    def __repr__(self):
        return '<Bucket: %s>' % self.name

    def __iter__(self):
        return iter(_KeyIterator(bucket=self))

    def __contains__(self, key):
        return self.get_key(key) is not None

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
        except exceptions.NotFoundError:
            return None

    def get_all_keys(self):
        """List all the keys in this bucket.

        This will **not** retrieve all the data for all the keys, it
        will only retrieve metadata about the keys.

        This is equivalent to::

          keys = [key for key in bucket]

        :rtype: list of :class:`gcloud.storage.key.Key`
        :returns: A list of all the Key objects in this bucket.
        """
        return list(self)

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

        # Support Python 2 and 3.
        try:
            string_type = basestring
        except NameError:  # pragma: NO COVER PY3k
            string_type = str

        if isinstance(key, string_type):
            return Key(bucket=self, name=key)

        raise TypeError('Invalid key: %s' % key)

    def delete(self, force=False):
        """Delete this bucket.

        The bucket **must** be empty in order to delete it.  If the
        bucket doesn't exist, this will raise a
        :class:`gcloud.storage.exceptions.NotFoundError`.  If the bucket
        is not empty, this will raise an Exception.

        If you want to delete a non-empty bucket you can pass in a force
        parameter set to true.  This will iterate through the bucket's
        keys and delete the related objects, before deleting the bucket.

        :type force: bool
        :param full: If True, empties the bucket's objects then deletes it.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError` if the
                 bucket does not exist, or
                 :class:`gcloud.storage.exceptions.ConnectionError` if the
                 bucket has keys and `force` is not passed.
        """
        return self.connection.delete_bucket(self.name, force=force)

    def delete_key(self, key):
        """Deletes a key from the current bucket.

        If the key isn't found,
        this will throw a :class:`gcloud.storage.exceptions.NotFoundError`.

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
          ... except exceptions.NotFoundError:
          ...   pass


        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: A key name or Key object to delete.

        :rtype: :class:`gcloud.storage.key.Key`
        :returns: The key that was just deleted.
        :raises: :class:`gcloud.storage.exceptions.NotFoundError` (to suppress
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
                         :class:`gcloud.storage.exceptions.NotFoundError`;
                         otherwise, the exception is propagated.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError` (if
                 `on_error` is not passed).
        """
        for key in keys:
            try:
                self.delete_key(key)
            except exceptions.NotFoundError:
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
        return key.set_contents_from_filename(filename)

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
        return key.set_contents_from_file(file_obj)

    def configure_website(self, main_page_suffix=None, not_found_page=None):
        """Configure website-related metadata.

        .. note::
          This (apparently) only works
          if your bucket name is a domain name
          (and to do that, you need to get approved somehow...).

          Check out the official documentation here:
          https://developers.google.com/storage/docs/website-configuration

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
        return self.patch_metadata(data)

    def disable_website(self):
        """Disable the website configuration for this bucket.

        This is really just a shortcut for setting the website-related
        attributes to ``None``.
        """
        return self.configure_website(None, None)

    def get_acl(self):
        """Get ACL metadata as a :class:`gcloud.storage.acl.BucketACL` object.

        :rtype: :class:`gcloud.storage.acl.BucketACL`
        :returns: An ACL object for the current bucket.
        """
        if not self.acl.loaded:
            self.acl.reload()
        return self.acl

    def get_default_object_acl(self):
        """Get the current Default Object ACL rules.

        If the appropriate metadata isn't available locally, this method
        will reload it from Cloud Storage.

        :rtype: :class:`gcloud.storage.acl.DefaultObjectACL`
        :returns: A DefaultObjectACL object for this bucket.
        """
        if not self.default_object_acl.loaded:
            self.default_object_acl.reload()
        return self.default_object_acl

    def make_public(self, recursive=False, future=False):
        """Make a bucket public.

        :type recursive: bool
        :param recursive: If True, this will make all keys inside the bucket
                          public as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future public as well.
        """
        self.get_acl().all().grant_read()
        self.acl.save()

        if future:
            doa = self.get_default_object_acl()
            doa.all().grant_read()
            doa.save()

        if recursive:
            for key in self:
                key.get_acl().all().grant_read()
                key.save_acl()

    def get_cors(self):
        """Retrieve CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each CORS policy.
                  Keys include 'max_age', 'methods', 'origins', and
                  'headers'.
        """
        if not self.has_metadata('cors'):
            self.reload_metadata()
        result = []
        for entry in self.metadata.get('cors', ()):
            entry = entry.copy()
            result.append(entry)
            if 'maxAgeSeconds' in entry:
                entry['max_age'] = entry.pop('maxAgeSeconds')
            if 'method' in entry:
                entry['methods'] = entry.pop('method')
            if 'origin' in entry:
                entry['origins'] = entry.pop('origin')
            if 'responseHeader' in entry:
                entry['headers'] = entry.pop('responseHeader')
        return result

    def update_cors(self, entries):
        """Update CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list(dict)
        :param entries: A sequence of mappings describing each CORS policy.
                        Keys include 'max_age', 'methods', 'origins', and
                        'headers'.
        """
        to_patch = []
        for entry in entries:
            entry = entry.copy()
            to_patch.append(entry)
            if 'max_age' in entry:
                entry['maxAgeSeconds'] = entry.pop('max_age')
            if 'methods' in entry:
                entry['method'] = entry.pop('methods')
            if 'origins' in entry:
                entry['origin'] = entry.pop('origins')
            if 'headers' in entry:
                entry['responseHeader'] = entry.pop('headers')
        self.patch_metadata({'cors': to_patch})


class BucketIterator(Iterator):
    """An iterator listing all buckets.

    You shouldn't have to use this directly, but instead should use the helper
    methods on :class:`gcloud.storage.connection.Connection` objects.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use for querying the list of buckets.
    """

    def __init__(self, connection):
        super(BucketIterator, self).__init__(connection=connection, path='/b')

    def get_items_from_response(self, response):
        """Factory method which yields :class:`.Bucket` items from a response.

        :type response: dict
        :param response: The JSON API response for a page of buckets.
        """
        for item in response.get('items', []):
            yield Bucket.from_dict(item, connection=self.connection)
