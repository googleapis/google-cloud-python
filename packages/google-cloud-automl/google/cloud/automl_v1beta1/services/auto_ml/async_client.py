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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.automl_v1beta1.services.auto_ml import pagers
from google.cloud.automl_v1beta1.types import annotation_spec
from google.cloud.automl_v1beta1.types import classification
from google.cloud.automl_v1beta1.types import column_spec
from google.cloud.automl_v1beta1.types import column_spec as gca_column_spec
from google.cloud.automl_v1beta1.types import data_stats
from google.cloud.automl_v1beta1.types import data_types
from google.cloud.automl_v1beta1.types import dataset
from google.cloud.automl_v1beta1.types import dataset as gca_dataset
from google.cloud.automl_v1beta1.types import detection
from google.cloud.automl_v1beta1.types import image
from google.cloud.automl_v1beta1.types import io
from google.cloud.automl_v1beta1.types import model
from google.cloud.automl_v1beta1.types import model as gca_model
from google.cloud.automl_v1beta1.types import model_evaluation
from google.cloud.automl_v1beta1.types import operations
from google.cloud.automl_v1beta1.types import regression
from google.cloud.automl_v1beta1.types import service
from google.cloud.automl_v1beta1.types import table_spec
from google.cloud.automl_v1beta1.types import table_spec as gca_table_spec
from google.cloud.automl_v1beta1.types import tables
from google.cloud.automl_v1beta1.types import text
from google.cloud.automl_v1beta1.types import text_extraction
from google.cloud.automl_v1beta1.types import text_sentiment
from google.cloud.automl_v1beta1.types import translation
from google.cloud.automl_v1beta1.types import video
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import AutoMlTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AutoMlGrpcAsyncIOTransport
from .client import AutoMlClient


class AutoMlAsyncClient:
    """AutoML Server API.

    The resource names are assigned by the server. The server never
    reuses names that it has created after the resources with those
    names are deleted.

    An ID of a resource is the last element of the item's resource name.
    For
    ``projects/{project_id}/locations/{location_id}/datasets/{dataset_id}``,
    then the id for the item is ``{dataset_id}``.

    Currently the only supported ``location_id`` is "us-central1".

    On any input that is documented to expect a string parameter in
    snake_case or kebab-case, either of those cases is accepted.
    """

    _client: AutoMlClient

    DEFAULT_ENDPOINT = AutoMlClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AutoMlClient.DEFAULT_MTLS_ENDPOINT

    annotation_spec_path = staticmethod(AutoMlClient.annotation_spec_path)
    parse_annotation_spec_path = staticmethod(AutoMlClient.parse_annotation_spec_path)
    column_spec_path = staticmethod(AutoMlClient.column_spec_path)
    parse_column_spec_path = staticmethod(AutoMlClient.parse_column_spec_path)
    dataset_path = staticmethod(AutoMlClient.dataset_path)
    parse_dataset_path = staticmethod(AutoMlClient.parse_dataset_path)
    model_path = staticmethod(AutoMlClient.model_path)
    parse_model_path = staticmethod(AutoMlClient.parse_model_path)
    model_evaluation_path = staticmethod(AutoMlClient.model_evaluation_path)
    parse_model_evaluation_path = staticmethod(AutoMlClient.parse_model_evaluation_path)
    table_spec_path = staticmethod(AutoMlClient.table_spec_path)
    parse_table_spec_path = staticmethod(AutoMlClient.parse_table_spec_path)
    common_billing_account_path = staticmethod(AutoMlClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        AutoMlClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AutoMlClient.common_folder_path)
    parse_common_folder_path = staticmethod(AutoMlClient.parse_common_folder_path)
    common_organization_path = staticmethod(AutoMlClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        AutoMlClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AutoMlClient.common_project_path)
    parse_common_project_path = staticmethod(AutoMlClient.parse_common_project_path)
    common_location_path = staticmethod(AutoMlClient.common_location_path)
    parse_common_location_path = staticmethod(AutoMlClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AutoMlAsyncClient: The constructed client.
        """
        return AutoMlClient.from_service_account_info.__func__(AutoMlAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AutoMlAsyncClient: The constructed client.
        """
        return AutoMlClient.from_service_account_file.__func__(AutoMlAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AutoMlTransport:
        """Returns the transport used by the client instance.

        Returns:
            AutoMlTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AutoMlClient).get_transport_class, type(AutoMlClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AutoMlTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the auto ml client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AutoMlTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = AutoMlClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_dataset(
        self,
        request: service.CreateDatasetRequest = None,
        *,
        parent: str = None,
        dataset: gca_dataset.Dataset = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_dataset.Dataset:
        r"""Creates a dataset.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.CreateDatasetRequest`):
                The request object. Request message for
                [AutoMl.CreateDataset][google.cloud.automl.v1beta1.AutoMl.CreateDataset].
            parent (:class:`str`):
                Required. The resource name of the
                project to create the dataset for.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dataset (:class:`google.cloud.automl_v1beta1.types.Dataset`):
                Required. The dataset to create.
                This corresponds to the ``dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.Dataset:
                A workspace for solving a single,
                particular machine learning (ML)
                problem. A workspace contains examples
                that may be annotated.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, dataset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if dataset is not None:
            request.dataset = dataset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_dataset,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_dataset(
        self,
        request: service.GetDatasetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.Dataset:
        r"""Gets a dataset.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetDatasetRequest`):
                The request object. Request message for
                [AutoMl.GetDataset][google.cloud.automl.v1beta1.AutoMl.GetDataset].
            name (:class:`str`):
                Required. The resource name of the
                dataset to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.Dataset:
                A workspace for solving a single,
                particular machine learning (ML)
                problem. A workspace contains examples
                that may be annotated.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_dataset,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_datasets(
        self,
        request: service.ListDatasetsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatasetsAsyncPager:
        r"""Lists datasets in a project.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ListDatasetsRequest`):
                The request object. Request message for
                [AutoMl.ListDatasets][google.cloud.automl.v1beta1.AutoMl.ListDatasets].
            parent (:class:`str`):
                Required. The resource name of the
                project from which to list datasets.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.services.auto_ml.pagers.ListDatasetsAsyncPager:
                Response message for
                [AutoMl.ListDatasets][google.cloud.automl.v1beta1.AutoMl.ListDatasets].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ListDatasetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_datasets,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDatasetsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_dataset(
        self,
        request: service.UpdateDatasetRequest = None,
        *,
        dataset: gca_dataset.Dataset = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_dataset.Dataset:
        r"""Updates a dataset.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.UpdateDatasetRequest`):
                The request object. Request message for
                [AutoMl.UpdateDataset][google.cloud.automl.v1beta1.AutoMl.UpdateDataset]
            dataset (:class:`google.cloud.automl_v1beta1.types.Dataset`):
                Required. The dataset which replaces
                the resource on the server.

                This corresponds to the ``dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.Dataset:
                A workspace for solving a single,
                particular machine learning (ML)
                problem. A workspace contains examples
                that may be annotated.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([dataset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if dataset is not None:
            request.dataset = dataset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_dataset,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("dataset.name", request.dataset.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_dataset(
        self,
        request: service.DeleteDatasetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a dataset and all of its contents. Returns empty
        response in the
        [response][google.longrunning.Operation.response] field when it
        completes, and ``delete_details`` in the
        [metadata][google.longrunning.Operation.metadata] field.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.DeleteDatasetRequest`):
                The request object. Request message for
                [AutoMl.DeleteDataset][google.cloud.automl.v1beta1.AutoMl.DeleteDataset].
            name (:class:`str`):
                Required. The resource name of the
                dataset to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.DeleteDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_dataset,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def import_data(
        self,
        request: service.ImportDataRequest = None,
        *,
        name: str = None,
        input_config: io.InputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports data into a dataset. For Tables this method can only be
        called on an empty Dataset.

        For Tables:

        -  A
           [schema_inference_version][google.cloud.automl.v1beta1.InputConfig.params]
           parameter must be explicitly set. Returns an empty response
           in the [response][google.longrunning.Operation.response]
           field when it completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ImportDataRequest`):
                The request object. Request message for
                [AutoMl.ImportData][google.cloud.automl.v1beta1.AutoMl.ImportData].
            name (:class:`str`):
                Required. Dataset name. Dataset must
                already exist. All imported annotations
                and examples will be added.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_config (:class:`google.cloud.automl_v1beta1.types.InputConfig`):
                Required. The desired input location
                and its domain specific semantics, if
                any.

                This corresponds to the ``input_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, input_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ImportDataRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if input_config is not None:
            request.input_config = input_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_data,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def export_data(
        self,
        request: service.ExportDataRequest = None,
        *,
        name: str = None,
        output_config: io.OutputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports dataset's data to the provided output location. Returns
        an empty response in the
        [response][google.longrunning.Operation.response] field when it
        completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ExportDataRequest`):
                The request object. Request message for
                [AutoMl.ExportData][google.cloud.automl.v1beta1.AutoMl.ExportData].
            name (:class:`str`):
                Required. The resource name of the
                dataset.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`google.cloud.automl_v1beta1.types.OutputConfig`):
                Required. The desired output
                location.

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, output_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ExportDataRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if output_config is not None:
            request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_data,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_annotation_spec(
        self,
        request: service.GetAnnotationSpecRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> annotation_spec.AnnotationSpec:
        r"""Gets an annotation spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetAnnotationSpecRequest`):
                The request object. Request message for
                [AutoMl.GetAnnotationSpec][google.cloud.automl.v1beta1.AutoMl.GetAnnotationSpec].
            name (:class:`str`):
                Required. The resource name of the
                annotation spec to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.AnnotationSpec:
                A definition of an annotation spec.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetAnnotationSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_annotation_spec,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_table_spec(
        self,
        request: service.GetTableSpecRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> table_spec.TableSpec:
        r"""Gets a table spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetTableSpecRequest`):
                The request object. Request message for
                [AutoMl.GetTableSpec][google.cloud.automl.v1beta1.AutoMl.GetTableSpec].
            name (:class:`str`):
                Required. The resource name of the
                table spec to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.TableSpec:
                A specification of a relational table.
                   The table's schema is represented via its child
                   column specs. It is pre-populated as part of
                   ImportData by schema inference algorithm, the version
                   of which is a required parameter of ImportData
                   InputConfig. Note: While working with a table, at
                   times the schema may be inconsistent with the data in
                   the table (e.g. string in a FLOAT64 column). The
                   consistency validation is done upon creation of a
                   model. Used by: \* Tables

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetTableSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_table_spec,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_table_specs(
        self,
        request: service.ListTableSpecsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTableSpecsAsyncPager:
        r"""Lists table specs in a dataset.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ListTableSpecsRequest`):
                The request object. Request message for
                [AutoMl.ListTableSpecs][google.cloud.automl.v1beta1.AutoMl.ListTableSpecs].
            parent (:class:`str`):
                Required. The resource name of the
                dataset to list table specs from.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.services.auto_ml.pagers.ListTableSpecsAsyncPager:
                Response message for
                [AutoMl.ListTableSpecs][google.cloud.automl.v1beta1.AutoMl.ListTableSpecs].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ListTableSpecsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_table_specs,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTableSpecsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_table_spec(
        self,
        request: service.UpdateTableSpecRequest = None,
        *,
        table_spec: gca_table_spec.TableSpec = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_table_spec.TableSpec:
        r"""Updates a table spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.UpdateTableSpecRequest`):
                The request object. Request message for
                [AutoMl.UpdateTableSpec][google.cloud.automl.v1beta1.AutoMl.UpdateTableSpec]
            table_spec (:class:`google.cloud.automl_v1beta1.types.TableSpec`):
                Required. The table spec which
                replaces the resource on the server.

                This corresponds to the ``table_spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.TableSpec:
                A specification of a relational table.
                   The table's schema is represented via its child
                   column specs. It is pre-populated as part of
                   ImportData by schema inference algorithm, the version
                   of which is a required parameter of ImportData
                   InputConfig. Note: While working with a table, at
                   times the schema may be inconsistent with the data in
                   the table (e.g. string in a FLOAT64 column). The
                   consistency validation is done upon creation of a
                   model. Used by: \* Tables

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_spec])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateTableSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if table_spec is not None:
            request.table_spec = table_spec

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_table_spec,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_spec.name", request.table_spec.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_column_spec(
        self,
        request: service.GetColumnSpecRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> column_spec.ColumnSpec:
        r"""Gets a column spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetColumnSpecRequest`):
                The request object. Request message for
                [AutoMl.GetColumnSpec][google.cloud.automl.v1beta1.AutoMl.GetColumnSpec].
            name (:class:`str`):
                Required. The resource name of the
                column spec to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.ColumnSpec:
                A representation of a column in a relational table. When listing them, column specs are returned in the same order in which they were
                   given on import . Used by: \* Tables

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetColumnSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_column_spec,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_column_specs(
        self,
        request: service.ListColumnSpecsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListColumnSpecsAsyncPager:
        r"""Lists column specs in a table spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ListColumnSpecsRequest`):
                The request object. Request message for
                [AutoMl.ListColumnSpecs][google.cloud.automl.v1beta1.AutoMl.ListColumnSpecs].
            parent (:class:`str`):
                Required. The resource name of the
                table spec to list column specs from.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.services.auto_ml.pagers.ListColumnSpecsAsyncPager:
                Response message for
                [AutoMl.ListColumnSpecs][google.cloud.automl.v1beta1.AutoMl.ListColumnSpecs].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ListColumnSpecsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_column_specs,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListColumnSpecsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_column_spec(
        self,
        request: service.UpdateColumnSpecRequest = None,
        *,
        column_spec: gca_column_spec.ColumnSpec = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_column_spec.ColumnSpec:
        r"""Updates a column spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.UpdateColumnSpecRequest`):
                The request object. Request message for
                [AutoMl.UpdateColumnSpec][google.cloud.automl.v1beta1.AutoMl.UpdateColumnSpec]
            column_spec (:class:`google.cloud.automl_v1beta1.types.ColumnSpec`):
                Required. The column spec which
                replaces the resource on the server.

                This corresponds to the ``column_spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.ColumnSpec:
                A representation of a column in a relational table. When listing them, column specs are returned in the same order in which they were
                   given on import . Used by: \* Tables

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([column_spec])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateColumnSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if column_spec is not None:
            request.column_spec = column_spec

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_column_spec,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("column_spec.name", request.column_spec.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_model(
        self,
        request: service.CreateModelRequest = None,
        *,
        parent: str = None,
        model: gca_model.Model = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a model. Returns a Model in the
        [response][google.longrunning.Operation.response] field when it
        completes. When you create a model, several model evaluations
        are created for it: a global evaluation, and one evaluation for
        each annotation spec.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.CreateModelRequest`):
                The request object. Request message for
                [AutoMl.CreateModel][google.cloud.automl.v1beta1.AutoMl.CreateModel].
            parent (:class:`str`):
                Required. Resource name of the parent
                project where the model is being
                created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (:class:`google.cloud.automl_v1beta1.types.Model`):
                Required. The model to create.
                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.automl_v1beta1.types.Model` API
                proto representing a trained machine learning model.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, model])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if model is not None:
            request.model = model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_model,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gca_model.Model,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_model(
        self,
        request: service.GetModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> model.Model:
        r"""Gets a model.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetModelRequest`):
                The request object. Request message for
                [AutoMl.GetModel][google.cloud.automl.v1beta1.AutoMl.GetModel].
            name (:class:`str`):
                Required. Resource name of the model.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.Model:
                API proto representing a trained
                machine learning model.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_model,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_models(
        self,
        request: service.ListModelsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListModelsAsyncPager:
        r"""Lists models.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ListModelsRequest`):
                The request object. Request message for
                [AutoMl.ListModels][google.cloud.automl.v1beta1.AutoMl.ListModels].
            parent (:class:`str`):
                Required. Resource name of the
                project, from which to list the models.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.services.auto_ml.pagers.ListModelsAsyncPager:
                Response message for
                [AutoMl.ListModels][google.cloud.automl.v1beta1.AutoMl.ListModels].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ListModelsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_models,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListModelsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_model(
        self,
        request: service.DeleteModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a model. Returns ``google.protobuf.Empty`` in the
        [response][google.longrunning.Operation.response] field when it
        completes, and ``delete_details`` in the
        [metadata][google.longrunning.Operation.metadata] field.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.DeleteModelRequest`):
                The request object. Request message for
                [AutoMl.DeleteModel][google.cloud.automl.v1beta1.AutoMl.DeleteModel].
            name (:class:`str`):
                Required. Resource name of the model
                being deleted.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.DeleteModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_model,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def deploy_model(
        self,
        request: service.DeployModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deploys a model. If a model is already deployed, deploying it
        with the same parameters has no effect. Deploying with different
        parametrs (as e.g. changing

        [node_number][google.cloud.automl.v1beta1.ImageObjectDetectionModelDeploymentMetadata.node_number])
        will reset the deployment state without pausing the model's
        availability.

        Only applicable for Text Classification, Image Object Detection
        , Tables, and Image Segmentation; all other domains manage
        deployment automatically.

        Returns an empty response in the
        [response][google.longrunning.Operation.response] field when it
        completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.DeployModelRequest`):
                The request object. Request message for
                [AutoMl.DeployModel][google.cloud.automl.v1beta1.AutoMl.DeployModel].
            name (:class:`str`):
                Required. Resource name of the model
                to deploy.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.DeployModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.deploy_model,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def undeploy_model(
        self,
        request: service.UndeployModelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Undeploys a model. If the model is not deployed this method has
        no effect.

        Only applicable for Text Classification, Image Object Detection
        and Tables; all other domains manage deployment automatically.

        Returns an empty response in the
        [response][google.longrunning.Operation.response] field when it
        completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.UndeployModelRequest`):
                The request object. Request message for
                [AutoMl.UndeployModel][google.cloud.automl.v1beta1.AutoMl.UndeployModel].
            name (:class:`str`):
                Required. Resource name of the model
                to undeploy.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UndeployModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.undeploy_model,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def export_model(
        self,
        request: service.ExportModelRequest = None,
        *,
        name: str = None,
        output_config: io.ModelExportOutputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports a trained, "export-able", model to a user specified
        Google Cloud Storage location. A model is considered export-able
        if and only if it has an export format defined for it in

        [ModelExportOutputConfig][google.cloud.automl.v1beta1.ModelExportOutputConfig].

        Returns an empty response in the
        [response][google.longrunning.Operation.response] field when it
        completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ExportModelRequest`):
                The request object. Request message for
                [AutoMl.ExportModel][google.cloud.automl.v1beta1.AutoMl.ExportModel].
                Models need to be enabled for exporting, otherwise an
                error code will be returned.
            name (:class:`str`):
                Required. The resource name of the
                model to export.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`google.cloud.automl_v1beta1.types.ModelExportOutputConfig`):
                Required. The desired output location
                and configuration.

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, output_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ExportModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if output_config is not None:
            request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_model,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def export_evaluated_examples(
        self,
        request: service.ExportEvaluatedExamplesRequest = None,
        *,
        name: str = None,
        output_config: io.ExportEvaluatedExamplesOutputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports examples on which the model was evaluated (i.e. which
        were in the TEST set of the dataset the model was created from),
        together with their ground truth annotations and the annotations
        created (predicted) by the model. The examples, ground truth and
        predictions are exported in the state they were at the moment
        the model was evaluated.

        This export is available only for 30 days since the model
        evaluation is created.

        Currently only available for Tables.

        Returns an empty response in the
        [response][google.longrunning.Operation.response] field when it
        completes.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ExportEvaluatedExamplesRequest`):
                The request object. Request message for
                [AutoMl.ExportEvaluatedExamples][google.cloud.automl.v1beta1.AutoMl.ExportEvaluatedExamples].
            name (:class:`str`):
                Required. The resource name of the
                model whose evaluated examples are to be
                exported.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`google.cloud.automl_v1beta1.types.ExportEvaluatedExamplesOutputConfig`):
                Required. The desired output location
                and configuration.

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, output_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ExportEvaluatedExamplesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if output_config is not None:
            request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_evaluated_examples,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_model_evaluation(
        self,
        request: service.GetModelEvaluationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> model_evaluation.ModelEvaluation:
        r"""Gets a model evaluation.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.GetModelEvaluationRequest`):
                The request object. Request message for
                [AutoMl.GetModelEvaluation][google.cloud.automl.v1beta1.AutoMl.GetModelEvaluation].
            name (:class:`str`):
                Required. Resource name for the model
                evaluation.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.types.ModelEvaluation:
                Evaluation results of a model.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetModelEvaluationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_model_evaluation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5.0,
            ),
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_model_evaluations(
        self,
        request: service.ListModelEvaluationsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListModelEvaluationsAsyncPager:
        r"""Lists model evaluations.

        Args:
            request (:class:`google.cloud.automl_v1beta1.types.ListModelEvaluationsRequest`):
                The request object. Request message for
                [AutoMl.ListModelEvaluations][google.cloud.automl.v1beta1.AutoMl.ListModelEvaluations].
            parent (:class:`str`):
                Required. Resource name of the model
                to list the model evaluations for. If
                modelId is set as "-", this will list
                model evaluations from across all models
                of the parent location.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1beta1.services.auto_ml.pagers.ListModelEvaluationsAsyncPager:
                Response message for
                [AutoMl.ListModelEvaluations][google.cloud.automl.v1beta1.AutoMl.ListModelEvaluations].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.ListModelEvaluationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_model_evaluations,
            default_timeout=5.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListModelEvaluationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-automl",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AutoMlAsyncClient",)
