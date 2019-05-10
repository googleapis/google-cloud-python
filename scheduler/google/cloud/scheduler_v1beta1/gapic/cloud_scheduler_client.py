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
"""Accesses the google.cloud.scheduler.v1beta1 CloudScheduler API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.scheduler_v1beta1.gapic import cloud_scheduler_client_config
from google.cloud.scheduler_v1beta1.gapic import enums
from google.cloud.scheduler_v1beta1.gapic.transports import (
    cloud_scheduler_grpc_transport,
)
from google.cloud.scheduler_v1beta1.proto import cloudscheduler_pb2
from google.cloud.scheduler_v1beta1.proto import cloudscheduler_pb2_grpc
from google.cloud.scheduler_v1beta1.proto import job_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-scheduler"
).version


class CloudSchedulerClient(object):
    """
    The Cloud Scheduler API allows external entities to reliably
    schedule asynchronous jobs.
    """

    SERVICE_ADDRESS = "cloudscheduler.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.scheduler.v1beta1.CloudScheduler"

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
            CloudSchedulerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def job_path(cls, project, location, job):
        """Return a fully-qualified job string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/jobs/{job}",
            project=project,
            location=location,
            job=job,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.CloudSchedulerGrpcTransport,
                    Callable[[~.Credentials, type], ~.CloudSchedulerGrpcTransport]): A transport
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
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = cloud_scheduler_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=cloud_scheduler_grpc_transport.CloudSchedulerGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cloud_scheduler_grpc_transport.CloudSchedulerGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
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
    def list_jobs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists jobs.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_jobs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_jobs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required.

                The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.scheduler_v1beta1.types.Job` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

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

        request = cloudscheduler_pb2.ListJobsRequest(parent=parent, page_size=page_size)
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

    def get_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a job.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[LOCATION]', '[JOB]')
            >>>
            >>> response = client.get_job(name)

        Args:
            name (str): Required.

                The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

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

        request = cloudscheduler_pb2.GetJobRequest(name=name)
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

    def create_job(
        self,
        parent,
        job,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a job.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.create_job(parent, job)

        Args:
            parent (str): Required.

                The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.
            job (Union[dict, ~google.cloud.scheduler_v1beta1.types.Job]): Required.

                The job to add. The user can optionally specify a name for the job in
                ``name``. ``name`` cannot be the same as an existing job. If a name is
                not specified then the system will generate a random unique name that
                will be returned (``name``) in the response.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.scheduler_v1beta1.types.Job`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

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

        request = cloudscheduler_pb2.CreateJobRequest(parent=parent, job=job)
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

    def update_job(
        self,
        job,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a job.

        If successful, the updated ``Job`` is returned. If the job does not
        exist, ``NOT_FOUND`` is returned.

        If UpdateJob does not successfully return, it is possible for the job to
        be in an ``Job.State.UPDATE_FAILED`` state. A job in this state may not
        be executed. If this happens, retry the UpdateJob request until a
        successful response is received.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.update_job(job)

        Args:
            job (Union[dict, ~google.cloud.scheduler_v1beta1.types.Job]): Required.

                The new job properties. ``name`` must be specified.

                Output only fields cannot be modified using UpdateJob. Any value
                specified for an output only field will be ignored.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.scheduler_v1beta1.types.Job`
            update_mask (Union[dict, ~google.cloud.scheduler_v1beta1.types.FieldMask]): A  mask used to specify which fields of the job are being updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.scheduler_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

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

        request = cloudscheduler_pb2.UpdateJobRequest(job=job, update_mask=update_mask)
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
        Deletes a job.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[LOCATION]', '[JOB]')
            >>>
            >>> client.delete_job(name)

        Args:
            name (str): Required.

                The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
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

        request = cloudscheduler_pb2.DeleteJobRequest(name=name)
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

    def pause_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Pauses a job.

        If a job is paused then the system will stop executing the job until it
        is re-enabled via ``ResumeJob``. The state of the job is stored in
        ``state``; if paused it will be set to ``Job.State.PAUSED``. A job must
        be in ``Job.State.ENABLED`` to be paused.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[LOCATION]', '[JOB]')
            >>>
            >>> response = client.pause_job(name)

        Args:
            name (str): Required.

                The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "pause_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "pause_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.pause_job,
                default_retry=self._method_configs["PauseJob"].retry,
                default_timeout=self._method_configs["PauseJob"].timeout,
                client_info=self._client_info,
            )

        request = cloudscheduler_pb2.PauseJobRequest(name=name)
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

        return self._inner_api_calls["pause_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def resume_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Resume a job.

        This method reenables a job after it has been ``Job.State.PAUSED``. The
        state of a job is stored in ``Job.state``; after calling this method it
        will be set to ``Job.State.ENABLED``. A job must be in
        ``Job.State.PAUSED`` to be resumed.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[LOCATION]', '[JOB]')
            >>>
            >>> response = client.resume_job(name)

        Args:
            name (str): Required.

                The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "resume_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "resume_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.resume_job,
                default_retry=self._method_configs["ResumeJob"].retry,
                default_timeout=self._method_configs["ResumeJob"].timeout,
                client_info=self._client_info,
            )

        request = cloudscheduler_pb2.ResumeJobRequest(name=name)
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

        return self._inner_api_calls["resume_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def run_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Forces a job to run now.

        When this method is called, Cloud Scheduler will dispatch the job, even
        if the job is already running.

        Example:
            >>> from google.cloud import scheduler_v1beta1
            >>>
            >>> client = scheduler_v1beta1.CloudSchedulerClient()
            >>>
            >>> name = client.job_path('[PROJECT]', '[LOCATION]', '[JOB]')
            >>>
            >>> response = client.run_job(name)

        Args:
            name (str): Required.

                The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.scheduler_v1beta1.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "run_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "run_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.run_job,
                default_retry=self._method_configs["RunJob"].retry,
                default_timeout=self._method_configs["RunJob"].timeout,
                client_info=self._client_info,
            )

        request = cloudscheduler_pb2.RunJobRequest(name=name)
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

        return self._inner_api_calls["run_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
