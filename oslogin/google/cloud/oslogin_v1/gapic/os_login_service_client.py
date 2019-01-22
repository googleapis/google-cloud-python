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
"""Accesses the google.cloud.oslogin.v1 OsLoginService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.oslogin_v1.gapic import os_login_service_client_config
from google.cloud.oslogin_v1.gapic.transports import os_login_service_grpc_transport
from google.cloud.oslogin_v1.proto import common_pb2
from google.cloud.oslogin_v1.proto import oslogin_pb2
from google.cloud.oslogin_v1.proto import oslogin_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-os-login").version


class OsLoginServiceClient(object):
    """
    Cloud OS Login API

    The Cloud OS Login API allows you to manage users and their associated SSH
    public keys for logging into virtual machines on Google Cloud Platform.
    """

    SERVICE_ADDRESS = "oslogin.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.oslogin.v1.OsLoginService"

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
            OsLoginServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def user_path(cls, user):
        """Return a fully-qualified user string."""
        return google.api_core.path_template.expand("users/{user}", user=user)

    @classmethod
    def project_path(cls, user, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "users/{user}/projects/{project}", user=user, project=project
        )

    @classmethod
    def fingerprint_path(cls, user, fingerprint):
        """Return a fully-qualified fingerprint string."""
        return google.api_core.path_template.expand(
            "users/{user}/sshPublicKeys/{fingerprint}",
            user=user,
            fingerprint=fingerprint,
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
            transport (Union[~.OsLoginServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.OsLoginServiceGrpcTransport]): A transport
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
            client_config = os_login_service_client_config.config

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
                    default_class=os_login_service_grpc_transport.OsLoginServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = os_login_service_grpc_transport.OsLoginServiceGrpcTransport(
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
    def delete_posix_account(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a POSIX account.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> name = client.project_path('[USER]', '[PROJECT]')
            >>>
            >>> client.delete_posix_account(name)

        Args:
            name (str): A reference to the POSIX account to update. POSIX accounts are
                identified by the project ID they are associated with. A reference to
                the POSIX account is in format ``users/{user}/projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if "delete_posix_account" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_posix_account"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_posix_account,
                default_retry=self._method_configs["DeletePosixAccount"].retry,
                default_timeout=self._method_configs["DeletePosixAccount"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.DeletePosixAccountRequest(name=name)
        self._inner_api_calls["delete_posix_account"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_ssh_public_key(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an SSH public key.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> name = client.fingerprint_path('[USER]', '[FINGERPRINT]')
            >>>
            >>> client.delete_ssh_public_key(name)

        Args:
            name (str): The fingerprint of the public key to update. Public keys are identified
                by their SHA-256 fingerprint. The fingerprint of the public key is in
                format ``users/{user}/sshPublicKeys/{fingerprint}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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
        if "delete_ssh_public_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_ssh_public_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_ssh_public_key,
                default_retry=self._method_configs["DeleteSshPublicKey"].retry,
                default_timeout=self._method_configs["DeleteSshPublicKey"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.DeleteSshPublicKeyRequest(name=name)
        self._inner_api_calls["delete_ssh_public_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_login_profile(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves the profile information used for logging in to a virtual machine
        on Google Compute Engine.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> name = client.user_path('[USER]')
            >>>
            >>> response = client.get_login_profile(name)

        Args:
            name (str): The unique ID for the user in format ``users/{user}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.oslogin_v1.types.LoginProfile` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_login_profile" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_login_profile"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_login_profile,
                default_retry=self._method_configs["GetLoginProfile"].retry,
                default_timeout=self._method_configs["GetLoginProfile"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.GetLoginProfileRequest(name=name)
        return self._inner_api_calls["get_login_profile"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_ssh_public_key(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves an SSH public key.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> name = client.fingerprint_path('[USER]', '[FINGERPRINT]')
            >>>
            >>> response = client.get_ssh_public_key(name)

        Args:
            name (str): The fingerprint of the public key to retrieve. Public keys are
                identified by their SHA-256 fingerprint. The fingerprint of the public
                key is in format ``users/{user}/sshPublicKeys/{fingerprint}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.oslogin_v1.types.SshPublicKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_ssh_public_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_ssh_public_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_ssh_public_key,
                default_retry=self._method_configs["GetSshPublicKey"].retry,
                default_timeout=self._method_configs["GetSshPublicKey"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.GetSshPublicKeyRequest(name=name)
        return self._inner_api_calls["get_ssh_public_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def import_ssh_public_key(
        self,
        parent,
        ssh_public_key,
        project_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Adds an SSH public key and returns the profile information. Default POSIX
        account information is set when no username and UID exist as part of the
        login profile.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> parent = client.user_path('[USER]')
            >>>
            >>> # TODO: Initialize `ssh_public_key`:
            >>> ssh_public_key = {}
            >>>
            >>> response = client.import_ssh_public_key(parent, ssh_public_key)

        Args:
            parent (str): The unique ID for the user in format ``users/{user}``.
            ssh_public_key (Union[dict, ~google.cloud.oslogin_v1.types.SshPublicKey]): The SSH public key and expiration time.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.oslogin_v1.types.SshPublicKey`
            project_id (str): The project ID of the Google Cloud Platform project.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.oslogin_v1.types.ImportSshPublicKeyResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_ssh_public_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_ssh_public_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_ssh_public_key,
                default_retry=self._method_configs["ImportSshPublicKey"].retry,
                default_timeout=self._method_configs["ImportSshPublicKey"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.ImportSshPublicKeyRequest(
            parent=parent, ssh_public_key=ssh_public_key, project_id=project_id
        )
        return self._inner_api_calls["import_ssh_public_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_ssh_public_key(
        self,
        name,
        ssh_public_key,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an SSH public key and returns the profile information. This method
        supports patch semantics.

        Example:
            >>> from google.cloud import oslogin_v1
            >>>
            >>> client = oslogin_v1.OsLoginServiceClient()
            >>>
            >>> name = client.fingerprint_path('[USER]', '[FINGERPRINT]')
            >>>
            >>> # TODO: Initialize `ssh_public_key`:
            >>> ssh_public_key = {}
            >>>
            >>> response = client.update_ssh_public_key(name, ssh_public_key)

        Args:
            name (str): The fingerprint of the public key to update. Public keys are identified
                by their SHA-256 fingerprint. The fingerprint of the public key is in
                format ``users/{user}/sshPublicKeys/{fingerprint}``.
            ssh_public_key (Union[dict, ~google.cloud.oslogin_v1.types.SshPublicKey]): The SSH public key and expiration time.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.oslogin_v1.types.SshPublicKey`
            update_mask (Union[dict, ~google.cloud.oslogin_v1.types.FieldMask]): Mask to control which fields get updated. Updates all if not present.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.oslogin_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.oslogin_v1.types.SshPublicKey` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_ssh_public_key" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_ssh_public_key"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_ssh_public_key,
                default_retry=self._method_configs["UpdateSshPublicKey"].retry,
                default_timeout=self._method_configs["UpdateSshPublicKey"].timeout,
                client_info=self._client_info,
            )

        request = oslogin_pb2.UpdateSshPublicKeyRequest(
            name=name, ssh_public_key=ssh_public_key, update_mask=update_mask
        )
        return self._inner_api_calls["update_ssh_public_key"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
