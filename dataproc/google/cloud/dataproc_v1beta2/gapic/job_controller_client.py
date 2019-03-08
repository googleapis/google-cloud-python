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
"""Accesses the google.cloud.dataproc.v1beta2 JobController API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import grpc

from google.cloud.dataproc_v1beta2.gapic import enums
from google.cloud.dataproc_v1beta2.gapic import job_controller_client_config
from google.cloud.dataproc_v1beta2.gapic.transports import job_controller_grpc_transport
from google.cloud.dataproc_v1beta2.proto import clusters_pb2
from google.cloud.dataproc_v1beta2.proto import clusters_pb2_grpc
from google.cloud.dataproc_v1beta2.proto import jobs_pb2
from google.cloud.dataproc_v1beta2.proto import jobs_pb2_grpc
from google.cloud.dataproc_v1beta2.proto import operations_pb2 as proto_operations_pb2
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-dataproc").version


class JobControllerClient(object):
    """The JobController provides methods to manage jobs."""

    SERVICE_ADDRESS = "dataproc.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dataproc.v1beta2.JobController"

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
            JobControllerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
            transport (Union[~.JobControllerGrpcTransport,
                    Callable[[~.Credentials, type], ~.JobControllerGrpcTransport]): A transport
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
            client_config = job_controller_client_config.config

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
                    default_class=job_controller_grpc_transport.JobControllerGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = job_controller_grpc_transport.JobControllerGrpcTransport(
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
    def submit_job(
        self,
        project_id,
        region,
        job,
        request_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Submits a job to a cluster.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.submit_job(project_id, region, job)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            job (Union[dict, ~google.cloud.dataproc_v1beta2.types.Job]): Required. The job resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1beta2.types.Job`
            request_id (str): Optional. A unique id used to identify the request. If the server
                receives two ``SubmitJobRequest`` requests with the same id, then the
                second request will be ignored and the first ``Job`` created and stored
                in the backend is returned.

                It is recommended to always set this value to a
                `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.

                The id must contain only letters (a-z, A-Z), numbers (0-9), underscores
                (\_), and hyphens (-). The maximum length is 40 characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "submit_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "submit_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.submit_job,
                default_retry=self._method_configs["SubmitJob"].retry,
                default_timeout=self._method_configs["SubmitJob"].timeout,
                client_info=self._client_info,
            )

        request = jobs_pb2.SubmitJobRequest(
            project_id=project_id, region=region, job=job, request_id=request_id
        )
        return self._inner_api_calls["submit_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_job(
        self,
        project_id,
        region,
        job_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the resource representation for a job in a project.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `job_id`:
            >>> job_id = ''
            >>>
            >>> response = client.get_job(project_id, region, job_id)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            job_id (str): Required. The job ID.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.Job` instance.

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

        request = jobs_pb2.GetJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        return self._inner_api_calls["get_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_jobs(
        self,
        project_id,
        region,
        page_size=None,
        cluster_name=None,
        job_state_matcher=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists regions/{region}/jobs in a project.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_jobs(project_id, region):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_jobs(project_id, region).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            cluster_name (str): Optional. If set, the returned jobs list includes only jobs that were
                submitted to the named cluster.
            job_state_matcher (~google.cloud.dataproc_v1beta2.types.JobStateMatcher): Optional. Specifies enumerated categories of jobs to list. (default =
                match ALL jobs).

                If ``filter`` is provided, ``jobStateMatcher`` will be ignored.
            filter_ (str): Optional. A filter constraining the jobs to list. Filters are
                case-sensitive and have the following syntax:

                [field = value] AND [field [= value]] ...

                where **field** is ``status.state`` or ``labels.[KEY]``, and ``[KEY]``
                is a label key. **value** can be ``*`` to match all values.
                ``status.state`` can be either ``ACTIVE`` or ``NON_ACTIVE``. Only the
                logical ``AND`` operator is supported; space-separated items are treated
                as having an implicit ``AND`` operator.

                Example filter:

                status.state = ACTIVE AND labels.env = staging AND labels.starred = \*
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
            is an iterable of :class:`~google.cloud.dataproc_v1beta2.types.Job` instances.
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

        request = jobs_pb2.ListJobsRequest(
            project_id=project_id,
            region=region,
            page_size=page_size,
            cluster_name=cluster_name,
            job_state_matcher=job_state_matcher,
            filter=filter_,
        )
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

    def update_job(
        self,
        project_id,
        region,
        job_id,
        job,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a job in a project.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `job_id`:
            >>> job_id = ''
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_job(project_id, region, job_id, job, update_mask)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            job_id (str): Required. The job ID.
            job (Union[dict, ~google.cloud.dataproc_v1beta2.types.Job]): Required. The changes to the job.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1beta2.types.Job`
            update_mask (Union[dict, ~google.cloud.dataproc_v1beta2.types.FieldMask]): Required. Specifies the path, relative to Job, of the field to update.
                For example, to update the labels of a Job the update\_mask parameter
                would be specified as labels, and the ``PATCH`` request body would
                specify the new value. Note: Currently, labels is the only field that
                can be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dataproc_v1beta2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.Job` instance.

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

        request = jobs_pb2.UpdateJobRequest(
            project_id=project_id,
            region=region,
            job_id=job_id,
            job=job,
            update_mask=update_mask,
        )
        return self._inner_api_calls["update_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def cancel_job(
        self,
        project_id,
        region,
        job_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts a job cancellation request. To access the job resource after
        cancellation, call
        `regions/{region}/jobs.list <https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/projects.regions.jobs/list>`__
        or
        `regions/{region}/jobs.get <https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/projects.regions.jobs/get>`__.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `job_id`:
            >>> job_id = ''
            >>>
            >>> response = client.cancel_job(project_id, region, job_id)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            job_id (str): Required. The job ID.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dataproc_v1beta2.types.Job` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "cancel_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "cancel_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.cancel_job,
                default_retry=self._method_configs["CancelJob"].retry,
                default_timeout=self._method_configs["CancelJob"].timeout,
                client_info=self._client_info,
            )

        request = jobs_pb2.CancelJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        return self._inner_api_calls["cancel_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_job(
        self,
        project_id,
        region,
        job_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the job from the project. If the job is active, the delete
        fails, and the response returns ``FAILED_PRECONDITION``.

        Example:
            >>> from google.cloud import dataproc_v1beta2
            >>>
            >>> client = dataproc_v1beta2.JobControllerClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `region`:
            >>> region = ''
            >>>
            >>> # TODO: Initialize `job_id`:
            >>> job_id = ''
            >>>
            >>> client.delete_job(project_id, region, job_id)

        Args:
            project_id (str): Required. The ID of the Google Cloud Platform project that the job
                belongs to.
            region (str): Required. The Cloud Dataproc region in which to handle the request.
            job_id (str): Required. The job ID.
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

        request = jobs_pb2.DeleteJobRequest(
            project_id=project_id, region=region, job_id=job_id
        )
        self._inner_api_calls["delete_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
