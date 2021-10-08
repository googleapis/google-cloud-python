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

from google.cloud.artifactregistry_v1.services.artifact_registry import pagers
from google.cloud.artifactregistry_v1.types import artifact
from google.cloud.artifactregistry_v1.types import repository
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ArtifactRegistryTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ArtifactRegistryGrpcAsyncIOTransport
from .client import ArtifactRegistryClient


class ArtifactRegistryAsyncClient:
    """The Artifact Registry API service.

    Artifact Registry is an artifact management system for storing
    artifacts from different package management systems.

    The resources managed by this API are:

    -  Repositories, which group packages and their data.
    -  Packages, which group versions and their tags.
    -  Versions, which are specific forms of a package.
    -  Tags, which represent alternative names for versions.
    -  Files, which contain content and are optionally associated with a
       Package or Version.
    """

    _client: ArtifactRegistryClient

    DEFAULT_ENDPOINT = ArtifactRegistryClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ArtifactRegistryClient.DEFAULT_MTLS_ENDPOINT

    docker_image_path = staticmethod(ArtifactRegistryClient.docker_image_path)
    parse_docker_image_path = staticmethod(
        ArtifactRegistryClient.parse_docker_image_path
    )
    repository_path = staticmethod(ArtifactRegistryClient.repository_path)
    parse_repository_path = staticmethod(ArtifactRegistryClient.parse_repository_path)
    common_billing_account_path = staticmethod(
        ArtifactRegistryClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ArtifactRegistryClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ArtifactRegistryClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ArtifactRegistryClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ArtifactRegistryClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ArtifactRegistryClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ArtifactRegistryClient.common_project_path)
    parse_common_project_path = staticmethod(
        ArtifactRegistryClient.parse_common_project_path
    )
    common_location_path = staticmethod(ArtifactRegistryClient.common_location_path)
    parse_common_location_path = staticmethod(
        ArtifactRegistryClient.parse_common_location_path
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
            ArtifactRegistryAsyncClient: The constructed client.
        """
        return ArtifactRegistryClient.from_service_account_info.__func__(ArtifactRegistryAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ArtifactRegistryAsyncClient: The constructed client.
        """
        return ArtifactRegistryClient.from_service_account_file.__func__(ArtifactRegistryAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ArtifactRegistryTransport:
        """Returns the transport used by the client instance.

        Returns:
            ArtifactRegistryTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ArtifactRegistryClient).get_transport_class, type(ArtifactRegistryClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ArtifactRegistryTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the artifact registry client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ArtifactRegistryTransport]): The
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
        self._client = ArtifactRegistryClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_docker_images(
        self,
        request: artifact.ListDockerImagesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDockerImagesAsyncPager:
        r"""Lists docker images.

        Args:
            request (:class:`google.cloud.artifactregistry_v1.types.ListDockerImagesRequest`):
                The request object. The request to list docker images.
            parent (:class:`str`):
                Required. The name of the parent
                resource whose docker images will be
                listed.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.artifactregistry_v1.services.artifact_registry.pagers.ListDockerImagesAsyncPager:
                The response from listing docker
                images.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = artifact.ListDockerImagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_docker_images,
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
        response = pagers.ListDockerImagesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_repositories(
        self,
        request: repository.ListRepositoriesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRepositoriesAsyncPager:
        r"""Lists repositories.

        Args:
            request (:class:`google.cloud.artifactregistry_v1.types.ListRepositoriesRequest`):
                The request object. The request to list repositories.
            parent (:class:`str`):
                Required. The name of the parent
                resource whose repositories will be
                listed.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.artifactregistry_v1.services.artifact_registry.pagers.ListRepositoriesAsyncPager:
                The response from listing
                repositories.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = repository.ListRepositoriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_repositories,
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
        response = pagers.ListRepositoriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_repository(
        self,
        request: repository.GetRepositoryRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> repository.Repository:
        r"""Gets a repository.

        Args:
            request (:class:`google.cloud.artifactregistry_v1.types.GetRepositoryRequest`):
                The request object. The request to retrieve a
                repository.
            name (:class:`str`):
                Required. The name of the repository
                to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.artifactregistry_v1.types.Repository:
                A Repository for storing artifacts
                with a specific format.

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

        request = repository.GetRepositoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_repository,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-artifact-registry",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ArtifactRegistryAsyncClient",)
