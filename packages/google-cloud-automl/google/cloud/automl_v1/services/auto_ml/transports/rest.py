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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.automl_v1.types import annotation_spec
from google.cloud.automl_v1.types import dataset
from google.cloud.automl_v1.types import dataset as gca_dataset
from google.cloud.automl_v1.types import model
from google.cloud.automl_v1.types import model as gca_model
from google.cloud.automl_v1.types import model_evaluation, service

from .base import AutoMlTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AutoMlRestInterceptor:
    """Interceptor for AutoMl.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AutoMlRestTransport.

    .. code-block:: python
        class MyCustomAutoMlInterceptor(AutoMlRestInterceptor):
            def pre_create_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_deploy_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_deploy_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_data(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_data(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_annotation_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_annotation_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model_evaluation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model_evaluation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_data(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_data(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_datasets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_datasets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_model_evaluations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_model_evaluations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_models(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_models(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undeploy_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undeploy_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_model(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AutoMlRestTransport(interceptor=MyCustomAutoMlInterceptor())
        client = AutoMlClient(transport=transport)


    """

    def pre_create_dataset(
        self, request: service.CreateDatasetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_create_dataset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_dataset

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_create_model(
        self, request: service.CreateModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_create_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_delete_dataset(
        self, request: service.DeleteDatasetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_delete_dataset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_dataset

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_delete_model(
        self, request: service.DeleteModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_delete_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_deploy_model(
        self, request: service.DeployModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeployModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for deploy_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_deploy_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for deploy_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_export_data(
        self, request: service.ExportDataRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ExportDataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_data

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_export_data(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_data

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_export_model(
        self, request: service.ExportModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ExportModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_export_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_get_annotation_spec(
        self,
        request: service.GetAnnotationSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetAnnotationSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_annotation_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_get_annotation_spec(
        self, response: annotation_spec.AnnotationSpec
    ) -> annotation_spec.AnnotationSpec:
        """Post-rpc interceptor for get_annotation_spec

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_get_dataset(
        self, request: service.GetDatasetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_get_dataset(self, response: dataset.Dataset) -> dataset.Dataset:
        """Post-rpc interceptor for get_dataset

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_get_model(
        self, request: service.GetModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_get_model(self, response: model.Model) -> model.Model:
        """Post-rpc interceptor for get_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_get_model_evaluation(
        self,
        request: service.GetModelEvaluationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetModelEvaluationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model_evaluation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_get_model_evaluation(
        self, response: model_evaluation.ModelEvaluation
    ) -> model_evaluation.ModelEvaluation:
        """Post-rpc interceptor for get_model_evaluation

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_import_data(
        self, request: service.ImportDataRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ImportDataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_data

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_import_data(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_data

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_list_datasets(
        self, request: service.ListDatasetsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListDatasetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_datasets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_list_datasets(
        self, response: service.ListDatasetsResponse
    ) -> service.ListDatasetsResponse:
        """Post-rpc interceptor for list_datasets

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_list_model_evaluations(
        self,
        request: service.ListModelEvaluationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListModelEvaluationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_model_evaluations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_list_model_evaluations(
        self, response: service.ListModelEvaluationsResponse
    ) -> service.ListModelEvaluationsResponse:
        """Post-rpc interceptor for list_model_evaluations

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_list_models(
        self, request: service.ListModelsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListModelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_models

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_list_models(
        self, response: service.ListModelsResponse
    ) -> service.ListModelsResponse:
        """Post-rpc interceptor for list_models

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_undeploy_model(
        self, request: service.UndeployModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UndeployModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undeploy_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_undeploy_model(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undeploy_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_update_dataset(
        self, request: service.UpdateDatasetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_update_dataset(self, response: gca_dataset.Dataset) -> gca_dataset.Dataset:
        """Post-rpc interceptor for update_dataset

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response

    def pre_update_model(
        self, request: service.UpdateModelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AutoMl server.
        """
        return request, metadata

    def post_update_model(self, response: gca_model.Model) -> gca_model.Model:
        """Post-rpc interceptor for update_model

        Override in a subclass to manipulate the response
        after it is returned by the AutoMl server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AutoMlRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AutoMlRestInterceptor


class AutoMlRestTransport(AutoMlTransport):
    """REST backend transport for AutoMl.

    AutoML Server API.

    The resource names are assigned by the server. The server never
    reuses names that it has created after the resources with those
    names are deleted.

    An ID of a resource is the last element of the item's resource name.
    For
    ``projects/{project_id}/locations/{location_id}/datasets/{dataset_id}``,
    then the id for the item is ``{dataset_id}``.

    Currently the only supported ``location_id`` is "us-central1".

    On any input that is documented to expect a string parameter in
    snake_case or dash-case, either of those cases is accepted.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "automl.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AutoMlRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'automl.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or AutoMlRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
                "google.longrunning.Operations.WaitOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:wait",
                        "body": "*",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateDataset(AutoMlRestStub):
        def __hash__(self):
            return hash("CreateDataset")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.CreateDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create dataset method over HTTP.

            Args:
                request (~.service.CreateDatasetRequest):
                    The request object. Request message for
                [AutoMl.CreateDataset][google.cloud.automl.v1.AutoMl.CreateDataset].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/datasets",
                    "body": "dataset",
                },
            ]
            request, metadata = self._interceptor.pre_create_dataset(request, metadata)
            pb_request = service.CreateDatasetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_dataset(resp)
            return resp

    class _CreateModel(AutoMlRestStub):
        def __hash__(self):
            return hash("CreateModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.CreateModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create model method over HTTP.

            Args:
                request (~.service.CreateModelRequest):
                    The request object. Request message for
                [AutoMl.CreateModel][google.cloud.automl.v1.AutoMl.CreateModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/models",
                    "body": "model",
                },
            ]
            request, metadata = self._interceptor.pre_create_model(request, metadata)
            pb_request = service.CreateModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_model(resp)
            return resp

    class _DeleteDataset(AutoMlRestStub):
        def __hash__(self):
            return hash("DeleteDataset")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.DeleteDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete dataset method over HTTP.

            Args:
                request (~.service.DeleteDatasetRequest):
                    The request object. Request message for
                [AutoMl.DeleteDataset][google.cloud.automl.v1.AutoMl.DeleteDataset].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_dataset(request, metadata)
            pb_request = service.DeleteDatasetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_dataset(resp)
            return resp

    class _DeleteModel(AutoMlRestStub):
        def __hash__(self):
            return hash("DeleteModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.DeleteModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete model method over HTTP.

            Args:
                request (~.service.DeleteModelRequest):
                    The request object. Request message for
                [AutoMl.DeleteModel][google.cloud.automl.v1.AutoMl.DeleteModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/models/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_model(request, metadata)
            pb_request = service.DeleteModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_model(resp)
            return resp

    class _DeployModel(AutoMlRestStub):
        def __hash__(self):
            return hash("DeployModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.DeployModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the deploy model method over HTTP.

            Args:
                request (~.service.DeployModelRequest):
                    The request object. Request message for
                [AutoMl.DeployModel][google.cloud.automl.v1.AutoMl.DeployModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/models/*}:deploy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_deploy_model(request, metadata)
            pb_request = service.DeployModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_deploy_model(resp)
            return resp

    class _ExportData(AutoMlRestStub):
        def __hash__(self):
            return hash("ExportData")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ExportDataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export data method over HTTP.

            Args:
                request (~.service.ExportDataRequest):
                    The request object. Request message for
                [AutoMl.ExportData][google.cloud.automl.v1.AutoMl.ExportData].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/datasets/*}:exportData",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_export_data(request, metadata)
            pb_request = service.ExportDataRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_data(resp)
            return resp

    class _ExportModel(AutoMlRestStub):
        def __hash__(self):
            return hash("ExportModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ExportModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export model method over HTTP.

            Args:
                request (~.service.ExportModelRequest):
                    The request object. Request message for
                [AutoMl.ExportModel][google.cloud.automl.v1.AutoMl.ExportModel].
                Models need to be enabled for exporting, otherwise an
                error code will be returned.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/models/*}:export",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_export_model(request, metadata)
            pb_request = service.ExportModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_model(resp)
            return resp

    class _GetAnnotationSpec(AutoMlRestStub):
        def __hash__(self):
            return hash("GetAnnotationSpec")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetAnnotationSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> annotation_spec.AnnotationSpec:
            r"""Call the get annotation spec method over HTTP.

            Args:
                request (~.service.GetAnnotationSpecRequest):
                    The request object. Request message for
                [AutoMl.GetAnnotationSpec][google.cloud.automl.v1.AutoMl.GetAnnotationSpec].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.annotation_spec.AnnotationSpec:
                    A definition of an annotation spec.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_annotation_spec(
                request, metadata
            )
            pb_request = service.GetAnnotationSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = annotation_spec.AnnotationSpec()
            pb_resp = annotation_spec.AnnotationSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_annotation_spec(resp)
            return resp

    class _GetDataset(AutoMlRestStub):
        def __hash__(self):
            return hash("GetDataset")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataset.Dataset:
            r"""Call the get dataset method over HTTP.

            Args:
                request (~.service.GetDatasetRequest):
                    The request object. Request message for
                [AutoMl.GetDataset][google.cloud.automl.v1.AutoMl.GetDataset].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataset.Dataset:
                    A workspace for solving a single,
                particular machine learning (ML)
                problem. A workspace contains examples
                that may be annotated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/datasets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_dataset(request, metadata)
            pb_request = service.GetDatasetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataset.Dataset()
            pb_resp = dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_dataset(resp)
            return resp

    class _GetModel(AutoMlRestStub):
        def __hash__(self):
            return hash("GetModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> model.Model:
            r"""Call the get model method over HTTP.

            Args:
                request (~.service.GetModelRequest):
                    The request object. Request message for
                [AutoMl.GetModel][google.cloud.automl.v1.AutoMl.GetModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model.Model:
                    API proto representing a trained
                machine learning model.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/models/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_model(request, metadata)
            pb_request = service.GetModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model.Model()
            pb_resp = model.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model(resp)
            return resp

    class _GetModelEvaluation(AutoMlRestStub):
        def __hash__(self):
            return hash("GetModelEvaluation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.GetModelEvaluationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> model_evaluation.ModelEvaluation:
            r"""Call the get model evaluation method over HTTP.

            Args:
                request (~.service.GetModelEvaluationRequest):
                    The request object. Request message for
                [AutoMl.GetModelEvaluation][google.cloud.automl.v1.AutoMl.GetModelEvaluation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_evaluation.ModelEvaluation:
                    Evaluation results of a model.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/models/*/modelEvaluations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_model_evaluation(
                request, metadata
            )
            pb_request = service.GetModelEvaluationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_evaluation.ModelEvaluation()
            pb_resp = model_evaluation.ModelEvaluation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model_evaluation(resp)
            return resp

    class _ImportData(AutoMlRestStub):
        def __hash__(self):
            return hash("ImportData")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ImportDataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import data method over HTTP.

            Args:
                request (~.service.ImportDataRequest):
                    The request object. Request message for
                [AutoMl.ImportData][google.cloud.automl.v1.AutoMl.ImportData].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/datasets/*}:importData",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_data(request, metadata)
            pb_request = service.ImportDataRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_data(resp)
            return resp

    class _ListDatasets(AutoMlRestStub):
        def __hash__(self):
            return hash("ListDatasets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ListDatasetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListDatasetsResponse:
            r"""Call the list datasets method over HTTP.

            Args:
                request (~.service.ListDatasetsRequest):
                    The request object. Request message for
                [AutoMl.ListDatasets][google.cloud.automl.v1.AutoMl.ListDatasets].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListDatasetsResponse:
                    Response message for
                [AutoMl.ListDatasets][google.cloud.automl.v1.AutoMl.ListDatasets].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/datasets",
                },
            ]
            request, metadata = self._interceptor.pre_list_datasets(request, metadata)
            pb_request = service.ListDatasetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListDatasetsResponse()
            pb_resp = service.ListDatasetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_datasets(resp)
            return resp

    class _ListModelEvaluations(AutoMlRestStub):
        def __hash__(self):
            return hash("ListModelEvaluations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "filter": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ListModelEvaluationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListModelEvaluationsResponse:
            r"""Call the list model evaluations method over HTTP.

            Args:
                request (~.service.ListModelEvaluationsRequest):
                    The request object. Request message for
                [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListModelEvaluationsResponse:
                    Response message for
                [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/models/*}/modelEvaluations",
                },
            ]
            request, metadata = self._interceptor.pre_list_model_evaluations(
                request, metadata
            )
            pb_request = service.ListModelEvaluationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListModelEvaluationsResponse()
            pb_resp = service.ListModelEvaluationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_model_evaluations(resp)
            return resp

    class _ListModels(AutoMlRestStub):
        def __hash__(self):
            return hash("ListModels")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.ListModelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListModelsResponse:
            r"""Call the list models method over HTTP.

            Args:
                request (~.service.ListModelsRequest):
                    The request object. Request message for
                [AutoMl.ListModels][google.cloud.automl.v1.AutoMl.ListModels].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListModelsResponse:
                    Response message for
                [AutoMl.ListModels][google.cloud.automl.v1.AutoMl.ListModels].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/models",
                },
            ]
            request, metadata = self._interceptor.pre_list_models(request, metadata)
            pb_request = service.ListModelsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListModelsResponse()
            pb_resp = service.ListModelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_models(resp)
            return resp

    class _UndeployModel(AutoMlRestStub):
        def __hash__(self):
            return hash("UndeployModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.UndeployModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undeploy model method over HTTP.

            Args:
                request (~.service.UndeployModelRequest):
                    The request object. Request message for
                [AutoMl.UndeployModel][google.cloud.automl.v1.AutoMl.UndeployModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/models/*}:undeploy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undeploy_model(request, metadata)
            pb_request = service.UndeployModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undeploy_model(resp)
            return resp

    class _UpdateDataset(AutoMlRestStub):
        def __hash__(self):
            return hash("UpdateDataset")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.UpdateDatasetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gca_dataset.Dataset:
            r"""Call the update dataset method over HTTP.

            Args:
                request (~.service.UpdateDatasetRequest):
                    The request object. Request message for
                [AutoMl.UpdateDataset][google.cloud.automl.v1.AutoMl.UpdateDataset]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gca_dataset.Dataset:
                    A workspace for solving a single,
                particular machine learning (ML)
                problem. A workspace contains examples
                that may be annotated.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{dataset.name=projects/*/locations/*/datasets/*}",
                    "body": "dataset",
                },
            ]
            request, metadata = self._interceptor.pre_update_dataset(request, metadata)
            pb_request = service.UpdateDatasetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gca_dataset.Dataset()
            pb_resp = gca_dataset.Dataset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_dataset(resp)
            return resp

    class _UpdateModel(AutoMlRestStub):
        def __hash__(self):
            return hash("UpdateModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: service.UpdateModelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gca_model.Model:
            r"""Call the update model method over HTTP.

            Args:
                request (~.service.UpdateModelRequest):
                    The request object. Request message for
                [AutoMl.UpdateModel][google.cloud.automl.v1.AutoMl.UpdateModel]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gca_model.Model:
                    API proto representing a trained
                machine learning model.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{model.name=projects/*/locations/*/models/*}",
                    "body": "model",
                },
            ]
            request, metadata = self._interceptor.pre_update_model(request, metadata)
            pb_request = service.UpdateModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gca_model.Model()
            pb_resp = gca_model.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_model(resp)
            return resp

    @property
    def create_dataset(
        self,
    ) -> Callable[[service.CreateDatasetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_model(
        self,
    ) -> Callable[[service.CreateModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_dataset(
        self,
    ) -> Callable[[service.DeleteDatasetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_model(
        self,
    ) -> Callable[[service.DeleteModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def deploy_model(
        self,
    ) -> Callable[[service.DeployModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeployModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_data(
        self,
    ) -> Callable[[service.ExportDataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportData(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_model(
        self,
    ) -> Callable[[service.ExportModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_annotation_spec(
        self,
    ) -> Callable[[service.GetAnnotationSpecRequest], annotation_spec.AnnotationSpec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnnotationSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_dataset(self) -> Callable[[service.GetDatasetRequest], dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_model(self) -> Callable[[service.GetModelRequest], model.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_model_evaluation(
        self,
    ) -> Callable[
        [service.GetModelEvaluationRequest], model_evaluation.ModelEvaluation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModelEvaluation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_data(
        self,
    ) -> Callable[[service.ImportDataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportData(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_datasets(
        self,
    ) -> Callable[[service.ListDatasetsRequest], service.ListDatasetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatasets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_model_evaluations(
        self,
    ) -> Callable[
        [service.ListModelEvaluationsRequest], service.ListModelEvaluationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModelEvaluations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_models(
        self,
    ) -> Callable[[service.ListModelsRequest], service.ListModelsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undeploy_model(
        self,
    ) -> Callable[[service.UndeployModelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeployModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_dataset(
        self,
    ) -> Callable[[service.UpdateDatasetRequest], gca_dataset.Dataset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_model(self) -> Callable[[service.UpdateModelRequest], gca_model.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateModel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AutoMlRestTransport",)
