# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.devtools.cloudbuild_v1.proto import cloudbuild_pb2_grpc


class CloudBuildGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.devtools.cloudbuild.v1 CloudBuild API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="cloudbuild.googleapis.com:443"
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
                "The `channel` and `credentials` arguments are mutually " "exclusive.",
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "cloud_build_stub": cloudbuild_pb2_grpc.CloudBuildStub(channel),
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="cloudbuild.googleapis.com:443", credentials=None, **kwargs
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
    def list_builds(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_builds`.

        Lists previously requested builds.

        Previously requested builds may still be in-progress, or may have finished
        successfully or unsuccessfully.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListBuilds

    @property
    def delete_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.delete_build_trigger`.

        Deletes a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].DeleteBuildTrigger

    @property
    def create_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_build`.

        Starts a build with the specified configuration.

        This method returns a long-running ``Operation``, which includes the
        build ID. Pass the build ID to ``GetBuild`` to determine the build
        status (such as ``SUCCESS`` or ``FAILURE``).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateBuild

    @property
    def get_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_build`.

        Returns information about a previously requested build.

        The ``Build`` that is returned includes its status (such as ``SUCCESS``,
        ``FAILURE``, or ``WORKING``), and timing information.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetBuild

    @property
    def cancel_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.cancel_build`.

        Cancels a build in progress.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CancelBuild

    @property
    def retry_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.retry_build`.

        Creates a new build based on the specified build.

        This method creates a new build using the original build request, which
        may or may not result in an identical build.

        For triggered builds:

        -  Triggered builds resolve to a precise revision; therefore a retry of
           a triggered build will result in a build that uses the same revision.

        For non-triggered builds that specify ``RepoSource``:

        -  If the original build built from the tip of a branch, the retried
           build will build from the tip of that branch, which may not be the
           same revision as the original build.
        -  If the original build specified a commit sha or revision ID, the
           retried build will use the identical source.

        For builds that specify ``StorageSource``:

        -  If the original build pulled source from Google Cloud Storage without
           specifying the generation of the object, the new build will use the
           current object, which may be different from the original build
           source.
        -  If the original build pulled source from Cloud Storage and specified
           the generation of the object, the new build will attempt to use the
           same object, which may or may not be available depending on the
           bucket's lifecycle management settings.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].RetryBuild

    @property
    def create_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_build_trigger`.

        Creates a new ``BuildTrigger``.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateBuildTrigger

    @property
    def get_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_build_trigger`.

        Returns information about a ``BuildTrigger``.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetBuildTrigger

    @property
    def list_build_triggers(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_build_triggers`.

        Lists existing ``BuildTrigger``\ s.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListBuildTriggers

    @property
    def update_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.update_build_trigger`.

        Updates a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].UpdateBuildTrigger

    @property
    def run_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.run_build_trigger`.

        Runs a ``BuildTrigger`` at a particular source revision.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].RunBuildTrigger

    @property
    def create_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_worker_pool`.

        Creates a ``WorkerPool`` to run the builds, and returns the new
        worker pool.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateWorkerPool

    @property
    def get_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_worker_pool`.

        Returns information about a ``WorkerPool``.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetWorkerPool

    @property
    def delete_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.delete_worker_pool`.

        Deletes a ``WorkerPool`` by its project ID and WorkerPool name.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].DeleteWorkerPool

    @property
    def update_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.update_worker_pool`.

        Update a ``WorkerPool``.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].UpdateWorkerPool

    @property
    def list_worker_pools(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_worker_pools`.

        List project's ``WorkerPool``\ s.

        This API is experimental.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListWorkerPools
