"""Create / interact with gcloud storage keys."""

import mimetypes
import os
from StringIO import StringIO

from gcloud.storage.acl import ObjectACL
from gcloud.storage.exceptions import StorageError
from gcloud.storage.iterator import Iterator


class Key(object):
    """A wrapper around Cloud Storage's concept of an ``Object``."""

    CHUNK_SIZE = 1024 * 1024  # 1 MB.
    """The size of a chunk of data whenever iterating (1 MB).

    This must be a multiple of 256 KB per the API specification.
    """
    # ACL rules are lazily retrieved.
    _acl = None

    def __init__(self, bucket=None, name=None, metadata=None):
        """Key constructor.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs.

        :type name: string
        :param name: The name of the key.  This corresponds to the
                     unique path of the object in the bucket.

        :type metadata: dict
        :param metadata: All the other data provided by Cloud Storage.
        """
        self.bucket = bucket
        self.name = name
        self.metadata = metadata or {}

    @property
    def acl(self):
        """Create our ACL on demand."""
        if self._acl is None:
            self._acl = ObjectACL(self)
        return self._acl

    @classmethod
    def from_dict(cls, key_dict, bucket=None):
        """Instantiate a :class:`Key` from data returned by the JSON API.

        :type key_dict: dict
        :param key_dict: A dictionary of data returned from getting an
                         Cloud Storage object.

        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this key belongs (and by
                       proxy, which connection to use).

        :rtype: :class:`Key`
        :returns: A key based on the data provided.
        """

        return cls(bucket=bucket, name=key_dict['name'], metadata=key_dict)

    def __repr__(self):
        if self.bucket:
            bucket_name = self.bucket.name
        else:
            bucket_name = None

        return '<Key: %s, %s>' % (bucket_name, self.name)

    @property
    def connection(self):
        """Getter property for the connection to use with this Key.

        :rtype: :class:`gcloud.storage.connection.Connection` or None
        :returns: The connection to use, or None if no connection is set.
        """
        if self.bucket and self.bucket.connection:
            return self.bucket.connection

    @property
    def path(self):
        """Getter property for the URL path to this Key.

        :rtype: string
        :returns: The URL path to this Key.
        """
        if not self.bucket:
            raise ValueError('Cannot determine path without a bucket defined.')
        elif not self.name:
            raise ValueError('Cannot determine path without a key name.')

        return self.bucket.path + '/o/' + self.name

    @property
    def public_url(self):
        """The public URL for this key's object.

        :rtype: `string`
        :returns: The public URL for this key.
        """
        return '{storage_base_url}/{self.bucket.name}/{self.name}'.format(
            storage_base_url='http://commondatastorage.googleapis.com',
            self=self)

    def generate_signed_url(self, expiration, method='GET'):
        """Generates a signed URL for this key.

        If you have a key that you want to allow access to for a set
        amount of time, you can use this method to generate a URL that
        is only valid within a certain time period.

        This is particularly useful if you don't want publicly
        accessible keys, but don't want to require users to explicitly
        log in.

        :type expiration: int, long, datetime.datetime, datetime.timedelta
        :param expiration: When the signed URL should expire.

        :type method: string
        :param method: The HTTP verb that will be used when requesting the URL.

        :rtype: string
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """
        resource = '/{self.bucket.name}/{self.name}'.format(self=self)
        return self.connection.generate_signed_url(resource=resource,
                                                   expiration=expiration,
                                                   method=method)

    def exists(self):
        """Determines whether or not this key exists.

        :rtype: bool
        :returns: True if the key exists in Cloud Storage.
        """
        return self.bucket.get_key(self.name) is not None

    def rename(self, new_name):
        """Renames this key using copy and delete operations.

        Effectively, copies key to the same bucket with a new name, then
        deletes the key.

        .. warning::
          This method will first duplicate the data and then delete the
          old key.  This means that with very large objects renaming
          could be a very (temporarily) costly or a very slow operation.

        :type new_name: string
        :param new_name: The new name for this key.

        :rtype: :class:`Key`
        :returns: The newly-copied key.
        """
        new_key = self.bucket.copy_key(self, self.bucket, new_name)
        self.bucket.delete_key(self)
        return new_key

    def delete(self):
        """Deletes a key from Cloud Storage.

        :rtype: :class:`Key`
        :returns: The key that was just deleted.
        """
        return self.bucket.delete_key(self)

    def download_to_file(self, file_obj):
        """Download the contents of this key into a file-like object.

        :type file_obj: file
        :param file_obj: A file handle to which to write the key's data.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """
        for chunk in _KeyDataIterator(self):
            file_obj.write(chunk)

    # NOTE: Alias for boto-like API.
    get_contents_to_file = download_to_file

    def download_to_filename(self, filename):
        """Download the contents of this key into a named file.

        :type filename: string
        :param filename: A filename to be passed to ``open``.

        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """
        with open(filename, 'wb') as file_obj:
            self.download_to_file(file_obj)

    # NOTE: Alias for boto-like API.
    get_contents_to_filename = download_to_filename

    def download_as_string(self):
        """Download the contents of this key as a string.

        :rtype: string
        :returns: The data stored in this key.
        :raises: :class:`gcloud.storage.exceptions.NotFoundError`
        """
        string_buffer = StringIO()
        self.download_to_file(string_buffer)
        return string_buffer.getvalue()

    # NOTE: Alias for boto-like API.
    get_contents_as_string = download_as_string

    def upload_from_file(self, file_obj, rewind=False, size=None,
                         content_type=None):
        """Upload the contents of this key from a file-like object.

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file to Cloud Storage.

        :type size: int
        :param size: The number of bytes to read from the file handle.
                     If not provided, we'll try to guess the size using
                     :func:`os.fstat`
        """
        # Rewind the file if desired.
        if rewind:
            file_obj.seek(0, os.SEEK_SET)

        # Get the basic stats about the file.
        total_bytes = size or os.fstat(file_obj.fileno()).st_size
        bytes_uploaded = 0

        # Set up a resumable upload session.
        headers = {
            'X-Upload-Content-Type': content_type or 'application/unknown',
            'X-Upload-Content-Length': total_bytes,
        }

        upload_url = self.connection.build_api_url(
            path=self.bucket.path + '/o',
            query_params={'uploadType': 'resumable', 'name': self.name},
            api_base_url=self.connection.API_BASE_URL + '/upload')

        response, _ = self.connection.make_request(
            method='POST', url=upload_url,
            headers=headers)

        # Get the resumable upload URL.
        upload_url = response['location']

        while bytes_uploaded < total_bytes:
            # Construct the range header.
            data = file_obj.read(self.CHUNK_SIZE)
            chunk_size = len(data)

            start = bytes_uploaded
            end = bytes_uploaded + chunk_size - 1

            headers = {
                'Content-Range': 'bytes %d-%d/%d' % (start, end, total_bytes),
            }

            response, _ = self.connection.make_request(
                content_type='text/plain',
                method='POST', url=upload_url, headers=headers, data=data)

            bytes_uploaded += chunk_size

    # NOTE: Alias for boto-like API.
    set_contents_from_file = upload_from_file

    def upload_from_filename(self, filename):
        """Upload this key's contents from the content of f named file.

        :type filename: string
        :param filename: The path to the file.
        """
        content_type, _ = mimetypes.guess_type(filename)

        with open(filename, 'rb') as file_obj:
            self.upload_from_file(file_obj, content_type=content_type)

    # NOTE: Alias for boto-like API.
    set_contents_from_filename = upload_from_filename

    def upload_from_string(self, data, content_type='text/plain'):
        """Upload contents of this key from the provided string.

        :type data: string
        :param data: The data to store in this key.

        :rtype: :class:`Key`
        :returns: The updated Key object.
        """
        string_buffer = StringIO()
        string_buffer.write(data)
        self.set_contents_from_file(file_obj=string_buffer, rewind=True,
                                    size=string_buffer.len,
                                    content_type=content_type)
        return self

    # NOTE: Alias for boto-like API.
    set_contents_from_string = upload_from_string

    def has_metadata(self, field=None):
        """Check if metadata is available locally.

        :type field: string
        :param field: (optional) the particular field to check for.

        :rtype: bool
        :returns: Whether metadata is available locally.
        """
        if not self.metadata:
            return False
        elif field and field not in self.metadata:
            return False
        else:
            return True

    def reload_metadata(self):
        """Reload metadata from Cloud Storage.

        :rtype: :class:`Key`
        :returns: The key you just reloaded data for.
        """
        # Pass only '?projection=noAcl' here because 'acl' is handled via
        # 'get_acl().
        query_params = {'projection': 'noAcl'}
        self.metadata = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def get_metadata(self, field=None, default=None):
        """Get all metadata or a specific field.

        If you request a field that isn't available, and that field can
        be retrieved by refreshing data from Cloud Storage, this method
        will reload the data using :func:`Key.reload_metadata`.

        :type field: string
        :param field: (optional) A particular field to retrieve from metadata.

        :type default: anything
        :param default: The value to return if the field provided wasn't found.

        :rtype: dict or anything
        :returns: All metadata or the value of the specific field.
        """
        # We ignore 'acl' because it is meant to be handled via 'get_acl()'.
        if field == 'acl':
            raise KeyError("Use 'get_acl()'")

        if not self.has_metadata(field=field):
            self.reload_metadata()

        if field:
            return self.metadata.get(field, default)
        else:
            return self.metadata

    def patch_metadata(self, metadata):
        """Update particular fields of this key's metadata.

        This method will only update the fields provided and will not
        touch the other fields.

        It will also reload the metadata locally based on the servers
        response.

        :type metadata: dict
        :param metadata: The dictionary of values to update.

        :rtype: :class:`Key`
        :returns: The current key.
        """
        self.metadata = self.connection.api_request(
            method='PATCH', path=self.path, data=metadata,
            query_params={'projection': 'full'})
        return self

    def reload_acl(self):
        """Reload the ACL data from Cloud Storage.

        :rtype: :class:`Key`
        :returns: The current key.
        """
        self.acl.clear()

        url_path = '%s/acl' % self.path
        found = self.connection.api_request(method='GET', path=url_path)
        for entry in found['items']:
            self.acl.add_entity(self.acl.entity_from_dict(entry))

        # Even if we fetch no entries, the ACL is still loaded.
        self.acl.loaded = True

        return self

    def get_acl(self):
        """Get ACL metadata as a :class:`gcloud.storage.acl.ObjectACL` object.

        :rtype: :class:`gcloud.storage.acl.ObjectACL`
        :returns: An ACL object for the current key.
        """
        if not self.acl.loaded:
            self.reload_acl()
        return self.acl

    def save_acl(self, acl=None):
        """Save the ACL data for this key.

        :type acl: :class:`gcloud.storage.acl.ACL`
        :param acl: The ACL object to save.  If left blank, this will
                    save the ACL set locally on the key.
        """
        if acl is None:
            acl = self.acl
            dirty = acl.loaded
        else:
            dirty = True

        if dirty:
            result = self.connection.api_request(
                method='PATCH', path=self.path, data={'acl': list(acl)},
                query_params={'projection': 'full'})
            self.acl.clear()
            for entry in result['acl']:
                self.acl.entity(self.acl.entity_from_dict(entry))
            self.acl.loaded = True

        return self

    def clear_acl(self):
        """Remove all ACL rules from the key.

        Note that this won't actually remove *ALL* the rules, but it
        will remove all the non-default rules.  In short, you'll still
        have access to a key that you created even after you clear ACL
        rules with this method.
        """
        return self.save_acl([])

    def make_public(self):
        """Make this key public giving all users read access.

        :rtype: :class:`Key`
        :returns: The current key.
        """
        self.get_acl().all().grant_read()
        self.save_acl()
        return self


class _KeyIterator(Iterator):
    """An iterator listing keys.

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.key.Key` objects.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: The bucket from which to list keys.
    """
    def __init__(self, bucket):
        self.bucket = bucket
        super(_KeyIterator, self).__init__(
            connection=bucket.connection, path=bucket.path + '/o')

    def get_items_from_response(self, response):
        """Factory method, yields :class:`.storage.key.Key` items from response.

        :type response: dict
        :param response: The JSON API response for a page of keys.
        """
        for item in response.get('items', []):
            yield Key.from_dict(item, bucket=self.bucket)


class _KeyDataIterator(object):
    """An iterator listing data stored in a key.

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.key.Key` objects.

    :type key: :class:`gcloud.storage.key.Key`
    :param key: The key from which to list data..
    """

    def __init__(self, key):
        self.key = key
        # NOTE: These variables will be initialized by reset().
        self._bytes_written = None
        self._total_bytes = None
        self.reset()

    def __iter__(self):
        while self.has_more_data():
            yield self.get_next_chunk()

    def reset(self):
        """Resets the iterator to the beginning."""
        self._bytes_written = 0
        self._total_bytes = None

    def has_more_data(self):
        """Determines whether or not this iterator has more data to read.

        :rtype: bool
        :returns: Whether the iterator has more data or not.
        """
        if self._bytes_written == 0:
            return True
        elif not self._total_bytes:
            # self._total_bytes **should** be set by this point.
            # If it isn't, something is wrong.
            raise ValueError('Size of object is unknown.')
        else:
            return self._bytes_written < self._total_bytes

    def get_headers(self):
        """Gets range header(s) for next chunk of data.

        :rtype: dict
        :returns: A dictionary of query parameters.
        """
        start = self._bytes_written
        end = self._bytes_written + self.key.CHUNK_SIZE - 1

        if self._total_bytes and end > self._total_bytes:
            end = ''

        return {'Range': 'bytes=%s-%s' % (start, end)}

    def get_url(self):
        """Gets URL to read next chunk of data.

        :rtype: string
        :returns: A URL.
        """
        return self.key.connection.build_api_url(
            path=self.key.path, query_params={'alt': 'media'})

    def get_next_chunk(self):
        """Gets the next chunk of data.

        Uses CHUNK_SIZE to determine how much data to get.

        :rtype: string
        :returns: The chunk of data read from the key.
        :raises: :class:`RuntimeError` if no more data or
                 :class:`gcloud.storage.exceptions.StorageError` in the
                 case of an unexpected response status code.
        """
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

        # Expected a 200 or a 206. Got something else, which is unknown.
        raise StorageError(response)
