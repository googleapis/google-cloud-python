# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import grpc  # type: ignore

from google.cloud.support_v2.types import case
from google.cloud.support_v2.types import case as gcs_case
from google.cloud.support_v2.types import case_service

from .base import DEFAULT_CLIENT_INFO, CaseServiceTransport


class CaseServiceGrpcTransport(CaseServiceTransport):
    """gRPC backend transport for CaseService.

    A service to manage Google Cloud support cases.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "cloudsupport.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudsupport.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
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

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
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

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudsupport.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def get_case(self) -> Callable[[case_service.GetCaseRequest], case.Case]:
        r"""Return a callable for the get case method over gRPC.

        Retrieve the specified case.

        Returns:
            Callable[[~.GetCaseRequest],
                    ~.Case]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_case" not in self._stubs:
            self._stubs["get_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/GetCase",
                request_serializer=case_service.GetCaseRequest.serialize,
                response_deserializer=case.Case.deserialize,
            )
        return self._stubs["get_case"]

    @property
    def list_cases(
        self,
    ) -> Callable[[case_service.ListCasesRequest], case_service.ListCasesResponse]:
        r"""Return a callable for the list cases method over gRPC.

        Retrieve all cases under the specified parent.

        Note: Listing cases under an Organization returns only the cases
        directly parented by that organization. To retrieve all cases
        under an organization, including cases parented by projects
        under that organization, use ``cases.search``.

        Returns:
            Callable[[~.ListCasesRequest],
                    ~.ListCasesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cases" not in self._stubs:
            self._stubs["list_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/ListCases",
                request_serializer=case_service.ListCasesRequest.serialize,
                response_deserializer=case_service.ListCasesResponse.deserialize,
            )
        return self._stubs["list_cases"]

    @property
    def search_cases(
        self,
    ) -> Callable[[case_service.SearchCasesRequest], case_service.SearchCasesResponse]:
        r"""Return a callable for the search cases method over gRPC.

        Search cases using the specified query.

        Returns:
            Callable[[~.SearchCasesRequest],
                    ~.SearchCasesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_cases" not in self._stubs:
            self._stubs["search_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/SearchCases",
                request_serializer=case_service.SearchCasesRequest.serialize,
                response_deserializer=case_service.SearchCasesResponse.deserialize,
            )
        return self._stubs["search_cases"]

    @property
    def create_case(self) -> Callable[[case_service.CreateCaseRequest], gcs_case.Case]:
        r"""Return a callable for the create case method over gRPC.

        Create a new case and associate it with the given Google Cloud
        Resource. The case object must have the following fields set:
        ``display_name``, ``description``, ``classification``, and
        ``priority``.

        Returns:
            Callable[[~.CreateCaseRequest],
                    ~.Case]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_case" not in self._stubs:
            self._stubs["create_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/CreateCase",
                request_serializer=case_service.CreateCaseRequest.serialize,
                response_deserializer=gcs_case.Case.deserialize,
            )
        return self._stubs["create_case"]

    @property
    def update_case(self) -> Callable[[case_service.UpdateCaseRequest], gcs_case.Case]:
        r"""Return a callable for the update case method over gRPC.

        Update the specified case. Only a subset of fields
        can be updated.

        Returns:
            Callable[[~.UpdateCaseRequest],
                    ~.Case]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_case" not in self._stubs:
            self._stubs["update_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/UpdateCase",
                request_serializer=case_service.UpdateCaseRequest.serialize,
                response_deserializer=gcs_case.Case.deserialize,
            )
        return self._stubs["update_case"]

    @property
    def escalate_case(self) -> Callable[[case_service.EscalateCaseRequest], case.Case]:
        r"""Return a callable for the escalate case method over gRPC.

        Escalate a case. Escalating a case will initiate the
        Google Cloud Support escalation management process.

        This operation is only available to certain Customer
        Care tiers. Go to https://cloud.google.com/support and
        look for 'Technical support escalations' in the feature
        list to find out which tiers are able to perform
        escalations.

        Returns:
            Callable[[~.EscalateCaseRequest],
                    ~.Case]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "escalate_case" not in self._stubs:
            self._stubs["escalate_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/EscalateCase",
                request_serializer=case_service.EscalateCaseRequest.serialize,
                response_deserializer=case.Case.deserialize,
            )
        return self._stubs["escalate_case"]

    @property
    def close_case(self) -> Callable[[case_service.CloseCaseRequest], case.Case]:
        r"""Return a callable for the close case method over gRPC.

        Close the specified case.

        Returns:
            Callable[[~.CloseCaseRequest],
                    ~.Case]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "close_case" not in self._stubs:
            self._stubs["close_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/CloseCase",
                request_serializer=case_service.CloseCaseRequest.serialize,
                response_deserializer=case.Case.deserialize,
            )
        return self._stubs["close_case"]

    @property
    def search_case_classifications(
        self,
    ) -> Callable[
        [case_service.SearchCaseClassificationsRequest],
        case_service.SearchCaseClassificationsResponse,
    ]:
        r"""Return a callable for the search case classifications method over gRPC.

        Retrieve valid classifications to be used when
        creating a support case. The classications are
        hierarchical, with each classification containing all
        levels of the hierarchy, separated by " > ". For example
        "Technical Issue > Compute > Compute Engine".

        Returns:
            Callable[[~.SearchCaseClassificationsRequest],
                    ~.SearchCaseClassificationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_case_classifications" not in self._stubs:
            self._stubs["search_case_classifications"] = self.grpc_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/SearchCaseClassifications",
                request_serializer=case_service.SearchCaseClassificationsRequest.serialize,
                response_deserializer=case_service.SearchCaseClassificationsResponse.deserialize,
            )
        return self._stubs["search_case_classifications"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("CaseServiceGrpcTransport",)
