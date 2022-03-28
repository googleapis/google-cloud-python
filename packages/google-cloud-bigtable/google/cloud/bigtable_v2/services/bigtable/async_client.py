# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import (
    Dict,
    Optional,
    AsyncIterable,
    Awaitable,
    Sequence,
    Tuple,
    Type,
    Union,
)
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

from google.cloud.bigtable_v2.types import bigtable
from google.cloud.bigtable_v2.types import data
from .transports.base import BigtableTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import BigtableGrpcAsyncIOTransport
from .client import BigtableClient


class BigtableAsyncClient:
    """Service for reading from and writing to existing Bigtable
    tables.
    """

    _client: BigtableClient

    DEFAULT_ENDPOINT = BigtableClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BigtableClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(BigtableClient.instance_path)
    parse_instance_path = staticmethod(BigtableClient.parse_instance_path)
    table_path = staticmethod(BigtableClient.table_path)
    parse_table_path = staticmethod(BigtableClient.parse_table_path)
    common_billing_account_path = staticmethod(
        BigtableClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BigtableClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BigtableClient.common_folder_path)
    parse_common_folder_path = staticmethod(BigtableClient.parse_common_folder_path)
    common_organization_path = staticmethod(BigtableClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        BigtableClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BigtableClient.common_project_path)
    parse_common_project_path = staticmethod(BigtableClient.parse_common_project_path)
    common_location_path = staticmethod(BigtableClient.common_location_path)
    parse_common_location_path = staticmethod(BigtableClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            BigtableAsyncClient: The constructed client.
        """
        return BigtableClient.from_service_account_info.__func__(BigtableAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BigtableAsyncClient: The constructed client.
        """
        return BigtableClient.from_service_account_file.__func__(BigtableAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return BigtableClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> BigtableTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigtableTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BigtableClient).get_transport_class, type(BigtableClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BigtableTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bigtable client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigtableTransport]): The
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
        self._client = BigtableClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    def read_rows(
        self,
        request: Union[bigtable.ReadRowsRequest, dict] = None,
        *,
        table_name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[bigtable.ReadRowsResponse]]:
        r"""Streams back the contents of all requested rows in
        key order, optionally applying the same Reader filter to
        each. Depending on their size, rows and cells may be
        broken up across multiple responses, but atomicity of
        each row will still be preserved. See the
        ReadRowsResponse documentation for details.

        Args:
            request (Union[google.cloud.bigtable_v2.types.ReadRowsRequest, dict]):
                The request object. Request message for
                Bigtable.ReadRows.
            table_name (:class:`str`):
                Required. The unique name of the table from which to
                read. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.bigtable_v2.types.ReadRowsResponse]:
                Response message for
                Bigtable.ReadRows.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.ReadRowsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.read_rows,
            default_timeout=43200.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def sample_row_keys(
        self,
        request: Union[bigtable.SampleRowKeysRequest, dict] = None,
        *,
        table_name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[bigtable.SampleRowKeysResponse]]:
        r"""Returns a sample of row keys in the table. The
        returned row keys will delimit contiguous sections of
        the table of approximately equal size, which can be used
        to break up the data for distributed tasks like
        mapreduces.

        Args:
            request (Union[google.cloud.bigtable_v2.types.SampleRowKeysRequest, dict]):
                The request object. Request message for
                Bigtable.SampleRowKeys.
            table_name (:class:`str`):
                Required. The unique name of the table from which to
                sample row keys. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.bigtable_v2.types.SampleRowKeysResponse]:
                Response message for
                Bigtable.SampleRowKeys.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.SampleRowKeysRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.sample_row_keys,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def mutate_row(
        self,
        request: Union[bigtable.MutateRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        mutations: Sequence[data.Mutation] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.MutateRowResponse:
        r"""Mutates a row atomically. Cells already present in the row are
        left unchanged unless explicitly changed by ``mutation``.

        Args:
            request (Union[google.cloud.bigtable_v2.types.MutateRowRequest, dict]):
                The request object. Request message for
                Bigtable.MutateRow.
            table_name (:class:`str`):
                Required. The unique name of the table to which the
                mutation should be applied. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (:class:`bytes`):
                Required. The key of the row to which
                the mutation should be applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutations (:class:`Sequence[google.cloud.bigtable_v2.types.Mutation]`):
                Required. Changes to be atomically
                applied to the specified row. Entries
                are applied in order, meaning that
                earlier mutations can be masked by later
                ones. Must contain at least one entry
                and at most 100000.

                This corresponds to the ``mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.MutateRowResponse:
                Response message for
                Bigtable.MutateRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, row_key, mutations, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.MutateRowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if row_key is not None:
            request.row_key = row_key
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id
        if mutations:
            request.mutations.extend(mutations)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mutate_row,
            default_retry=retries.Retry(
                initial=0.01,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def mutate_rows(
        self,
        request: Union[bigtable.MutateRowsRequest, dict] = None,
        *,
        table_name: str = None,
        entries: Sequence[bigtable.MutateRowsRequest.Entry] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[bigtable.MutateRowsResponse]]:
        r"""Mutates multiple rows in a batch. Each individual row
        is mutated atomically as in MutateRow, but the entire
        batch is not executed atomically.

        Args:
            request (Union[google.cloud.bigtable_v2.types.MutateRowsRequest, dict]):
                The request object. Request message for
                BigtableService.MutateRows.
            table_name (:class:`str`):
                Required. The unique name of the
                table to which the mutations should be
                applied.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entries (:class:`Sequence[google.cloud.bigtable_v2.types.MutateRowsRequest.Entry]`):
                Required. The row keys and
                corresponding mutations to be applied in
                bulk. Each entry is applied as an atomic
                mutation, but the entries may be applied
                in arbitrary order (even between entries
                for the same row). At least one entry
                must be specified, and in total the
                entries can contain at most 100000
                mutations.

                This corresponds to the ``entries`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.bigtable_v2.types.MutateRowsResponse]:
                Response message for
                BigtableService.MutateRows.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, entries, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.MutateRowsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id
        if entries:
            request.entries.extend(entries)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.mutate_rows,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def check_and_mutate_row(
        self,
        request: Union[bigtable.CheckAndMutateRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        predicate_filter: data.RowFilter = None,
        true_mutations: Sequence[data.Mutation] = None,
        false_mutations: Sequence[data.Mutation] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.CheckAndMutateRowResponse:
        r"""Mutates a row atomically based on the output of a
        predicate Reader filter.

        Args:
            request (Union[google.cloud.bigtable_v2.types.CheckAndMutateRowRequest, dict]):
                The request object. Request message for
                Bigtable.CheckAndMutateRow.
            table_name (:class:`str`):
                Required. The unique name of the table to which the
                conditional mutation should be applied. Values are of
                the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (:class:`bytes`):
                Required. The key of the row to which
                the conditional mutation should be
                applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            predicate_filter (:class:`google.cloud.bigtable_v2.types.RowFilter`):
                The filter to be applied to the contents of the
                specified row. Depending on whether or not any results
                are yielded, either ``true_mutations`` or
                ``false_mutations`` will be executed. If unset, checks
                that the row contains any values at all.

                This corresponds to the ``predicate_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            true_mutations (:class:`Sequence[google.cloud.bigtable_v2.types.Mutation]`):
                Changes to be atomically applied to the specified row if
                ``predicate_filter`` yields at least one cell when
                applied to ``row_key``. Entries are applied in order,
                meaning that earlier mutations can be masked by later
                ones. Must contain at least one entry if
                ``false_mutations`` is empty, and at most 100000.

                This corresponds to the ``true_mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            false_mutations (:class:`Sequence[google.cloud.bigtable_v2.types.Mutation]`):
                Changes to be atomically applied to the specified row if
                ``predicate_filter`` does not yield any cells when
                applied to ``row_key``. Entries are applied in order,
                meaning that earlier mutations can be masked by later
                ones. Must contain at least one entry if
                ``true_mutations`` is empty, and at most 100000.

                This corresponds to the ``false_mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.CheckAndMutateRowResponse:
                Response message for
                Bigtable.CheckAndMutateRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                table_name,
                row_key,
                predicate_filter,
                true_mutations,
                false_mutations,
                app_profile_id,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.CheckAndMutateRowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if row_key is not None:
            request.row_key = row_key
        if predicate_filter is not None:
            request.predicate_filter = predicate_filter
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id
        if true_mutations:
            request.true_mutations.extend(true_mutations)
        if false_mutations:
            request.false_mutations.extend(false_mutations)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.check_and_mutate_row,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def ping_and_warm(
        self,
        request: Union[bigtable.PingAndWarmRequest, dict] = None,
        *,
        name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.PingAndWarmResponse:
        r"""Warm up associated instance metadata for this
        connection. This call is not required but may be useful
        for connection keep-alive.

        Args:
            request (Union[google.cloud.bigtable_v2.types.PingAndWarmRequest, dict]):
                The request object. Request message for client
                connection keep-alive and warming.
            name (:class:`str`):
                Required. The unique name of the instance to check
                permissions for as well as respond. Values are of the
                form ``projects/<project>/instances/<instance>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.PingAndWarmResponse:
                Response message for
                Bigtable.PingAndWarm connection
                keepalive and warming.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.PingAndWarmRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.ping_and_warm,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def read_modify_write_row(
        self,
        request: Union[bigtable.ReadModifyWriteRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        rules: Sequence[data.ReadModifyWriteRule] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.ReadModifyWriteRowResponse:
        r"""Modifies a row atomically on the server. The method
        reads the latest existing timestamp and value from the
        specified columns and writes a new entry based on
        pre-defined read/modify/write rules. The new value for
        the timestamp is the greater of the existing timestamp
        or the current server time. The method returns the new
        contents of all modified cells.

        Args:
            request (Union[google.cloud.bigtable_v2.types.ReadModifyWriteRowRequest, dict]):
                The request object. Request message for
                Bigtable.ReadModifyWriteRow.
            table_name (:class:`str`):
                Required. The unique name of the table to which the
                read/modify/write rules should be applied. Values are of
                the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (:class:`bytes`):
                Required. The key of the row to which
                the read/modify/write rules should be
                applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rules (:class:`Sequence[google.cloud.bigtable_v2.types.ReadModifyWriteRule]`):
                Required. Rules specifying how the
                specified row's contents are to be
                transformed into writes. Entries are
                applied in order, meaning that earlier
                rules will affect the results of later
                ones.

                This corresponds to the ``rules`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.ReadModifyWriteRowResponse:
                Response message for
                Bigtable.ReadModifyWriteRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, row_key, rules, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable.ReadModifyWriteRowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_name is not None:
            request.table_name = table_name
        if row_key is not None:
            request.row_key = row_key
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id
        if rules:
            request.rules.extend(rules)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.read_modify_write_row,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_name", request.table_name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigtable",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigtableAsyncClient",)
