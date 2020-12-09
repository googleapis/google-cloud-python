# Copyright 2014 Google LLC
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
from hashlib import md5
from datetime import datetime
import os

from six.moves.urllib.parse import urlsplit
from google.cloud.storage.constants import _DEFAULT_TIMEOUT
from google.cloud.storage.retry import DEFAULT_RETRY
from google.cloud.storage.retry import DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED


STORAGE_EMULATOR_ENV_VAR = "STORAGE_EMULATOR_HOST"
"""Environment variable defining host for Storage emulator."""

_DEFAULT_STORAGE_HOST = u"https://storage.googleapis.com"

# generation match parameters in camel and snake cases
_GENERATION_MATCH_PARAMETERS = (
    ("if_generation_match", "ifGenerationMatch"),
    ("if_generation_not_match", "ifGenerationNotMatch"),
    ("if_metageneration_match", "ifMetagenerationMatch"),
    ("if_metageneration_not_match", "ifMetagenerationNotMatch"),
    ("if_source_generation_match", "ifSourceGenerationMatch"),
    ("if_source_generation_not_match", "ifSourceGenerationNotMatch"),
    ("if_source_metageneration_match", "ifSourceMetagenerationMatch"),
    ("if_source_metageneration_not_match", "ifSourceMetagenerationNotMatch"),
)


def _get_storage_host():
    return os.environ.get(STORAGE_EMULATOR_ENV_VAR, _DEFAULT_STORAGE_HOST)


def _validate_name(name):
    """Pre-flight ``Bucket`` name validation.

    :type name: str or :data:`NoneType`
    :param name: Proposed bucket name.

    :rtype: str or :data:`NoneType`
    :returns: ``name`` if valid.
    """
    if name is None:
        return

    # The first and last characters must be alphanumeric.
    if not all([name[0].isalnum(), name[-1].isalnum()]):
        raise ValueError("Bucket names must start and end with a number or letter.")
    return name


class _PropertyMixin(object):
    """Abstract mixin for cloud storage classes with associated properties.

    Non-abstract subclasses should implement:
      - path
      - client
      - user_project

    :type name: str
    :param name: The name of the object. Bucket names must start and end with a
                 number or letter.
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

    @property
    def user_project(self):
        """Abstract getter for the object user_project."""
        raise NotImplementedError

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current object.

        :rtype: :class:`google.cloud.storage.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self.client
        return client

    def _encryption_headers(self):
        """Return any encryption headers needed to fetch the object.

        .. note::
           Defined here because :meth:`reload` calls it, but this method is
           really only relevant for :class:`~google.cloud.storage.blob.Blob`.

        :rtype: dict
        :returns: a mapping of encryption-related headers.
        """
        return {}

    @property
    def _query_params(self):
        """Default query parameters."""
        params = {}
        if self.user_project is not None:
            params["userProject"] = self.user_project
        return params

    def reload(
        self,
        client=None,
        projection="noAcl",
        timeout=_DEFAULT_TIMEOUT,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        retry=DEFAULT_RETRY,
    ):
        """Reload properties from Cloud Storage.

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use. If not passed, falls back to the
                       ``client`` stored on the current object.

        :type projection: str
        :param projection: (Optional) If used, must be 'full' or 'noAcl'.
                           Defaults to ``'noAcl'``. Specifies the set of
                           properties to return.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :type if_generation_match: long
        :param if_generation_match: (Optional) Make the operation conditional on whether
                                    the blob's current generation matches the given value.
                                    Setting to 0 makes the operation succeed only if there
                                    are no live versions of the blob.

        :type if_generation_not_match: long
        :param if_generation_not_match: (Optional) Make the operation conditional on whether
                                        the blob's current generation does not match the given
                                        value. If no live blob exists, the precondition fails.
                                        Setting to 0 makes the operation succeed only if there
                                        is a live version of the blob.

        :type if_metageneration_match: long
        :param if_metageneration_match: (Optional) Make the operation conditional on whether the
                                        blob's current metageneration matches the given value.

        :type if_metageneration_not_match: long
        :param if_metageneration_not_match: (Optional) Make the operation conditional on whether the
                                            blob's current metageneration does not match the given value.

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry: (Optional) How to retry the RPC. A None value will disable retries.
            A google.api_core.retry.Retry value will enable retries, and the object will
            define retriable response codes and errors and configure backoff and timeout options.

            A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
            activates it only if certain conditions are met. This class exists to provide safe defaults
            for RPC calls that are not technically safe to retry normally (due to potential data
            duplication or other side-effects) but become safe to retry if a condition such as
            if_metageneration_match is set.

            See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
            information on retry types and how to configure them.
        """
        client = self._require_client(client)
        query_params = self._query_params
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via custom endpoints.
        query_params["projection"] = projection
        _add_generation_match_parameters(
            query_params,
            if_generation_match=if_generation_match,
            if_generation_not_match=if_generation_not_match,
            if_metageneration_match=if_metageneration_match,
            if_metageneration_not_match=if_metageneration_not_match,
        )
        api_response = client._connection.api_request(
            method="GET",
            path=self.path,
            query_params=query_params,
            headers=self._encryption_headers(),
            _target_object=self,
            timeout=timeout,
            retry=retry,
        )
        self._set_properties(api_response)

    def _patch_property(self, name, value):
        """Update field of this object's properties.

        This method will only update the field provided and will not
        touch the other fields.

        It **will not** reload the properties from the server. The behavior is
        local only and syncing occurs via :meth:`patch`.

        :type name: str
        :param name: The field name to update.

        :type value: object
        :param value: The value being updated.
        """
        self._changes.add(name)
        self._properties[name] = value

    def _set_properties(self, value):
        """Set the properties for the current object.

        :type value: dict or :class:`google.cloud.storage.batch._FutureDict`
        :param value: The properties to be set.
        """
        self._properties = value
        # If the values are reset, the changes must as well.
        self._changes = set()

    def patch(
        self,
        client=None,
        timeout=_DEFAULT_TIMEOUT,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        retry=DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED,
    ):
        """Sends all changed properties in a PATCH request.

        Updates the ``_properties`` with the response from the backend.

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use. If not passed, falls back to the
                       ``client`` stored on the current object.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :type if_generation_match: long
        :param if_generation_match: (Optional) Make the operation conditional on whether
                                    the blob's current generation matches the given value.
                                    Setting to 0 makes the operation succeed only if there
                                    are no live versions of the blob.

        :type if_generation_not_match: long
        :param if_generation_not_match: (Optional) Make the operation conditional on whether
                                        the blob's current generation does not match the given
                                        value. If no live blob exists, the precondition fails.
                                        Setting to 0 makes the operation succeed only if there
                                        is a live version of the blob.

        :type if_metageneration_match: long
        :param if_metageneration_match: (Optional) Make the operation conditional on whether the
                                        blob's current metageneration matches the given value.

        :type if_metageneration_not_match: long
        :param if_metageneration_not_match: (Optional) Make the operation conditional on whether the
                                            blob's current metageneration does not match the given value.

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry: (Optional) How to retry the RPC. A None value will disable retries.
            A google.api_core.retry.Retry value will enable retries, and the object will
            define retriable response codes and errors and configure backoff and timeout options.

            A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
            activates it only if certain conditions are met. This class exists to provide safe defaults
            for RPC calls that are not technically safe to retry normally (due to potential data
            duplication or other side-effects) but become safe to retry if a condition such as
            if_metageneration_match is set.

            See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
            information on retry types and how to configure them.
        """
        client = self._require_client(client)
        query_params = self._query_params
        # Pass '?projection=full' here because 'PATCH' documented not
        # to work properly w/ 'noAcl'.
        query_params["projection"] = "full"
        _add_generation_match_parameters(
            query_params,
            if_generation_match=if_generation_match,
            if_generation_not_match=if_generation_not_match,
            if_metageneration_match=if_metageneration_match,
            if_metageneration_not_match=if_metageneration_not_match,
        )
        update_properties = {key: self._properties[key] for key in self._changes}

        # Make the API call.
        api_response = client._connection.api_request(
            method="PATCH",
            path=self.path,
            data=update_properties,
            query_params=query_params,
            _target_object=self,
            timeout=timeout,
            retry=retry,
        )
        self._set_properties(api_response)

    def update(
        self,
        client=None,
        timeout=_DEFAULT_TIMEOUT,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        retry=DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED,
    ):
        """Sends all properties in a PUT request.

        Updates the ``_properties`` with the response from the backend.

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use. If not passed, falls back to the
                       ``client`` stored on the current object.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :type if_generation_match: long
        :param if_generation_match: (Optional) Make the operation conditional on whether
                                    the blob's current generation matches the given value.
                                    Setting to 0 makes the operation succeed only if there
                                    are no live versions of the blob.

        :type if_generation_not_match: long
        :param if_generation_not_match: (Optional) Make the operation conditional on whether
                                        the blob's current generation does not match the given
                                        value. If no live blob exists, the precondition fails.
                                        Setting to 0 makes the operation succeed only if there
                                        is a live version of the blob.

        :type if_metageneration_match: long
        :param if_metageneration_match: (Optional) Make the operation conditional on whether the
                                        blob's current metageneration matches the given value.

        :type if_metageneration_not_match: long
        :param if_metageneration_not_match: (Optional) Make the operation conditional on whether the
                                            blob's current metageneration does not match the given value.

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry: (Optional) How to retry the RPC. A None value will disable retries.
            A google.api_core.retry.Retry value will enable retries, and the object will
            define retriable response codes and errors and configure backoff and timeout options.

            A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
            activates it only if certain conditions are met. This class exists to provide safe defaults
            for RPC calls that are not technically safe to retry normally (due to potential data
            duplication or other side-effects) but become safe to retry if a condition such as
            if_metageneration_match is set.

            See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
            information on retry types and how to configure them.
        """
        client = self._require_client(client)

        query_params = self._query_params
        query_params["projection"] = "full"
        _add_generation_match_parameters(
            query_params,
            if_generation_match=if_generation_match,
            if_generation_not_match=if_generation_not_match,
            if_metageneration_match=if_metageneration_match,
            if_metageneration_not_match=if_metageneration_not_match,
        )

        api_response = client._connection.api_request(
            method="PUT",
            path=self.path,
            data=self._properties,
            query_params=query_params,
            _target_object=self,
            timeout=timeout,
            retry=retry,
        )
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

    :type digest_block_size: int
    :param digest_block_size: The block size to write to the hash.
                              Defaults to 8192.
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

    :rtype: str
    :returns: A base64 encoded digest of the MD5 hash.
    """
    hash_obj = md5()
    _write_buffer_to_hash(buffer_object, hash_obj)
    digest_bytes = hash_obj.digest()
    return base64.b64encode(digest_bytes)


def _convert_to_timestamp(value):
    """Convert non-none datetime to timestamp.

    :type value: :class:`datetime.datetime`
    :param value: The datetime to convert.

    :rtype: int
    :returns: The timestamp.
    """
    utc_naive = value.replace(tzinfo=None) - value.utcoffset()
    mtime = (utc_naive - datetime(1970, 1, 1)).total_seconds()
    return mtime


def _add_generation_match_parameters(parameters, **match_parameters):
    """Add generation match parameters into the given parameters list.

    :type parameters: list or dict
    :param parameters: Parameters list or dict.

    :type match_parameters: dict
    :param match_parameters: if*generation*match parameters to add.

    :raises: :exc:`ValueError` if ``parameters`` is not a ``list()``
             or a ``dict()``.
    """
    for snakecase_name, camelcase_name in _GENERATION_MATCH_PARAMETERS:
        value = match_parameters.get(snakecase_name)

        if value is not None:
            if isinstance(parameters, list):
                parameters.append((camelcase_name, value))

            elif isinstance(parameters, dict):
                parameters[camelcase_name] = value

            else:
                raise ValueError(
                    "`parameters` argument should be a dict() or a list()."
                )


def _raise_if_more_than_one_set(**kwargs):
    """Raise ``ValueError`` exception if more than one parameter was set.

    :type error: :exc:`ValueError`
    :param error: Description of which fields were set

    :raises: :class:`~ValueError` containing the fields that were set
    """
    if sum(arg is not None for arg in kwargs.values()) > 1:
        escaped_keys = ["'%s'" % name for name in kwargs.keys()]

        keys_but_last = ", ".join(escaped_keys[:-1])
        last_key = escaped_keys[-1]

        msg = "Pass at most one of {keys_but_last} and {last_key}".format(
            keys_but_last=keys_but_last, last_key=last_key
        )

        raise ValueError(msg)


def _bucket_bound_hostname_url(host, scheme=None):
    """Helper to build bucket bound hostname URL.

    :type host: str
    :param host: Host name.

    :type scheme: str
    :param scheme: (Optional) Web scheme. If passed, use it
                   as a scheme in the result URL.

    :rtype: str
    :returns: A bucket bound hostname URL.
    """
    url_parts = urlsplit(host)
    if url_parts.scheme and url_parts.netloc:
        return host

    return "{scheme}://{host}/".format(scheme=scheme, host=host)
