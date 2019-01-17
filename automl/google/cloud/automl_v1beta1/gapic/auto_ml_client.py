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
"""Accesses the google.cloud.automl.v1beta1 AutoMl API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.automl_v1beta1.gapic import auto_ml_client_config
from google.cloud.automl_v1beta1.gapic import enums
from google.cloud.automl_v1beta1.gapic.transports import auto_ml_grpc_transport
from google.cloud.automl_v1beta1.proto import data_items_pb2
from google.cloud.automl_v1beta1.proto import dataset_pb2
from google.cloud.automl_v1beta1.proto import io_pb2
from google.cloud.automl_v1beta1.proto import model_evaluation_pb2
from google.cloud.automl_v1beta1.proto import model_pb2
from google.cloud.automl_v1beta1.proto import operations_pb2 as proto_operations_pb2
from google.cloud.automl_v1beta1.proto import prediction_service_pb2
from google.cloud.automl_v1beta1.proto import prediction_service_pb2_grpc
from google.cloud.automl_v1beta1.proto import service_pb2
from google.cloud.automl_v1beta1.proto import service_pb2_grpc
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import empty_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-automl").version


class AutoMlClient(object):
    """
    AutoML Server API.

    The resource names are assigned by the server. The server never reuses
    names that it has created after the resources with those names are
    deleted.

    An ID of a resource is the last element of the item's resource name. For
    ``projects/{project_id}/locations/{location_id}/datasets/{dataset_id}``,
    then the id for the item is ``{dataset_id}``.
    """

    SERVICE_ADDRESS = "automl.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.automl.v1beta1.AutoMl"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AutoMlClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def dataset_path(cls, project, location, dataset):
        """Return a fully-qualified dataset string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/datasets/{dataset}",
            project=project,
            location=location,
            dataset=dataset,
        )

    @classmethod
    def model_path(cls, project, location, model):
        """Return a fully-qualified model string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/models/{model}",
            project=project,
            location=location,
            model=model,
        )

    @classmethod
    def model_evaluation_path(cls, project, location, model, model_evaluation):
        """Return a fully-qualified model_evaluation string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/models/{model}/modelEvaluations/{model_evaluation}",
            project=project,
            location=location,
            model=model,
            model_evaluation=model_evaluation,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.AutoMlGrpcTransport,
                    Callable[[~.Credentials, type], ~.AutoMlGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = auto_ml_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=auto_ml_grpc_transport.AutoMlGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = auto_ml_grpc_transport.AutoMlGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_dataset(
        self,
        parent,
        dataset,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `dataset`:
            >>> dataset = {}
            >>>
            >>> response = client.create_dataset(parent, dataset)

        Args:
            parent (str): The resource name of the project to create the dataset for.
            dataset (Union[dict, ~google.cloud.automl_v1beta1.types.Dataset]): The dataset to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.Dataset`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_dataset,
                default_retry=self._method_configs["CreateDataset"].retry,
                default_timeout=self._method_configs["CreateDataset"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateDatasetRequest(parent=parent, dataset=dataset)
        return self._inner_api_calls["create_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_dataset(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[LOCATION]', '[DATASET]')
            >>>
            >>> response = client.get_dataset(name)

        Args:
            name (str): The resource name of the dataset to retrieve.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_dataset,
                default_retry=self._method_configs["GetDataset"].retry,
                default_timeout=self._method_configs["GetDataset"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetDatasetRequest(name=name)
        return self._inner_api_calls["get_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_datasets(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists datasets in a project.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_datasets(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_datasets(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource name of the project from which to list datasets.
            filter_ (str): An expression for filtering the results of the request.

                -  ``dataset_metadata`` - for existence of the case.

                An example of using the filter is:

                -  ``translation_dataset_metadata:*`` --> The dataset has
                   translation\_dataset\_metadata.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.automl_v1beta1.types.Dataset` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_datasets" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_datasets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_datasets,
                default_retry=self._method_configs["ListDatasets"].retry,
                default_timeout=self._method_configs["ListDatasets"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListDatasetsRequest(
            parent=parent, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_datasets"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="datasets",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_dataset(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a dataset and all of its contents. Returns empty response in the
        ``response`` field when it completes, and ``delete_details`` in the
        ``metadata`` field.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[LOCATION]', '[DATASET]')
            >>>
            >>> response = client.delete_dataset(name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): The resource name of the dataset to delete.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_dataset,
                default_retry=self._method_configs["DeleteDataset"].retry,
                default_timeout=self._method_configs["DeleteDataset"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DeleteDatasetRequest(name=name)
        operation = self._inner_api_calls["delete_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def import_data(
        self,
        name,
        input_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports data into a dataset. Returns an empty response in the
        ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[LOCATION]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `input_config`:
            >>> input_config = {}
            >>>
            >>> response = client.import_data(name, input_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): Required. Dataset name. Dataset must already exist. All imported
                annotations and examples will be added.
            input_config (Union[dict, ~google.cloud.automl_v1beta1.types.InputConfig]): Required. The desired input location.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.InputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_data" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_data"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_data,
                default_retry=self._method_configs["ImportData"].retry,
                default_timeout=self._method_configs["ImportData"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ImportDataRequest(name=name, input_config=input_config)
        operation = self._inner_api_calls["import_data"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def export_data(
        self,
        name,
        output_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports dataset's data to a Google Cloud Storage bucket. Returns an
        empty response in the ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[LOCATION]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.export_data(name, output_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): Required. The resource name of the dataset.
            output_config (Union[dict, ~google.cloud.automl_v1beta1.types.OutputConfig]): Required. The desired output location.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.OutputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "export_data" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_data"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_data,
                default_retry=self._method_configs["ExportData"].retry,
                default_timeout=self._method_configs["ExportData"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ExportDataRequest(name=name, output_config=output_config)
        operation = self._inner_api_calls["export_data"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def create_model(
        self,
        parent,
        model,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a model. Returns a Model in the ``response`` field when it
        completes. When you create a model, several model evaluations are
        created for it: a global evaluation, and one evaluation for each
        annotation spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `model`:
            >>> model = {}
            >>>
            >>> response = client.create_model(parent, model)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Resource name of the parent project where the model is being created.
            model (Union[dict, ~google.cloud.automl_v1beta1.types.Model]): The model to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.Model`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_model,
                default_retry=self._method_configs["CreateModel"].retry,
                default_timeout=self._method_configs["CreateModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.CreateModelRequest(parent=parent, model=model)
        operation = self._inner_api_calls["create_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            model_pb2.Model,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def get_model(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.get_model(name)

        Args:
            name (str): Resource name of the model.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Model` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_model,
                default_retry=self._method_configs["GetModel"].retry,
                default_timeout=self._method_configs["GetModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetModelRequest(name=name)
        return self._inner_api_calls["get_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_models(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists models.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_models(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_models(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the project, from which to list the models.
            filter_ (str): An expression for filtering the results of the request.

                -  ``model_metadata`` - for existence of the case.
                -  ``dataset_id`` - for = or !=.

                Some examples of using the filter are:

                -  ``image_classification_model_metadata:*`` --> The model has
                   image\_classification\_model\_metadata.
                -  ``dataset_id=5`` --> The model was created from a sibling dataset
                   with ID 5.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.automl_v1beta1.types.Model` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_models" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_models"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_models,
                default_retry=self._method_configs["ListModels"].retry,
                default_timeout=self._method_configs["ListModels"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListModelsRequest(
            parent=parent, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_models"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="model",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_model(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a model. If a model is already deployed, this only deletes the
        model in AutoML BE, and does not change the status of the deployed model
        in the production environment. Returns ``google.protobuf.Empty`` in the
        ``response`` field when it completes, and ``delete_details`` in the
        ``metadata`` field.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.delete_model(name)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): Resource name of the model being deleted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_model,
                default_retry=self._method_configs["DeleteModel"].retry,
                default_timeout=self._method_configs["DeleteModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DeleteModelRequest(name=name)
        operation = self._inner_api_calls["delete_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def deploy_model(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deploys model. Returns a ``DeployModelResponse`` in the ``response``
        field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.deploy_model(name)

        Args:
            name (str): Resource name of the model to deploy.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "deploy_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "deploy_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.deploy_model,
                default_retry=self._method_configs["DeployModel"].retry,
                default_timeout=self._method_configs["DeployModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.DeployModelRequest(name=name)
        return self._inner_api_calls["deploy_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def undeploy_model(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Undeploys model. Returns an ``UndeployModelResponse`` in the
        ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.undeploy_model(name)

        Args:
            name (str): Resource name of the model to undeploy.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Operation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "undeploy_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "undeploy_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.undeploy_model,
                default_retry=self._method_configs["UndeployModel"].retry,
                default_timeout=self._method_configs["UndeployModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UndeployModelRequest(name=name)
        return self._inner_api_calls["undeploy_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_model_evaluation(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a model evaluation.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_evaluation_path('[PROJECT]', '[LOCATION]', '[MODEL]', '[MODEL_EVALUATION]')
            >>>
            >>> response = client.get_model_evaluation(name)

        Args:
            name (str): Resource name for the model evaluation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ModelEvaluation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_model_evaluation" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_model_evaluation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_model_evaluation,
                default_retry=self._method_configs["GetModelEvaluation"].retry,
                default_timeout=self._method_configs["GetModelEvaluation"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetModelEvaluationRequest(name=name)
        return self._inner_api_calls["get_model_evaluation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_model_evaluations(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists model evaluations.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_model_evaluations(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_model_evaluations(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the model to list the model evaluations for.
                If modelId is set as "-", this will list model evaluations from across all
                models of the parent location.
            filter_ (str): An expression for filtering the results of the request.

                -  ``annotation_spec_id`` - for =, != or existence. See example below
                   for the last.

                Some examples of using the filter are:

                -  ``annotation_spec_id!=4`` --> The model evaluation was done for
                   annotation spec with ID different than 4.
                -  ``NOT annotation_spec_id:*`` --> The model evaluation was done for
                   aggregate of all annotation specs.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.automl_v1beta1.types.ModelEvaluation` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_model_evaluations" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_model_evaluations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_model_evaluations,
                default_retry=self._method_configs["ListModelEvaluations"].retry,
                default_timeout=self._method_configs["ListModelEvaluations"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListModelEvaluationsRequest(
            parent=parent, filter=filter_, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_model_evaluations"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="model_evaluation",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
