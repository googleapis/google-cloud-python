# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.support_v2.types import case
from google.cloud.support_v2.types import case as gcs_case
from google.cloud.support_v2.types import case_service

from .base import DEFAULT_CLIENT_INFO, CaseServiceTransport
from .grpc import CaseServiceGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.support.v2.CaseService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.support.v2.CaseService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class CaseServiceGrpcAsyncIOTransport(CaseServiceTransport):
    """gRPC AsyncIO backend transport for CaseService.

    A service to manage Google Cloud support cases.

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
        host: str = "cloudsupport.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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
        host: str = "cloudsupport.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
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

        if isinstance(channel, aio.Channel):
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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
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
    def get_case(self) -> Callable[[case_service.GetCaseRequest], Awaitable[case.Case]]:
        r"""Return a callable for the get case method over gRPC.

        Retrieve a case.

        Returns:
            Callable[[~.GetCaseRequest],
                    Awaitable[~.Case]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_case" not in self._stubs:
            self._stubs["get_case"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/GetCase",
                request_serializer=case_service.GetCaseRequest.serialize,
                response_deserializer=case.Case.deserialize,
            )
        return self._stubs["get_case"]

    @property
    def list_cases(
        self,
    ) -> Callable[
        [case_service.ListCasesRequest], Awaitable[case_service.ListCasesResponse]
    ]:
        r"""Return a callable for the list cases method over gRPC.

        Retrieve all cases under a parent, but not its children.

        For example, listing cases under an organization only returns
        the cases that are directly parented by that organization. To
        retrieve cases under an organization and its projects, use
        ``cases.search``.

        Returns:
            Callable[[~.ListCasesRequest],
                    Awaitable[~.ListCasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cases" not in self._stubs:
            self._stubs["list_cases"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/ListCases",
                request_serializer=case_service.ListCasesRequest.serialize,
                response_deserializer=case_service.ListCasesResponse.deserialize,
            )
        return self._stubs["list_cases"]

    @property
    def search_cases(
        self,
    ) -> Callable[
        [case_service.SearchCasesRequest], Awaitable[case_service.SearchCasesResponse]
    ]:
        r"""Return a callable for the search cases method over gRPC.

        Search for cases using a query.

        Returns:
            Callable[[~.SearchCasesRequest],
                    Awaitable[~.SearchCasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_cases" not in self._stubs:
            self._stubs["search_cases"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/SearchCases",
                request_serializer=case_service.SearchCasesRequest.serialize,
                response_deserializer=case_service.SearchCasesResponse.deserialize,
            )
        return self._stubs["search_cases"]

    @property
    def create_case(
        self,
    ) -> Callable[[case_service.CreateCaseRequest], Awaitable[gcs_case.Case]]:
        r"""Return a callable for the create case method over gRPC.

        Create a new case and associate it with a parent.

        It must have the following fields set: ``display_name``,
        ``description``, ``classification``, and ``priority``. If you're
        just testing the API and don't want to route your case to an
        agent, set ``testCase=true``.

        Returns:
            Callable[[~.CreateCaseRequest],
                    Awaitable[~.Case]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_case" not in self._stubs:
            self._stubs["create_case"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/CreateCase",
                request_serializer=case_service.CreateCaseRequest.serialize,
                response_deserializer=gcs_case.Case.deserialize,
            )
        return self._stubs["create_case"]

    @property
    def update_case(
        self,
    ) -> Callable[[case_service.UpdateCaseRequest], Awaitable[gcs_case.Case]]:
        r"""Return a callable for the update case method over gRPC.

        Update a case. Only some fields can be updated.

        Returns:
            Callable[[~.UpdateCaseRequest],
                    Awaitable[~.Case]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_case" not in self._stubs:
            self._stubs["update_case"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/UpdateCase",
                request_serializer=case_service.UpdateCaseRequest.serialize,
                response_deserializer=gcs_case.Case.deserialize,
            )
        return self._stubs["update_case"]

    @property
    def escalate_case(
        self,
    ) -> Callable[[case_service.EscalateCaseRequest], Awaitable[case.Case]]:
        r"""Return a callable for the escalate case method over gRPC.

        Escalate a case, starting the Google Cloud Support
        escalation management process.

        This operation is only available for some support
        services. Go to https://cloud.google.com/support and
        look for 'Technical support escalations' in the feature
        list to find out which ones let you do that.

        Returns:
            Callable[[~.EscalateCaseRequest],
                    Awaitable[~.Case]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "escalate_case" not in self._stubs:
            self._stubs["escalate_case"] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/EscalateCase",
                request_serializer=case_service.EscalateCaseRequest.serialize,
                response_deserializer=case.Case.deserialize,
            )
        return self._stubs["escalate_case"]

    @property
    def close_case(
        self,
    ) -> Callable[[case_service.CloseCaseRequest], Awaitable[case.Case]]:
        r"""Return a callable for the close case method over gRPC.

        Close a case.

        Returns:
            Callable[[~.CloseCaseRequest],
                    Awaitable[~.Case]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "close_case" not in self._stubs:
            self._stubs["close_case"] = self._logged_channel.unary_unary(
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
        Awaitable[case_service.SearchCaseClassificationsResponse],
    ]:
        r"""Return a callable for the search case classifications method over gRPC.

        Retrieve valid classifications to use when creating a support
        case.

        Classifications are hierarchical. Each classification is a
        string containing all levels of the hierarchy separated by
        ``" > "``. For example,
        ``"Technical Issue > Compute > Compute Engine"``.

        Classification IDs returned by this endpoint are valid for at
        least six months. When a classification is deactivated, this
        endpoint immediately stops returning it. After six months,
        ``case.create`` requests using the classification will fail.

        Returns:
            Callable[[~.SearchCaseClassificationsRequest],
                    Awaitable[~.SearchCaseClassificationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_case_classifications" not in self._stubs:
            self._stubs[
                "search_case_classifications"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.support.v2.CaseService/SearchCaseClassifications",
                request_serializer=case_service.SearchCaseClassificationsRequest.serialize,
                response_deserializer=case_service.SearchCaseClassificationsResponse.deserialize,
            )
        return self._stubs["search_case_classifications"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.get_case: self._wrap_method(
                self.get_case,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_cases: self._wrap_method(
                self.list_cases,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_cases: self._wrap_method(
                self.search_cases,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_case: self._wrap_method(
                self.create_case,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_case: self._wrap_method(
                self.update_case,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.escalate_case: self._wrap_method(
                self.escalate_case,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.close_case: self._wrap_method(
                self.close_case,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_case_classifications: self._wrap_method(
                self.search_case_classifications,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("CaseServiceGrpcAsyncIOTransport",)
