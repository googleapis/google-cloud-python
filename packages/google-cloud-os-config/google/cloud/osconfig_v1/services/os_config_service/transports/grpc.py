# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Callable, Dict, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import OsConfigServiceTransport


class OsConfigServiceGrpcTransport(OsConfigServiceTransport):
    """gRPC backend transport for OsConfigService.

    OS Config API
    The OS Config service is a server-side component that you can
    use to manage package installations and patch jobs for virtual
    machine instances.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "osconfig.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
          google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = grpc_helpers.create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_credentials,
                scopes=self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

    @classmethod
    def create_channel(
        cls,
        host: str = "osconfig.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def execute_patch_job(
        self
    ) -> Callable[[patch_jobs.ExecutePatchJobRequest], patch_jobs.PatchJob]:
        r"""Return a callable for the execute patch job method over gRPC.

        Patch VM instances by creating and running a patch
        job.

        Returns:
            Callable[[~.ExecutePatchJobRequest],
                    ~.PatchJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "execute_patch_job" not in self._stubs:
            self._stubs["execute_patch_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/ExecutePatchJob",
                request_serializer=patch_jobs.ExecutePatchJobRequest.serialize,
                response_deserializer=patch_jobs.PatchJob.deserialize,
            )
        return self._stubs["execute_patch_job"]

    @property
    def get_patch_job(
        self
    ) -> Callable[[patch_jobs.GetPatchJobRequest], patch_jobs.PatchJob]:
        r"""Return a callable for the get patch job method over gRPC.

        Get the patch job. This can be used to track the
        progress of an ongoing patch job or review the details
        of completed jobs.

        Returns:
            Callable[[~.GetPatchJobRequest],
                    ~.PatchJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_patch_job" not in self._stubs:
            self._stubs["get_patch_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/GetPatchJob",
                request_serializer=patch_jobs.GetPatchJobRequest.serialize,
                response_deserializer=patch_jobs.PatchJob.deserialize,
            )
        return self._stubs["get_patch_job"]

    @property
    def cancel_patch_job(
        self
    ) -> Callable[[patch_jobs.CancelPatchJobRequest], patch_jobs.PatchJob]:
        r"""Return a callable for the cancel patch job method over gRPC.

        Cancel a patch job. The patch job must be active.
        Canceled patch jobs cannot be restarted.

        Returns:
            Callable[[~.CancelPatchJobRequest],
                    ~.PatchJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_patch_job" not in self._stubs:
            self._stubs["cancel_patch_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/CancelPatchJob",
                request_serializer=patch_jobs.CancelPatchJobRequest.serialize,
                response_deserializer=patch_jobs.PatchJob.deserialize,
            )
        return self._stubs["cancel_patch_job"]

    @property
    def list_patch_jobs(
        self
    ) -> Callable[[patch_jobs.ListPatchJobsRequest], patch_jobs.ListPatchJobsResponse]:
        r"""Return a callable for the list patch jobs method over gRPC.

        Get a list of patch jobs.

        Returns:
            Callable[[~.ListPatchJobsRequest],
                    ~.ListPatchJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_patch_jobs" not in self._stubs:
            self._stubs["list_patch_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/ListPatchJobs",
                request_serializer=patch_jobs.ListPatchJobsRequest.serialize,
                response_deserializer=patch_jobs.ListPatchJobsResponse.deserialize,
            )
        return self._stubs["list_patch_jobs"]

    @property
    def list_patch_job_instance_details(
        self
    ) -> Callable[
        [patch_jobs.ListPatchJobInstanceDetailsRequest],
        patch_jobs.ListPatchJobInstanceDetailsResponse,
    ]:
        r"""Return a callable for the list patch job instance
        details method over gRPC.

        Get a list of instance details for a given patch job.

        Returns:
            Callable[[~.ListPatchJobInstanceDetailsRequest],
                    ~.ListPatchJobInstanceDetailsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_patch_job_instance_details" not in self._stubs:
            self._stubs[
                "list_patch_job_instance_details"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/ListPatchJobInstanceDetails",
                request_serializer=patch_jobs.ListPatchJobInstanceDetailsRequest.serialize,
                response_deserializer=patch_jobs.ListPatchJobInstanceDetailsResponse.deserialize,
            )
        return self._stubs["list_patch_job_instance_details"]

    @property
    def create_patch_deployment(
        self
    ) -> Callable[
        [patch_deployments.CreatePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        r"""Return a callable for the create patch deployment method over gRPC.

        Create an OS Config patch deployment.

        Returns:
            Callable[[~.CreatePatchDeploymentRequest],
                    ~.PatchDeployment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_patch_deployment" not in self._stubs:
            self._stubs["create_patch_deployment"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/CreatePatchDeployment",
                request_serializer=patch_deployments.CreatePatchDeploymentRequest.serialize,
                response_deserializer=patch_deployments.PatchDeployment.deserialize,
            )
        return self._stubs["create_patch_deployment"]

    @property
    def get_patch_deployment(
        self
    ) -> Callable[
        [patch_deployments.GetPatchDeploymentRequest], patch_deployments.PatchDeployment
    ]:
        r"""Return a callable for the get patch deployment method over gRPC.

        Get an OS Config patch deployment.

        Returns:
            Callable[[~.GetPatchDeploymentRequest],
                    ~.PatchDeployment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_patch_deployment" not in self._stubs:
            self._stubs["get_patch_deployment"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/GetPatchDeployment",
                request_serializer=patch_deployments.GetPatchDeploymentRequest.serialize,
                response_deserializer=patch_deployments.PatchDeployment.deserialize,
            )
        return self._stubs["get_patch_deployment"]

    @property
    def list_patch_deployments(
        self
    ) -> Callable[
        [patch_deployments.ListPatchDeploymentsRequest],
        patch_deployments.ListPatchDeploymentsResponse,
    ]:
        r"""Return a callable for the list patch deployments method over gRPC.

        Get a page of OS Config patch deployments.

        Returns:
            Callable[[~.ListPatchDeploymentsRequest],
                    ~.ListPatchDeploymentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_patch_deployments" not in self._stubs:
            self._stubs["list_patch_deployments"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/ListPatchDeployments",
                request_serializer=patch_deployments.ListPatchDeploymentsRequest.serialize,
                response_deserializer=patch_deployments.ListPatchDeploymentsResponse.deserialize,
            )
        return self._stubs["list_patch_deployments"]

    @property
    def delete_patch_deployment(
        self
    ) -> Callable[[patch_deployments.DeletePatchDeploymentRequest], empty.Empty]:
        r"""Return a callable for the delete patch deployment method over gRPC.

        Delete an OS Config patch deployment.

        Returns:
            Callable[[~.DeletePatchDeploymentRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_patch_deployment" not in self._stubs:
            self._stubs["delete_patch_deployment"] = self.grpc_channel.unary_unary(
                "/google.cloud.osconfig.v1.OsConfigService/DeletePatchDeployment",
                request_serializer=patch_deployments.DeletePatchDeploymentRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_patch_deployment"]


__all__ = ("OsConfigServiceGrpcTransport",)
