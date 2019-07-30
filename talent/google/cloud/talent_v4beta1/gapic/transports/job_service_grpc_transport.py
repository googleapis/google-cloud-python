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


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.talent_v4beta1.proto import job_service_pb2_grpc


class JobServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.talent.v4beta1 JobService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/jobs",
    )

    def __init__(
        self, channel=None, credentials=None, address="jobs.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"job_service_stub": job_service_pb2_grpc.JobServiceStub(channel)}

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="jobs.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_job(self):
        """Return the gRPC stub for :meth:`JobServiceClient.create_job`.

        Creates a new job.

        Typically, the job becomes searchable within 10 seconds, but it may take
        up to 5 minutes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].CreateJob

    @property
    def get_job(self):
        """Return the gRPC stub for :meth:`JobServiceClient.get_job`.

        Retrieves the specified job, whose status is OPEN or recently EXPIRED
        within the last 90 days.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].GetJob

    @property
    def update_job(self):
        """Return the gRPC stub for :meth:`JobServiceClient.update_job`.

        Updates specified job.

        Typically, updated contents become visible in search results within 10
        seconds, but it may take up to 5 minutes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].UpdateJob

    @property
    def delete_job(self):
        """Return the gRPC stub for :meth:`JobServiceClient.delete_job`.

        Deletes the specified job.

        Typically, the job becomes unsearchable within 10 seconds, but it may take
        up to 5 minutes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].DeleteJob

    @property
    def list_jobs(self):
        """Return the gRPC stub for :meth:`JobServiceClient.list_jobs`.

        Lists jobs by filter.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].ListJobs

    @property
    def batch_delete_jobs(self):
        """Return the gRPC stub for :meth:`JobServiceClient.batch_delete_jobs`.

        Deletes a list of ``Job``\ s by filter.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].BatchDeleteJobs

    @property
    def search_jobs(self):
        """Return the gRPC stub for :meth:`JobServiceClient.search_jobs`.

        Searches for jobs using the provided ``SearchJobsRequest``.

        This call constrains the ``visibility`` of jobs present in the database,
        and only returns jobs that the caller has permission to search against.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].SearchJobs

    @property
    def search_jobs_for_alert(self):
        """Return the gRPC stub for :meth:`JobServiceClient.search_jobs_for_alert`.

        Searches for jobs using the provided ``SearchJobsRequest``.

        This API call is intended for the use case of targeting passive job
        seekers (for example, job seekers who have signed up to receive email
        alerts about potential job opportunities), and has different algorithmic
        adjustments that are targeted to passive job seekers.

        This call constrains the ``visibility`` of jobs present in the database,
        and only returns jobs the caller has permission to search against.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].SearchJobsForAlert

    @property
    def batch_create_jobs(self):
        """Return the gRPC stub for :meth:`JobServiceClient.batch_create_jobs`.

        Begins executing a batch create jobs operation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].BatchCreateJobs

    @property
    def batch_update_jobs(self):
        """Return the gRPC stub for :meth:`JobServiceClient.batch_update_jobs`.

        Begins executing a batch update jobs operation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["job_service_stub"].BatchUpdateJobs
