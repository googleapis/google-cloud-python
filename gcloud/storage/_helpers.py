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

import base64
import binascii
try:
    import crcmod
except ImportError:
    crcmod = None

from Crypto.Hash import MD5


class _PropertyMixin(object):
    """Abstract mixin for cloud storage classes with associated propertties.

    Non-abstract subclasses should implement:
      - client
      - path

    :type name: string
    :param name: The name of the object.
    """

    def __init__(self, name=None):
        self.name = name
        self._properties = {}
        self._changes = set()

    @property
    def path(self):
        """Abstract getter for the object path."""
        raise NotImplementedError

    @property
    def client(self):
        """Abstract getter for the object client."""
        raise NotImplementedError

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.storage.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current object.

        :rtype: :class:`gcloud.storage.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self.client
        return client

    def reload(self, client=None):
        """Reload properties from Cloud Storage.

        :type client: :class:`gcloud.storage.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current object.
        """
        client = self._require_client(client)
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via custom endpoints.
        query_params = {'projection': 'noAcl'}
        api_response = client.connection.api_request(
            method='GET', path=self.path, query_params=query_params,
            _target_object=self)
        self._set_properties(api_response)

    def _patch_property(self, name, value):
        """Update field of this object's properties.

        This method will only update the field provided and will not
        touch the other fields.

        It **will not** reload the properties from the server. The behavior is
        local only and syncing occurs via :meth:`patch`.

        :type name: string
        :param name: The field name to update.

        :type value: object
        :param value: The value being updated.
        """
        self._changes.add(name)
        self._properties[name] = value

    def _set_properties(self, value):
        """Set the properties for the current object.

        :type value: dict or :class:`gcloud.storage.batch._FutureDict`
        :param value: The properties to be set.
        """
        self._properties = value
        # If the values are reset, the changes must as well.
        self._changes = set()

    def patch(self, client=None):
        """Sends all changed properties in a PATCH request.

        Updates the ``_properties`` with the response from the backend.

        :type client: :class:`gcloud.storage.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current object.
        """
        client = self._require_client(client)
        # Pass '?projection=full' here because 'PATCH' documented not
        # to work properly w/ 'noAcl'.
        update_properties = dict((key, self._properties[key])
                                 for key in self._changes)
        api_response = client.connection.api_request(
            method='PATCH', path=self.path, data=update_properties,
            query_params={'projection': 'full'}, _target_object=self)
        self._set_properties(api_response)


def _scalar_property(fieldname):
    """Create a property descriptor around the :class:`_PropertyMixin` helpers.
    """
    def _getter(self):
        """Scalar property getter."""
        return self._properties.get(fieldname)

    def _setter(self, value):
        """Scalar property setter."""
        self._patch_property(fieldname, value)

    return property(_getter, _setter)


def _write_buffer_to_hash(buffer_object, hash_obj, digest_block_size=8192):
    """Read blocks from a buffer and update a hash with them.

    :type buffer_object: bytes buffer
    :param buffer_object: Buffer containing bytes used to update a hash object.

    :type hash_obj: object that implements update
    :param hash_obj: A hash object (MD5 or CRC32-C).

    :type digest_block_size: integer
    :param digest_block_size: The block size to write to the hash.
                              Defaults to 8192.
    """
    block = buffer_object.read(digest_block_size)

    while len(block) > 0:
        hash_obj.update(block)
        # Update the block for the next iteration.
        block = buffer_object.read(digest_block_size)


def _base64_crc32c(buffer_object):
    """Get CRC-32C hash of bytes (as base64).

    Here 32C stands for 32 bit hash using Castagnoli polynomial. See:
        https://cloud.google.com/storage/docs/hashes-etags#_CRC32C

    :type buffer_object: bytes buffer
    :param buffer_object: Buffer containing bytes used to compute a CRC-32C
                          hash (as base64) using the Castagnoli polynomial.

    :rtype: string
    :returns: The base64 encoded CRC-32C hash of the contents in buffer object.
    """
    if crcmod is None:
        raise NotImplementedError('crcmod is not installed')
    hash_obj = crcmod.predefined.Crc('crc-32c')
    _write_buffer_to_hash(buffer_object, hash_obj)
    digest_bytes = binascii.unhexlify(hash_obj.hexdigest())
    return base64.b64encode(digest_bytes)


def _base64_md5hash(buffer_object):
    """Get MD5 hash of bytes (as base64).

    :type buffer_object: bytes buffer
    :param buffer_object: Buffer containing bytes used to compute an MD5
                          hash (as base64).

    :rtype: string
    :returns: The base64 encoded MD5 hash of the contents in buffer object.
    """
    hash_obj = MD5.new()
    _write_buffer_to_hash(buffer_object, hash_obj)
    digest_bytes = hash_obj.digest()
    return base64.b64encode(digest_bytes)
