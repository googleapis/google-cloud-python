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

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.datacatalog_v1.services.data_catalog import pagers
from google.cloud.datacatalog_v1.types import common
from google.cloud.datacatalog_v1.types import data_source
from google.cloud.datacatalog_v1.types import datacatalog
from google.cloud.datacatalog_v1.types import gcs_fileset_spec
from google.cloud.datacatalog_v1.types import schema
from google.cloud.datacatalog_v1.types import search
from google.cloud.datacatalog_v1.types import table_spec
from google.cloud.datacatalog_v1.types import tags
from google.cloud.datacatalog_v1.types import timestamps
from google.cloud.datacatalog_v1.types import usage
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import DataCatalogTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DataCatalogGrpcAsyncIOTransport
from .client import DataCatalogClient


class DataCatalogAsyncClient:
    """Data Catalog API service allows you to discover, understand,
    and manage your data.
    """

    _client: DataCatalogClient

    DEFAULT_ENDPOINT = DataCatalogClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DataCatalogClient.DEFAULT_MTLS_ENDPOINT

    entry_path = staticmethod(DataCatalogClient.entry_path)
    parse_entry_path = staticmethod(DataCatalogClient.parse_entry_path)
    entry_group_path = staticmethod(DataCatalogClient.entry_group_path)
    parse_entry_group_path = staticmethod(DataCatalogClient.parse_entry_group_path)
    tag_path = staticmethod(DataCatalogClient.tag_path)
    parse_tag_path = staticmethod(DataCatalogClient.parse_tag_path)
    tag_template_path = staticmethod(DataCatalogClient.tag_template_path)
    parse_tag_template_path = staticmethod(DataCatalogClient.parse_tag_template_path)
    tag_template_field_path = staticmethod(DataCatalogClient.tag_template_field_path)
    parse_tag_template_field_path = staticmethod(
        DataCatalogClient.parse_tag_template_field_path
    )
    tag_template_field_enum_value_path = staticmethod(
        DataCatalogClient.tag_template_field_enum_value_path
    )
    parse_tag_template_field_enum_value_path = staticmethod(
        DataCatalogClient.parse_tag_template_field_enum_value_path
    )
    common_billing_account_path = staticmethod(
        DataCatalogClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DataCatalogClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DataCatalogClient.common_folder_path)
    parse_common_folder_path = staticmethod(DataCatalogClient.parse_common_folder_path)
    common_organization_path = staticmethod(DataCatalogClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        DataCatalogClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DataCatalogClient.common_project_path)
    parse_common_project_path = staticmethod(
        DataCatalogClient.parse_common_project_path
    )
    common_location_path = staticmethod(DataCatalogClient.common_location_path)
    parse_common_location_path = staticmethod(
        DataCatalogClient.parse_common_location_path
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
            DataCatalogAsyncClient: The constructed client.
        """
        return DataCatalogClient.from_service_account_info.__func__(DataCatalogAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DataCatalogAsyncClient: The constructed client.
        """
        return DataCatalogClient.from_service_account_file.__func__(DataCatalogAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataCatalogTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataCatalogTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DataCatalogClient).get_transport_class, type(DataCatalogClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DataCatalogTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the data catalog client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DataCatalogTransport]): The
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
        self._client = DataCatalogClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def search_catalog(
        self,
        request: Union[datacatalog.SearchCatalogRequest, dict] = None,
        *,
        scope: datacatalog.SearchCatalogRequest.Scope = None,
        query: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchCatalogAsyncPager:
        r"""Searches Data Catalog for multiple resources like entries and
        tags that match a query.

        This is a [Custom Method]
        (https://cloud.google.com/apis/design/custom_methods) that
        doesn't return all information on a resource, only its ID and
        high level fields. To get more information, you can subsequently
        call specific get methods.

        Note: Data Catalog search queries don't guarantee full recall.
        Results that match your query might not be returned, even in
        subsequent result pages. Additionally, returned (and not
        returned) results can vary if you repeat search queries.

        For more information, see [Data Catalog search syntax]
        (https://cloud.google.com/data-catalog/docs/how-to/search-reference).

        Args:
            request (Union[google.cloud.datacatalog_v1.types.SearchCatalogRequest, dict]):
                The request object. Request message for
                [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].
            scope (:class:`google.cloud.datacatalog_v1.types.SearchCatalogRequest.Scope`):
                Required. The scope of this search request.

                The ``scope`` is invalid if ``include_org_ids``,
                ``include_project_ids`` are empty AND
                ``include_gcp_public_datasets`` is set to ``false``. In
                this case, the request returns an error.

                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Optional. The query string with a minimum of 3
                characters and specific syntax. For more information,
                see `Data Catalog search
                syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__.

                An empty query string returns all data assets (in the
                specified scope) that you have access to.

                A query string can be a simple ``xyz`` or qualified by
                predicates:

                -  ``name:x``
                -  ``column:y``
                -  ``description:z``

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.services.data_catalog.pagers.SearchCatalogAsyncPager:
                Response message for
                   [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = datacatalog.SearchCatalogRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if scope is not None:
            request.scope = scope
        if query is not None:
            request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_catalog,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.SearchCatalogAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_entry_group(
        self,
        request: Union[datacatalog.CreateEntryGroupRequest, dict] = None,
        *,
        parent: str = None,
        entry_group_id: str = None,
        entry_group: datacatalog.EntryGroup = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.EntryGroup:
        r"""Creates an entry group.

        An entry group contains logically related entries together with
        `Cloud Identity and Access
        Management </data-catalog/docs/concepts/iam>`__ policies. These
        policies specify users who can create, edit, and view entries
        within entry groups.

        Data Catalog automatically creates entry groups with names that
        start with the ``@`` symbol for the following resources:

        -  BigQuery entries (``@bigquery``)
        -  Pub/Sub topics (``@pubsub``)
        -  Dataproc Metastore services
           (``@dataproc_metastore_{SERVICE_NAME_HASH}``)

        You can create your own entry groups for Cloud Storage fileset
        entries and custom entries together with the corresponding IAM
        policies. User-created entry groups can't contain the ``@``
        symbol, it is reserved for automatically created groups.

        Entry groups, like entries, can be searched.

        A maximum of 10,000 entry groups may be created per organization
        across all locations.

        You must enable the Data Catalog API in the project identified
        by the ``parent`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.CreateEntryGroupRequest, dict]):
                The request object. Request message for
                [CreateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.CreateEntryGroup].
            parent (:class:`str`):
                Required. The names of the project
                and location that the new entry group
                belongs to.  Note: The entry group
                itself and its child resources might not
                be stored in the location specified in
                its name.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entry_group_id (:class:`str`):
                Required. The ID of the entry group to create.

                The ID must contain only letters (a-z, A-Z), numbers
                (0-9), underscores (_), and must start with a letter or
                underscore. The maximum size is 64 bytes when encoded in
                UTF-8.

                This corresponds to the ``entry_group_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entry_group (:class:`google.cloud.datacatalog_v1.types.EntryGroup`):
                The entry group to create. Defaults
                to empty.

                This corresponds to the ``entry_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.EntryGroup:
                Entry group metadata.

                   An EntryGroup resource represents a logical grouping
                   of zero or more Data Catalog
                   [Entry][google.cloud.datacatalog.v1.Entry] resources.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, entry_group_id, entry_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.CreateEntryGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if entry_group_id is not None:
            request.entry_group_id = entry_group_id
        if entry_group is not None:
            request.entry_group = entry_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_entry_group,
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

    async def get_entry_group(
        self,
        request: Union[datacatalog.GetEntryGroupRequest, dict] = None,
        *,
        name: str = None,
        read_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.EntryGroup:
        r"""Gets an entry group.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.GetEntryGroupRequest, dict]):
                The request object. Request message for
                [GetEntryGroup][google.cloud.datacatalog.v1.DataCatalog.GetEntryGroup].
            name (:class:`str`):
                Required. The name of the entry group
                to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            read_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The fields to return. If empty or
                omitted, all fields are returned.

                This corresponds to the ``read_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.EntryGroup:
                Entry group metadata.

                   An EntryGroup resource represents a logical grouping
                   of zero or more Data Catalog
                   [Entry][google.cloud.datacatalog.v1.Entry] resources.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, read_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.GetEntryGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if read_mask is not None:
            request.read_mask = read_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_entry_group,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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

    async def update_entry_group(
        self,
        request: Union[datacatalog.UpdateEntryGroupRequest, dict] = None,
        *,
        entry_group: datacatalog.EntryGroup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.EntryGroup:
        r"""Updates an entry group.

        You must enable the Data Catalog API in the project identified
        by the ``entry_group.name`` parameter. For more information, see
        `Data Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.UpdateEntryGroupRequest, dict]):
                The request object. Request message for
                [UpdateEntryGroup][google.cloud.datacatalog.v1.DataCatalog.UpdateEntryGroup].
            entry_group (:class:`google.cloud.datacatalog_v1.types.EntryGroup`):
                Required. Updates for the entry group. The ``name``
                field must be set.

                This corresponds to the ``entry_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Names of fields whose values to
                overwrite on an entry group.
                If this parameter is absent or empty,
                all modifiable fields are overwritten.
                If such fields are non-required and
                omitted in the request body, their
                values are emptied.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.EntryGroup:
                Entry group metadata.

                   An EntryGroup resource represents a logical grouping
                   of zero or more Data Catalog
                   [Entry][google.cloud.datacatalog.v1.Entry] resources.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([entry_group, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.UpdateEntryGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if entry_group is not None:
            request.entry_group = entry_group
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_entry_group,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("entry_group.name", request.entry_group.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_entry_group(
        self,
        request: Union[datacatalog.DeleteEntryGroupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an entry group.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.DeleteEntryGroupRequest, dict]):
                The request object. Request message for
                [DeleteEntryGroup][google.cloud.datacatalog.v1.DataCatalog.DeleteEntryGroup].
            name (:class:`str`):
                Required. The name of the entry group
                to delete.

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

        request = datacatalog.DeleteEntryGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_entry_group,
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

    async def list_entry_groups(
        self,
        request: Union[datacatalog.ListEntryGroupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntryGroupsAsyncPager:
        r"""Lists entry groups.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.ListEntryGroupsRequest, dict]):
                The request object. Request message for
                [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].
            parent (:class:`str`):
                Required. The name of the location
                that contains the entry groups to list.
                Can be provided as a URL.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.services.data_catalog.pagers.ListEntryGroupsAsyncPager:
                Response message for
                   [ListEntryGroups][google.cloud.datacatalog.v1.DataCatalog.ListEntryGroups].

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

        request = datacatalog.ListEntryGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_entry_groups,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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
        response = pagers.ListEntryGroupsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_entry(
        self,
        request: Union[datacatalog.CreateEntryRequest, dict] = None,
        *,
        parent: str = None,
        entry_id: str = None,
        entry: datacatalog.Entry = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.Entry:
        r"""Creates an entry.

        You can create entries only with 'FILESET', 'CLUSTER',
        'DATA_STREAM', or custom types. Data Catalog automatically
        creates entries with other types during metadata ingestion from
        integrated systems.

        You must enable the Data Catalog API in the project identified
        by the ``parent`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        An entry group can have a maximum of 100,000 entries.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.CreateEntryRequest, dict]):
                The request object. Request message for
                [CreateEntry][google.cloud.datacatalog.v1.DataCatalog.CreateEntry].
            parent (:class:`str`):
                Required. The name of the entry group
                this entry belongs to.
                Note: The entry itself and its child
                resources might not be stored in the
                location specified in its name.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entry_id (:class:`str`):
                Required. The ID of the entry to create.

                The ID must contain only letters (a-z, A-Z), numbers
                (0-9), and underscores (_). The maximum size is 64 bytes
                when encoded in UTF-8.

                This corresponds to the ``entry_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entry (:class:`google.cloud.datacatalog_v1.types.Entry`):
                Required. The entry to create.
                This corresponds to the ``entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Entry:
                Entry metadata.
                   A Data Catalog entry represents another resource in
                   Google Cloud Platform (such as a BigQuery dataset or
                   a Pub/Sub topic) or outside of it. You can use the
                   linked_resource field in the entry resource to refer
                   to the original resource ID of the source system.

                   An entry resource contains resource details, for
                   example, its schema. Additionally, you can attach
                   flexible metadata to an entry in the form of a
                   [Tag][google.cloud.datacatalog.v1.Tag].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, entry_id, entry])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.CreateEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if entry_id is not None:
            request.entry_id = entry_id
        if entry is not None:
            request.entry = entry

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_entry,
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

    async def update_entry(
        self,
        request: Union[datacatalog.UpdateEntryRequest, dict] = None,
        *,
        entry: datacatalog.Entry = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.Entry:
        r"""Updates an existing entry.

        You must enable the Data Catalog API in the project identified
        by the ``entry.name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.UpdateEntryRequest, dict]):
                The request object. Request message for
                [UpdateEntry][google.cloud.datacatalog.v1.DataCatalog.UpdateEntry].
            entry (:class:`google.cloud.datacatalog_v1.types.Entry`):
                Required. Updates for the entry. The ``name`` field must
                be set.

                This corresponds to the ``entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Names of fields whose values to overwrite on an entry.

                If this parameter is absent or empty, all modifiable
                fields are overwritten. If such fields are non-required
                and omitted in the request body, their values are
                emptied.

                You can modify only the fields listed below.

                For entries with type ``DATA_STREAM``:

                -  ``schema``

                For entries with type ``FILESET``:

                -  ``schema``
                -  ``display_name``
                -  ``description``
                -  ``gcs_fileset_spec``
                -  ``gcs_fileset_spec.file_patterns``

                For entries with ``user_specified_type``:

                -  ``schema``
                -  ``display_name``
                -  ``description``
                -  ``user_specified_type``
                -  ``user_specified_system``
                -  ``linked_resource``
                -  ``source_system_timestamps``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Entry:
                Entry metadata.
                   A Data Catalog entry represents another resource in
                   Google Cloud Platform (such as a BigQuery dataset or
                   a Pub/Sub topic) or outside of it. You can use the
                   linked_resource field in the entry resource to refer
                   to the original resource ID of the source system.

                   An entry resource contains resource details, for
                   example, its schema. Additionally, you can attach
                   flexible metadata to an entry in the form of a
                   [Tag][google.cloud.datacatalog.v1.Tag].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([entry, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.UpdateEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if entry is not None:
            request.entry = entry
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_entry,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("entry.name", request.entry.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_entry(
        self,
        request: Union[datacatalog.DeleteEntryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an existing entry.

        You can delete only the entries created by the
        [CreateEntry][google.cloud.datacatalog.v1.DataCatalog.CreateEntry]
        method.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.DeleteEntryRequest, dict]):
                The request object. Request message for
                [DeleteEntry][google.cloud.datacatalog.v1.DataCatalog.DeleteEntry].
            name (:class:`str`):
                Required. The name of the entry to
                delete.

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

        request = datacatalog.DeleteEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_entry,
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

    async def get_entry(
        self,
        request: Union[datacatalog.GetEntryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.Entry:
        r"""Gets an entry.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.GetEntryRequest, dict]):
                The request object. Request message for
                [GetEntry][google.cloud.datacatalog.v1.DataCatalog.GetEntry].
            name (:class:`str`):
                Required. The name of the entry to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Entry:
                Entry metadata.
                   A Data Catalog entry represents another resource in
                   Google Cloud Platform (such as a BigQuery dataset or
                   a Pub/Sub topic) or outside of it. You can use the
                   linked_resource field in the entry resource to refer
                   to the original resource ID of the source system.

                   An entry resource contains resource details, for
                   example, its schema. Additionally, you can attach
                   flexible metadata to an entry in the form of a
                   [Tag][google.cloud.datacatalog.v1.Tag].

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

        request = datacatalog.GetEntryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_entry,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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

    async def lookup_entry(
        self,
        request: Union[datacatalog.LookupEntryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datacatalog.Entry:
        r"""Gets an entry by its target resource name.
        The resource name comes from the source Google Cloud
        Platform service.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.LookupEntryRequest, dict]):
                The request object. Request message for
                [LookupEntry][google.cloud.datacatalog.v1.DataCatalog.LookupEntry].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Entry:
                Entry metadata.
                   A Data Catalog entry represents another resource in
                   Google Cloud Platform (such as a BigQuery dataset or
                   a Pub/Sub topic) or outside of it. You can use the
                   linked_resource field in the entry resource to refer
                   to the original resource ID of the source system.

                   An entry resource contains resource details, for
                   example, its schema. Additionally, you can attach
                   flexible metadata to an entry in the form of a
                   [Tag][google.cloud.datacatalog.v1.Tag].

        """
        # Create or coerce a protobuf request object.
        request = datacatalog.LookupEntryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.lookup_entry,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_entries(
        self,
        request: Union[datacatalog.ListEntriesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntriesAsyncPager:
        r"""Lists entries.

        Note: Currently, this method can list only custom entries. To
        get a list of both custom and automatically created entries, use
        [SearchCatalog][google.cloud.datacatalog.v1.DataCatalog.SearchCatalog].

        Args:
            request (Union[google.cloud.datacatalog_v1.types.ListEntriesRequest, dict]):
                The request object. Request message for
                [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].
            parent (:class:`str`):
                Required. The name of the entry group
                that contains the entries to list.
                Can be provided in URL format.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.services.data_catalog.pagers.ListEntriesAsyncPager:
                Response message for
                   [ListEntries][google.cloud.datacatalog.v1.DataCatalog.ListEntries].

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

        request = datacatalog.ListEntriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_entries,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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
        response = pagers.ListEntriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_tag_template(
        self,
        request: Union[datacatalog.CreateTagTemplateRequest, dict] = None,
        *,
        parent: str = None,
        tag_template_id: str = None,
        tag_template: tags.TagTemplate = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplate:
        r"""Creates a tag template.

        You must enable the Data Catalog API in the project identified
        by the ``parent`` parameter. For more information, see [Data
        Catalog resource project]
        (https://cloud.google.com/data-catalog/docs/concepts/resource-project).

        Args:
            request (Union[google.cloud.datacatalog_v1.types.CreateTagTemplateRequest, dict]):
                The request object. Request message for
                [CreateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplate].
            parent (:class:`str`):
                Required. The name of the project and the template
                location
                `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag_template_id (:class:`str`):
                Required. The ID of the tag template to create.

                The ID must contain only lowercase letters (a-z),
                numbers (0-9), or underscores (_), and must start with a
                letter or underscore. The maximum size is 64 bytes when
                encoded in UTF-8.

                This corresponds to the ``tag_template_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag_template (:class:`google.cloud.datacatalog_v1.types.TagTemplate`):
                Required. The tag template to create.
                This corresponds to the ``tag_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplate:
                A tag template defines a tag that can have one or more
                typed fields.

                   The template is used to create tags that are attached
                   to GCP resources. [Tag template roles]
                   (https://cloud.google.com/iam/docs/understanding-roles#data-catalog-roles)
                   provide permissions to create, edit, and use the
                   template. For example, see the [TagTemplate User]
                   (https://cloud.google.com/data-catalog/docs/how-to/template-user)
                   role that includes a permission to use the tag
                   template to tag resources.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tag_template_id, tag_template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.CreateTagTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if tag_template_id is not None:
            request.tag_template_id = tag_template_id
        if tag_template is not None:
            request.tag_template = tag_template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_tag_template,
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

    async def get_tag_template(
        self,
        request: Union[datacatalog.GetTagTemplateRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplate:
        r"""Gets a tag template.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.GetTagTemplateRequest, dict]):
                The request object. Request message for
                [GetTagTemplate][google.cloud.datacatalog.v1.DataCatalog.GetTagTemplate].
            name (:class:`str`):
                Required. The name of the tag
                template to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplate:
                A tag template defines a tag that can have one or more
                typed fields.

                   The template is used to create tags that are attached
                   to GCP resources. [Tag template roles]
                   (https://cloud.google.com/iam/docs/understanding-roles#data-catalog-roles)
                   provide permissions to create, edit, and use the
                   template. For example, see the [TagTemplate User]
                   (https://cloud.google.com/data-catalog/docs/how-to/template-user)
                   role that includes a permission to use the tag
                   template to tag resources.

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

        request = datacatalog.GetTagTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_tag_template,
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

    async def update_tag_template(
        self,
        request: Union[datacatalog.UpdateTagTemplateRequest, dict] = None,
        *,
        tag_template: tags.TagTemplate = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplate:
        r"""Updates a tag template.

        You can't update template fields with this method. These fields
        are separate resources with their own create, update, and delete
        methods.

        You must enable the Data Catalog API in the project identified
        by the ``tag_template.name`` parameter. For more information,
        see `Data Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.UpdateTagTemplateRequest, dict]):
                The request object. Request message for
                [UpdateTagTemplate][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplate].
            tag_template (:class:`google.cloud.datacatalog_v1.types.TagTemplate`):
                Required. The template to update. The ``name`` field
                must be set.

                This corresponds to the ``tag_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Names of fields whose values to overwrite on a tag
                template. Currently, only ``display_name`` and
                ``is_publicly_readable`` can be overwritten.

                If this parameter is absent or empty, all modifiable
                fields are overwritten. If such fields are non-required
                and omitted in the request body, their values are
                emptied.

                Note: Updating the ``is_publicly_readable`` field may
                require up to 12 hours to take effect in search results.
                Additionally, it also requires the
                ``tagTemplates.getIamPolicy`` and
                ``tagTemplates.setIamPolicy`` permissions.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplate:
                A tag template defines a tag that can have one or more
                typed fields.

                   The template is used to create tags that are attached
                   to GCP resources. [Tag template roles]
                   (https://cloud.google.com/iam/docs/understanding-roles#data-catalog-roles)
                   provide permissions to create, edit, and use the
                   template. For example, see the [TagTemplate User]
                   (https://cloud.google.com/data-catalog/docs/how-to/template-user)
                   role that includes a permission to use the tag
                   template to tag resources.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tag_template, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.UpdateTagTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if tag_template is not None:
            request.tag_template = tag_template
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_tag_template,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tag_template.name", request.tag_template.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_tag_template(
        self,
        request: Union[datacatalog.DeleteTagTemplateRequest, dict] = None,
        *,
        name: str = None,
        force: bool = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a tag template and all tags that use it.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.DeleteTagTemplateRequest, dict]):
                The request object. Request message for
                [DeleteTagTemplate][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplate].
            name (:class:`str`):
                Required. The name of the tag
                template to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            force (:class:`bool`):
                Required. If true, deletes all tags that use this
                template.

                Currently, ``true`` is the only supported value.

                This corresponds to the ``force`` field
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
        has_flattened_params = any([name, force])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.DeleteTagTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if force is not None:
            request.force = force

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_tag_template,
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

    async def create_tag_template_field(
        self,
        request: Union[datacatalog.CreateTagTemplateFieldRequest, dict] = None,
        *,
        parent: str = None,
        tag_template_field_id: str = None,
        tag_template_field: tags.TagTemplateField = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplateField:
        r"""Creates a field in a tag template.

        You must enable the Data Catalog API in the project identified
        by the ``parent`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.CreateTagTemplateFieldRequest, dict]):
                The request object. Request message for
                [CreateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.CreateTagTemplateField].
            parent (:class:`str`):
                Required. The name of the project and the template
                location
                `region <https://cloud.google.com/data-catalog/docs/concepts/regions>`__.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag_template_field_id (:class:`str`):
                Required. The ID of the tag template field to create.

                Note: Adding a required field to an existing template is
                *not* allowed.

                Field IDs can contain letters (both uppercase and
                lowercase), numbers (0-9), underscores (_) and dashes
                (-). Field IDs must be at least 1 character long and at
                most 128 characters long. Field IDs must also be unique
                within their template.

                This corresponds to the ``tag_template_field_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag_template_field (:class:`google.cloud.datacatalog_v1.types.TagTemplateField`):
                Required. The tag template field to
                create.

                This corresponds to the ``tag_template_field`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplateField:
                The template for an individual field
                within a tag template.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tag_template_field_id, tag_template_field])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.CreateTagTemplateFieldRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if tag_template_field_id is not None:
            request.tag_template_field_id = tag_template_field_id
        if tag_template_field is not None:
            request.tag_template_field = tag_template_field

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_tag_template_field,
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

    async def update_tag_template_field(
        self,
        request: Union[datacatalog.UpdateTagTemplateFieldRequest, dict] = None,
        *,
        name: str = None,
        tag_template_field: tags.TagTemplateField = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplateField:
        r"""Updates a field in a tag template.

        You can't update the field type with this method.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.UpdateTagTemplateFieldRequest, dict]):
                The request object. Request message for
                [UpdateTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.UpdateTagTemplateField].
            name (:class:`str`):
                Required. The name of the tag
                template field.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag_template_field (:class:`google.cloud.datacatalog_v1.types.TagTemplateField`):
                Required. The template to update.
                This corresponds to the ``tag_template_field`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Names of fields whose values to overwrite on
                an individual field of a tag template. The following
                fields are modifiable:

                -  ``display_name``
                -  ``type.enum_type``
                -  ``is_required``

                If this parameter is absent or empty, all modifiable
                fields are overwritten. If such fields are non-required
                and omitted in the request body, their values are
                emptied with one exception: when updating an enum type,
                the provided values are merged with the existing values.
                Therefore, enum values can only be added, existing enum
                values cannot be deleted or renamed.

                Additionally, updating a template field from optional to
                required is *not* allowed.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplateField:
                The template for an individual field
                within a tag template.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, tag_template_field, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.UpdateTagTemplateFieldRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if tag_template_field is not None:
            request.tag_template_field = tag_template_field
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_tag_template_field,
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

    async def rename_tag_template_field(
        self,
        request: Union[datacatalog.RenameTagTemplateFieldRequest, dict] = None,
        *,
        name: str = None,
        new_tag_template_field_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplateField:
        r"""Renames a field in a tag template.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see [Data
        Catalog resource project]
        (https://cloud.google.com/data-catalog/docs/concepts/resource-project).

        Args:
            request (Union[google.cloud.datacatalog_v1.types.RenameTagTemplateFieldRequest, dict]):
                The request object. Request message for
                [RenameTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateField].
            name (:class:`str`):
                Required. The name of the tag
                template field.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            new_tag_template_field_id (:class:`str`):
                Required. The new ID of this tag template field. For
                example, ``my_new_field``.

                This corresponds to the ``new_tag_template_field_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplateField:
                The template for an individual field
                within a tag template.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, new_tag_template_field_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.RenameTagTemplateFieldRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if new_tag_template_field_id is not None:
            request.new_tag_template_field_id = new_tag_template_field_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rename_tag_template_field,
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

    async def rename_tag_template_field_enum_value(
        self,
        request: Union[datacatalog.RenameTagTemplateFieldEnumValueRequest, dict] = None,
        *,
        name: str = None,
        new_enum_value_display_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.TagTemplateField:
        r"""Renames an enum value in a tag template.
        Within a single enum field, enum values must be unique.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.RenameTagTemplateFieldEnumValueRequest, dict]):
                The request object. Request message for
                [RenameTagTemplateFieldEnumValue][google.cloud.datacatalog.v1.DataCatalog.RenameTagTemplateFieldEnumValue].
            name (:class:`str`):
                Required. The name of the enum field
                value.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            new_enum_value_display_name (:class:`str`):
                Required. The new display name of the enum value. For
                example, ``my_new_enum_value``.

                This corresponds to the ``new_enum_value_display_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.TagTemplateField:
                The template for an individual field
                within a tag template.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, new_enum_value_display_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.RenameTagTemplateFieldEnumValueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if new_enum_value_display_name is not None:
            request.new_enum_value_display_name = new_enum_value_display_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rename_tag_template_field_enum_value,
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

    async def delete_tag_template_field(
        self,
        request: Union[datacatalog.DeleteTagTemplateFieldRequest, dict] = None,
        *,
        name: str = None,
        force: bool = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a field in a tag template and all uses of this field
        from the tags based on this template.

        You must enable the Data Catalog API in the project identified
        by the ``name`` parameter. For more information, see `Data
        Catalog resource
        project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.DeleteTagTemplateFieldRequest, dict]):
                The request object. Request message for
                [DeleteTagTemplateField][google.cloud.datacatalog.v1.DataCatalog.DeleteTagTemplateField].
            name (:class:`str`):
                Required. The name of the tag
                template field to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            force (:class:`bool`):
                Required. If true, deletes this field from any tags that
                use it.

                Currently, ``true`` is the only supported value.

                This corresponds to the ``force`` field
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
        has_flattened_params = any([name, force])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.DeleteTagTemplateFieldRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if force is not None:
            request.force = force

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_tag_template_field,
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

    async def create_tag(
        self,
        request: Union[datacatalog.CreateTagRequest, dict] = None,
        *,
        parent: str = None,
        tag: tags.Tag = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.Tag:
        r"""Creates a tag and assigns it to:

        -  An [Entry][google.cloud.datacatalog.v1.Entry] if the method
           name is
           ``projects.locations.entryGroups.entries.tags.create``.
        -  Or [EntryGroup][google.cloud.datacatalog.v1.EntryGroup]if the
           method name is
           ``projects.locations.entryGroups.tags.create``.

        Note: The project identified by the ``parent`` parameter for the
        [tag]
        (https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries.tags/create#path-parameters)
        and the [tag template]
        (https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.tagTemplates/create#path-parameters)
        used to create the tag must be in the same organization.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.CreateTagRequest, dict]):
                The request object. Request message for
                [CreateTag][google.cloud.datacatalog.v1.DataCatalog.CreateTag].
            parent (:class:`str`):
                Required. The name of the resource to
                attach this tag to.
                Tags can be attached to entries or entry
                groups. An entry can have up to 1000
                attached tags.

                Note: The tag and its child resources
                might not be stored in the location
                specified in its name.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tag (:class:`google.cloud.datacatalog_v1.types.Tag`):
                Required. The tag to create.
                This corresponds to the ``tag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Tag:
                Tags contain custom metadata and are attached to Data Catalog resources. Tags
                   conform with the specification of their tag template.

                   See [Data Catalog
                   IAM](\ https://cloud.google.com/data-catalog/docs/concepts/iam)
                   for information on the permissions needed to create
                   or view tags.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.CreateTagRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if tag is not None:
            request.tag = tag

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_tag,
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

    async def update_tag(
        self,
        request: Union[datacatalog.UpdateTagRequest, dict] = None,
        *,
        tag: tags.Tag = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tags.Tag:
        r"""Updates an existing tag.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.UpdateTagRequest, dict]):
                The request object. Request message for
                [UpdateTag][google.cloud.datacatalog.v1.DataCatalog.UpdateTag].
            tag (:class:`google.cloud.datacatalog_v1.types.Tag`):
                Required. The updated tag. The "name"
                field must be set.

                This corresponds to the ``tag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Names of fields whose values to overwrite on a tag.
                Currently, a tag has the only modifiable field with the
                name ``fields``.

                In general, if this parameter is absent or empty, all
                modifiable fields are overwritten. If such fields are
                non-required and omitted in the request body, their
                values are emptied.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.types.Tag:
                Tags contain custom metadata and are attached to Data Catalog resources. Tags
                   conform with the specification of their tag template.

                   See [Data Catalog
                   IAM](\ https://cloud.google.com/data-catalog/docs/concepts/iam)
                   for information on the permissions needed to create
                   or view tags.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tag, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datacatalog.UpdateTagRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if tag is not None:
            request.tag = tag
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_tag,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("tag.name", request.tag.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_tag(
        self,
        request: Union[datacatalog.DeleteTagRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a tag.

        Args:
            request (Union[google.cloud.datacatalog_v1.types.DeleteTagRequest, dict]):
                The request object. Request message for
                [DeleteTag][google.cloud.datacatalog.v1.DataCatalog.DeleteTag].
            name (:class:`str`):
                Required. The name of the tag to
                delete.

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

        request = datacatalog.DeleteTagRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_tag,
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

    async def list_tags(
        self,
        request: Union[datacatalog.ListTagsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTagsAsyncPager:
        r"""Lists tags assigned to an
        [Entry][google.cloud.datacatalog.v1.Entry].

        Args:
            request (Union[google.cloud.datacatalog_v1.types.ListTagsRequest, dict]):
                The request object. Request message for
                [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].
            parent (:class:`str`):
                Required. The name of the Data Catalog resource to list
                the tags of.

                The resource can be an
                [Entry][google.cloud.datacatalog.v1.Entry] or an
                [EntryGroup][google.cloud.datacatalog.v1.EntryGroup]
                (without ``/entries/{entries}`` at the end).

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datacatalog_v1.services.data_catalog.pagers.ListTagsAsyncPager:
                Response message for
                   [ListTags][google.cloud.datacatalog.v1.DataCatalog.ListTags].

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

        request = datacatalog.ListTagsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_tags,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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
        response = pagers.ListTagsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets an access control policy for a resource. Replaces any
        existing policy.

        Supported resources are:

        -  Tag templates
        -  Entry groups

        Note: This method sets policies only within Data Catalog and
        can't be used to manage policies in BigQuery, Pub/Sub, Dataproc
        Metastore, and any external Google Cloud Platform resources
        synced with the Data Catalog.

        To call this method, you must have the following Google IAM
        permissions:

        -  ``datacatalog.tagTemplates.setIamPolicy`` to set policies on
           tag templates.
        -  ``datacatalog.entryGroups.setIamPolicy`` to set policies on
           entry groups.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.SetIamPolicyRequest(resource=resource,)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a resource.

        May return:

        -  A\ ``NOT_FOUND`` error if the resource doesn't exist or you
           don't have the permission to view it.
        -  An empty policy if the resource exists but doesn't have a set
           policy.

        Supported resources are:

        -  Tag templates
        -  Entry groups

        Note: This method doesn't get policies from Google Cloud
        Platform resources ingested into Data Catalog.

        To call this method, you must have the following Google IAM
        permissions:

        -  ``datacatalog.tagTemplates.getIamPolicy`` to get policies on
           tag templates.
        -  ``datacatalog.entryGroups.getIamPolicy`` to get policies on
           entry groups.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.GetIamPolicyRequest(resource=resource,)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Gets your permissions on a resource.
        Returns an empty set of permissions if the resource
        doesn't exist.
        Supported resources are:

        - Tag templates
        - Entry groups

        Note: This method gets policies only within Data Catalog
        and can't be used to get policies from BigQuery,
        Pub/Sub, Dataproc Metastore, and any external Google
        Cloud Platform resources ingested into Data Catalog.
        No Google IAM permissions are required to call this
        method.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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
            "google-cloud-datacatalog",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataCatalogAsyncClient",)
