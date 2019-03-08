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
            channel = self.create_channel(address=address, credentials=credentials)

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
    def create_channel(cls, address="cloudasset.googleapis.com:443", credentials=None):
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
    def export_assets(self):
        """Return the gRPC stub for :meth:`AssetServiceClient.export_assets`.

        Exports assets with time and resource types to a given Cloud Storage
        location. The output format is newline-delimited JSON. This API
        implements the ``google.longrunning.Operation`` API allowing you to keep
        track of the export.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["asset_service_stub"].ExportAssets

    @property
    def batch_get_assets_history(self):
        """Return the gRPC stub for :meth:`AssetServiceClient.batch_get_assets_history`.

        Batch gets the update history of assets that overlap a time window. For
        RESOURCE content, this API outputs history with asset in both non-delete
        or deleted status. For IAM\_POLICY content, this API outputs history
        when the asset and its attached IAM POLICY both exist. This can create
        gaps in the output history.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["asset_service_stub"].BatchGetAssetsHistory
