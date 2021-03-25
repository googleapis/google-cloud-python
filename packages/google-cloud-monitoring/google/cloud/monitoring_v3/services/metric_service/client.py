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

from google.api import label_pb2 as label  # type: ignore
from google.api import launch_stage_pb2 as launch_stage  # type: ignore
from google.api import metric_pb2 as ga_metric  # type: ignore
from google.api import monitored_resource_pb2 as monitored_resource  # type: ignore
from google.cloud.monitoring_v3.services.metric_service import pagers
from google.cloud.monitoring_v3.types import common
from google.cloud.monitoring_v3.types import metric as gm_metric
from google.cloud.monitoring_v3.types import metric_service

from .transports.base import MetricServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import MetricServiceGrpcTransport
from .transports.grpc_asyncio import MetricServiceGrpcAsyncIOTransport


class MetricServiceClientMeta(type):
    """Metaclass for the MetricService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[MetricServiceTransport]]
    _transport_registry["grpc"] = MetricServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = MetricServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[MetricServiceTransport]:
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


class MetricServiceClient(metaclass=MetricServiceClientMeta):
    """Manages metric descriptors, monitored resource descriptors,
    and time series data.
    """

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

    DEFAULT_ENDPOINT = "monitoring.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            MetricServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            MetricServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> MetricServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            MetricServiceTransport: The transport used by the client instance.
        """
        return self._transport

    '''@staticmethod
    def metric_descriptor_path(project: str,) -> str:
        """Return a fully-qualified metric_descriptor string."""
        return "projects/{project}/metricDescriptors/{metric_descriptor=**}".format(project=project, )

    @staticmethod
    def parse_metric_descriptor_path(path: str) -> Dict[str,str]:
        """Parse a metric_descriptor path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/metricDescriptors/{metric_descriptor=**}$", path)
        return m.groupdict() if m else {}'''

    @staticmethod
    def monitored_resource_descriptor_path(
        project: str, monitored_resource_descriptor: str,
    ) -> str:
        """Return a fully-qualified monitored_resource_descriptor string."""
        return "projects/{project}/monitoredResourceDescriptors/{monitored_resource_descriptor}".format(
            project=project,
            monitored_resource_descriptor=monitored_resource_descriptor,
        )

    @staticmethod
    def parse_monitored_resource_descriptor_path(path: str) -> Dict[str, str]:
        """Parse a monitored_resource_descriptor path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/monitoredResourceDescriptors/(?P<monitored_resource_descriptor>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def time_series_path(project: str, time_series: str,) -> str:
        """Return a fully-qualified time_series string."""
        return "projects/{project}/timeSeries/{time_series}".format(
            project=project, time_series=time_series,
        )

    @staticmethod
    def parse_time_series_path(path: str) -> Dict[str, str]:
        """Parse a time_series path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/timeSeries/(?P<time_series>.+?)$", path
        )
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
        transport: Union[str, MetricServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the metric service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, MetricServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
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

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                client_cert_source_func = (
                    mtls.default_client_cert_source() if is_mtls else None
                )

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
        if isinstance(transport, MetricServiceTransport):
            # transport is a MetricServiceTransport instance.
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
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def list_monitored_resource_descriptors(
        self,
        request: metric_service.ListMonitoredResourceDescriptorsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMonitoredResourceDescriptorsPager:
        r"""Lists monitored resource descriptors that match a
        filter. This method does not require a Workspace.

        Args:
            request (google.cloud.monitoring_v3.types.ListMonitoredResourceDescriptorsRequest):
                The request object. The
                `ListMonitoredResourceDescriptors` request.
            name (str):
                Required. The project on which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListMonitoredResourceDescriptorsPager:
                The ListMonitoredResourceDescriptors response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a metric_service.ListMonitoredResourceDescriptorsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, metric_service.ListMonitoredResourceDescriptorsRequest
        ):
            request = metric_service.ListMonitoredResourceDescriptorsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_monitored_resource_descriptors
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMonitoredResourceDescriptorsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_monitored_resource_descriptor(
        self,
        request: metric_service.GetMonitoredResourceDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> monitored_resource.MonitoredResourceDescriptor:
        r"""Gets a single monitored resource descriptor. This
        method does not require a Workspace.

        Args:
            request (google.cloud.monitoring_v3.types.GetMonitoredResourceDescriptorRequest):
                The request object. The `GetMonitoredResourceDescriptor`
                request.
            name (str):
                Required. The monitored resource descriptor to get. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/monitoredResourceDescriptors/[RESOURCE_TYPE]

                The ``[RESOURCE_TYPE]`` is a predefined type, such as
                ``cloudsql_database``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.monitored_resource_pb2.MonitoredResourceDescriptor:
                An object that describes the schema of a [MonitoredResource][google.api.MonitoredResource] object using a
                   type name and a set of labels. For example, the
                   monitored resource descriptor for Google Compute
                   Engine VM instances has a type of "gce_instance" and
                   specifies the use of the labels "instance_id" and
                   "zone" to identify particular VM instances.

                   Different APIs can support different monitored
                   resource types. APIs generally provide a list method
                   that returns the monitored resource descriptors used
                   by the API.

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
        # in a metric_service.GetMonitoredResourceDescriptorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, metric_service.GetMonitoredResourceDescriptorRequest
        ):
            request = metric_service.GetMonitoredResourceDescriptorRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_monitored_resource_descriptor
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_metric_descriptors(
        self,
        request: metric_service.ListMetricDescriptorsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetricDescriptorsPager:
        r"""Lists metric descriptors that match a filter. This
        method does not require a Workspace.

        Args:
            request (google.cloud.monitoring_v3.types.ListMetricDescriptorsRequest):
                The request object. The `ListMetricDescriptors` request.
            name (str):
                Required. The project on which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListMetricDescriptorsPager:
                The ListMetricDescriptors response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a metric_service.ListMetricDescriptorsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.ListMetricDescriptorsRequest):
            request = metric_service.ListMetricDescriptorsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_metric_descriptors]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMetricDescriptorsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_metric_descriptor(
        self,
        request: metric_service.GetMetricDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_metric.MetricDescriptor:
        r"""Gets a single metric descriptor. This method does not
        require a Workspace.

        Args:
            request (google.cloud.monitoring_v3.types.GetMetricDescriptorRequest):
                The request object. The `GetMetricDescriptor` request.
            name (str):
                Required. The metric descriptor on which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/metricDescriptors/[METRIC_ID]

                An example value of ``[METRIC_ID]`` is
                ``"compute.googleapis.com/instance/disk/read_bytes_count"``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.metric_pb2.MetricDescriptor:
                Defines a metric type and its schema.
                Once a metric descriptor is created,
                deleting or altering it stops data
                collection and makes the metric type's
                existing data unusable.

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
        # in a metric_service.GetMetricDescriptorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.GetMetricDescriptorRequest):
            request = metric_service.GetMetricDescriptorRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metric_descriptor]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_metric_descriptor(
        self,
        request: metric_service.CreateMetricDescriptorRequest = None,
        *,
        name: str = None,
        metric_descriptor: ga_metric.MetricDescriptor = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_metric.MetricDescriptor:
        r"""Creates a new metric descriptor. User-created metric descriptors
        define `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__.

        Args:
            request (google.cloud.monitoring_v3.types.CreateMetricDescriptorRequest):
                The request object. The `CreateMetricDescriptor`
                request.
            name (str):
                Required. The project on which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metric_descriptor (google.api.metric_pb2.MetricDescriptor):
                Required. The new `custom
                metric <https://cloud.google.com/monitoring/custom-metrics>`__
                descriptor.

                This corresponds to the ``metric_descriptor`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.metric_pb2.MetricDescriptor:
                Defines a metric type and its schema.
                Once a metric descriptor is created,
                deleting or altering it stops data
                collection and makes the metric type's
                existing data unusable.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, metric_descriptor])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metric_service.CreateMetricDescriptorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.CreateMetricDescriptorRequest):
            request = metric_service.CreateMetricDescriptorRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if metric_descriptor is not None:
                request.metric_descriptor = metric_descriptor

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_metric_descriptor]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_metric_descriptor(
        self,
        request: metric_service.DeleteMetricDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a metric descriptor. Only user-created `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__
        can be deleted.

        Args:
            request (google.cloud.monitoring_v3.types.DeleteMetricDescriptorRequest):
                The request object. The `DeleteMetricDescriptor`
                request.
            name (str):
                Required. The metric descriptor on which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/metricDescriptors/[METRIC_ID]

                An example of ``[METRIC_ID]`` is:
                ``"custom.googleapis.com/my_test_metric"``.

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
        # in a metric_service.DeleteMetricDescriptorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.DeleteMetricDescriptorRequest):
            request = metric_service.DeleteMetricDescriptorRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_metric_descriptor]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def list_time_series(
        self,
        request: metric_service.ListTimeSeriesRequest = None,
        *,
        name: str = None,
        filter: str = None,
        interval: common.TimeInterval = None,
        view: metric_service.ListTimeSeriesRequest.TimeSeriesView = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTimeSeriesPager:
        r"""Lists time series that match a filter. This method
        does not require a Workspace.

        Args:
            request (google.cloud.monitoring_v3.types.ListTimeSeriesRequest):
                The request object. The `ListTimeSeries` request.
            name (str):
                Required. The project, organization or folder on which
                to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
                    organizations/[ORGANIZATION_ID]
                    folders/[FOLDER_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. A `monitoring
                filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                that specifies which time series should be returned. The
                filter must specify a single metric type, and can
                additionally specify metric labels and other
                information. For example:

                ::

                    metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND
                        metric.labels.instance_name = "my-instance-name"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            interval (google.cloud.monitoring_v3.types.TimeInterval):
                Required. The time interval for which
                results should be returned. Only time
                series that contain data points in the
                specified interval are included in the
                response.

                This corresponds to the ``interval`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (google.cloud.monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView):
                Required. Specifies which information
                is returned about the time series.

                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListTimeSeriesPager:
                The ListTimeSeries response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, filter, interval, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metric_service.ListTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.ListTimeSeriesRequest):
            request = metric_service.ListTimeSeriesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if filter is not None:
                request.filter = filter
            if interval is not None:
                request.interval = interval
            if view is not None:
                request.view = view

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_time_series]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTimeSeriesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_time_series(
        self,
        request: metric_service.CreateTimeSeriesRequest = None,
        *,
        name: str = None,
        time_series: Sequence[gm_metric.TimeSeries] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Creates or adds data to one or more time series.
        The response is empty if all time series in the request
        were written. If any time series could not be written, a
        corresponding failure message is included in the error
        response.

        Args:
            request (google.cloud.monitoring_v3.types.CreateTimeSeriesRequest):
                The request object. The `CreateTimeSeries` request.
            name (str):
                Required. The project on which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            time_series (Sequence[google.cloud.monitoring_v3.types.TimeSeries]):
                Required. The new data to be added to a list of time
                series. Adds at most one data point to each of several
                time series. The new data point must be more recent than
                any other point in its time series. Each ``TimeSeries``
                value must fully specify a unique time series by
                supplying all label values for the metric and the
                monitored resource.

                The maximum number of ``TimeSeries`` objects per
                ``Create`` request is 200.

                This corresponds to the ``time_series`` field
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
        has_flattened_params = any([name, time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metric_service.CreateTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metric_service.CreateTimeSeriesRequest):
            request = metric_service.CreateTimeSeriesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if time_series is not None:
                request.time_series = time_series

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_time_series]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetricServiceClient",)
