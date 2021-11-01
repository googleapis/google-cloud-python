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

from google.api import distribution_pb2  # type: ignore
from google.api import metric_pb2  # type: ignore
from google.cloud.logging_v2.services.metrics_service_v2 import pagers
from google.cloud.logging_v2.types import logging_metrics
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import MetricsServiceV2Transport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import MetricsServiceV2GrpcAsyncIOTransport
from .client import MetricsServiceV2Client


class MetricsServiceV2AsyncClient:
    """Service for configuring logs-based metrics."""

    _client: MetricsServiceV2Client

    DEFAULT_ENDPOINT = MetricsServiceV2Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MetricsServiceV2Client.DEFAULT_MTLS_ENDPOINT

    log_metric_path = staticmethod(MetricsServiceV2Client.log_metric_path)
    parse_log_metric_path = staticmethod(MetricsServiceV2Client.parse_log_metric_path)
    common_billing_account_path = staticmethod(
        MetricsServiceV2Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MetricsServiceV2Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(MetricsServiceV2Client.common_folder_path)
    parse_common_folder_path = staticmethod(
        MetricsServiceV2Client.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MetricsServiceV2Client.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MetricsServiceV2Client.parse_common_organization_path
    )
    common_project_path = staticmethod(MetricsServiceV2Client.common_project_path)
    parse_common_project_path = staticmethod(
        MetricsServiceV2Client.parse_common_project_path
    )
    common_location_path = staticmethod(MetricsServiceV2Client.common_location_path)
    parse_common_location_path = staticmethod(
        MetricsServiceV2Client.parse_common_location_path
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
            MetricsServiceV2AsyncClient: The constructed client.
        """
        return MetricsServiceV2Client.from_service_account_info.__func__(MetricsServiceV2AsyncClient, info, *args, **kwargs)  # type: ignore

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
            MetricsServiceV2AsyncClient: The constructed client.
        """
        return MetricsServiceV2Client.from_service_account_file.__func__(MetricsServiceV2AsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> MetricsServiceV2Transport:
        """Returns the transport used by the client instance.

        Returns:
            MetricsServiceV2Transport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(MetricsServiceV2Client).get_transport_class, type(MetricsServiceV2Client)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, MetricsServiceV2Transport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the metrics service v2 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MetricsServiceV2Transport]): The
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
        self._client = MetricsServiceV2Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_log_metrics(
        self,
        request: Union[logging_metrics.ListLogMetricsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLogMetricsAsyncPager:
        r"""Lists logs-based metrics.

        Args:
            request (Union[google.cloud.logging_v2.types.ListLogMetricsRequest, dict]):
                The request object. The parameters to ListLogMetrics.
            parent (:class:`str`):
                Required. The name of the project containing the
                metrics:

                ::

                    "projects/[PROJECT_ID]"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.services.metrics_service_v2.pagers.ListLogMetricsAsyncPager:
                Result returned from ListLogMetrics.
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

        request = logging_metrics.ListLogMetricsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_log_metrics,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
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
        response = pagers.ListLogMetricsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_log_metric(
        self,
        request: Union[logging_metrics.GetLogMetricRequest, dict] = None,
        *,
        metric_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Gets a logs-based metric.

        Args:
            request (Union[google.cloud.logging_v2.types.GetLogMetricRequest, dict]):
                The request object. The parameters to GetLogMetric.
            metric_name (:class:`str`):
                Required. The resource name of the desired metric:

                ::

                    "projects/[PROJECT_ID]/metrics/[METRIC_ID]"

                This corresponds to the ``metric_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.types.LogMetric:
                Describes a logs-based metric. The
                value of the metric is the number of log
                entries that match a logs filter in a
                given time interval.
                Logs-based metrics can also be used to
                extract values from logs and create a
                distribution of the values. The
                distribution records the statistics of
                the extracted values along with an
                optional histogram of the values as
                specified by the bucket options.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([metric_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging_metrics.GetLogMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if metric_name is not None:
            request.metric_name = metric_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_log_metric,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
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
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_log_metric(
        self,
        request: Union[logging_metrics.CreateLogMetricRequest, dict] = None,
        *,
        parent: str = None,
        metric: logging_metrics.LogMetric = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Creates a logs-based metric.

        Args:
            request (Union[google.cloud.logging_v2.types.CreateLogMetricRequest, dict]):
                The request object. The parameters to CreateLogMetric.
            parent (:class:`str`):
                Required. The resource name of the project in which to
                create the metric:

                ::

                    "projects/[PROJECT_ID]"

                The new metric must be provided in the request.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metric (:class:`google.cloud.logging_v2.types.LogMetric`):
                Required. The new logs-based metric,
                which must not have an identifier that
                already exists.

                This corresponds to the ``metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.types.LogMetric:
                Describes a logs-based metric. The
                value of the metric is the number of log
                entries that match a logs filter in a
                given time interval.
                Logs-based metrics can also be used to
                extract values from logs and create a
                distribution of the values. The
                distribution records the statistics of
                the extracted values along with an
                optional histogram of the values as
                specified by the bucket options.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, metric])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging_metrics.CreateLogMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if metric is not None:
            request.metric = metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_log_metric,
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

        # Done; return the response.
        return response

    async def update_log_metric(
        self,
        request: Union[logging_metrics.UpdateLogMetricRequest, dict] = None,
        *,
        metric_name: str = None,
        metric: logging_metrics.LogMetric = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Creates or updates a logs-based metric.

        Args:
            request (Union[google.cloud.logging_v2.types.UpdateLogMetricRequest, dict]):
                The request object. The parameters to UpdateLogMetric.
            metric_name (:class:`str`):
                Required. The resource name of the metric to update:

                ::

                    "projects/[PROJECT_ID]/metrics/[METRIC_ID]"

                The updated metric must be provided in the request and
                it's ``name`` field must be the same as ``[METRIC_ID]``
                If the metric does not exist in ``[PROJECT_ID]``, then a
                new metric is created.

                This corresponds to the ``metric_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metric (:class:`google.cloud.logging_v2.types.LogMetric`):
                Required. The updated metric.
                This corresponds to the ``metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.types.LogMetric:
                Describes a logs-based metric. The
                value of the metric is the number of log
                entries that match a logs filter in a
                given time interval.
                Logs-based metrics can also be used to
                extract values from logs and create a
                distribution of the values. The
                distribution records the statistics of
                the extracted values along with an
                optional histogram of the values as
                specified by the bucket options.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([metric_name, metric])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging_metrics.UpdateLogMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if metric_name is not None:
            request.metric_name = metric_name
        if metric is not None:
            request.metric = metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_log_metric,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
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
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_log_metric(
        self,
        request: Union[logging_metrics.DeleteLogMetricRequest, dict] = None,
        *,
        metric_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a logs-based metric.

        Args:
            request (Union[google.cloud.logging_v2.types.DeleteLogMetricRequest, dict]):
                The request object. The parameters to DeleteLogMetric.
            metric_name (:class:`str`):
                Required. The resource name of the metric to delete:

                ::

                    "projects/[PROJECT_ID]/metrics/[METRIC_ID]"

                This corresponds to the ``metric_name`` field
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
        has_flattened_params = any([metric_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging_metrics.DeleteLogMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if metric_name is not None:
            request.metric_name = metric_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_log_metric,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
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
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-logging",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetricsServiceV2AsyncClient",)
