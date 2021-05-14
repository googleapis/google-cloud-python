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

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflow_v2.services.versions import pagers
from google.cloud.dialogflow_v2.types import version
from google.cloud.dialogflow_v2.types import version as gcd_version
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import VersionsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import VersionsGrpcAsyncIOTransport
from .client import VersionsClient


class VersionsAsyncClient:
    """Service for managing [Versions][google.cloud.dialogflow.v2.Version]."""

    _client: VersionsClient

    DEFAULT_ENDPOINT = VersionsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = VersionsClient.DEFAULT_MTLS_ENDPOINT

    version_path = staticmethod(VersionsClient.version_path)
    parse_version_path = staticmethod(VersionsClient.parse_version_path)
    common_billing_account_path = staticmethod(
        VersionsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        VersionsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(VersionsClient.common_folder_path)
    parse_common_folder_path = staticmethod(VersionsClient.parse_common_folder_path)
    common_organization_path = staticmethod(VersionsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        VersionsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(VersionsClient.common_project_path)
    parse_common_project_path = staticmethod(VersionsClient.parse_common_project_path)
    common_location_path = staticmethod(VersionsClient.common_location_path)
    parse_common_location_path = staticmethod(VersionsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            VersionsAsyncClient: The constructed client.
        """
        return VersionsClient.from_service_account_info.__func__(VersionsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            VersionsAsyncClient: The constructed client.
        """
        return VersionsClient.from_service_account_file.__func__(VersionsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> VersionsTransport:
        """Returns the transport used by the client instance.

        Returns:
            VersionsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(VersionsClient).get_transport_class, type(VersionsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, VersionsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the versions client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.VersionsTransport]): The
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
        self._client = VersionsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_versions(
        self,
        request: version.ListVersionsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVersionsAsyncPager:
        r"""Returns the list of all versions of the specified
        agent.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ListVersionsRequest`):
                The request object. The request message for
                [Versions.ListVersions][google.cloud.dialogflow.v2.Versions.ListVersions].
            parent (:class:`str`):
                Required. The agent to list all versions from. Supported
                formats:

                -  ``projects/<Project ID>/agent``
                -  ``projects/<Project ID>/locations/<Location ID>/agent``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.versions.pagers.ListVersionsAsyncPager:
                The response message for
                [Versions.ListVersions][google.cloud.dialogflow.v2.Versions.ListVersions].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = version.ListVersionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_versions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListVersionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_version(
        self,
        request: version.GetVersionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> version.Version:
        r"""Retrieves the specified agent version.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetVersionRequest`):
                The request object. The request message for
                [Versions.GetVersion][google.cloud.dialogflow.v2.Versions.GetVersion].
            name (:class:`str`):
                Required. The name of the version. Supported formats:

                -  ``projects/<Project ID>/agent/versions/<Version ID>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/versions/<Version ID>``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Version:
                You can create multiple versions of your agent and publish them to separate
                   environments.

                   When you edit an agent, you are editing the draft
                   agent. At any point, you can save the draft agent as
                   an agent version, which is an immutable snapshot of
                   your agent.

                   When you save the draft agent, it is published to the
                   default environment. When you create agent versions,
                   you can publish them to custom environments. You can
                   create a variety of custom environments for:

                   -  testing
                   -  development
                   -  production
                   -  etc.

                   For more information, see the [versions and
                   environments
                   guide](\ https://cloud.google.com/dialogflow/docs/agents-versions).

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

        request = version.GetVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_version,
            default_timeout=None,
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

    async def create_version(
        self,
        request: gcd_version.CreateVersionRequest = None,
        *,
        parent: str = None,
        version: gcd_version.Version = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_version.Version:
        r"""Creates an agent version.
        The new version points to the agent instance in the
        "default" environment.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.CreateVersionRequest`):
                The request object. The request message for
                [Versions.CreateVersion][google.cloud.dialogflow.v2.Versions.CreateVersion].
            parent (:class:`str`):
                Required. The agent to create a version for. Supported
                formats:

                -  ``projects/<Project ID>/agent``
                -  ``projects/<Project ID>/locations/<Location ID>/agent``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            version (:class:`google.cloud.dialogflow_v2.types.Version`):
                Required. The version to create.
                This corresponds to the ``version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Version:
                You can create multiple versions of your agent and publish them to separate
                   environments.

                   When you edit an agent, you are editing the draft
                   agent. At any point, you can save the draft agent as
                   an agent version, which is an immutable snapshot of
                   your agent.

                   When you save the draft agent, it is published to the
                   default environment. When you create agent versions,
                   you can publish them to custom environments. You can
                   create a variety of custom environments for:

                   -  testing
                   -  development
                   -  production
                   -  etc.

                   For more information, see the [versions and
                   environments
                   guide](\ https://cloud.google.com/dialogflow/docs/agents-versions).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, version])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_version.CreateVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if version is not None:
            request.version = version

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_version,
            default_timeout=None,
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

    async def update_version(
        self,
        request: gcd_version.UpdateVersionRequest = None,
        *,
        version: gcd_version.Version = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_version.Version:
        r"""Updates the specified agent version.
        Note that this method does not allow you to update the
        state of the agent the given version points to. It
        allows you to update only mutable properties of the
        version resource.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateVersionRequest`):
                The request object. The request message for
                [Versions.UpdateVersion][google.cloud.dialogflow.v2.Versions.UpdateVersion].
            version (:class:`google.cloud.dialogflow_v2.types.Version`):
                Required. The version to update. Supported formats:

                -  ``projects/<Project ID>/agent/versions/<Version ID>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/versions/<Version ID>``

                This corresponds to the ``version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Version:
                You can create multiple versions of your agent and publish them to separate
                   environments.

                   When you edit an agent, you are editing the draft
                   agent. At any point, you can save the draft agent as
                   an agent version, which is an immutable snapshot of
                   your agent.

                   When you save the draft agent, it is published to the
                   default environment. When you create agent versions,
                   you can publish them to custom environments. You can
                   create a variety of custom environments for:

                   -  testing
                   -  development
                   -  production
                   -  etc.

                   For more information, see the [versions and
                   environments
                   guide](\ https://cloud.google.com/dialogflow/docs/agents-versions).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([version, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_version.UpdateVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if version is not None:
            request.version = version
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_version,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("version.name", request.version.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_version(
        self,
        request: version.DeleteVersionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete the specified agent version.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.DeleteVersionRequest`):
                The request object. The request message for
                [Versions.DeleteVersion][google.cloud.dialogflow.v2.Versions.DeleteVersion].
            name (:class:`str`):
                Required. The name of the version to delete. Supported
                formats:

                -  ``projects/<Project ID>/agent/versions/<Version ID>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/versions/<Version ID>``

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

        request = version.DeleteVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_version,
            default_timeout=None,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("VersionsAsyncClient",)
