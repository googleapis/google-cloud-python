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

from google.cloud.bigquery_datatransfer_v1.proto import datatransfer_pb2_grpc


class DataTransferServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.bigquery.datatransfer.v1 DataTransferService API.

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
        address="bigquerydatatransfer.googleapis.com:443",
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
            "data_transfer_service_stub": datatransfer_pb2_grpc.DataTransferServiceStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="bigquerydatatransfer.googleapis.com:443", credentials=None
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
    def get_data_source(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.get_data_source`.

        Retrieves a supported data source and returns its settings,
        which can be used for UI rendering.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].GetDataSource

    @property
    def list_data_sources(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.list_data_sources`.

        Lists supported data sources and returns their settings,
        which can be used for UI rendering.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].ListDataSources

    @property
    def create_transfer_config(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.create_transfer_config`.

        Creates a new data transfer configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].CreateTransferConfig

    @property
    def update_transfer_config(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.update_transfer_config`.

        Updates a data transfer configuration.
        All fields must be set, even if they are not updated.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].UpdateTransferConfig

    @property
    def delete_transfer_config(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.delete_transfer_config`.

        Deletes a data transfer configuration,
        including any associated transfer runs and logs.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].DeleteTransferConfig

    @property
    def get_transfer_config(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.get_transfer_config`.

        Returns information about a data transfer config.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].GetTransferConfig

    @property
    def list_transfer_configs(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.list_transfer_configs`.

        Returns information about all data transfers in the project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].ListTransferConfigs

    @property
    def schedule_transfer_runs(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.schedule_transfer_runs`.

        Creates transfer runs for a time range [start\_time, end\_time]. For
        each date - or whatever granularity the data source supports - in the
        range, one transfer run is created. Note that runs are created per UTC
        time in the time range.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].ScheduleTransferRuns

    @property
    def get_transfer_run(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.get_transfer_run`.

        Returns information about the particular transfer run.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].GetTransferRun

    @property
    def delete_transfer_run(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.delete_transfer_run`.

        Deletes the specified transfer run.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].DeleteTransferRun

    @property
    def list_transfer_runs(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.list_transfer_runs`.

        Returns information about running and completed jobs.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].ListTransferRuns

    @property
    def list_transfer_logs(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.list_transfer_logs`.

        Returns user facing log messages for the data transfer run.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].ListTransferLogs

    @property
    def check_valid_creds(self):
        """Return the gRPC stub for :meth:`DataTransferServiceClient.check_valid_creds`.

        Returns true if valid credentials exist for the given data source and
        requesting user.
        Some data sources doesn't support service account, so we need to talk to
        them on behalf of the end user. This API just checks whether we have OAuth
        token for the particular user, which is a pre-requisite before user can
        create a transfer config.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_transfer_service_stub"].CheckValidCreds
