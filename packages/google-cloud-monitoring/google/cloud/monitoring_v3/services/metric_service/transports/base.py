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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.api import metric_pb2 as ga_metric  # type: ignore
from google.api import monitored_resource_pb2 as monitored_resource  # type: ignore
from google.cloud.monitoring_v3.types import metric_service
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class MetricServiceTransport(abc.ABC):
    """Abstract transport class for MetricService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/monitoring.read",
        "https://www.googleapis.com/auth/monitoring.write",
    )

    def __init__(
        self,
        *,
        host: str = "monitoring.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_monitored_resource_descriptors: gapic_v1.method.wrap_method(
                self.list_monitored_resource_descriptors,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_monitored_resource_descriptor: gapic_v1.method.wrap_method(
                self.get_monitored_resource_descriptor,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_metric_descriptors: gapic_v1.method.wrap_method(
                self.list_metric_descriptors,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_metric_descriptor: gapic_v1.method.wrap_method(
                self.get_metric_descriptor,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_metric_descriptor: gapic_v1.method.wrap_method(
                self.create_metric_descriptor,
                default_timeout=12.0,
                client_info=client_info,
            ),
            self.delete_metric_descriptor: gapic_v1.method.wrap_method(
                self.delete_metric_descriptor,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_time_series: gapic_v1.method.wrap_method(
                self.list_time_series,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_time_series: gapic_v1.method.wrap_method(
                self.create_time_series, default_timeout=12.0, client_info=client_info,
            ),
        }

    @property
    def list_monitored_resource_descriptors(
        self,
    ) -> typing.Callable[
        [metric_service.ListMonitoredResourceDescriptorsRequest],
        typing.Union[
            metric_service.ListMonitoredResourceDescriptorsResponse,
            typing.Awaitable[metric_service.ListMonitoredResourceDescriptorsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_monitored_resource_descriptor(
        self,
    ) -> typing.Callable[
        [metric_service.GetMonitoredResourceDescriptorRequest],
        typing.Union[
            monitored_resource.MonitoredResourceDescriptor,
            typing.Awaitable[monitored_resource.MonitoredResourceDescriptor],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_metric_descriptors(
        self,
    ) -> typing.Callable[
        [metric_service.ListMetricDescriptorsRequest],
        typing.Union[
            metric_service.ListMetricDescriptorsResponse,
            typing.Awaitable[metric_service.ListMetricDescriptorsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_metric_descriptor(
        self,
    ) -> typing.Callable[
        [metric_service.GetMetricDescriptorRequest],
        typing.Union[
            ga_metric.MetricDescriptor, typing.Awaitable[ga_metric.MetricDescriptor]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_metric_descriptor(
        self,
    ) -> typing.Callable[
        [metric_service.CreateMetricDescriptorRequest],
        typing.Union[
            ga_metric.MetricDescriptor, typing.Awaitable[ga_metric.MetricDescriptor]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_metric_descriptor(
        self,
    ) -> typing.Callable[
        [metric_service.DeleteMetricDescriptorRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_time_series(
        self,
    ) -> typing.Callable[
        [metric_service.ListTimeSeriesRequest],
        typing.Union[
            metric_service.ListTimeSeriesResponse,
            typing.Awaitable[metric_service.ListTimeSeriesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_time_series(
        self,
    ) -> typing.Callable[
        [metric_service.CreateTimeSeriesRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()


__all__ = ("MetricServiceTransport",)
