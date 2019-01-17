# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.cloud.kms.v1 KeyManagementService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.kms_v1.gapic import enums
from google.cloud.kms_v1.gapic import key_management_service_client_config
from google.cloud.kms_v1.gapic.transports import key_management_service_grpc_transport
from google.cloud.kms_v1.proto import resources_pb2
from google.cloud.kms_v1.proto import service_pb2
from google.cloud.kms_v1.proto import service_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-kms").version


class KeyManagementServiceClient(object):
    """
    Google Cloud Key Management Service

    Manages cryptographic keys and operations using those keys. Implements a
    REST model with the following objects:

    -  ``KeyRing``
    -  ``CryptoKey``
    -  ``CryptoKeyVersion``

    If you are using manual gRPC libraries, see `Using gRPC with Cloud
    KMS <https://cloud.google.com/kms/docs/grpc>`__.
    """

    SERVICE_ADDRESS = "cloudkms.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.kms.v1.KeyManagementService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            KeyManagementServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def key_ring_path(cls, project, location, key_ring):
        """Return a fully-qualified key_ring string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/keyRings/{key_ring}",
            project=project,
            location=location,
            key_ring=key_ring,
        )

    @classmethod
    def crypto_key_path_path(cls, project, location, key_ring, crypto_key_path):
        """Return a fully-qualified crypto_key_path string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key_path=**}",
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key_path=crypto_key_path,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def crypto_key_path(cls, project, location, key_ring, crypto_key):
        """Return a fully-qualified crypto_key string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}",
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
        )

    @classmethod
    def crypto_key_version_path(
        cls, project, location, key_ring, crypto_key, crypto_key_version
    ):
        """Return a fully-qualified crypto_key_version string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}",
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
            crypto_key_version=crypto_key_version,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.KeyManagementServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.KeyManagementServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = key_management_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=key_management_service_grpc_transport.KeyManagementServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = key_management_service_grpc_transport.KeyManagementServiceGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_key_rings(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ``KeyRings``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_key_rings(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_key_rings(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the location associated with the
                ``KeyRings``, in the format ``projects/*/locations/*``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.kms_v1.types.KeyRing` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_key_rings" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_key_rings"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_key_rings,
                default_retry=self._method_configs["ListKeyRings"].retry,
                default_timeout=self._method_configs["ListKeyRings"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListKeyRingsRequest(parent=parent, page_size=page_size)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_key_rings"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="key_rings",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_crypto_keys(
        self,
        parent,
        page_size=None,
        version_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ``CryptoKeys``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_crypto_keys(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_crypto_keys(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the ``KeyRing`` to list, in the format
                ``projects/*/locations/*/keyRings/*``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            version_view (~google.cloud.kms_v1.types.CryptoKeyVersionView): The fields of the primary version to include in the response.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.kms_v1.types.CryptoKey` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_crypto_keys" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_crypto_keys"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_crypto_keys,
                default_retry=self._method_configs["ListCryptoKeys"].retry,
                default_timeout=self._method_configs["ListCryptoKeys"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListCryptoKeysRequest(
            parent=parent, page_size=page_size, version_view=version_view
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_crypto_keys"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="crypto_keys",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_crypto_key_versions(
        self,
        parent,
        page_size=None,
        view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ``CryptoKeyVersions``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.crypto_key_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_crypto_key_versions(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_crypto_key_versions(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the ``CryptoKey`` to list, in the format
                ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            view (~google.cloud.kms_v1.types.CryptoKeyVersionView): The fields to include in the response.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_crypto_key_versions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_crypto_key_versions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_crypto_key_versions,
                default_retry=self._method_configs["ListCryptoKeyVersions"].retry,
                default_timeout=self._method_configs["ListCryptoKeyVersions"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListCryptoKeyVersionsRequest(
            parent=parent, page_size=page_size, view=view
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_crypto_key_versions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="crypto_key_versions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_key_ring(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns metadata for a given ``KeyRing``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>>
            >>> response = client.get_key_ring(name)

        Args:
            name (str): The ``name`` of the ``KeyRing`` to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.KeyRing` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_key_ring" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_key_ring"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_key_ring,
                default_retry=self._method_configs["GetKeyRing"].retry,
                default_timeout=self._method_configs["GetKeyRing"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetKeyRingRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_key_ring"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_crypto_key(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns metadata for a given ``CryptoKey``, as well as its ``primary``
        ``CryptoKeyVersion``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]')
            >>>
            >>> response = client.get_crypto_key(name)

        Args:
            name (str): The ``name`` of the ``CryptoKey`` to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_crypto_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_crypto_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_crypto_key,
                default_retry=self._method_configs["GetCryptoKey"].retry,
                default_timeout=self._method_configs["GetCryptoKey"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetCryptoKeyRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_crypto_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_crypto_key_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns metadata for a given ``CryptoKeyVersion``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> response = client.get_crypto_key_version(name)

        Args:
            name (str): The ``name`` of the ``CryptoKeyVersion`` to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_crypto_key_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_crypto_key_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_crypto_key_version,
                default_retry=self._method_configs["GetCryptoKeyVersion"].retry,
                default_timeout=self._method_configs["GetCryptoKeyVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetCryptoKeyVersionRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_crypto_key_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_key_ring(
        self,
        parent,
        key_ring_id,
        key_ring,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create a new ``KeyRing`` in a given Project and Location.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `key_ring_id`:
            >>> key_ring_id = ''
            >>>
            >>> # TODO: Initialize `key_ring`:
            >>> key_ring = {}
            >>>
            >>> response = client.create_key_ring(parent, key_ring_id, key_ring)

        Args:
            parent (str): Required. The resource name of the location associated with the
                ``KeyRings``, in the format ``projects/*/locations/*``.
            key_ring_id (str): Required. It must be unique within a location and match the regular
                expression ``[a-zA-Z0-9_-]{1,63}``
            key_ring (Union[dict, ~google.cloud.kms_v1.types.KeyRing]): A ``KeyRing`` with initial field values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.KeyRing`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.KeyRing` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_key_ring" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_key_ring"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_key_ring,
                default_retry=self._method_configs["CreateKeyRing"].retry,
                default_timeout=self._method_configs["CreateKeyRing"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateKeyRingRequest(
            parent=parent, key_ring_id=key_ring_id, key_ring=key_ring
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_key_ring"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_crypto_key(
        self,
        parent,
        crypto_key_id,
        crypto_key,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create a new ``CryptoKey`` within a ``KeyRing``.

        ``CryptoKey.purpose`` and ``CryptoKey.version_template.algorithm`` are
        required.

        Example:
            >>> from google.cloud import kms_v1
            >>> from google.cloud.kms_v1 import enums
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>> crypto_key_id = 'my-app-key'
            >>> purpose = enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
            >>> seconds = 2147483647
            >>> next_rotation_time = {'seconds': seconds}
            >>> seconds_2 = 604800
            >>> rotation_period = {'seconds': seconds_2}
            >>> crypto_key = {'purpose': purpose, 'next_rotation_time': next_rotation_time, 'rotation_period': rotation_period}
            >>>
            >>> response = client.create_crypto_key(parent, crypto_key_id, crypto_key)

        Args:
            parent (str): Required. The ``name`` of the KeyRing associated with the
                ``CryptoKeys``.
            crypto_key_id (str): Required. It must be unique within a KeyRing and match the regular
                expression ``[a-zA-Z0-9_-]{1,63}``
            crypto_key (Union[dict, ~google.cloud.kms_v1.types.CryptoKey]): A ``CryptoKey`` with initial field values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.CryptoKey`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_crypto_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_crypto_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_crypto_key,
                default_retry=self._method_configs["CreateCryptoKey"].retry,
                default_timeout=self._method_configs["CreateCryptoKey"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateCryptoKeyRequest(
            parent=parent, crypto_key_id=crypto_key_id, crypto_key=crypto_key
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_crypto_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_crypto_key_version(
        self,
        parent,
        crypto_key_version,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Create a new ``CryptoKeyVersion`` in a ``CryptoKey``.

        The server will assign the next sequential id. If unset, ``state`` will
        be set to ``ENABLED``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> parent = client.crypto_key_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]')
            >>>
            >>> # TODO: Initialize `crypto_key_version`:
            >>> crypto_key_version = {}
            >>>
            >>> response = client.create_crypto_key_version(parent, crypto_key_version)

        Args:
            parent (str): Required. The ``name`` of the ``CryptoKey`` associated with the
                ``CryptoKeyVersions``.
            crypto_key_version (Union[dict, ~google.cloud.kms_v1.types.CryptoKeyVersion]): A ``CryptoKeyVersion`` with initial field values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.CryptoKeyVersion`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_crypto_key_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_crypto_key_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_crypto_key_version,
                default_retry=self._method_configs["CreateCryptoKeyVersion"].retry,
                default_timeout=self._method_configs["CreateCryptoKeyVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateCryptoKeyVersionRequest(
            parent=parent, crypto_key_version=crypto_key_version
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_crypto_key_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_crypto_key(
        self,
        crypto_key,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Update a ``CryptoKey``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> # TODO: Initialize `crypto_key`:
            >>> crypto_key = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_crypto_key(crypto_key, update_mask)

        Args:
            crypto_key (Union[dict, ~google.cloud.kms_v1.types.CryptoKey]): ``CryptoKey`` with updated values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.CryptoKey`
            update_mask (Union[dict, ~google.cloud.kms_v1.types.FieldMask]): Required list of fields to be updated in this request.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_crypto_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_crypto_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_crypto_key,
                default_retry=self._method_configs["UpdateCryptoKey"].retry,
                default_timeout=self._method_configs["UpdateCryptoKey"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateCryptoKeyRequest(
            crypto_key=crypto_key, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("crypto_key.name", crypto_key.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_crypto_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_crypto_key_version(
        self,
        crypto_key_version,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Update a ``CryptoKeyVersion``'s metadata.

        ``state`` may be changed between ``ENABLED`` and ``DISABLED`` using this
        method. See ``DestroyCryptoKeyVersion`` and ``RestoreCryptoKeyVersion``
        to move between other states.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> # TODO: Initialize `crypto_key_version`:
            >>> crypto_key_version = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_crypto_key_version(crypto_key_version, update_mask)

        Args:
            crypto_key_version (Union[dict, ~google.cloud.kms_v1.types.CryptoKeyVersion]): ``CryptoKeyVersion`` with updated values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.CryptoKeyVersion`
            update_mask (Union[dict, ~google.cloud.kms_v1.types.FieldMask]): Required list of fields to be updated in this request.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_crypto_key_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_crypto_key_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_crypto_key_version,
                default_retry=self._method_configs["UpdateCryptoKeyVersion"].retry,
                default_timeout=self._method_configs["UpdateCryptoKeyVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateCryptoKeyVersionRequest(
            crypto_key_version=crypto_key_version, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("crypto_key_version.name", crypto_key_version.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_crypto_key_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def encrypt(
        self,
        name,
        plaintext,
        additional_authenticated_data=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Encrypts data, so that it can only be recovered by a call to
        ``Decrypt``. The ``CryptoKey.purpose`` must be ``ENCRYPT_DECRYPT``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_path_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY_PATH]')
            >>>
            >>> # TODO: Initialize `plaintext`:
            >>> plaintext = b''
            >>>
            >>> response = client.encrypt(name, plaintext)

        Args:
            name (str): Required. The resource name of the ``CryptoKey`` or ``CryptoKeyVersion``
                to use for encryption.

                If a ``CryptoKey`` is specified, the server will use its
                ``primary version``.
            plaintext (bytes): Required. The data to encrypt. Must be no larger than 64KiB.

                The maximum size depends on the key version's ``protection_level``. For
                ``SOFTWARE`` keys, the plaintext must be no larger than 64KiB. For
                ``HSM`` keys, the combined length of the plaintext and
                additional\_authenticated\_data fields must be no larger than 8KiB.
            additional_authenticated_data (bytes): Optional data that, if specified, must also be provided during
                decryption through ``DecryptRequest.additional_authenticated_data``.

                The maximum size depends on the key version's ``protection_level``. For
                ``SOFTWARE`` keys, the AAD must be no larger than 64KiB. For ``HSM``
                keys, the combined length of the plaintext and
                additional\_authenticated\_data fields must be no larger than 8KiB.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.EncryptResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "encrypt" not in self._inner_api_calls:
            self._inner_api_calls[
                "encrypt"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.encrypt,
                default_retry=self._method_configs["Encrypt"].retry,
                default_timeout=self._method_configs["Encrypt"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.EncryptRequest(
            name=name,
            plaintext=plaintext,
            additional_authenticated_data=additional_authenticated_data,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["encrypt"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def decrypt(
        self,
        name,
        ciphertext,
        additional_authenticated_data=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Decrypts data that was protected by ``Encrypt``. The
        ``CryptoKey.purpose`` must be ``ENCRYPT_DECRYPT``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]')
            >>>
            >>> # TODO: Initialize `ciphertext`:
            >>> ciphertext = b''
            >>>
            >>> response = client.decrypt(name, ciphertext)

        Args:
            name (str): Required. The resource name of the ``CryptoKey`` to use for decryption.
                The server will choose the appropriate version.
            ciphertext (bytes): Required. The encrypted data originally returned in
                ``EncryptResponse.ciphertext``.
            additional_authenticated_data (bytes): Optional data that must match the data originally supplied in
                ``EncryptRequest.additional_authenticated_data``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.DecryptResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "decrypt" not in self._inner_api_calls:
            self._inner_api_calls[
                "decrypt"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.decrypt,
                default_retry=self._method_configs["Decrypt"].retry,
                default_timeout=self._method_configs["Decrypt"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DecryptRequest(
            name=name,
            ciphertext=ciphertext,
            additional_authenticated_data=additional_authenticated_data,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["decrypt"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_crypto_key_primary_version(
        self,
        name,
        crypto_key_version_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Update the version of a ``CryptoKey`` that will be used in ``Encrypt``.

        Returns an error if called on an asymmetric key.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]')
            >>>
            >>> # TODO: Initialize `crypto_key_version_id`:
            >>> crypto_key_version_id = ''
            >>>
            >>> response = client.update_crypto_key_primary_version(name, crypto_key_version_id)

        Args:
            name (str): The resource name of the ``CryptoKey`` to update.
            crypto_key_version_id (str): The id of the child ``CryptoKeyVersion`` to use as primary.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_crypto_key_primary_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_crypto_key_primary_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_crypto_key_primary_version,
                default_retry=self._method_configs[
                    "UpdateCryptoKeyPrimaryVersion"
                ].retry,
                default_timeout=self._method_configs[
                    "UpdateCryptoKeyPrimaryVersion"
                ].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateCryptoKeyPrimaryVersionRequest(
            name=name, crypto_key_version_id=crypto_key_version_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_crypto_key_primary_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def destroy_crypto_key_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Schedule a ``CryptoKeyVersion`` for destruction.

        Upon calling this method, ``CryptoKeyVersion.state`` will be set to
        ``DESTROY_SCHEDULED`` and ``destroy_time`` will be set to a time 24
        hours in the future, at which point the ``state`` will be changed to
        ``DESTROYED``, and the key material will be irrevocably destroyed.

        Before the ``destroy_time`` is reached, ``RestoreCryptoKeyVersion`` may
        be called to reverse the process.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> response = client.destroy_crypto_key_version(name)

        Args:
            name (str): The resource name of the ``CryptoKeyVersion`` to destroy.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "destroy_crypto_key_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "destroy_crypto_key_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.destroy_crypto_key_version,
                default_retry=self._method_configs["DestroyCryptoKeyVersion"].retry,
                default_timeout=self._method_configs["DestroyCryptoKeyVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DestroyCryptoKeyVersionRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["destroy_crypto_key_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def restore_crypto_key_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Restore a ``CryptoKeyVersion`` in the ``DESTROY_SCHEDULED`` state.

        Upon restoration of the CryptoKeyVersion, ``state`` will be set to
        ``DISABLED``, and ``destroy_time`` will be cleared.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> response = client.restore_crypto_key_version(name)

        Args:
            name (str): The resource name of the ``CryptoKeyVersion`` to restore.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.CryptoKeyVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "restore_crypto_key_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "restore_crypto_key_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.restore_crypto_key_version,
                default_retry=self._method_configs["RestoreCryptoKeyVersion"].retry,
                default_timeout=self._method_configs["RestoreCryptoKeyVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.RestoreCryptoKeyVersionRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["restore_crypto_key_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_public_key(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns the public key for the given ``CryptoKeyVersion``. The
        ``CryptoKey.purpose`` must be ``ASYMMETRIC_SIGN`` or
        ``ASYMMETRIC_DECRYPT``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> response = client.get_public_key(name)

        Args:
            name (str): The ``name`` of the ``CryptoKeyVersion`` public key to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.PublicKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_public_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_public_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_public_key,
                default_retry=self._method_configs["GetPublicKey"].retry,
                default_timeout=self._method_configs["GetPublicKey"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetPublicKeyRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_public_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def asymmetric_decrypt(
        self,
        name,
        ciphertext,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Decrypts data that was encrypted with a public key retrieved from
        ``GetPublicKey`` corresponding to a ``CryptoKeyVersion`` with
        ``CryptoKey.purpose`` ASYMMETRIC\_DECRYPT.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> # TODO: Initialize `ciphertext`:
            >>> ciphertext = b''
            >>>
            >>> response = client.asymmetric_decrypt(name, ciphertext)

        Args:
            name (str): Required. The resource name of the ``CryptoKeyVersion`` to use for
                decryption.
            ciphertext (bytes): Required. The data encrypted with the named ``CryptoKeyVersion``'s
                public key using OAEP.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.AsymmetricDecryptResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "asymmetric_decrypt" not in self._inner_api_calls:
            self._inner_api_calls[
                "asymmetric_decrypt"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.asymmetric_decrypt,
                default_retry=self._method_configs["AsymmetricDecrypt"].retry,
                default_timeout=self._method_configs["AsymmetricDecrypt"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.AsymmetricDecryptRequest(name=name, ciphertext=ciphertext)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["asymmetric_decrypt"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def asymmetric_sign(
        self,
        name,
        digest,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Signs data using a ``CryptoKeyVersion`` with ``CryptoKey.purpose``
        ASYMMETRIC\_SIGN, producing a signature that can be verified with the
        public key retrieved from ``GetPublicKey``.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> name = client.crypto_key_version_path('[PROJECT]', '[LOCATION]', '[KEY_RING]', '[CRYPTO_KEY]', '[CRYPTO_KEY_VERSION]')
            >>>
            >>> # TODO: Initialize `digest`:
            >>> digest = {}
            >>>
            >>> response = client.asymmetric_sign(name, digest)

        Args:
            name (str): Required. The resource name of the ``CryptoKeyVersion`` to use for
                signing.
            digest (Union[dict, ~google.cloud.kms_v1.types.Digest]): Required. The digest of the data to sign. The digest must be produced
                with the same digest algorithm as specified by the key version's
                ``algorithm``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.Digest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.AsymmetricSignResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "asymmetric_sign" not in self._inner_api_calls:
            self._inner_api_calls[
                "asymmetric_sign"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.asymmetric_sign,
                default_retry=self._method_configs["AsymmetricSign"].retry,
                default_timeout=self._method_configs["AsymmetricSign"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.AsymmetricSignRequest(name=name, digest=digest)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["asymmetric_sign"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> resource = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.kms_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.kms_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> resource = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of permissions,
        not a NOT\_FOUND error.

        Example:
            >>> from google.cloud import kms_v1
            >>>
            >>> client = kms_v1.KeyManagementServiceClient()
            >>>
            >>> resource = client.key_ring_path('[PROJECT]', '[LOCATION]', '[KEY_RING]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.kms_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
