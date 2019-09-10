# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.cloud.talent.v4beta1 JobService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.talent_v4beta1.gapic import enums
from google.cloud.talent_v4beta1.gapic import job_service_client_config
from google.cloud.talent_v4beta1.gapic.transports import job_service_grpc_transport
from google.cloud.talent_v4beta1.proto import application_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import common_pb2
from google.cloud.talent_v4beta1.proto import company_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import completion_service_pb2
from google.cloud.talent_v4beta1.proto import completion_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import event_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2_grpc
from google.cloud.talent_v4beta1.proto import filters_pb2
from google.cloud.talent_v4beta1.proto import histogram_pb2
from google.cloud.talent_v4beta1.proto import job_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2
from google.cloud.talent_v4beta1.proto import job_service_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-talent").version


class JobServiceClient(object):
    """A service handles job management, including job CRUD, enumeration and search."""

    SERVICE_ADDRESS = "jobs.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.talent.v4beta1.JobService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            JobServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def company_path(cls, project, tenant, company):
        """Return a fully-qualified company string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}/companies/{company}",
            project=project,
            tenant=tenant,
            company=company,
        )

    @classmethod
    def company_without_tenant_path(cls, project, company):
        """Return a fully-qualified company_without_tenant string."""
        return google.api_core.path_template.expand(
            "projects/{project}/companies/{company}", project=project, company=company
        )

    @classmethod
    def job_path(cls, project, tenant, jobs):
        """Return a fully-qualified job string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}/jobs/{jobs}",
            project=project,
            tenant=tenant,
            jobs=jobs,
        )

    @classmethod
    def job_without_tenant_path(cls, project, jobs):
        """Return a fully-qualified job_without_tenant string."""
        return google.api_core.path_template.expand(
            "projects/{project}/jobs/{jobs}", project=project, jobs=jobs
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def tenant_path(cls, project, tenant):
        """Return a fully-qualified tenant string."""
        return google.api_core.path_template.expand(
            "projects/{project}/tenants/{tenant}", project=project, tenant=tenant
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.JobServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.JobServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = job_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=job_service_grpc_transport.JobServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = job_service_grpc_transport.JobServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_job(
        self,
        parent,
        job,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new job.

        Typically, the job becomes searchable within 10 seconds, but it may take
        up to 5 minutes.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.create_job(parent, job)

        Args:
            parent (str): Required. The resource name of the tenant under which the job is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and a default tenant is created if unspecified,
                for example, "projects/api-test-project".
            job (Union[dict, ~google.cloud.talent_v4beta1.types.Job]): Required. The Job to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Job`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_job,
                default_retry=self._method_configs["CreateJob"].retry,
                default_timeout=self._method_configs["CreateJob"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.CreateJobRequest(parent=parent, job=job)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Retrieves the specified job, whose status is OPEN or recently EXPIRED
        within the last 90 days.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[TENANT]', '[JOBS]')
            >>>
            >>> response = client.get_job(name)

        Args:
            name (str): Required. The resource name of the job to retrieve.

                The format is
                "projects/{project\_id}/tenants/{tenant\_id}/jobs/{job\_id}", for
                example, "projects/api-test-project/tenants/foo/jobs/1234".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project/jobs/1234".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_job,
                default_retry=self._method_configs["GetJob"].retry,
                default_timeout=self._method_configs["GetJob"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.GetJobRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_job(
        self,
        job,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates specified job.

        Typically, updated contents become visible in search results within 10
        seconds, but it may take up to 5 minutes.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.update_job(job)

        Args:
            job (Union[dict, ~google.cloud.talent_v4beta1.types.Job]): Required. The Job to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Job`
            update_mask (Union[dict, ~google.cloud.talent_v4beta1.types.FieldMask]): Optional but strongly recommended to be provided for the best service
                experience.

                If ``update_mask`` is provided, only the specified fields in ``job`` are
                updated. Otherwise all the fields are updated.

                A field mask to restrict the fields that are updated. Only top level
                fields of ``Job`` are supported.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_job,
                default_retry=self._method_configs["UpdateJob"].retry,
                default_timeout=self._method_configs["UpdateJob"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.UpdateJobRequest(job=job, update_mask=update_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("job.name", job.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified job.

        Typically, the job becomes unsearchable within 10 seconds, but it may take
        up to 5 minutes.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[TENANT]', '[JOBS]')
            >>>
            >>> client.delete_job(name)

        Args:
            name (str): Required. The resource name of the job to be deleted.

                The format is
                "projects/{project\_id}/tenants/{tenant\_id}/jobs/{job\_id}", for
                example, "projects/api-test-project/tenants/foo/jobs/1234".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project/jobs/1234".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_job,
                default_retry=self._method_configs["DeleteJob"].retry,
                default_timeout=self._method_configs["DeleteJob"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.DeleteJobRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_jobs(
        self,
        parent,
        filter_,
        page_size=None,
        job_view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists jobs by filter.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_jobs(parent, filter_):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_jobs(parent, filter_).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the tenant under which the job is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            filter_ (str): Required. The filter string specifies the jobs to be enumerated.

                Supported operator: =, AND

                The fields eligible for filtering are:

                -  ``companyName`` (Required)
                -  ``requisitionId`` (Optional)
                -  ``status`` (Optional) Available values: OPEN, EXPIRED, ALL. Defaults
                   to OPEN if no value is specified.

                Sample Query:

                -  companyName = "projects/api-test-project/tenants/foo/companies/bar"
                -  companyName = "projects/api-test-project/tenants/foo/companies/bar"
                   AND requisitionId = "req-1"
                -  companyName = "projects/api-test-project/tenants/foo/companies/bar"
                   AND status = "EXPIRED"
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            job_view (~google.cloud.talent_v4beta1.types.JobView): Optional. The desired job attributes returned for jobs in the search
                response. Defaults to ``JobView.JOB_VIEW_FULL`` if no value is
                specified.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.talent_v4beta1.types.Job` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_jobs,
                default_retry=self._method_configs["ListJobs"].retry,
                default_timeout=self._method_configs["ListJobs"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.ListJobsRequest(
            parent=parent, filter=filter_, page_size=page_size, job_view=job_view
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_jobs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="jobs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def batch_delete_jobs(
        self,
        parent,
        filter_,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a list of ``Job``\ s by filter.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> client.batch_delete_jobs(parent, filter_)

        Args:
            parent (str): Required. The resource name of the tenant under which the job is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            filter_ (str): Required. The filter string specifies the jobs to be deleted.

                Supported operator: =, AND

                The fields eligible for filtering are:

                -  ``companyName`` (Required)
                -  ``requisitionId`` (Required)

                Sample Query: companyName = "projects/api-test-project/companies/123"
                AND requisitionId = "req-1"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_delete_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_delete_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_delete_jobs,
                default_retry=self._method_configs["BatchDeleteJobs"].retry,
                default_timeout=self._method_configs["BatchDeleteJobs"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.BatchDeleteJobsRequest(parent=parent, filter=filter_)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["batch_delete_jobs"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_jobs(
        self,
        parent,
        request_metadata,
        search_mode=None,
        job_query=None,
        enable_broadening=None,
        require_precise_result_size=None,
        histogram_queries=None,
        job_view=None,
        offset=None,
        page_size=None,
        order_by=None,
        diversification_level=None,
        custom_ranking_info=None,
        disable_keyword_match=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Searches for jobs using the provided ``SearchJobsRequest``.

        This call constrains the ``visibility`` of jobs present in the database,
        and only returns jobs that the caller has permission to search against.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `request_metadata`:
            >>> request_metadata = {}
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_jobs(parent, request_metadata):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_jobs(parent, request_metadata).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the tenant to search within.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            request_metadata (Union[dict, ~google.cloud.talent_v4beta1.types.RequestMetadata]): Required. The meta information collected about the job searcher, used to
                improve the search quality of the service. The identifiers (such as
                ``user_id``) are provided by users, and must be unique and consistent.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.RequestMetadata`
            search_mode (~google.cloud.talent_v4beta1.types.SearchMode): Optional. Mode of a search.

                Defaults to ``SearchMode.JOB_SEARCH``.
            job_query (Union[dict, ~google.cloud.talent_v4beta1.types.JobQuery]): Optional. Query used to search against jobs, such as keyword, location
                filters, etc.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.JobQuery`
            enable_broadening (bool): Optional. Controls whether to broaden the search when it produces sparse
                results. Broadened queries append results to the end of the matching
                results list.

                Defaults to false.
            require_precise_result_size (bool): Optional. Controls if the search job request requires the return of a
                precise count of the first 300 results. Setting this to ``true`` ensures
                consistency in the number of results per page. Best practice is to set
                this value to true if a client allows users to jump directly to a
                non-sequential search results page.

                Enabling this flag may adversely impact performance.

                Defaults to false.
            histogram_queries (list[Union[dict, ~google.cloud.talent_v4beta1.types.HistogramQuery]]): Optional. An expression specifies a histogram request against matching
                jobs.

                Expression syntax is an aggregation function call with histogram facets
                and other options.

                Available aggregation function calls are:

                -  ``count(string_histogram_facet)``: Count the number of matching
                   entities, for each distinct attribute value.
                -  ``count(numeric_histogram_facet, list of buckets)``: Count the number
                   of matching entities within each bucket.

                Data types:

                -  Histogram facet: facet names with format [a-zA-Z][a-zA-Z0-9\_]+.
                -  String: string like "any string with backslash escape for quote(")."
                -  Number: whole number and floating point number like 10, -1 and -0.01.
                -  List: list of elements with comma(,) separator surrounded by square
                   brackets, for example, [1, 2, 3] and ["one", "two", "three"].

                Built-in constants:

                -  MIN (minimum number similar to java Double.MIN\_VALUE)
                -  MAX (maximum number similar to java Double.MAX\_VALUE)

                Built-in functions:

                -  bucket(start, end[, label]): bucket built-in function creates a
                   bucket with range of \`start, end). Note that the end is exclusive,
                   for example, bucket(1, MAX, "positive number") or bucket(1, 10).

                Job histogram facets:

                -  company\_display\_name: histogram by [Job.company\_display\_name\`.
                -  employment\_type: histogram by ``Job.employment_types``, for example,
                   "FULL\_TIME", "PART\_TIME".
                -  company\_size: histogram by ``CompanySize``, for example, "SMALL",
                   "MEDIUM", "BIG".
                -  publish\_time\_in\_month: histogram by the
                   ``Job.posting_publish_time`` in months. Must specify list of numeric
                   buckets in spec.
                -  publish\_time\_in\_year: histogram by the
                   ``Job.posting_publish_time`` in years. Must specify list of numeric
                   buckets in spec.
                -  degree\_types: histogram by the ``Job.degree_types``, for example,
                   "Bachelors", "Masters".
                -  job\_level: histogram by the ``Job.job_level``, for example, "Entry
                   Level".
                -  country: histogram by the country code of jobs, for example, "US",
                   "FR".
                -  admin1: histogram by the admin1 code of jobs, which is a global
                   placeholder referring to the state, province, or the particular term
                   a country uses to define the geographic structure below the country
                   level, for example, "CA", "IL".
                -  city: histogram by a combination of the "city name, admin1 code". For
                   example, "Mountain View, CA", "New York, NY".
                -  admin1\_country: histogram by a combination of the "admin1 code,
                   country", for example, "CA, US", "IL, US".
                -  city\_coordinate: histogram by the city center's GPS coordinates
                   (latitude and longitude), for example, 37.4038522,-122.0987765. Since
                   the coordinates of a city center can change, customers may need to
                   refresh them periodically.
                -  locale: histogram by the ``Job.language_code``, for example, "en-US",
                   "fr-FR".
                -  language: histogram by the language subtag of the
                   ``Job.language_code``, for example, "en", "fr".
                -  category: histogram by the ``JobCategory``, for example,
                   "COMPUTER\_AND\_IT", "HEALTHCARE".
                -  base\_compensation\_unit: histogram by the
                   ``CompensationInfo.CompensationUnit`` of base salary, for example,
                   "WEEKLY", "MONTHLY".
                -  base\_compensation: histogram by the base salary. Must specify list
                   of numeric buckets to group results by.
                -  annualized\_base\_compensation: histogram by the base annualized
                   salary. Must specify list of numeric buckets to group results by.
                -  annualized\_total\_compensation: histogram by the total annualized
                   salary. Must specify list of numeric buckets to group results by.
                -  string\_custom\_attribute: histogram by string
                   ``Job.custom_attributes``. Values can be accessed via square bracket
                   notations like string\_custom\_attribute["key1"].
                -  numeric\_custom\_attribute: histogram by numeric
                   ``Job.custom_attributes``. Values can be accessed via square bracket
                   notations like numeric\_custom\_attribute["key1"]. Must specify list
                   of numeric buckets to group results by.

                Example expressions:

                -  ``count(admin1)``
                -  ``count(base_compensation, [bucket(1000, 10000), bucket(10000, 100000), bucket(100000, MAX)])``
                -  ``count(string_custom_attribute["some-string-custom-attribute"])``
                -  ``count(numeric_custom_attribute["some-numeric-custom-attribute"], [bucket(MIN, 0, "negative"), bucket(0, MAX, "non-negative"])``

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.HistogramQuery`
            job_view (~google.cloud.talent_v4beta1.types.JobView): Optional. The desired job attributes returned for jobs in the search
                response. Defaults to ``JobView.JOB_VIEW_SMALL`` if no value is
                specified.
            offset (int): Optional. An integer that specifies the current offset (that is,
                starting result location, amongst the jobs deemed by the API as
                relevant) in search results. This field is only considered if
                ``page_token`` is unset.

                For example, 0 means to return results starting from the first matching
                job, and 10 means to return from the 11th job. This can be used for
                pagination, (for example, pageSize = 10 and offset = 10 means to return
                from the second page).
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional. The criteria determining how search results are sorted.
                Default is ``"relevance desc"``.

                Supported options are:

                -  ``"relevance desc"``: By relevance descending, as determined by the
                   API algorithms. Relevance thresholding of query results is only
                   available with this ordering.
                -  ``"posting_publish_time desc"``: By ``Job.posting_publish_time``
                   descending.
                -  ``"posting_update_time desc"``: By ``Job.posting_update_time``
                   descending.
                -  ``"title"``: By ``Job.title`` ascending.
                -  ``"title desc"``: By ``Job.title`` descending.
                -  ``"annualized_base_compensation"``: By job's
                   ``CompensationInfo.annualized_base_compensation_range`` ascending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_base_compensation desc"``: By job's
                   ``CompensationInfo.annualized_base_compensation_range`` descending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_total_compensation"``: By job's
                   ``CompensationInfo.annualized_total_compensation_range`` ascending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_total_compensation desc"``: By job's
                   ``CompensationInfo.annualized_total_compensation_range`` descending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"custom_ranking desc"``: By the relevance score adjusted to the
                   ``SearchJobsRequest.CustomRankingInfo.ranking_expression`` with
                   weight factor assigned by
                   ``SearchJobsRequest.CustomRankingInfo.importance_level`` in
                   descending order.
                -  Location sorting: Use the special syntax to order jobs by distance:
                   ``"distance_from('Hawaii')"``: Order by distance from Hawaii.
                   ``"distance_from(19.89, 155.5)"``: Order by distance from a
                   coordinate.
                   ``"distance_from('Hawaii'), distance_from('Puerto Rico')"``: Order by
                   multiple locations. See details below.
                   ``"distance_from('Hawaii'), distance_from(19.89, 155.5)"``: Order by
                   multiple locations. See details below. The string can have a maximum
                   of 256 characters. When multiple distance centers are provided, a job
                   that is close to any of the distance centers would have a high rank.
                   When a job has multiple locations, the job location closest to one of
                   the distance centers will be used. Jobs that don't have locations
                   will be ranked at the bottom. Distance is calculated with a precision
                   of 11.3 meters (37.4 feet). Diversification strategy is still applied
                   unless explicitly disabled in ``diversification_level``.
            diversification_level (~google.cloud.talent_v4beta1.types.DiversificationLevel): Optional. Controls whether highly similar jobs are returned next to each
                other in the search results. Jobs are identified as highly similar based
                on their titles, job categories, and locations. Highly similar results
                are clustered so that only one representative job of the cluster is
                displayed to the job seeker higher up in the results, with the other
                jobs being displayed lower down in the results.

                Defaults to ``DiversificationLevel.SIMPLE`` if no value is specified.
            custom_ranking_info (Union[dict, ~google.cloud.talent_v4beta1.types.CustomRankingInfo]): Optional. Controls over how job documents get ranked on top of existing
                relevance score (determined by API algorithm).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.CustomRankingInfo`
            disable_keyword_match (bool): Optional. Controls whether to disable exact keyword match on
                ``Job.title``, ``Job.description``, ``Job.company_display_name``,
                ``Job.addresses``, ``Job.qualifications``. When disable keyword match is
                turned off, a keyword match returns jobs that do not match given
                category filters when there are matching keywords. For example, for the
                query "program manager," a result is returned even if the job posting
                has the title "software developer," which doesn't fall into "program
                manager" ontology, but does have "program manager" appearing in its
                description.

                For queries like "cloud" that don't contain title or location specific
                ontology, jobs with "cloud" keyword matches are returned regardless of
                this flag's value.

                Use ``Company.keyword_searchable_job_custom_attributes`` if
                company-specific globally matched custom field/attribute string values
                are needed. Enabling keyword match improves recall of subsequent search
                requests.

                Defaults to false.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.talent_v4beta1.types.MatchingJob` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_jobs,
                default_retry=self._method_configs["SearchJobs"].retry,
                default_timeout=self._method_configs["SearchJobs"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.SearchJobsRequest(
            parent=parent,
            request_metadata=request_metadata,
            search_mode=search_mode,
            job_query=job_query,
            enable_broadening=enable_broadening,
            require_precise_result_size=require_precise_result_size,
            histogram_queries=histogram_queries,
            job_view=job_view,
            offset=offset,
            page_size=page_size,
            order_by=order_by,
            diversification_level=diversification_level,
            custom_ranking_info=custom_ranking_info,
            disable_keyword_match=disable_keyword_match,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["search_jobs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="matching_jobs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def search_jobs_for_alert(
        self,
        parent,
        request_metadata,
        search_mode=None,
        job_query=None,
        enable_broadening=None,
        require_precise_result_size=None,
        histogram_queries=None,
        job_view=None,
        offset=None,
        page_size=None,
        order_by=None,
        diversification_level=None,
        custom_ranking_info=None,
        disable_keyword_match=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Searches for jobs using the provided ``SearchJobsRequest``.

        This API call is intended for the use case of targeting passive job
        seekers (for example, job seekers who have signed up to receive email
        alerts about potential job opportunities), and has different algorithmic
        adjustments that are targeted to passive job seekers.

        This call constrains the ``visibility`` of jobs present in the database,
        and only returns jobs the caller has permission to search against.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `request_metadata`:
            >>> request_metadata = {}
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_jobs_for_alert(parent, request_metadata):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_jobs_for_alert(parent, request_metadata).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The resource name of the tenant to search within.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            request_metadata (Union[dict, ~google.cloud.talent_v4beta1.types.RequestMetadata]): Required. The meta information collected about the job searcher, used to
                improve the search quality of the service. The identifiers (such as
                ``user_id``) are provided by users, and must be unique and consistent.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.RequestMetadata`
            search_mode (~google.cloud.talent_v4beta1.types.SearchMode): Optional. Mode of a search.

                Defaults to ``SearchMode.JOB_SEARCH``.
            job_query (Union[dict, ~google.cloud.talent_v4beta1.types.JobQuery]): Optional. Query used to search against jobs, such as keyword, location
                filters, etc.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.JobQuery`
            enable_broadening (bool): Optional. Controls whether to broaden the search when it produces sparse
                results. Broadened queries append results to the end of the matching
                results list.

                Defaults to false.
            require_precise_result_size (bool): Optional. Controls if the search job request requires the return of a
                precise count of the first 300 results. Setting this to ``true`` ensures
                consistency in the number of results per page. Best practice is to set
                this value to true if a client allows users to jump directly to a
                non-sequential search results page.

                Enabling this flag may adversely impact performance.

                Defaults to false.
            histogram_queries (list[Union[dict, ~google.cloud.talent_v4beta1.types.HistogramQuery]]): Optional. An expression specifies a histogram request against matching
                jobs.

                Expression syntax is an aggregation function call with histogram facets
                and other options.

                Available aggregation function calls are:

                -  ``count(string_histogram_facet)``: Count the number of matching
                   entities, for each distinct attribute value.
                -  ``count(numeric_histogram_facet, list of buckets)``: Count the number
                   of matching entities within each bucket.

                Data types:

                -  Histogram facet: facet names with format [a-zA-Z][a-zA-Z0-9\_]+.
                -  String: string like "any string with backslash escape for quote(")."
                -  Number: whole number and floating point number like 10, -1 and -0.01.
                -  List: list of elements with comma(,) separator surrounded by square
                   brackets, for example, [1, 2, 3] and ["one", "two", "three"].

                Built-in constants:

                -  MIN (minimum number similar to java Double.MIN\_VALUE)
                -  MAX (maximum number similar to java Double.MAX\_VALUE)

                Built-in functions:

                -  bucket(start, end[, label]): bucket built-in function creates a
                   bucket with range of \`start, end). Note that the end is exclusive,
                   for example, bucket(1, MAX, "positive number") or bucket(1, 10).

                Job histogram facets:

                -  company\_display\_name: histogram by [Job.company\_display\_name\`.
                -  employment\_type: histogram by ``Job.employment_types``, for example,
                   "FULL\_TIME", "PART\_TIME".
                -  company\_size: histogram by ``CompanySize``, for example, "SMALL",
                   "MEDIUM", "BIG".
                -  publish\_time\_in\_month: histogram by the
                   ``Job.posting_publish_time`` in months. Must specify list of numeric
                   buckets in spec.
                -  publish\_time\_in\_year: histogram by the
                   ``Job.posting_publish_time`` in years. Must specify list of numeric
                   buckets in spec.
                -  degree\_types: histogram by the ``Job.degree_types``, for example,
                   "Bachelors", "Masters".
                -  job\_level: histogram by the ``Job.job_level``, for example, "Entry
                   Level".
                -  country: histogram by the country code of jobs, for example, "US",
                   "FR".
                -  admin1: histogram by the admin1 code of jobs, which is a global
                   placeholder referring to the state, province, or the particular term
                   a country uses to define the geographic structure below the country
                   level, for example, "CA", "IL".
                -  city: histogram by a combination of the "city name, admin1 code". For
                   example, "Mountain View, CA", "New York, NY".
                -  admin1\_country: histogram by a combination of the "admin1 code,
                   country", for example, "CA, US", "IL, US".
                -  city\_coordinate: histogram by the city center's GPS coordinates
                   (latitude and longitude), for example, 37.4038522,-122.0987765. Since
                   the coordinates of a city center can change, customers may need to
                   refresh them periodically.
                -  locale: histogram by the ``Job.language_code``, for example, "en-US",
                   "fr-FR".
                -  language: histogram by the language subtag of the
                   ``Job.language_code``, for example, "en", "fr".
                -  category: histogram by the ``JobCategory``, for example,
                   "COMPUTER\_AND\_IT", "HEALTHCARE".
                -  base\_compensation\_unit: histogram by the
                   ``CompensationInfo.CompensationUnit`` of base salary, for example,
                   "WEEKLY", "MONTHLY".
                -  base\_compensation: histogram by the base salary. Must specify list
                   of numeric buckets to group results by.
                -  annualized\_base\_compensation: histogram by the base annualized
                   salary. Must specify list of numeric buckets to group results by.
                -  annualized\_total\_compensation: histogram by the total annualized
                   salary. Must specify list of numeric buckets to group results by.
                -  string\_custom\_attribute: histogram by string
                   ``Job.custom_attributes``. Values can be accessed via square bracket
                   notations like string\_custom\_attribute["key1"].
                -  numeric\_custom\_attribute: histogram by numeric
                   ``Job.custom_attributes``. Values can be accessed via square bracket
                   notations like numeric\_custom\_attribute["key1"]. Must specify list
                   of numeric buckets to group results by.

                Example expressions:

                -  ``count(admin1)``
                -  ``count(base_compensation, [bucket(1000, 10000), bucket(10000, 100000), bucket(100000, MAX)])``
                -  ``count(string_custom_attribute["some-string-custom-attribute"])``
                -  ``count(numeric_custom_attribute["some-numeric-custom-attribute"], [bucket(MIN, 0, "negative"), bucket(0, MAX, "non-negative"])``

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.HistogramQuery`
            job_view (~google.cloud.talent_v4beta1.types.JobView): Optional. The desired job attributes returned for jobs in the search
                response. Defaults to ``JobView.JOB_VIEW_SMALL`` if no value is
                specified.
            offset (int): Optional. An integer that specifies the current offset (that is,
                starting result location, amongst the jobs deemed by the API as
                relevant) in search results. This field is only considered if
                ``page_token`` is unset.

                For example, 0 means to return results starting from the first matching
                job, and 10 means to return from the 11th job. This can be used for
                pagination, (for example, pageSize = 10 and offset = 10 means to return
                from the second page).
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            order_by (str): Optional. The criteria determining how search results are sorted.
                Default is ``"relevance desc"``.

                Supported options are:

                -  ``"relevance desc"``: By relevance descending, as determined by the
                   API algorithms. Relevance thresholding of query results is only
                   available with this ordering.
                -  ``"posting_publish_time desc"``: By ``Job.posting_publish_time``
                   descending.
                -  ``"posting_update_time desc"``: By ``Job.posting_update_time``
                   descending.
                -  ``"title"``: By ``Job.title`` ascending.
                -  ``"title desc"``: By ``Job.title`` descending.
                -  ``"annualized_base_compensation"``: By job's
                   ``CompensationInfo.annualized_base_compensation_range`` ascending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_base_compensation desc"``: By job's
                   ``CompensationInfo.annualized_base_compensation_range`` descending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_total_compensation"``: By job's
                   ``CompensationInfo.annualized_total_compensation_range`` ascending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"annualized_total_compensation desc"``: By job's
                   ``CompensationInfo.annualized_total_compensation_range`` descending.
                   Jobs whose annualized base compensation is unspecified are put at the
                   end of search results.
                -  ``"custom_ranking desc"``: By the relevance score adjusted to the
                   ``SearchJobsRequest.CustomRankingInfo.ranking_expression`` with
                   weight factor assigned by
                   ``SearchJobsRequest.CustomRankingInfo.importance_level`` in
                   descending order.
                -  Location sorting: Use the special syntax to order jobs by distance:
                   ``"distance_from('Hawaii')"``: Order by distance from Hawaii.
                   ``"distance_from(19.89, 155.5)"``: Order by distance from a
                   coordinate.
                   ``"distance_from('Hawaii'), distance_from('Puerto Rico')"``: Order by
                   multiple locations. See details below.
                   ``"distance_from('Hawaii'), distance_from(19.89, 155.5)"``: Order by
                   multiple locations. See details below. The string can have a maximum
                   of 256 characters. When multiple distance centers are provided, a job
                   that is close to any of the distance centers would have a high rank.
                   When a job has multiple locations, the job location closest to one of
                   the distance centers will be used. Jobs that don't have locations
                   will be ranked at the bottom. Distance is calculated with a precision
                   of 11.3 meters (37.4 feet). Diversification strategy is still applied
                   unless explicitly disabled in ``diversification_level``.
            diversification_level (~google.cloud.talent_v4beta1.types.DiversificationLevel): Optional. Controls whether highly similar jobs are returned next to each
                other in the search results. Jobs are identified as highly similar based
                on their titles, job categories, and locations. Highly similar results
                are clustered so that only one representative job of the cluster is
                displayed to the job seeker higher up in the results, with the other
                jobs being displayed lower down in the results.

                Defaults to ``DiversificationLevel.SIMPLE`` if no value is specified.
            custom_ranking_info (Union[dict, ~google.cloud.talent_v4beta1.types.CustomRankingInfo]): Optional. Controls over how job documents get ranked on top of existing
                relevance score (determined by API algorithm).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.CustomRankingInfo`
            disable_keyword_match (bool): Optional. Controls whether to disable exact keyword match on
                ``Job.title``, ``Job.description``, ``Job.company_display_name``,
                ``Job.addresses``, ``Job.qualifications``. When disable keyword match is
                turned off, a keyword match returns jobs that do not match given
                category filters when there are matching keywords. For example, for the
                query "program manager," a result is returned even if the job posting
                has the title "software developer," which doesn't fall into "program
                manager" ontology, but does have "program manager" appearing in its
                description.

                For queries like "cloud" that don't contain title or location specific
                ontology, jobs with "cloud" keyword matches are returned regardless of
                this flag's value.

                Use ``Company.keyword_searchable_job_custom_attributes`` if
                company-specific globally matched custom field/attribute string values
                are needed. Enabling keyword match improves recall of subsequent search
                requests.

                Defaults to false.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.talent_v4beta1.types.MatchingJob` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_jobs_for_alert" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_jobs_for_alert"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_jobs_for_alert,
                default_retry=self._method_configs["SearchJobsForAlert"].retry,
                default_timeout=self._method_configs["SearchJobsForAlert"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.SearchJobsRequest(
            parent=parent,
            request_metadata=request_metadata,
            search_mode=search_mode,
            job_query=job_query,
            enable_broadening=enable_broadening,
            require_precise_result_size=require_precise_result_size,
            histogram_queries=histogram_queries,
            job_view=job_view,
            offset=offset,
            page_size=page_size,
            order_by=order_by,
            diversification_level=diversification_level,
            custom_ranking_info=custom_ranking_info,
            disable_keyword_match=disable_keyword_match,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["search_jobs_for_alert"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="matching_jobs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def batch_create_jobs(
        self,
        parent,
        jobs,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Begins executing a batch create jobs operation.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `jobs`:
            >>> jobs = []
            >>>
            >>> response = client.batch_create_jobs(parent, jobs)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The resource name of the tenant under which the job is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and a default tenant is created if unspecified,
                for example, "projects/api-test-project".
            jobs (list[Union[dict, ~google.cloud.talent_v4beta1.types.Job]]): Required. The jobs to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Job`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_jobs,
                default_retry=self._method_configs["BatchCreateJobs"].retry,
                default_timeout=self._method_configs["BatchCreateJobs"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.BatchCreateJobsRequest(parent=parent, jobs=jobs)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["batch_create_jobs"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            job_service_pb2.JobOperationResult,
            metadata_type=common_pb2.BatchOperationMetadata,
        )

    def batch_update_jobs(
        self,
        parent,
        jobs,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Begins executing a batch update jobs operation.

        Example:
            >>> from google.cloud import talent_v4beta1
            >>>
            >>> client = talent_v4beta1.JobServiceClient()
            >>>
            >>> parent = client.tenant_path('[PROJECT]', '[TENANT]')
            >>>
            >>> # TODO: Initialize `jobs`:
            >>> jobs = []
            >>>
            >>> response = client.batch_update_jobs(parent, jobs)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The resource name of the tenant under which the job is
                created.

                The format is "projects/{project\_id}/tenants/{tenant\_id}", for
                example, "projects/api-test-project/tenant/foo".

                Tenant id is optional and the default tenant is used if unspecified, for
                example, "projects/api-test-project".
            jobs (list[Union[dict, ~google.cloud.talent_v4beta1.types.Job]]): Required. The jobs to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.Job`
            update_mask (Union[dict, ~google.cloud.talent_v4beta1.types.FieldMask]): Optional but strongly recommended to be provided for the best service
                experience, also increase latency when checking status of batch
                operation.

                If ``update_mask`` is provided, only the specified fields in ``Job`` are
                updated. Otherwise all the fields are updated.

                A field mask to restrict the fields that are updated. Only top level
                fields of ``Job`` are supported.

                If ``update_mask`` is provided, The ``Job`` inside ``JobResult`` will
                only contains fields that is updated, plus the Id of the Job. Otherwise,
                ``Job`` will include all fields, which can yield a very large response.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.talent_v4beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.talent_v4beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_update_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_update_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_update_jobs,
                default_retry=self._method_configs["BatchUpdateJobs"].retry,
                default_timeout=self._method_configs["BatchUpdateJobs"].timeout,
                client_info=self._client_info,
            )

        request = job_service_pb2.BatchUpdateJobsRequest(
            parent=parent, jobs=jobs, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["batch_update_jobs"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            job_service_pb2.JobOperationResult,
            metadata_type=common_pb2.BatchOperationMetadata,
        )
