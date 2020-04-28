# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.cloud.secrets.v1beta1 SecretManagerService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.secretmanager_v1beta1.gapic import enums
from google.cloud.secretmanager_v1beta1.gapic import (
    secret_manager_service_client_config,
)
from google.cloud.secretmanager_v1beta1.gapic.transports import (
    secret_manager_service_grpc_transport,
)
from google.cloud.secretmanager_v1beta1.proto import resources_pb2
from google.cloud.secretmanager_v1beta1.proto import service_pb2
from google.cloud.secretmanager_v1beta1.proto import service_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-secret-manager"
).version


class SecretManagerServiceClient(object):
    """
    Secret Manager Service

    Manages secrets and operations using those secrets. Implements a REST
    model with the following objects:

    -  ``Secret``
    -  ``SecretVersion``
    """

    SERVICE_ADDRESS = "secretmanager.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.secrets.v1beta1.SecretManagerService"

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
            SecretManagerServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def secret_path(cls, project, secret):
        """Return a fully-qualified secret string."""
        return google.api_core.path_template.expand(
            "projects/{project}/secrets/{secret}", project=project, secret=secret
        )

    @classmethod
    def secret_version_path(cls, project, secret, secret_version):
        """Return a fully-qualified secret_version string."""
        return google.api_core.path_template.expand(
            "projects/{project}/secrets/{secret}/versions/{secret_version}",
            project=project,
            secret=secret,
            secret_version=secret_version,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.SecretManagerServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.SecretManagerServiceGrpcTransport]): A transport
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = secret_manager_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=secret_manager_service_grpc_transport.SecretManagerServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = secret_manager_service_grpc_transport.SecretManagerServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
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
    def list_secrets(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ``Secrets``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_secrets(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_secrets(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the project associated with the
                ``Secrets``, in the format ``projects/*``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.secretmanager_v1beta1.types.Secret` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_secrets" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_secrets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_secrets,
                default_retry=self._method_configs["ListSecrets"].retry,
                default_timeout=self._method_configs["ListSecrets"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListSecretsRequest(parent=parent, page_size=page_size)
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
                self._inner_api_calls["list_secrets"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="secrets",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_secret(
        self,
        parent,
        secret_id,
        secret=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new ``Secret`` containing no ``SecretVersions``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `secret_id`:
            >>> secret_id = ''
            >>>
            >>> response = client.create_secret(parent, secret_id)

        Args:
            parent (str): Required. The resource name of the project to associate with the
                ``Secret``, in the format ``projects/*``.
            secret_id (str): Required. This must be unique within the project.

                A secret ID is a string with a maximum length of 255 characters and can
                contain uppercase and lowercase letters, numerals, and the hyphen
                (``-``) and underscore (``_``) characters.
            secret (Union[dict, ~google.cloud.secretmanager_v1beta1.types.Secret]): A ``Secret`` with initial field values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.Secret`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.Secret` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_secret" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_secret"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_secret,
                default_retry=self._method_configs["CreateSecret"].retry,
                default_timeout=self._method_configs["CreateSecret"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateSecretRequest(
            parent=parent, secret_id=secret_id, secret=secret
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

        return self._inner_api_calls["create_secret"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def add_secret_version(
        self,
        parent,
        payload,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new ``SecretVersion`` containing secret data and attaches
        it to an existing ``Secret``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> parent = client.secret_path('[PROJECT]', '[SECRET]')
            >>>
            >>> # TODO: Initialize `payload`:
            >>> payload = {}
            >>>
            >>> response = client.add_secret_version(parent, payload)

        Args:
            parent (str): Required. The resource name of the ``Secret`` to associate with the
                ``SecretVersion`` in the format ``projects/*/secrets/*``.
            payload (Union[dict, ~google.cloud.secretmanager_v1beta1.types.SecretPayload]): Required. The secret payload of the ``SecretVersion``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.SecretPayload`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "add_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "add_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.add_secret_version,
                default_retry=self._method_configs["AddSecretVersion"].retry,
                default_timeout=self._method_configs["AddSecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.AddSecretVersionRequest(parent=parent, payload=payload)
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

        return self._inner_api_calls["add_secret_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_secret(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets metadata for a given ``Secret``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_path('[PROJECT]', '[SECRET]')
            >>>
            >>> response = client.get_secret(name)

        Args:
            name (str): Required. The resource name of the ``Secret``, in the format
                ``projects/*/secrets/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.Secret` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_secret" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_secret"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_secret,
                default_retry=self._method_configs["GetSecret"].retry,
                default_timeout=self._method_configs["GetSecret"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetSecretRequest(name=name)
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

        return self._inner_api_calls["get_secret"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_secret(
        self,
        secret,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates metadata of an existing ``Secret``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> # TODO: Initialize `secret`:
            >>> secret = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_secret(secret, update_mask)

        Args:
            secret (Union[dict, ~google.cloud.secretmanager_v1beta1.types.Secret]): Required. ``Secret`` with updated field values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.Secret`
            update_mask (Union[dict, ~google.cloud.secretmanager_v1beta1.types.FieldMask]): Required. Specifies the fields to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.Secret` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_secret" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_secret"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_secret,
                default_retry=self._method_configs["UpdateSecret"].retry,
                default_timeout=self._method_configs["UpdateSecret"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateSecretRequest(
            secret=secret, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("secret.name", secret.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_secret"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_secret(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a ``Secret``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_path('[PROJECT]', '[SECRET]')
            >>>
            >>> client.delete_secret(name)

        Args:
            name (str): Required. The resource name of the ``Secret`` to delete in the
                format ``projects/*/secrets/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_secret" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_secret"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_secret,
                default_retry=self._method_configs["DeleteSecret"].retry,
                default_timeout=self._method_configs["DeleteSecret"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DeleteSecretRequest(name=name)
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

        self._inner_api_calls["delete_secret"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_secret_versions(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ``SecretVersions``. This call does not return secret data.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> parent = client.secret_path('[PROJECT]', '[SECRET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_secret_versions(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_secret_versions(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the ``Secret`` associated with the
                ``SecretVersions`` to list, in the format ``projects/*/secrets/*``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_secret_versions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_secret_versions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_secret_versions,
                default_retry=self._method_configs["ListSecretVersions"].retry,
                default_timeout=self._method_configs["ListSecretVersions"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListSecretVersionsRequest(
            parent=parent, page_size=page_size
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
                self._inner_api_calls["list_secret_versions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="versions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_secret_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets metadata for a ``SecretVersion``.

        ``projects/*/secrets/*/versions/latest`` is an alias to the ``latest``
        ``SecretVersion``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_version_path('[PROJECT]', '[SECRET]', '[SECRET_VERSION]')
            >>>
            >>> response = client.get_secret_version(name)

        Args:
            name (str): Required. The resource name of the ``SecretVersion`` in the format
                ``projects/*/secrets/*/versions/*``.
                ``projects/*/secrets/*/versions/latest`` is an alias to the ``latest``
                ``SecretVersion``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_secret_version,
                default_retry=self._method_configs["GetSecretVersion"].retry,
                default_timeout=self._method_configs["GetSecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetSecretVersionRequest(name=name)
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

        return self._inner_api_calls["get_secret_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def access_secret_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Accesses a ``SecretVersion``. This call returns the secret data.

        ``projects/*/secrets/*/versions/latest`` is an alias to the ``latest``
        ``SecretVersion``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_version_path('[PROJECT]', '[SECRET]', '[SECRET_VERSION]')
            >>>
            >>> response = client.access_secret_version(name)

        Args:
            name (str): Required. The resource name of the ``SecretVersion`` in the format
                ``projects/*/secrets/*/versions/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.AccessSecretVersionResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "access_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "access_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.access_secret_version,
                default_retry=self._method_configs["AccessSecretVersion"].retry,
                default_timeout=self._method_configs["AccessSecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.AccessSecretVersionRequest(name=name)
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

        return self._inner_api_calls["access_secret_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def disable_secret_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Disables a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``DISABLED``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_version_path('[PROJECT]', '[SECRET]', '[SECRET_VERSION]')
            >>>
            >>> response = client.disable_secret_version(name)

        Args:
            name (str): Required. The resource name of the ``SecretVersion`` to disable in
                the format ``projects/*/secrets/*/versions/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "disable_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "disable_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.disable_secret_version,
                default_retry=self._method_configs["DisableSecretVersion"].retry,
                default_timeout=self._method_configs["DisableSecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DisableSecretVersionRequest(name=name)
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

        return self._inner_api_calls["disable_secret_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def enable_secret_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Enables a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``ENABLED``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_version_path('[PROJECT]', '[SECRET]', '[SECRET_VERSION]')
            >>>
            >>> response = client.enable_secret_version(name)

        Args:
            name (str): Required. The resource name of the ``SecretVersion`` to enable in
                the format ``projects/*/secrets/*/versions/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "enable_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "enable_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.enable_secret_version,
                default_retry=self._method_configs["EnableSecretVersion"].retry,
                default_timeout=self._method_configs["EnableSecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.EnableSecretVersionRequest(name=name)
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

        return self._inner_api_calls["enable_secret_version"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def destroy_secret_version(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Destroys a ``SecretVersion``.

        Sets the ``state`` of the ``SecretVersion`` to ``DESTROYED`` and
        irrevocably destroys the secret data.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> name = client.secret_version_path('[PROJECT]', '[SECRET]', '[SECRET_VERSION]')
            >>>
            >>> response = client.destroy_secret_version(name)

        Args:
            name (str): Required. The resource name of the ``SecretVersion`` to destroy in
                the format ``projects/*/secrets/*/versions/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.SecretVersion` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "destroy_secret_version" not in self._inner_api_calls:
            self._inner_api_calls[
                "destroy_secret_version"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.destroy_secret_version,
                default_retry=self._method_configs["DestroySecretVersion"].retry,
                default_timeout=self._method_configs["DestroySecretVersion"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DestroySecretVersionRequest(name=name)
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

        return self._inner_api_calls["destroy_secret_version"](
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
        Sets the access control policy on the specified secret. Replaces any
        existing policy.

        Permissions on ``SecretVersions`` are enforced according to the policy
        set on the associated ``Secret``.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.secretmanager_v1beta1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.Policy` instance.

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
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a secret.
        Returns empty policy if the secret exists and does not have a policy set.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.secretmanager_v1beta1.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.secretmanager_v1beta1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.Policy` instance.

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

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
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
        Returns permissions that a caller has for the specified secret. If
        the secret does not exist, this call returns an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Example:
            >>> from google.cloud import secretmanager_v1beta1
            >>>
            >>> client = secretmanager_v1beta1.SecretManagerServiceClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions
                with wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.secretmanager_v1beta1.types.TestIamPermissionsResponse` instance.

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
