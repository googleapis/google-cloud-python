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
from typing import (
    Dict,
    AsyncIterable,
    Awaitable,
    AsyncIterator,
    Sequence,
    Tuple,
    Type,
    Union,
)
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigquery_storage_v1beta2.types import storage
from google.cloud.bigquery_storage_v1beta2.types import stream
from google.cloud.bigquery_storage_v1beta2.types import table
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import BigQueryWriteTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import BigQueryWriteGrpcAsyncIOTransport
from .client import BigQueryWriteClient


class BigQueryWriteAsyncClient:
    """BigQuery Write API.
    The Write API can be used to write data to BigQuery.
    """

    _client: BigQueryWriteClient

    DEFAULT_ENDPOINT = BigQueryWriteClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BigQueryWriteClient.DEFAULT_MTLS_ENDPOINT

    table_path = staticmethod(BigQueryWriteClient.table_path)
    parse_table_path = staticmethod(BigQueryWriteClient.parse_table_path)
    write_stream_path = staticmethod(BigQueryWriteClient.write_stream_path)
    parse_write_stream_path = staticmethod(BigQueryWriteClient.parse_write_stream_path)
    common_billing_account_path = staticmethod(
        BigQueryWriteClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BigQueryWriteClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BigQueryWriteClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        BigQueryWriteClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        BigQueryWriteClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        BigQueryWriteClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BigQueryWriteClient.common_project_path)
    parse_common_project_path = staticmethod(
        BigQueryWriteClient.parse_common_project_path
    )
    common_location_path = staticmethod(BigQueryWriteClient.common_location_path)
    parse_common_location_path = staticmethod(
        BigQueryWriteClient.parse_common_location_path
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
            BigQueryWriteAsyncClient: The constructed client.
        """
        return BigQueryWriteClient.from_service_account_info.__func__(BigQueryWriteAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BigQueryWriteAsyncClient: The constructed client.
        """
        return BigQueryWriteClient.from_service_account_file.__func__(BigQueryWriteAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BigQueryWriteTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigQueryWriteTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BigQueryWriteClient).get_transport_class, type(BigQueryWriteClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BigQueryWriteTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the big query write client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigQueryWriteTransport]): The
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
        self._client = BigQueryWriteClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_write_stream(
        self,
        request: storage.CreateWriteStreamRequest = None,
        *,
        parent: str = None,
        write_stream: stream.WriteStream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> stream.WriteStream:
        r"""Creates a write stream to the given table. Additionally, every
        table has a special COMMITTED stream named '_default' to which
        data can be written. This stream doesn't need to be created
        using CreateWriteStream. It is a stream that can be used
        simultaneously by any number of clients. Data written to this
        stream is considered committed as soon as an acknowledgement is
        received.

        Args:
            request (:class:`google.cloud.bigquery_storage_v1beta2.types.CreateWriteStreamRequest`):
                The request object. Request message for
                `CreateWriteStream`.
            parent (:class:`str`):
                Required. Reference to the table to which the stream
                belongs, in the format of
                ``projects/{project}/datasets/{dataset}/tables/{table}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            write_stream (:class:`google.cloud.bigquery_storage_v1beta2.types.WriteStream`):
                Required. Stream to be created.
                This corresponds to the ``write_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_storage_v1beta2.types.WriteStream:
                Information about a single stream
                that gets data inside the storage
                system.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, write_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = storage.CreateWriteStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if write_stream is not None:
            request.write_stream = write_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_write_stream,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    def append_rows(
        self,
        requests: AsyncIterator[storage.AppendRowsRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[storage.AppendRowsResponse]]:
        r"""Appends data to the given stream.

        If ``offset`` is specified, the ``offset`` is checked against
        the end of stream. The server returns ``OUT_OF_RANGE`` in
        ``AppendRowsResponse`` if an attempt is made to append to an
        offset beyond the current end of the stream or
        ``ALREADY_EXISTS`` if user provids an ``offset`` that has
        already been written to. User can retry with adjusted offset
        within the same RPC stream. If ``offset`` is not specified,
        append happens at the end of the stream.

        The response contains the offset at which the append happened.
        Responses are received in the same order in which requests are
        sent. There will be one response for each successful request. If
        the ``offset`` is not set in response, it means append didn't
        happen due to some errors. If one request fails, all the
        subsequent requests will also fail until a success request is
        made again.

        If the stream is of ``PENDING`` type, data will only be
        available for read operations after the stream is committed.

        Args:
            requests (AsyncIterator[`google.cloud.bigquery_storage_v1beta2.types.AppendRowsRequest`]):
                The request object AsyncIterator. Request message for `AppendRows`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.bigquery_storage_v1beta2.types.AppendRowsResponse]:
                Response message for AppendRows.
        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.append_rows,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ResourceExhausted,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=None,
            ),
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (gapic_v1.routing_header.to_grpc_metadata(()),)

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_write_stream(
        self,
        request: storage.GetWriteStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> stream.WriteStream:
        r"""Gets a write stream.

        Args:
            request (:class:`google.cloud.bigquery_storage_v1beta2.types.GetWriteStreamRequest`):
                The request object. Request message for
                `GetWriteStreamRequest`.
            name (:class:`str`):
                Required. Name of the stream to get, in the form of
                ``projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_storage_v1beta2.types.WriteStream:
                Information about a single stream
                that gets data inside the storage
                system.

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

        request = storage.GetWriteStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_write_stream,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    async def finalize_write_stream(
        self,
        request: storage.FinalizeWriteStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.FinalizeWriteStreamResponse:
        r"""Finalize a write stream so that no new data can be appended to
        the stream. Finalize is not supported on the '_default' stream.

        Args:
            request (:class:`google.cloud.bigquery_storage_v1beta2.types.FinalizeWriteStreamRequest`):
                The request object. Request message for invoking
                `FinalizeWriteStream`.
            name (:class:`str`):
                Required. Name of the stream to finalize, in the form of
                ``projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_storage_v1beta2.types.FinalizeWriteStreamResponse:
                Response message for FinalizeWriteStream.
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

        request = storage.FinalizeWriteStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.finalize_write_stream,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    async def batch_commit_write_streams(
        self,
        request: storage.BatchCommitWriteStreamsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.BatchCommitWriteStreamsResponse:
        r"""Atomically commits a group of ``PENDING`` streams that belong to
        the same ``parent`` table. Streams must be finalized before
        commit and cannot be committed multiple times. Once a stream is
        committed, data in the stream becomes available for read
        operations.

        Args:
            request (:class:`google.cloud.bigquery_storage_v1beta2.types.BatchCommitWriteStreamsRequest`):
                The request object. Request message for
                `BatchCommitWriteStreams`.
            parent (:class:`str`):
                Required. Parent table that all the streams should
                belong to, in the form of
                ``projects/{project}/datasets/{dataset}/tables/{table}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_storage_v1beta2.types.BatchCommitWriteStreamsResponse:
                Response message for BatchCommitWriteStreams.
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

        request = storage.BatchCommitWriteStreamsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_commit_write_streams,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    async def flush_rows(
        self,
        request: storage.FlushRowsRequest = None,
        *,
        write_stream: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.FlushRowsResponse:
        r"""Flushes rows to a BUFFERED stream. If users are appending rows
        to BUFFERED stream, flush operation is required in order for the
        rows to become available for reading. A Flush operation flushes
        up to any previously flushed offset in a BUFFERED stream, to the
        offset specified in the request. Flush is not supported on the
        \_default stream, since it is not BUFFERED.

        Args:
            request (:class:`google.cloud.bigquery_storage_v1beta2.types.FlushRowsRequest`):
                The request object. Request message for `FlushRows`.
            write_stream (:class:`str`):
                Required. The stream that is the
                target of the flush operation.

                This corresponds to the ``write_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_storage_v1beta2.types.FlushRowsResponse:
                Respond message for FlushRows.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([write_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = storage.FlushRowsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if write_stream is not None:
            request.write_stream = write_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.flush_rows,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("write_stream", request.write_stream),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-storage",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigQueryWriteAsyncClient",)
