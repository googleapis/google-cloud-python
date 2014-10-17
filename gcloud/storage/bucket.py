"""Create / interact with gcloud storage buckets."""

import os

from gcloud.storage._helpers import _MetadataMixin
from gcloud.storage import exceptions
from gcloud.storage.acl import BucketACL
from gcloud.storage.acl import DefaultObjectACL
from gcloud.storage.iterator import KeyIterator
from gcloud.storage.key import Key


class Bucket(_MetadataMixin):
    """A class representing a Bucket on Cloud Storage.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use when sending requests.

    :type name: string
    :param name: The name of the bucket.
    """

    LOAD_FULL_FIELDS = ('acl', 'defaultObjectAcl')
    """Tuple of metadata fields pertaining to bucket ACLs."""

    ACL_CLASS = BucketACL
    """Class which holds ACL data for buckets."""

    ACL_KEYWORD = 'bucket'
    """Keyword for BucketACL constructor to pass a bucket in."""

    def __init__(self, connection=None, name=None, metadata=None):
        super(Bucket, self).__init__()

        self._connection = connection
        self.name = name
        self.metadata = metadata

        # ACL rules are lazily retrieved.
        self.acl = None
        self.default_object_acl = None

    # NOTE: Could also put this in _MetadataMixin.
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
        return iter(KeyIterator(bucket=self))

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

        This will **not** retrieve all the data for all the keys,
        it will only retrieve metadata about the keys.

        This is equivalent to::

          keys = [key for key in bucket]

        :rtype: list of :class:`gcloud.storage.key.Key`
        :returns: A list of all the Key objects in this bucket.
        """

        return list(self)

    def new_key(self, key):
        """Given path name (or Key), return a :class:`.storage.key.Key` object.

        This is really useful when you're not sure
        if you have a Key object or a string path name.
        Given either of those types,
        this returns the corresponding Key object.

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

        The bucket **must** be empty in order to delete it.
        If the bucket doesn't exist,
        this will raise a :class:`gcloud.storage.exceptions.NotFoundError`.
        If the bucket is not empty,
        this will raise an Exception.

        If you want to delete a non-empty bucket you can pass
        in a force parameter set to true.
        This will iterate through the bucket's keys and delete the
        related objects, before deleting the bucket.

        :type force: bool
        :param full: If True, empties the bucket's objects then deletes it.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
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
        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """

        key = self.new_key(key)
        self.connection.api_request(method='DELETE', path=key.path)
        return key

    def delete_keys(self, keys):
        """Deletes a list of keys from the current bucket.

        Uses :func:`Bucket.delete_key` to delete each individual key.

        :type keys: list of string or :class:`gcloud.storage.key.Key`
        :param key: A list of key names or Key objects to delete.
        """
        # NOTE: boto returns a MultiDeleteResult instance.
        for key in keys:
            self.delete_key(key)

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

        If you don't provide a key value,
        we will try to upload the file using the local filename
        as the key
        (**not** the complete path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file('~/my-file.txt')
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, my-file.txt>]

        :type filename: string
        :param filename: Local path to the file you want to upload.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The key (either an object or a remote path)
                    of where to put the file.

                    If this is blank,
                    we will try to upload the file
                    to the root of the bucket
                    with the same name as on your local file system.
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

        If you don't provide a key value,
        we will try to upload the file using the local filename
        as the key
        (**not** the complete path)::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email, key_path)
          >>> bucket = connection.get_bucket('my-bucket')
          >>> bucket.upload_file(open('~/my-file.txt'))
          >>> print bucket.get_all_keys()
          [<Key: my-bucket, my-file.txt>]

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type key: string or :class:`gcloud.storage.key.Key`
        :param key: The key (either an object or a remote path)
                    of where to put the file.

                    If this is blank,
                    we will try to upload the file
                    to the root of the bucket
                    with the same name as on your local file system.
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

        If you want this bucket to host a website,
        just provide the name of an index page
        and a page to use when a key isn't found::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email,
                                                  private_key_path)
          >>> bucket = connection.get_bucket(bucket_name)
          >>> bucket.configure_website('index.html', '404.html')

        You probably should also make the whole bucket public::

          >>> bucket.make_public(recursive=True, future=True)

        This says:
        "Make the bucket public,
        and all the stuff already in the bucket,
        and anything else I add to the bucket.
        Just make it all public."

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

        This is really just a shortcut for
        setting the website-related attributes to ``None``.
        """

        return self.configure_website(None, None)

    def reload_default_object_acl(self):
        """Reload the Default Object ACL rules for this bucket.

        :rtype: :class:`Bucket`
        :returns: The current bucket.
        """

        self.default_object_acl = DefaultObjectACL(bucket=self)

        for entry in self.get_metadata('defaultObjectAcl', []):
            entity = self.default_object_acl.entity_from_dict(entry)
            self.default_object_acl.add_entity(entity)

        return self

    def get_default_object_acl(self):
        """Get the current Default Object ACL rules.

        If the appropriate metadata isn't available locally,
        this method will reload it from Cloud Storage.

        :rtype: :class:`gcloud.storage.acl.DefaultObjectACL`
        :returns: A DefaultObjectACL object for this bucket.
        """

        if not self.default_object_acl:
            self.reload_default_object_acl()
        return self.default_object_acl

    def save_default_object_acl(self, acl=None):
        """Save the Default Object ACL rules for this bucket.

        :type acl: :class:`gcloud.storage.acl.DefaultObjectACL`
        :param acl: The DefaultObjectACL object to save.
                    If not provided, this will look at
                    the ``default_object_acl`` property
                    and save that.
        """

        if acl is None:
            acl = self.default_object_acl

        if acl is None:
            return self

        self.patch_metadata({'defaultObjectAcl': list(acl)})
        self.reload_default_object_acl()
        return self

    def clear_default_object_acl(self):
        """Remove the Default Object ACL from this bucket."""

        return self.save_default_object_acl(acl=[])

    def make_public(self, recursive=False, future=False):
        """Make a bucket public.

        :type recursive: bool
        :param recursive: If True, this will make all keys inside the bucket
                          public as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future public as well.
        """
        super(Bucket, self).make_public()

        if future:
            self.get_default_object_acl().all().grant_read()
            self.save_default_object_acl()

        if recursive:
            for key in self:
                key.get_acl().all().grant_read()
                key.save_acl()
