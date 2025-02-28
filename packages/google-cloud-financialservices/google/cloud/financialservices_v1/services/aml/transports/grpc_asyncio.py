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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.financialservices_v1.types import (
    backtest_result as gcf_backtest_result,
)
from google.cloud.financialservices_v1.types import engine_config as gcf_engine_config
from google.cloud.financialservices_v1.types import (
    prediction_result as gcf_prediction_result,
)
from google.cloud.financialservices_v1.types import backtest_result
from google.cloud.financialservices_v1.types import dataset
from google.cloud.financialservices_v1.types import dataset as gcf_dataset
from google.cloud.financialservices_v1.types import engine_config
from google.cloud.financialservices_v1.types import engine_version
from google.cloud.financialservices_v1.types import instance
from google.cloud.financialservices_v1.types import instance as gcf_instance
from google.cloud.financialservices_v1.types import model
from google.cloud.financialservices_v1.types import model as gcf_model
from google.cloud.financialservices_v1.types import prediction_result

from .base import DEFAULT_CLIENT_INFO, AMLTransport
from .grpc import AMLGrpcTransport

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
                    "serviceName": "google.cloud.financialservices.v1.AML",
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
                    "serviceName": "google.cloud.financialservices.v1.AML",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class AMLGrpcAsyncIOTransport(AMLTransport):
    """gRPC AsyncIO backend transport for AML.

    The AML (Anti Money Laundering) service allows users to
    perform REST operations on aml.

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
        host: str = "financialservices.googleapis.com",
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
        host: str = "financialservices.googleapis.com",
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
                 The hostname to connect to (default: 'financialservices.googleapis.com').
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
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_instances(
        self,
    ) -> Callable[
        [instance.ListInstancesRequest], Awaitable[instance.ListInstancesResponse]
    ]:
        r"""Return a callable for the list instances method over gRPC.

        Lists instances.

        Returns:
            Callable[[~.ListInstancesRequest],
                    Awaitable[~.ListInstancesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListInstances",
                request_serializer=instance.ListInstancesRequest.serialize,
                response_deserializer=instance.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self,
    ) -> Callable[[instance.GetInstanceRequest], Awaitable[instance.Instance]]:
        r"""Return a callable for the get instance method over gRPC.

        Gets an instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    Awaitable[~.Instance]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetInstance",
                request_serializer=instance.GetInstanceRequest.serialize,
                response_deserializer=instance.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self,
    ) -> Callable[
        [gcf_instance.CreateInstanceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create instance method over gRPC.

        Creates an instance.

        Returns:
            Callable[[~.CreateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreateInstance",
                request_serializer=gcf_instance.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def update_instance(
        self,
    ) -> Callable[
        [gcf_instance.UpdateInstanceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update instance method over gRPC.

        Updates the parameters of a single Instance.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance" not in self._stubs:
            self._stubs["update_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdateInstance",
                request_serializer=gcf_instance.UpdateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_instance"]

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [instance.DeleteInstanceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes an instance.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeleteInstance",
                request_serializer=instance.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def import_registered_parties(
        self,
    ) -> Callable[
        [instance.ImportRegisteredPartiesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import registered parties method over gRPC.

        Imports the list of registered parties. See `Create and manage
        instances <https://cloud.google.com/financial-services/anti-money-laundering/docs/create-and-manage-instances#import-registered-parties>`__
        for information on the input schema and response for this
        method.

        Returns:
            Callable[[~.ImportRegisteredPartiesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_registered_parties" not in self._stubs:
            self._stubs["import_registered_parties"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ImportRegisteredParties",
                request_serializer=instance.ImportRegisteredPartiesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_registered_parties"]

    @property
    def export_registered_parties(
        self,
    ) -> Callable[
        [instance.ExportRegisteredPartiesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export registered parties method over gRPC.

        Exports the list of registered parties. See `Create and manage
        instances <https://cloud.google.com/financial-services/anti-money-laundering/docs/create-and-manage-instances#export-registered-parties>`__
        for information on the output schema for this method.

        Returns:
            Callable[[~.ExportRegisteredPartiesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_registered_parties" not in self._stubs:
            self._stubs["export_registered_parties"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ExportRegisteredParties",
                request_serializer=instance.ExportRegisteredPartiesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_registered_parties"]

    @property
    def list_datasets(
        self,
    ) -> Callable[
        [dataset.ListDatasetsRequest], Awaitable[dataset.ListDatasetsResponse]
    ]:
        r"""Return a callable for the list datasets method over gRPC.

        Lists datasets.

        Returns:
            Callable[[~.ListDatasetsRequest],
                    Awaitable[~.ListDatasetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_datasets" not in self._stubs:
            self._stubs["list_datasets"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListDatasets",
                request_serializer=dataset.ListDatasetsRequest.serialize,
                response_deserializer=dataset.ListDatasetsResponse.deserialize,
            )
        return self._stubs["list_datasets"]

    @property
    def get_dataset(
        self,
    ) -> Callable[[dataset.GetDatasetRequest], Awaitable[dataset.Dataset]]:
        r"""Return a callable for the get dataset method over gRPC.

        Gets a dataset.

        Returns:
            Callable[[~.GetDatasetRequest],
                    Awaitable[~.Dataset]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_dataset" not in self._stubs:
            self._stubs["get_dataset"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetDataset",
                request_serializer=dataset.GetDatasetRequest.serialize,
                response_deserializer=dataset.Dataset.deserialize,
            )
        return self._stubs["get_dataset"]

    @property
    def create_dataset(
        self,
    ) -> Callable[
        [gcf_dataset.CreateDatasetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create dataset method over gRPC.

        Creates a dataset.

        Returns:
            Callable[[~.CreateDatasetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_dataset" not in self._stubs:
            self._stubs["create_dataset"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreateDataset",
                request_serializer=gcf_dataset.CreateDatasetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_dataset"]

    @property
    def update_dataset(
        self,
    ) -> Callable[
        [gcf_dataset.UpdateDatasetRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update dataset method over gRPC.

        Updates the parameters of a single Dataset.

        Returns:
            Callable[[~.UpdateDatasetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_dataset" not in self._stubs:
            self._stubs["update_dataset"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdateDataset",
                request_serializer=gcf_dataset.UpdateDatasetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_dataset"]

    @property
    def delete_dataset(
        self,
    ) -> Callable[[dataset.DeleteDatasetRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete dataset method over gRPC.

        Deletes a dataset.

        Returns:
            Callable[[~.DeleteDatasetRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_dataset" not in self._stubs:
            self._stubs["delete_dataset"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeleteDataset",
                request_serializer=dataset.DeleteDatasetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_dataset"]

    @property
    def list_models(
        self,
    ) -> Callable[[model.ListModelsRequest], Awaitable[model.ListModelsResponse]]:
        r"""Return a callable for the list models method over gRPC.

        Lists models.

        Returns:
            Callable[[~.ListModelsRequest],
                    Awaitable[~.ListModelsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_models" not in self._stubs:
            self._stubs["list_models"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListModels",
                request_serializer=model.ListModelsRequest.serialize,
                response_deserializer=model.ListModelsResponse.deserialize,
            )
        return self._stubs["list_models"]

    @property
    def get_model(self) -> Callable[[model.GetModelRequest], Awaitable[model.Model]]:
        r"""Return a callable for the get model method over gRPC.

        Gets a model.

        Returns:
            Callable[[~.GetModelRequest],
                    Awaitable[~.Model]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_model" not in self._stubs:
            self._stubs["get_model"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetModel",
                request_serializer=model.GetModelRequest.serialize,
                response_deserializer=model.Model.deserialize,
            )
        return self._stubs["get_model"]

    @property
    def create_model(
        self,
    ) -> Callable[[gcf_model.CreateModelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create model method over gRPC.

        Creates a model.

        Returns:
            Callable[[~.CreateModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_model" not in self._stubs:
            self._stubs["create_model"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreateModel",
                request_serializer=gcf_model.CreateModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_model"]

    @property
    def update_model(
        self,
    ) -> Callable[[gcf_model.UpdateModelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update model method over gRPC.

        Updates the parameters of a single Model.

        Returns:
            Callable[[~.UpdateModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_model" not in self._stubs:
            self._stubs["update_model"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdateModel",
                request_serializer=gcf_model.UpdateModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_model"]

    @property
    def export_model_metadata(
        self,
    ) -> Callable[
        [gcf_model.ExportModelMetadataRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export model metadata method over gRPC.

        Export governance information for a Model resource. For
        information on the exported fields, see `AML output data
        model <https://cloud.google.com/financial-services/anti-money-laundering/docs/reference/schemas/aml-output-data-model#model>`__.

        Returns:
            Callable[[~.ExportModelMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_model_metadata" not in self._stubs:
            self._stubs["export_model_metadata"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ExportModelMetadata",
                request_serializer=gcf_model.ExportModelMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_model_metadata"]

    @property
    def delete_model(
        self,
    ) -> Callable[[model.DeleteModelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete model method over gRPC.

        Deletes a model.

        Returns:
            Callable[[~.DeleteModelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_model" not in self._stubs:
            self._stubs["delete_model"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeleteModel",
                request_serializer=model.DeleteModelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_model"]

    @property
    def list_engine_configs(
        self,
    ) -> Callable[
        [engine_config.ListEngineConfigsRequest],
        Awaitable[engine_config.ListEngineConfigsResponse],
    ]:
        r"""Return a callable for the list engine configs method over gRPC.

        Lists engine configs.

        Returns:
            Callable[[~.ListEngineConfigsRequest],
                    Awaitable[~.ListEngineConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_engine_configs" not in self._stubs:
            self._stubs["list_engine_configs"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListEngineConfigs",
                request_serializer=engine_config.ListEngineConfigsRequest.serialize,
                response_deserializer=engine_config.ListEngineConfigsResponse.deserialize,
            )
        return self._stubs["list_engine_configs"]

    @property
    def get_engine_config(
        self,
    ) -> Callable[
        [engine_config.GetEngineConfigRequest], Awaitable[engine_config.EngineConfig]
    ]:
        r"""Return a callable for the get engine config method over gRPC.

        Gets an engine config.

        Returns:
            Callable[[~.GetEngineConfigRequest],
                    Awaitable[~.EngineConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_engine_config" not in self._stubs:
            self._stubs["get_engine_config"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetEngineConfig",
                request_serializer=engine_config.GetEngineConfigRequest.serialize,
                response_deserializer=engine_config.EngineConfig.deserialize,
            )
        return self._stubs["get_engine_config"]

    @property
    def create_engine_config(
        self,
    ) -> Callable[
        [gcf_engine_config.CreateEngineConfigRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create engine config method over gRPC.

        Creates an engine config.

        Returns:
            Callable[[~.CreateEngineConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_engine_config" not in self._stubs:
            self._stubs["create_engine_config"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreateEngineConfig",
                request_serializer=gcf_engine_config.CreateEngineConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_engine_config"]

    @property
    def update_engine_config(
        self,
    ) -> Callable[
        [gcf_engine_config.UpdateEngineConfigRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update engine config method over gRPC.

        Updates the parameters of a single EngineConfig.

        Returns:
            Callable[[~.UpdateEngineConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_engine_config" not in self._stubs:
            self._stubs["update_engine_config"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdateEngineConfig",
                request_serializer=gcf_engine_config.UpdateEngineConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_engine_config"]

    @property
    def export_engine_config_metadata(
        self,
    ) -> Callable[
        [gcf_engine_config.ExportEngineConfigMetadataRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the export engine config metadata method over gRPC.

        Export governance information for an EngineConfig resource. For
        information on the exported fields, see `AML output data
        model <https://cloud.google.com/financial-services/anti-money-laundering/docs/reference/schemas/aml-output-data-model#engine-config>`__.

        Returns:
            Callable[[~.ExportEngineConfigMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_engine_config_metadata" not in self._stubs:
            self._stubs[
                "export_engine_config_metadata"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ExportEngineConfigMetadata",
                request_serializer=gcf_engine_config.ExportEngineConfigMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_engine_config_metadata"]

    @property
    def delete_engine_config(
        self,
    ) -> Callable[
        [engine_config.DeleteEngineConfigRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete engine config method over gRPC.

        Deletes an engine config.

        Returns:
            Callable[[~.DeleteEngineConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_engine_config" not in self._stubs:
            self._stubs["delete_engine_config"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeleteEngineConfig",
                request_serializer=engine_config.DeleteEngineConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_engine_config"]

    @property
    def get_engine_version(
        self,
    ) -> Callable[
        [engine_version.GetEngineVersionRequest],
        Awaitable[engine_version.EngineVersion],
    ]:
        r"""Return a callable for the get engine version method over gRPC.

        Gets a single EngineVersion.

        Returns:
            Callable[[~.GetEngineVersionRequest],
                    Awaitable[~.EngineVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_engine_version" not in self._stubs:
            self._stubs["get_engine_version"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetEngineVersion",
                request_serializer=engine_version.GetEngineVersionRequest.serialize,
                response_deserializer=engine_version.EngineVersion.deserialize,
            )
        return self._stubs["get_engine_version"]

    @property
    def list_engine_versions(
        self,
    ) -> Callable[
        [engine_version.ListEngineVersionsRequest],
        Awaitable[engine_version.ListEngineVersionsResponse],
    ]:
        r"""Return a callable for the list engine versions method over gRPC.

        Lists EngineVersions for given location.

        Returns:
            Callable[[~.ListEngineVersionsRequest],
                    Awaitable[~.ListEngineVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_engine_versions" not in self._stubs:
            self._stubs["list_engine_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListEngineVersions",
                request_serializer=engine_version.ListEngineVersionsRequest.serialize,
                response_deserializer=engine_version.ListEngineVersionsResponse.deserialize,
            )
        return self._stubs["list_engine_versions"]

    @property
    def list_prediction_results(
        self,
    ) -> Callable[
        [prediction_result.ListPredictionResultsRequest],
        Awaitable[prediction_result.ListPredictionResultsResponse],
    ]:
        r"""Return a callable for the list prediction results method over gRPC.

        List PredictionResults.

        Returns:
            Callable[[~.ListPredictionResultsRequest],
                    Awaitable[~.ListPredictionResultsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_prediction_results" not in self._stubs:
            self._stubs["list_prediction_results"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListPredictionResults",
                request_serializer=prediction_result.ListPredictionResultsRequest.serialize,
                response_deserializer=prediction_result.ListPredictionResultsResponse.deserialize,
            )
        return self._stubs["list_prediction_results"]

    @property
    def get_prediction_result(
        self,
    ) -> Callable[
        [prediction_result.GetPredictionResultRequest],
        Awaitable[prediction_result.PredictionResult],
    ]:
        r"""Return a callable for the get prediction result method over gRPC.

        Gets a PredictionResult.

        Returns:
            Callable[[~.GetPredictionResultRequest],
                    Awaitable[~.PredictionResult]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_prediction_result" not in self._stubs:
            self._stubs["get_prediction_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetPredictionResult",
                request_serializer=prediction_result.GetPredictionResultRequest.serialize,
                response_deserializer=prediction_result.PredictionResult.deserialize,
            )
        return self._stubs["get_prediction_result"]

    @property
    def create_prediction_result(
        self,
    ) -> Callable[
        [gcf_prediction_result.CreatePredictionResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create prediction result method over gRPC.

        Create a PredictionResult.

        Returns:
            Callable[[~.CreatePredictionResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_prediction_result" not in self._stubs:
            self._stubs["create_prediction_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreatePredictionResult",
                request_serializer=gcf_prediction_result.CreatePredictionResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_prediction_result"]

    @property
    def update_prediction_result(
        self,
    ) -> Callable[
        [gcf_prediction_result.UpdatePredictionResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update prediction result method over gRPC.

        Updates the parameters of a single PredictionResult.

        Returns:
            Callable[[~.UpdatePredictionResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_prediction_result" not in self._stubs:
            self._stubs["update_prediction_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdatePredictionResult",
                request_serializer=gcf_prediction_result.UpdatePredictionResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_prediction_result"]

    @property
    def export_prediction_result_metadata(
        self,
    ) -> Callable[
        [gcf_prediction_result.ExportPredictionResultMetadataRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the export prediction result
        metadata method over gRPC.

        Export governance information for a PredictionResult resource.
        For information on the exported fields, see `AML output data
        model <https://cloud.google.com/financial-services/anti-money-laundering/docs/reference/schemas/aml-output-data-model#prediction-results>`__.

        Returns:
            Callable[[~.ExportPredictionResultMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_prediction_result_metadata" not in self._stubs:
            self._stubs[
                "export_prediction_result_metadata"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ExportPredictionResultMetadata",
                request_serializer=gcf_prediction_result.ExportPredictionResultMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_prediction_result_metadata"]

    @property
    def delete_prediction_result(
        self,
    ) -> Callable[
        [prediction_result.DeletePredictionResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete prediction result method over gRPC.

        Deletes a PredictionResult.

        Returns:
            Callable[[~.DeletePredictionResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_prediction_result" not in self._stubs:
            self._stubs["delete_prediction_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeletePredictionResult",
                request_serializer=prediction_result.DeletePredictionResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_prediction_result"]

    @property
    def list_backtest_results(
        self,
    ) -> Callable[
        [backtest_result.ListBacktestResultsRequest],
        Awaitable[backtest_result.ListBacktestResultsResponse],
    ]:
        r"""Return a callable for the list backtest results method over gRPC.

        List BacktestResults.

        Returns:
            Callable[[~.ListBacktestResultsRequest],
                    Awaitable[~.ListBacktestResultsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backtest_results" not in self._stubs:
            self._stubs["list_backtest_results"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ListBacktestResults",
                request_serializer=backtest_result.ListBacktestResultsRequest.serialize,
                response_deserializer=backtest_result.ListBacktestResultsResponse.deserialize,
            )
        return self._stubs["list_backtest_results"]

    @property
    def get_backtest_result(
        self,
    ) -> Callable[
        [backtest_result.GetBacktestResultRequest],
        Awaitable[backtest_result.BacktestResult],
    ]:
        r"""Return a callable for the get backtest result method over gRPC.

        Gets a BacktestResult.

        Returns:
            Callable[[~.GetBacktestResultRequest],
                    Awaitable[~.BacktestResult]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backtest_result" not in self._stubs:
            self._stubs["get_backtest_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/GetBacktestResult",
                request_serializer=backtest_result.GetBacktestResultRequest.serialize,
                response_deserializer=backtest_result.BacktestResult.deserialize,
            )
        return self._stubs["get_backtest_result"]

    @property
    def create_backtest_result(
        self,
    ) -> Callable[
        [gcf_backtest_result.CreateBacktestResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create backtest result method over gRPC.

        Create a BacktestResult.

        Returns:
            Callable[[~.CreateBacktestResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backtest_result" not in self._stubs:
            self._stubs["create_backtest_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/CreateBacktestResult",
                request_serializer=gcf_backtest_result.CreateBacktestResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backtest_result"]

    @property
    def update_backtest_result(
        self,
    ) -> Callable[
        [gcf_backtest_result.UpdateBacktestResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update backtest result method over gRPC.

        Updates the parameters of a single BacktestResult.

        Returns:
            Callable[[~.UpdateBacktestResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backtest_result" not in self._stubs:
            self._stubs["update_backtest_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/UpdateBacktestResult",
                request_serializer=gcf_backtest_result.UpdateBacktestResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backtest_result"]

    @property
    def export_backtest_result_metadata(
        self,
    ) -> Callable[
        [gcf_backtest_result.ExportBacktestResultMetadataRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the export backtest result
        metadata method over gRPC.

        Export governance information for a BacktestResult resource. For
        information on the exported fields, see `AML output data
        model <https://cloud.google.com/financial-services/anti-money-laundering/docs/reference/schemas/aml-output-data-model#backtest-results>`__.

        Returns:
            Callable[[~.ExportBacktestResultMetadataRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_backtest_result_metadata" not in self._stubs:
            self._stubs[
                "export_backtest_result_metadata"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/ExportBacktestResultMetadata",
                request_serializer=gcf_backtest_result.ExportBacktestResultMetadataRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_backtest_result_metadata"]

    @property
    def delete_backtest_result(
        self,
    ) -> Callable[
        [backtest_result.DeleteBacktestResultRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete backtest result method over gRPC.

        Deletes a BacktestResult.

        Returns:
            Callable[[~.DeleteBacktestResultRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backtest_result" not in self._stubs:
            self._stubs["delete_backtest_result"] = self._logged_channel.unary_unary(
                "/google.cloud.financialservices.v1.AML/DeleteBacktestResult",
                request_serializer=backtest_result.DeleteBacktestResultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backtest_result"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_instances: self._wrap_method(
                self.list_instances,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_instance: self._wrap_method(
                self.get_instance,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_instance: self._wrap_method(
                self.create_instance,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_instance: self._wrap_method(
                self.update_instance,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_instance: self._wrap_method(
                self.delete_instance,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.import_registered_parties: self._wrap_method(
                self.import_registered_parties,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.export_registered_parties: self._wrap_method(
                self.export_registered_parties,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_datasets: self._wrap_method(
                self.list_datasets,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_dataset: self._wrap_method(
                self.get_dataset,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_dataset: self._wrap_method(
                self.create_dataset,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_dataset: self._wrap_method(
                self.update_dataset,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_dataset: self._wrap_method(
                self.delete_dataset,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_models: self._wrap_method(
                self.list_models,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_model: self._wrap_method(
                self.get_model,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_model: self._wrap_method(
                self.create_model,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_model: self._wrap_method(
                self.update_model,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.export_model_metadata: self._wrap_method(
                self.export_model_metadata,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_model: self._wrap_method(
                self.delete_model,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_engine_configs: self._wrap_method(
                self.list_engine_configs,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_engine_config: self._wrap_method(
                self.get_engine_config,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_engine_config: self._wrap_method(
                self.create_engine_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_engine_config: self._wrap_method(
                self.update_engine_config,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.export_engine_config_metadata: self._wrap_method(
                self.export_engine_config_metadata,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_engine_config: self._wrap_method(
                self.delete_engine_config,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.get_engine_version: self._wrap_method(
                self.get_engine_version,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.list_engine_versions: self._wrap_method(
                self.list_engine_versions,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.list_prediction_results: self._wrap_method(
                self.list_prediction_results,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_prediction_result: self._wrap_method(
                self.get_prediction_result,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_prediction_result: self._wrap_method(
                self.create_prediction_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_prediction_result: self._wrap_method(
                self.update_prediction_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.export_prediction_result_metadata: self._wrap_method(
                self.export_prediction_result_metadata,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_prediction_result: self._wrap_method(
                self.delete_prediction_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_backtest_results: self._wrap_method(
                self.list_backtest_results,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_backtest_result: self._wrap_method(
                self.get_backtest_result,
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_backtest_result: self._wrap_method(
                self.create_backtest_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_backtest_result: self._wrap_method(
                self.update_backtest_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.export_backtest_result_metadata: self._wrap_method(
                self.export_backtest_result_metadata,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_backtest_result: self._wrap_method(
                self.delete_backtest_result,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
                default_timeout=None,
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

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("AMLGrpcAsyncIOTransport",)
