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

"""Helper functions for Cloud Storage utility classes.

These are *not* part of the API.
"""

from Crypto.Hash import MD5
import base64


class _PropertyMixin(object):
    """Abstract mixin for cloud storage classes with associated propertties.

    Non-abstract subclasses should implement:
      - connection
      - path
    """

    @property
    def connection(self):
        """Abstract getter for the connection to use."""
        raise NotImplementedError

    @property
    def path(self):
        """Abstract getter for the object path."""
        raise NotImplementedError

    def __init__(self, name=None):
        """_PropertyMixin constructor.

        :type name: string
        :param name: The name of the object.
        """
        self.name = name
        self._properties = {}
        self._changes = set()

    @property
    def properties(self):
        """Return a copy of properties.

        :rtype: dict
        :returns: Copy of properties.
        """
        return self._properties.copy()

    @property
    def batch(self):
        """Return a context manager which defers/batches updates.

        E.g., to batch multiple updates to a bucket::

            >>> with bucket.batch:
            ...     bucket.enable_versioning()
            ...     bucket.disable_website()

        or for a blob::

            >>> with blob.batch:
            ...     blob.content_type = 'image/jpeg'
            ...     blob.content_encoding = 'gzip'

        Updates will be aggregated and sent as a single call to
        :meth:`_patch_properties` IFF the ``with`` block exits without
        an exception.

        :rtype: :class:`_PropertyBatch`
        """
        return _PropertyBatch(self)

    def _reload_properties(self):
        """Reload properties from Cloud Storage.

        :rtype: :class:`_PropertyMixin`
        :returns: The object you just reloaded data for.
        """
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via custom endpoints.
        query_params = {'projection': 'noAcl'}
        self._properties = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def _patch_properties(self, properties):
        """Update particular fields of this object's properties.

        This method will only update the fields provided and will not
        touch the other fields.

        It **will not** reload the properties from the server. The behavior is
        local only and syncing occurs via :meth:`patch`.

        :type properties: dict
        :param properties: The dictionary of values to update.

        :rtype: :class:`_PropertyMixin`
        :returns: The current object.
        """
        self._changes.update(properties.keys())
        self._properties.update(properties)
        return self

    def patch(self):
        """Sends all changed properties in a PATCH request.

        Updates the ``properties`` with the response from the backend.

        :rtype: :class:`Bucket`
        :returns: The current bucket.
        """
        update_properties = dict((key, self._properties[key])
                                 for key in self._changes)
        self._properties = self.connection.api_request(
            method='PATCH', path=self.path, data=update_properties,
            query_params={'projection': 'noAcl'})
        return self


class _PropertyBatch(object):
    """Context manager: Batch updates to object.

    :type wrapped: class derived from :class:`_PropertyMixin`.
    :param wrapped:  the instance whose property updates to batch.
    """
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __enter__(self):
        """Do nothing method. Needed to be a context manager."""

    def __exit__(self, exc_type, value, traceback):
        """Patch deferred property updates if no error."""
        if exc_type is None:
            self._wrapped.patch()


def _scalar_property(fieldname):
    """Create a property descriptor around the :class:`_PropertyMixin` helpers.
    """
    def _getter(self):
        """Scalar property getter."""
        return self.properties[fieldname]

    def _setter(self, value):
        """Scalar property setter."""
        self._patch_properties({fieldname: value})

    return property(_getter, _setter)


def _write_buffer_to_hash(buffer_object, hash_obj, digest_block_size=8192):
    """Read blocks from a buffer and update a hash with them.

    :type buffer_object: bytes buffer
    :param buffer_object: Buffer containing bytes used to update a hash object.
    """
    block = buffer_object.read(digest_block_size)

    while len(block) > 0:
        hash_obj.update(block)
        # Update the block for the next iteration.
        block = buffer_object.read(digest_block_size)


def _base64_md5hash(buffer_object):
    """Get MD5 hash of bytes (as base64).

    :type buffer_object: bytes buffer
    :param buffer_object: Buffer containing bytes used to compute an MD5
                          hash (as base64).
    """
    hash_obj = MD5.new()
    _write_buffer_to_hash(buffer_object, hash_obj)
    digest_bytes = hash_obj.digest()
    return base64.b64encode(digest_bytes)
