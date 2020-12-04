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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api import distribution_pb2 as distribution  # type: ignore
from google.api import metric_pb2 as ga_metric  # type: ignore
from google.api import metric_pb2 as metric  # type: ignore
from google.cloud.logging_v2.services.metrics_service_v2 import pagers
from google.cloud.logging_v2.types import logging_metrics
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import MetricsServiceV2Transport, DEFAULT_CLIENT_INFO
from .transports.grpc import MetricsServiceV2GrpcTransport
from .transports.grpc_asyncio import MetricsServiceV2GrpcAsyncIOTransport


class MetricsServiceV2ClientMeta(type):
    """Metaclass for the MetricsServiceV2 client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[MetricsServiceV2Transport]]
    _transport_registry["grpc"] = MetricsServiceV2GrpcTransport
    _transport_registry["grpc_asyncio"] = MetricsServiceV2GrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[MetricsServiceV2Transport]:
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


class MetricsServiceV2Client(metaclass=MetricsServiceV2ClientMeta):
    """Service for configuring logs-based metrics."""

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

    DEFAULT_ENDPOINT = "logging.googleapis.com"
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

    @property
    def transport(self) -> MetricsServiceV2Transport:
        """Return the transport used by the client instance.

        Returns:
            MetricsServiceV2Transport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def log_metric_path(project: str, metric: str,) -> str:
        """Return a fully-qualified log_metric string."""
        return "projects/{project}/metrics/{metric}".format(
            project=project, metric=metric,
        )

    @staticmethod
    def parse_log_metric_path(path: str) -> Dict[str, str]:
        """Parse a log_metric path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/metrics/(?P<metric>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, MetricsServiceV2Transport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the metrics service v2 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MetricsServiceV2Transport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (client_options_lib.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, MetricsServiceV2Transport):
            # transport is a MetricsServiceV2Transport instance.
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
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def list_log_metrics(
        self,
        request: logging_metrics.ListLogMetricsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLogMetricsPager:
        r"""Lists logs-based metrics.

        Args:
            request (:class:`~.logging_metrics.ListLogMetricsRequest`):
                The request object. The parameters to ListLogMetrics.
            parent (:class:`str`):
                Required. The name of the project containing the
                metrics:

                ::

                    "projects/[PROJECT_ID]".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListLogMetricsPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a logging_metrics.ListLogMetricsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, logging_metrics.ListLogMetricsRequest):
            request = logging_metrics.ListLogMetricsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_log_metrics]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListLogMetricsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_log_metric(
        self,
        request: logging_metrics.GetLogMetricRequest = None,
        *,
        metric_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Gets a logs-based metric.

        Args:
            request (:class:`~.logging_metrics.GetLogMetricRequest`):
                The request object. The parameters to GetLogMetric.
            metric_name (:class:`str`):
                Required. The resource name of the desired metric:

                ::

                    "projects/[PROJECT_ID]/metrics/[METRIC_ID]".
                This corresponds to the ``metric_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.logging_metrics.LogMetric:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a logging_metrics.GetLogMetricRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, logging_metrics.GetLogMetricRequest):
            request = logging_metrics.GetLogMetricRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if metric_name is not None:
                request.metric_name = metric_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_log_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_log_metric(
        self,
        request: logging_metrics.CreateLogMetricRequest = None,
        *,
        parent: str = None,
        metric: logging_metrics.LogMetric = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Creates a logs-based metric.

        Args:
            request (:class:`~.logging_metrics.CreateLogMetricRequest`):
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
            metric (:class:`~.logging_metrics.LogMetric`):
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
            ~.logging_metrics.LogMetric:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a logging_metrics.CreateLogMetricRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, logging_metrics.CreateLogMetricRequest):
            request = logging_metrics.CreateLogMetricRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if metric is not None:
                request.metric = metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_log_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_log_metric(
        self,
        request: logging_metrics.UpdateLogMetricRequest = None,
        *,
        metric_name: str = None,
        metric: logging_metrics.LogMetric = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging_metrics.LogMetric:
        r"""Creates or updates a logs-based metric.

        Args:
            request (:class:`~.logging_metrics.UpdateLogMetricRequest`):
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
            metric (:class:`~.logging_metrics.LogMetric`):
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
            ~.logging_metrics.LogMetric:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a logging_metrics.UpdateLogMetricRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, logging_metrics.UpdateLogMetricRequest):
            request = logging_metrics.UpdateLogMetricRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if metric_name is not None:
                request.metric_name = metric_name
            if metric is not None:
                request.metric = metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_log_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_log_metric(
        self,
        request: logging_metrics.DeleteLogMetricRequest = None,
        *,
        metric_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a logs-based metric.

        Args:
            request (:class:`~.logging_metrics.DeleteLogMetricRequest`):
                The request object. The parameters to DeleteLogMetric.
            metric_name (:class:`str`):
                Required. The resource name of the metric to delete:

                ::

                    "projects/[PROJECT_ID]/metrics/[METRIC_ID]".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a logging_metrics.DeleteLogMetricRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, logging_metrics.DeleteLogMetricRequest):
            request = logging_metrics.DeleteLogMetricRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if metric_name is not None:
                request.metric_name = metric_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_log_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("metric_name", request.metric_name),)
            ),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-logging",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetricsServiceV2Client",)
