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

from google.cloud.asset_v1beta1.proto import asset_service_pb2_grpc


class AssetServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.asset.v1beta1 AssetService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="cloudasset.googleapis.com:443"
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
            "asset_service_stub": asset_service_pb2_grpc.AssetServiceStub(channel)
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="cloudasset.googleapis.com:443", credentials=None, **kwargs
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
    def export_assets(self):
        """Return the gRPC stub for :meth:`AssetServiceClient.export_assets`.

        See ``HttpRule``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["asset_service_stub"].ExportAssets

    @property
    def batch_get_assets_history(self):
        """Return the gRPC stub for :meth:`AssetServiceClient.batch_get_assets_history`.

        A URL/resource name that uniquely identifies the type of the
        serialized protocol buffer message. This string must contain at least
        one "/" character. The last segment of the URL's path must represent the
        fully qualified name of the type (as in
        ``path/google.protobuf.Duration``). The name should be in a canonical
        form (e.g., leading "." is not accepted).

        In practice, teams usually precompile into the binary all types that
        they expect it to use in the context of Any. However, for URLs which use
        the scheme ``http``, ``https``, or no scheme, one can optionally set up
        a type server that maps type URLs to message definitions as follows:

        -  If no scheme is provided, ``https`` is assumed.
        -  An HTTP GET on the URL must yield a ``google.protobuf.Type`` value in
           binary format, or produce an error.
        -  Applications are allowed to cache lookup results based on the URL, or
           have them precompiled into a binary to avoid any lookup. Therefore,
           binary compatibility needs to be preserved on changes to types. (Use
           versioned type names to manage breaking changes.)

        Note: this functionality is not currently available in the official
        protobuf release, and it is not used for type URLs beginning with
        type.googleapis.com.

        Schemes other than ``http``, ``https`` (or the empty scheme) might be
        used with implementation specific semantics.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["asset_service_stub"].BatchGetAssetsHistory
