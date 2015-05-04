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

from gcloud.storage._implicit_environ import get_default_connection
from gcloud.storage.batch import Batch


class _PropertyMixin(object):
    """Abstract mixin for cloud storage classes with associated propertties.

    Non-abstract subclasses should implement:
      - connection
      - path
    """

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

    def reload(self, connection=None):
        """Reload properties from Cloud Storage.

        :type connection: :class:`gcloud.storage.connection.Connection`
        :param connection: An explicit connection to use for the API request.
                           If not passed, use the connection assigned to
                           the object in its constructor.
        """
        connection = _require_connection(connection)
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via custom endpoints.
        query_params = {'projection': 'noAcl'}
        api_response = connection.api_request(
            method='GET', path=self.path, query_params=query_params)
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

        :type value: dict
        :param value: The properties to be set.
        """
        self._properties = value
        # If the values are reset, the changes must as well.
        self._changes = set()

    def patch(self, connection=None):
        """Sends all changed properties in a PATCH request.

        Updates the ``_properties`` with the response from the backend.

        :type connection: :class:`gcloud.storage.connection.Connection`
        :param connection: An explicit connection to use for the API request.
                           If not passed, use the connection assigned to
                           the object in its constructor.
        """
        connection = _require_connection(connection)
        # Pass '?projection=full' here because 'PATCH' documented not
        # to work properly w/ 'noAcl'.
        update_properties = dict((key, self._properties[key])
                                 for key in self._changes)
        api_response = connection.api_request(
            method='PATCH', path=self.path, data=update_properties,
            query_params={'projection': 'full'})
        self._set_properties(api_response)


def _require_connection(connection=None):
    """Infer a connection from the environment, if not passed explicitly.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: Optional.

    :rtype: :class:`gcloud.storage.connection.Connection`
    :returns: A connection based on the current environment.
    :raises: :class:`EnvironmentError` if ``connection`` is ``None``, and
             cannot be inferred from the environment.
    """
    # NOTE: We use current Batch directly since it inherits from Connection.
    if connection is None:
        connection = Batch.current()

    if connection is None:
        connection = get_default_connection()

    if connection is None:
        raise EnvironmentError('Connection could not be inferred.')

    return connection


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
