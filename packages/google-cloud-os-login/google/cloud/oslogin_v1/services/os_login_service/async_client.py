# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.cloud.oslogin_v1 import common  # type: ignore
from google.cloud.oslogin_v1.types import oslogin
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import OsLoginServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import OsLoginServiceGrpcAsyncIOTransport
from .client import OsLoginServiceClient


class OsLoginServiceAsyncClient:
    """Cloud OS Login API
    The Cloud OS Login API allows you to manage users and their
    associated SSH public keys for logging into virtual machines on
    Google Cloud Platform.
    """

    _client: OsLoginServiceClient

    DEFAULT_ENDPOINT = OsLoginServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = OsLoginServiceClient.DEFAULT_MTLS_ENDPOINT

    posix_account_path = staticmethod(OsLoginServiceClient.posix_account_path)
    parse_posix_account_path = staticmethod(
        OsLoginServiceClient.parse_posix_account_path
    )
    ssh_public_key_path = staticmethod(OsLoginServiceClient.ssh_public_key_path)
    parse_ssh_public_key_path = staticmethod(
        OsLoginServiceClient.parse_ssh_public_key_path
    )
    common_billing_account_path = staticmethod(
        OsLoginServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        OsLoginServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(OsLoginServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        OsLoginServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        OsLoginServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        OsLoginServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(OsLoginServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        OsLoginServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(OsLoginServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        OsLoginServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            OsLoginServiceAsyncClient: The constructed client.
        """
        return OsLoginServiceClient.from_service_account_info.__func__(OsLoginServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            OsLoginServiceAsyncClient: The constructed client.
        """
        return OsLoginServiceClient.from_service_account_file.__func__(OsLoginServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OsLoginServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            OsLoginServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(OsLoginServiceClient).get_transport_class, type(OsLoginServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, OsLoginServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the os login service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.OsLoginServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = OsLoginServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def delete_posix_account(
        self,
        request: Union[oslogin.DeletePosixAccountRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a POSIX account.

        Args:
            request (Union[google.cloud.oslogin_v1.types.DeletePosixAccountRequest, dict]):
                The request object. A request message for deleting a
                POSIX account entry.
            name (:class:`str`):
                Required. A reference to the POSIX account to update.
                POSIX accounts are identified by the project ID they are
                associated with. A reference to the POSIX account is in
                format ``users/{user}/projects/{project}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.DeletePosixAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_posix_account,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def delete_ssh_public_key(
        self,
        request: Union[oslogin.DeleteSshPublicKeyRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an SSH public key.

        Args:
            request (Union[google.cloud.oslogin_v1.types.DeleteSshPublicKeyRequest, dict]):
                The request object. A request message for deleting an
                SSH public key.
            name (:class:`str`):
                Required. The fingerprint of the public key to update.
                Public keys are identified by their SHA-256 fingerprint.
                The fingerprint of the public key is in format
                ``users/{user}/sshPublicKeys/{fingerprint}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.DeleteSshPublicKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_ssh_public_key,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def get_login_profile(
        self,
        request: Union[oslogin.GetLoginProfileRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> oslogin.LoginProfile:
        r"""Retrieves the profile information used for logging in
        to a virtual machine on Google Compute Engine.

        Args:
            request (Union[google.cloud.oslogin_v1.types.GetLoginProfileRequest, dict]):
                The request object. A request message for retrieving the
                login profile information for a user.
            name (:class:`str`):
                Required. The unique ID for the user in format
                ``users/{user}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.oslogin_v1.types.LoginProfile:
                The user profile information used for
                logging in to a virtual machine on
                Google Compute Engine.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.GetLoginProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_login_profile,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_ssh_public_key(
        self,
        request: Union[oslogin.GetSshPublicKeyRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> common.SshPublicKey:
        r"""Retrieves an SSH public key.

        Args:
            request (Union[google.cloud.oslogin_v1.types.GetSshPublicKeyRequest, dict]):
                The request object. A request message for retrieving an
                SSH public key.
            name (:class:`str`):
                Required. The fingerprint of the public key to retrieve.
                Public keys are identified by their SHA-256 fingerprint.
                The fingerprint of the public key is in format
                ``users/{user}/sshPublicKeys/{fingerprint}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.oslogin.v1.common.SshPublicKey:
                The SSH public key information
                associated with a Google account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.GetSshPublicKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_ssh_public_key,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def import_ssh_public_key(
        self,
        request: Union[oslogin.ImportSshPublicKeyRequest, dict] = None,
        *,
        parent: str = None,
        ssh_public_key: common.SshPublicKey = None,
        project_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> oslogin.ImportSshPublicKeyResponse:
        r"""Adds an SSH public key and returns the profile
        information. Default POSIX account information is set
        when no username and UID exist as part of the login
        profile.

        Args:
            request (Union[google.cloud.oslogin_v1.types.ImportSshPublicKeyRequest, dict]):
                The request object. A request message for importing an
                SSH public key.
            parent (:class:`str`):
                Required. The unique ID for the user in format
                ``users/{user}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ssh_public_key (:class:`google.cloud.oslogin.v1.common.SshPublicKey`):
                Optional. The SSH public key and
                expiration time.

                This corresponds to the ``ssh_public_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            project_id (:class:`str`):
                The project ID of the Google Cloud
                Platform project.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.oslogin_v1.types.ImportSshPublicKeyResponse:
                A response message for importing an
                SSH public key.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, ssh_public_key, project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.ImportSshPublicKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if ssh_public_key is not None:
            request.ssh_public_key = ssh_public_key
        if project_id is not None:
            request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_ssh_public_key,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_ssh_public_key(
        self,
        request: Union[oslogin.UpdateSshPublicKeyRequest, dict] = None,
        *,
        name: str = None,
        ssh_public_key: common.SshPublicKey = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> common.SshPublicKey:
        r"""Updates an SSH public key and returns the profile
        information. This method supports patch semantics.

        Args:
            request (Union[google.cloud.oslogin_v1.types.UpdateSshPublicKeyRequest, dict]):
                The request object. A request message for updating an
                SSH public key.
            name (:class:`str`):
                Required. The fingerprint of the public key to update.
                Public keys are identified by their SHA-256 fingerprint.
                The fingerprint of the public key is in format
                ``users/{user}/sshPublicKeys/{fingerprint}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ssh_public_key (:class:`google.cloud.oslogin.v1.common.SshPublicKey`):
                Required. The SSH public key and
                expiration time.

                This corresponds to the ``ssh_public_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Mask to control which fields get
                updated. Updates all if not present.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.oslogin.v1.common.SshPublicKey:
                The SSH public key information
                associated with a Google account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, ssh_public_key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = oslogin.UpdateSshPublicKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if ssh_public_key is not None:
            request.ssh_public_key = ssh_public_key
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_ssh_public_key,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=10.0,
            ),
            default_timeout=10.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-os-login",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("OsLoginServiceAsyncClient",)
