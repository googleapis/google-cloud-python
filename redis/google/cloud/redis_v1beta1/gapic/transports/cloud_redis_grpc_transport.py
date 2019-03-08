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

from google.cloud.redis_v1beta1.proto import cloud_redis_pb2_grpc


class CloudRedisGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.redis.v1beta1 CloudRedis API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="redis.googleapis.com:443"
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
        self._stubs = {"cloud_redis_stub": cloud_redis_pb2_grpc.CloudRedisStub(channel)}

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(cls, address="redis.googleapis.com:443", credentials=None):
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
    def list_instances(self):
        """Return the gRPC stub for :meth:`CloudRedisClient.list_instances`.

        Lists all Redis instances owned by a project in either the specified
        location (region) or all locations.

        The location should have the following format: \*
        ``projects/{project_id}/locations/{location_id}``

        If ``location_id`` is specified as ``-`` (wildcard), then all regions
        available to the project are queried, and the results are aggregated.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_redis_stub"].ListInstances

    @property
    def get_instance(self):
        """Return the gRPC stub for :meth:`CloudRedisClient.get_instance`.

        Gets the details of a specific Redis instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_redis_stub"].GetInstance

    @property
    def create_instance(self):
        """Return the gRPC stub for :meth:`CloudRedisClient.create_instance`.

        Creates a Redis instance based on the specified tier and memory size.

        By default, the instance is peered to the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        The creation is executed asynchronously and callers may check the
        returned operation to track its progress. Once the operation is
        completed the Redis instance will be fully functional. Completed
        longrunning.Operation will contain the new instance object in the
        response field.

        The returned operation is automatically deleted after a few hours, so
        there is no need to call DeleteOperation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_redis_stub"].CreateInstance

    @property
    def update_instance(self):
        """Return the gRPC stub for :meth:`CloudRedisClient.update_instance`.

        Updates the metadata and configuration of a specific Redis instance.

        Completed longrunning.Operation will contain the new instance object
        in the response field. The returned operation is automatically deleted
        after a few hours, so there is no need to call DeleteOperation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_redis_stub"].UpdateInstance

    @property
    def delete_instance(self):
        """Return the gRPC stub for :meth:`CloudRedisClient.delete_instance`.

        Deletes a specific Redis instance.  Instance stops serving and data is
        deleted.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_redis_stub"].DeleteInstance
