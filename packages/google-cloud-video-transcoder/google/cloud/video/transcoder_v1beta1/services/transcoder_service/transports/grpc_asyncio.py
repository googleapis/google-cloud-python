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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.video.transcoder_v1beta1.types import resources
from google.cloud.video.transcoder_v1beta1.types import services
from google.protobuf import empty_pb2  # type: ignore
from .base import TranscoderServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import TranscoderServiceGrpcTransport


class TranscoderServiceGrpcAsyncIOTransport(TranscoderServiceTransport):
    """gRPC AsyncIO backend transport for TranscoderService.

    Using the Transcoder API, you can queue asynchronous jobs for
    transcoding media into various output formats. Output formats
    may include different streaming standards such as HTTP Live
    Streaming (HLS) and Dynamic Adaptive Streaming over HTTP (DASH).
    You can also customize jobs using advanced features such as
    Digital Rights Management (DRM), audio equalization, content
    concatenation, and digital ad-stitch ready content generation.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "transcoder.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "transcoder.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_job(
        self,
    ) -> Callable[[services.CreateJobRequest], Awaitable[resources.Job]]:
        r"""Return a callable for the create job method over gRPC.

        Creates a job in the specified region.

        Returns:
            Callable[[~.CreateJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_job" not in self._stubs:
            self._stubs["create_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/CreateJob",
                request_serializer=services.CreateJobRequest.serialize,
                response_deserializer=resources.Job.deserialize,
            )
        return self._stubs["create_job"]

    @property
    def list_jobs(
        self,
    ) -> Callable[[services.ListJobsRequest], Awaitable[services.ListJobsResponse]]:
        r"""Return a callable for the list jobs method over gRPC.

        Lists jobs in the specified region.

        Returns:
            Callable[[~.ListJobsRequest],
                    Awaitable[~.ListJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_jobs" not in self._stubs:
            self._stubs["list_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/ListJobs",
                request_serializer=services.ListJobsRequest.serialize,
                response_deserializer=services.ListJobsResponse.deserialize,
            )
        return self._stubs["list_jobs"]

    @property
    def get_job(self) -> Callable[[services.GetJobRequest], Awaitable[resources.Job]]:
        r"""Return a callable for the get job method over gRPC.

        Returns the job data.

        Returns:
            Callable[[~.GetJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job" not in self._stubs:
            self._stubs["get_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/GetJob",
                request_serializer=services.GetJobRequest.serialize,
                response_deserializer=resources.Job.deserialize,
            )
        return self._stubs["get_job"]

    @property
    def delete_job(
        self,
    ) -> Callable[[services.DeleteJobRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete job method over gRPC.

        Deletes a job.

        Returns:
            Callable[[~.DeleteJobRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_job" not in self._stubs:
            self._stubs["delete_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/DeleteJob",
                request_serializer=services.DeleteJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_job"]

    @property
    def create_job_template(
        self,
    ) -> Callable[
        [services.CreateJobTemplateRequest], Awaitable[resources.JobTemplate]
    ]:
        r"""Return a callable for the create job template method over gRPC.

        Creates a job template in the specified region.

        Returns:
            Callable[[~.CreateJobTemplateRequest],
                    Awaitable[~.JobTemplate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_job_template" not in self._stubs:
            self._stubs["create_job_template"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/CreateJobTemplate",
                request_serializer=services.CreateJobTemplateRequest.serialize,
                response_deserializer=resources.JobTemplate.deserialize,
            )
        return self._stubs["create_job_template"]

    @property
    def list_job_templates(
        self,
    ) -> Callable[
        [services.ListJobTemplatesRequest], Awaitable[services.ListJobTemplatesResponse]
    ]:
        r"""Return a callable for the list job templates method over gRPC.

        Lists job templates in the specified region.

        Returns:
            Callable[[~.ListJobTemplatesRequest],
                    Awaitable[~.ListJobTemplatesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_job_templates" not in self._stubs:
            self._stubs["list_job_templates"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/ListJobTemplates",
                request_serializer=services.ListJobTemplatesRequest.serialize,
                response_deserializer=services.ListJobTemplatesResponse.deserialize,
            )
        return self._stubs["list_job_templates"]

    @property
    def get_job_template(
        self,
    ) -> Callable[[services.GetJobTemplateRequest], Awaitable[resources.JobTemplate]]:
        r"""Return a callable for the get job template method over gRPC.

        Returns the job template data.

        Returns:
            Callable[[~.GetJobTemplateRequest],
                    Awaitable[~.JobTemplate]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job_template" not in self._stubs:
            self._stubs["get_job_template"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/GetJobTemplate",
                request_serializer=services.GetJobTemplateRequest.serialize,
                response_deserializer=resources.JobTemplate.deserialize,
            )
        return self._stubs["get_job_template"]

    @property
    def delete_job_template(
        self,
    ) -> Callable[[services.DeleteJobTemplateRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete job template method over gRPC.

        Deletes a job template.

        Returns:
            Callable[[~.DeleteJobTemplateRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_job_template" not in self._stubs:
            self._stubs["delete_job_template"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.transcoder.v1beta1.TranscoderService/DeleteJobTemplate",
                request_serializer=services.DeleteJobTemplateRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_job_template"]


__all__ = ("TranscoderServiceGrpcAsyncIOTransport",)
