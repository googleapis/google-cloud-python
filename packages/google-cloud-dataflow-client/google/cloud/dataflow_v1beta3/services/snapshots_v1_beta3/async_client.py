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

from google.cloud.dataflow_v1beta3.types import snapshots
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import SnapshotsV1Beta3Transport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SnapshotsV1Beta3GrpcAsyncIOTransport
from .client import SnapshotsV1Beta3Client


class SnapshotsV1Beta3AsyncClient:
    """Provides methods to manage snapshots of Google Cloud Dataflow
    jobs.
    """

    _client: SnapshotsV1Beta3Client

    DEFAULT_ENDPOINT = SnapshotsV1Beta3Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SnapshotsV1Beta3Client.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        SnapshotsV1Beta3Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SnapshotsV1Beta3Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SnapshotsV1Beta3Client.common_folder_path)
    parse_common_folder_path = staticmethod(
        SnapshotsV1Beta3Client.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SnapshotsV1Beta3Client.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SnapshotsV1Beta3Client.parse_common_organization_path
    )
    common_project_path = staticmethod(SnapshotsV1Beta3Client.common_project_path)
    parse_common_project_path = staticmethod(
        SnapshotsV1Beta3Client.parse_common_project_path
    )
    common_location_path = staticmethod(SnapshotsV1Beta3Client.common_location_path)
    parse_common_location_path = staticmethod(
        SnapshotsV1Beta3Client.parse_common_location_path
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
            SnapshotsV1Beta3AsyncClient: The constructed client.
        """
        return SnapshotsV1Beta3Client.from_service_account_info.__func__(SnapshotsV1Beta3AsyncClient, info, *args, **kwargs)  # type: ignore

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
            SnapshotsV1Beta3AsyncClient: The constructed client.
        """
        return SnapshotsV1Beta3Client.from_service_account_file.__func__(SnapshotsV1Beta3AsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SnapshotsV1Beta3Transport:
        """Returns the transport used by the client instance.

        Returns:
            SnapshotsV1Beta3Transport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SnapshotsV1Beta3Client).get_transport_class, type(SnapshotsV1Beta3Client)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SnapshotsV1Beta3Transport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the snapshots v1 beta3 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SnapshotsV1Beta3Transport]): The
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
        self._client = SnapshotsV1Beta3Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_snapshot(
        self,
        request: snapshots.GetSnapshotRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> snapshots.Snapshot:
        r"""Gets information about a snapshot.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.GetSnapshotRequest`):
                The request object. Request to get information about a
                snapshot
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.Snapshot:
                Represents a snapshot of a job.
        """
        # Create or coerce a protobuf request object.
        request = snapshots.GetSnapshotRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_snapshot,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_snapshot(
        self,
        request: snapshots.DeleteSnapshotRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> snapshots.DeleteSnapshotResponse:
        r"""Deletes a snapshot.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.DeleteSnapshotRequest`):
                The request object. Request to delete a snapshot.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.DeleteSnapshotResponse:
                Response from deleting a snapshot.
        """
        # Create or coerce a protobuf request object.
        request = snapshots.DeleteSnapshotRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_snapshot,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_snapshots(
        self,
        request: snapshots.ListSnapshotsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> snapshots.ListSnapshotsResponse:
        r"""Lists snapshots.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.ListSnapshotsRequest`):
                The request object. Request to list snapshots.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.ListSnapshotsResponse:
                List of snapshots.
        """
        # Create or coerce a protobuf request object.
        request = snapshots.ListSnapshotsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_snapshots,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dataflow-client",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SnapshotsV1Beta3AsyncClient",)
