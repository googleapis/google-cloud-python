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

from google.cloud.scheduler_v1.proto import cloudscheduler_pb2_grpc


class CloudSchedulerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.scheduler.v1 CloudScheduler API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        channel=None,
        credentials=None,
        address="cloudscheduler.googleapis.com:443",
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
        self._stubs = {
            "cloud_scheduler_stub": cloudscheduler_pb2_grpc.CloudSchedulerStub(channel)
        }

    @classmethod
    def create_channel(
        cls, address="cloudscheduler.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_jobs(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.list_jobs`.

        Lists jobs.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].ListJobs

    @property
    def get_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.get_job`.

        Gets a job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].GetJob

    @property
    def create_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.create_job`.

        Creates a job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].CreateJob

    @property
    def update_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.update_job`.

        Updates a job.

        If successful, the updated ``Job`` is returned. If the job does not
        exist, ``NOT_FOUND`` is returned.

        If UpdateJob does not successfully return, it is possible for the job to
        be in an ``Job.State.UPDATE_FAILED`` state. A job in this state may not
        be executed. If this happens, retry the UpdateJob request until a
        successful response is received.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].UpdateJob

    @property
    def delete_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.delete_job`.

        Deletes a job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].DeleteJob

    @property
    def pause_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.pause_job`.

        Pauses a job.

        If a job is paused then the system will stop executing the job until it
        is re-enabled via ``ResumeJob``. The state of the job is stored in
        ``state``; if paused it will be set to ``Job.State.PAUSED``. A job must
        be in ``Job.State.ENABLED`` to be paused.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].PauseJob

    @property
    def resume_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.resume_job`.

        Resume a job.

        This method reenables a job after it has been ``Job.State.PAUSED``. The
        state of a job is stored in ``Job.state``; after calling this method it
        will be set to ``Job.State.ENABLED``. A job must be in
        ``Job.State.PAUSED`` to be resumed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].ResumeJob

    @property
    def run_job(self):
        """Return the gRPC stub for :meth:`CloudSchedulerClient.run_job`.

        Forces a job to run now.

        When this method is called, Cloud Scheduler will dispatch the job, even
        if the job is already running.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_scheduler_stub"].RunJob
