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
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.asset_v1.services.asset_service import pagers
from google.cloud.asset_v1.types import asset_service
from google.cloud.asset_v1.types import assets
from google.type import expr_pb2 as expr  # type: ignore

from .transports.base import AssetServiceTransport
from .transports.grpc import AssetServiceGrpcTransport
from .transports.grpc_asyncio import AssetServiceGrpcAsyncIOTransport


class AssetServiceClientMeta(type):
    """Metaclass for the AssetService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[AssetServiceTransport]]
    _transport_registry["grpc"] = AssetServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = AssetServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[AssetServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class AssetServiceClient(metaclass=AssetServiceClientMeta):
    """Asset service definition."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "cloudasset.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def feed_path(project: str, feed: str,) -> str:
        """Return a fully-qualified feed string."""
        return "projects/{project}/feeds/{feed}".format(project=project, feed=feed,)

    @staticmethod
    def parse_feed_path(path: str) -> Dict[str, str]:
        """Parse a feed path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/feeds/(?P<feed>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, AssetServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the asset service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AssetServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, AssetServiceTransport):
            # transport is a AssetServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
            )

    def export_assets(
        self,
        request: asset_service.ExportAssetsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Exports assets with time and resource types to a given Cloud
        Storage location/BigQuery table. For Cloud Storage location
        destinations, the output format is newline-delimited JSON. Each
        line represents a
        [google.cloud.asset.v1.Asset][google.cloud.asset.v1.Asset] in
        the JSON format; for BigQuery table destinations, the output
        table stores the fields in asset proto as columns. This API
        implements the
        [google.longrunning.Operation][google.longrunning.Operation] API
        , which allows you to keep track of the export. We recommend
        intervals of at least 2 seconds with exponential retry to poll
        the export operation result. For regular-size resource parent,
        the export operation usually finishes within 5 minutes.

        Args:
            request (:class:`~.asset_service.ExportAssetsRequest`):
                The request object. Export asset request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.asset_service.ExportAssetsResponse``: The
                export asset response. This message is returned by the
                [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
                method in the returned
                [google.longrunning.Operation.response][google.longrunning.Operation.response]
                field.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.ExportAssetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.ExportAssetsRequest):
            request = asset_service.ExportAssetsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_assets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            asset_service.ExportAssetsResponse,
            metadata_type=asset_service.ExportAssetsRequest,
        )

        # Done; return the response.
        return response

    def batch_get_assets_history(
        self,
        request: asset_service.BatchGetAssetsHistoryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> asset_service.BatchGetAssetsHistoryResponse:
        r"""Batch gets the update history of assets that overlap a time
        window. For IAM_POLICY content, this API outputs history when
        the asset and its attached IAM POLICY both exist. This can
        create gaps in the output history. Otherwise, this API outputs
        history with asset in both non-delete or deleted status. If a
        specified asset does not exist, this API returns an
        INVALID_ARGUMENT error.

        Args:
            request (:class:`~.asset_service.BatchGetAssetsHistoryRequest`):
                The request object. Batch get assets history request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.asset_service.BatchGetAssetsHistoryResponse:
                Batch get assets history response.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.BatchGetAssetsHistoryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.BatchGetAssetsHistoryRequest):
            request = asset_service.BatchGetAssetsHistoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_get_assets_history]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_feed(
        self,
        request: asset_service.CreateFeedRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> asset_service.Feed:
        r"""Creates a feed in a parent
        project/folder/organization to listen to its asset
        updates.

        Args:
            request (:class:`~.asset_service.CreateFeedRequest`):
                The request object. Create asset feed request.
            parent (:class:`str`):
                Required. The name of the
                project/folder/organization where this
                feed should be created in. It can only
                be an organization number (such as
                "organizations/123"), a folder number
                (such as "folders/123"), a project ID
                (such as "projects/my-project-id")", or
                a project number (such as
                "projects/12345").
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.asset_service.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.CreateFeedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.CreateFeedRequest):
            request = asset_service.CreateFeedRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_feed]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_feed(
        self,
        request: asset_service.GetFeedRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> asset_service.Feed:
        r"""Gets details about an asset feed.

        Args:
            request (:class:`~.asset_service.GetFeedRequest`):
                The request object. Get asset feed request.
            name (:class:`str`):
                Required. The name of the Feed and it must be in the
                format of: projects/project_number/feeds/feed_id
                folders/folder_number/feeds/feed_id
                organizations/organization_number/feeds/feed_id
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.asset_service.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.GetFeedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.GetFeedRequest):
            request = asset_service.GetFeedRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_feed]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_feeds(
        self,
        request: asset_service.ListFeedsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> asset_service.ListFeedsResponse:
        r"""Lists all asset feeds in a parent
        project/folder/organization.

        Args:
            request (:class:`~.asset_service.ListFeedsRequest`):
                The request object. List asset feeds request.
            parent (:class:`str`):
                Required. The parent
                project/folder/organization whose feeds
                are to be listed. It can only be using
                project/folder/organization number (such
                as "folders/12345")", or a project ID
                (such as "projects/my-project-id").
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.asset_service.ListFeedsResponse:

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

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.ListFeedsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.ListFeedsRequest):
            request = asset_service.ListFeedsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_feeds]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_feed(
        self,
        request: asset_service.UpdateFeedRequest = None,
        *,
        feed: asset_service.Feed = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> asset_service.Feed:
        r"""Updates an asset feed configuration.

        Args:
            request (:class:`~.asset_service.UpdateFeedRequest`):
                The request object. Update asset feed request.
            feed (:class:`~.asset_service.Feed`):
                Required. The new values of feed details. It must match
                an existing feed and the field ``name`` must be in the
                format of: projects/project_number/feeds/feed_id or
                folders/folder_number/feeds/feed_id or
                organizations/organization_number/feeds/feed_id.
                This corresponds to the ``feed`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.asset_service.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([feed])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.UpdateFeedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.UpdateFeedRequest):
            request = asset_service.UpdateFeedRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if feed is not None:
                request.feed = feed

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_feed]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("feed.name", request.feed.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_feed(
        self,
        request: asset_service.DeleteFeedRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an asset feed.

        Args:
            request (:class:`~.asset_service.DeleteFeedRequest`):
                The request object.
            name (:class:`str`):
                Required. The name of the feed and it must be in the
                format of: projects/project_number/feeds/feed_id
                folders/folder_number/feeds/feed_id
                organizations/organization_number/feeds/feed_id
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

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.DeleteFeedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.DeleteFeedRequest):
            request = asset_service.DeleteFeedRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_feed]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def search_all_resources(
        self,
        request: asset_service.SearchAllResourcesRequest = None,
        *,
        scope: str = None,
        query: str = None,
        asset_types: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAllResourcesPager:
        r"""Searches all the resources within the given
        accessible scope (e.g., a project, a folder or an
        organization). Callers should have
        cloud.assets.SearchAllResources permission upon the
        requested scope, otherwise the request will be rejected.

        Args:
            request (:class:`~.asset_service.SearchAllResourcesRequest`):
                The request object. Search all resources request.
            scope (:class:`str`):
                Required. A scope can be a project, a folder or an
                organization. The search is limited to the resources
                within the ``scope``.

                The allowed values are:

                -  projects/{PROJECT_ID}
                -  projects/{PROJECT_NUMBER}
                -  folders/{FOLDER_NUMBER}
                -  organizations/{ORGANIZATION_NUMBER}
                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Optional. The query statement. An empty query can be
                specified to search all the resources of certain
                ``asset_types`` within the given ``scope``.

                Examples:

                -  ``name : "Important"`` to find Cloud resources whose
                   name contains "Important" as a word.
                -  ``displayName : "Impor*"`` to find Cloud resources
                   whose display name contains "Impor" as a word prefix.
                -  ``description : "*por*"`` to find Cloud resources
                   whose description contains "por" as a substring.
                -  ``location : "us-west*"`` to find Cloud resources
                   whose location is prefixed with "us-west".
                -  ``labels : "prod"`` to find Cloud resources whose
                   labels contain "prod" as a key or value.
                -  ``labels.env : "prod"`` to find Cloud resources which
                   have a label "env" and its value is "prod".
                -  ``labels.env : *`` to find Cloud resources which have
                   a label "env".
                -  ``"Important"`` to find Cloud resources which contain
                   "Important" as a word in any of the searchable
                   fields.
                -  ``"Impor*"`` to find Cloud resources which contain
                   "Impor" as a word prefix in any of the searchable
                   fields.
                -  ``"*por*"`` to find Cloud resources which contain
                   "por" as a substring in any of the searchable fields.
                -  ``("Important" AND location : ("us-west1" OR "global"))``
                   to find Cloud resources which contain "Important" as
                   a word in any of the searchable fields and are also
                   located in the "us-west1" region or the "global"
                   location.

                See `how to construct a
                query <https://cloud.google.com/asset-inventory/docs/searching-resources#how_to_construct_a_query>`__
                for more details.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            asset_types (:class:`Sequence[str]`):
                Optional. A list of asset types that this request
                searches for. If empty, it will search all the
                `searchable asset
                types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__.
                This corresponds to the ``asset_types`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.SearchAllResourcesPager:
                Search all resources response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scope, query, asset_types])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.SearchAllResourcesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.SearchAllResourcesRequest):
            request = asset_service.SearchAllResourcesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if scope is not None:
                request.scope = scope
            if query is not None:
                request.query = query
            if asset_types is not None:
                request.asset_types = asset_types

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_all_resources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("scope", request.scope),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchAllResourcesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_all_iam_policies(
        self,
        request: asset_service.SearchAllIamPoliciesRequest = None,
        *,
        scope: str = None,
        query: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAllIamPoliciesPager:
        r"""Searches all the IAM policies within the given
        accessible scope (e.g., a project, a folder or an
        organization). Callers should have
        cloud.assets.SearchAllIamPolicies permission upon the
        requested scope, otherwise the request will be rejected.

        Args:
            request (:class:`~.asset_service.SearchAllIamPoliciesRequest`):
                The request object. Search all IAM policies request.
            scope (:class:`str`):
                Required. A scope can be a project, a folder or an
                organization. The search is limited to the IAM policies
                within the ``scope``.

                The allowed values are:

                -  projects/{PROJECT_ID}
                -  projects/{PROJECT_NUMBER}
                -  folders/{FOLDER_NUMBER}
                -  organizations/{ORGANIZATION_NUMBER}
                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Optional. The query statement. An empty query can be
                specified to search all the IAM policies within the
                given ``scope``.

                Examples:

                -  ``policy : "amy@gmail.com"`` to find Cloud IAM policy
                   bindings that specify user "amy@gmail.com".
                -  ``policy : "roles/compute.admin"`` to find Cloud IAM
                   policy bindings that specify the Compute Admin role.
                -  ``policy.role.permissions : "storage.buckets.update"``
                   to find Cloud IAM policy bindings that specify a role
                   containing "storage.buckets.update" permission.
                -  ``resource : "organizations/123"`` to find Cloud IAM
                   policy bindings that are set on "organizations/123".
                -  ``(resource : ("organizations/123" OR "folders/1234") AND policy : "amy")``
                   to find Cloud IAM policy bindings that are set on
                   "organizations/123" or "folders/1234", and also
                   specify user "amy".

                See `how to construct a
                query <https://cloud.google.com/asset-inventory/docs/searching-iam-policies#how_to_construct_a_query>`__
                for more details.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.SearchAllIamPoliciesPager:
                Search all IAM policies response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scope, query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a asset_service.SearchAllIamPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, asset_service.SearchAllIamPoliciesRequest):
            request = asset_service.SearchAllIamPoliciesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if scope is not None:
                request.scope = scope
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_all_iam_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("scope", request.scope),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchAllIamPoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-asset",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("AssetServiceClient",)
