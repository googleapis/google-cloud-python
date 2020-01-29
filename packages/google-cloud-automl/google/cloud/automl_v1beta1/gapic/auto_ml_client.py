# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.automl_v1beta1.gapic import auto_ml_client_config
from google.cloud.automl_v1beta1.gapic import enums
from google.cloud.automl_v1beta1.gapic.transports import auto_ml_grpc_transport
from google.cloud.automl_v1beta1.proto import annotation_spec_pb2
from google.cloud.automl_v1beta1.proto import column_spec_pb2
from google.cloud.automl_v1beta1.proto import dataset_pb2
from google.cloud.automl_v1beta1.proto import image_pb2
from google.cloud.automl_v1beta1.proto import io_pb2
from google.cloud.automl_v1beta1.proto import model_evaluation_pb2
from google.cloud.automl_v1beta1.proto import model_pb2
from google.cloud.automl_v1beta1.proto import operations_pb2 as proto_operations_pb2
from google.cloud.automl_v1beta1.proto import service_pb2
from google.cloud.automl_v1beta1.proto import service_pb2_grpc
from google.cloud.automl_v1beta1.proto import table_spec_pb2
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


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

    Currently the only supported ``location_id`` is "us-central1".

    On any input that is documented to expect a string parameter in
    snake\_case or kebab-case, either of those cases is accepted.
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
    def annotation_spec_path(cls, project, location, dataset, annotation_spec):
        """Return a fully-qualified annotation_spec string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/datasets/{dataset}/annotationSpecs/{annotation_spec}",
            project=project,
            location=location,
            dataset=dataset,
            annotation_spec=annotation_spec,
        )

    @classmethod
    def column_spec_path(cls, project, location, dataset, table_spec, column_spec):
        """Return a fully-qualified column_spec string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/datasets/{dataset}/tableSpecs/{table_spec}/columnSpecs/{column_spec}",
            project=project,
            location=location,
            dataset=dataset,
            table_spec=table_spec,
            column_spec=column_spec,
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
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
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

    @classmethod
    def table_spec_path(cls, project, location, dataset, table_spec):
        """Return a fully-qualified table_spec string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/datasets/{dataset}/tableSpecs/{table_spec}",
            project=project,
            location=location,
            dataset=dataset,
            table_spec=table_spec,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
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

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=auto_ml_grpc_transport.AutoMlGrpcTransport,
                    address=api_endpoint,
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
                address=api_endpoint, channel=channel, credentials=credentials
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_dataset(
        self,
        dataset,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> # TODO: Initialize `dataset`:
            >>> dataset = {}
            >>>
            >>> response = client.update_dataset(dataset)

        Args:
            dataset (Union[dict, ~google.cloud.automl_v1beta1.types.Dataset]): The dataset which replaces the resource on the server.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.Dataset`
            update_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): The update mask applies to the resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "update_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_dataset,
                default_retry=self._method_configs["UpdateDataset"].retry,
                default_timeout=self._method_configs["UpdateDataset"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateDatasetRequest(
            dataset=dataset, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("dataset.name", dataset.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_dataset"](
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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

                -  ``dataset_metadata`` - for existence of the case (e.g.
                   image\_classification\_dataset\_metadata:\*). Some examples of using
                   the filter are:

                -  ``translation_dataset_metadata:*`` --> The dataset has
                   translation\_dataset\_metadata.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.Dataset` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
        Imports data into a dataset. For Tables this method can only be called
        on an empty Dataset.

        For Tables:

        -  A ``schema_inference_version`` parameter must be explicitly set.
           Returns an empty response in the ``response`` field when it
           completes.

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
            input_config (Union[dict, ~google.cloud.automl_v1beta1.types.InputConfig]): Required. The desired input location and its domain specific semantics,
                if any.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.InputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
        Exports dataset's data to the provided output location. Returns an empty
        response in the ``response`` field when it completes.

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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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

                -  ``model_metadata`` - for existence of the case (e.g.
                   video\_classification\_model\_metadata:\*).

                -  ``dataset_id`` - for = or !=. Some examples of using the filter are:

                -  ``image_classification_model_metadata:*`` --> The model has
                   image\_classification\_model\_metadata.

                -  ``dataset_id=5`` --> The model was created from a dataset with ID 5.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.Model` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
        Deletes a model. Returns ``google.protobuf.Empty`` in the ``response``
        field when it completes, and ``delete_details`` in the ``metadata``
        field.

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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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
        image_object_detection_model_deployment_metadata=None,
        image_classification_model_deployment_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deploys a model. If a model is already deployed, deploying it with the
        same parameters has no effect. Deploying with different parametrs (as
        e.g. changing

        ``node_number``) will reset the deployment state without pausing the
        model's availability.

        Only applicable for Text Classification, Image Object Detection and
        Tables; all other domains manage deployment automatically.

        Returns an empty response in the ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.deploy_model(name)
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
            name (str): Resource name of the model to deploy.
            image_object_detection_model_deployment_metadata (Union[dict, ~google.cloud.automl_v1beta1.types.ImageObjectDetectionModelDeploymentMetadata]): Model deployment metadata specific to Image Object Detection.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ImageObjectDetectionModelDeploymentMetadata`
            image_classification_model_deployment_metadata (Union[dict, ~google.cloud.automl_v1beta1.types.ImageClassificationModelDeploymentMetadata]): Model deployment metadata specific to Image Classification.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ImageClassificationModelDeploymentMetadata`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "deploy_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "deploy_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.deploy_model,
                default_retry=self._method_configs["DeployModel"].retry,
                default_timeout=self._method_configs["DeployModel"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            image_object_detection_model_deployment_metadata=image_object_detection_model_deployment_metadata,
            image_classification_model_deployment_metadata=image_classification_model_deployment_metadata,
        )

        request = service_pb2.DeployModelRequest(
            name=name,
            image_object_detection_model_deployment_metadata=image_object_detection_model_deployment_metadata,
            image_classification_model_deployment_metadata=image_classification_model_deployment_metadata,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["deploy_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def undeploy_model(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Undeploys a model. If the model is not deployed this method has no
        effect.

        Only applicable for Text Classification, Image Object Detection and
        Tables; all other domains manage deployment automatically.

        Returns an empty response in the ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> response = client.undeploy_model(name)
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
            name (str): Resource name of the model to undeploy.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["undeploy_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_model_evaluation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def export_model(
        self,
        name,
        output_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports a trained, "export-able", model to a user specified Google Cloud
        Storage location. A model is considered export-able if and only if it
        has an export format defined for it in

        ``ModelExportOutputConfig``.

        Returns an empty response in the ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.export_model(name, output_config)
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
            name (str): Required. The resource name of the model to export.
            output_config (Union[dict, ~google.cloud.automl_v1beta1.types.ModelExportOutputConfig]): Required. The desired output location and configuration.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ModelExportOutputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "export_model" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_model"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_model,
                default_retry=self._method_configs["ExportModel"].retry,
                default_timeout=self._method_configs["ExportModel"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ExportModelRequest(name=name, output_config=output_config)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["export_model"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )

    def export_evaluated_examples(
        self,
        name,
        output_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports examples on which the model was evaluated (i.e. which were in
        the TEST set of the dataset the model was created from), together with
        their ground truth annotations and the annotations created (predicted)
        by the model. The examples, ground truth and predictions are exported in
        the state they were at the moment the model was evaluated.

        This export is available only for 30 days since the model evaluation is
        created.

        Currently only available for Tables.

        Returns an empty response in the ``response`` field when it completes.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.export_evaluated_examples(name, output_config)
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
            name (str): Required. The resource name of the model whose evaluated examples are to
                be exported.
            output_config (Union[dict, ~google.cloud.automl_v1beta1.types.ExportEvaluatedExamplesOutputConfig]): Required. The desired output location and configuration.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ExportEvaluatedExamplesOutputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "export_evaluated_examples" not in self._inner_api_calls:
            self._inner_api_calls[
                "export_evaluated_examples"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.export_evaluated_examples,
                default_retry=self._method_configs["ExportEvaluatedExamples"].retry,
                default_timeout=self._method_configs["ExportEvaluatedExamples"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ExportEvaluatedExamplesRequest(
            name=name, output_config=output_config
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["export_evaluated_examples"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=proto_operations_pb2.OperationMetadata,
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.ModelEvaluation` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

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

    def get_annotation_spec(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an annotation spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.annotation_spec_path('[PROJECT]', '[LOCATION]', '[DATASET]', '[ANNOTATION_SPEC]')
            >>>
            >>> response = client.get_annotation_spec(name)

        Args:
            name (str): The resource name of the annotation spec to retrieve.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.AnnotationSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_annotation_spec" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_annotation_spec"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_annotation_spec,
                default_retry=self._method_configs["GetAnnotationSpec"].retry,
                default_timeout=self._method_configs["GetAnnotationSpec"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetAnnotationSpecRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_annotation_spec"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_table_spec(
        self,
        name,
        field_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a table spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.table_spec_path('[PROJECT]', '[LOCATION]', '[DATASET]', '[TABLE_SPEC]')
            >>>
            >>> response = client.get_table_spec(name)

        Args:
            name (str): The resource name of the table spec to retrieve.
            field_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): Mask specifying which fields to read.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.TableSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_table_spec" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_table_spec"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_table_spec,
                default_retry=self._method_configs["GetTableSpec"].retry,
                default_timeout=self._method_configs["GetTableSpec"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetTableSpecRequest(name=name, field_mask=field_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_table_spec"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_table_specs(
        self,
        parent,
        field_mask=None,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists table specs in a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[LOCATION]', '[DATASET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_table_specs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_table_specs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource name of the dataset to list table specs from.
            field_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): Mask specifying which fields to read.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            filter_ (str): Filter expression, see go/filtering.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.TableSpec` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_table_specs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_table_specs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_table_specs,
                default_retry=self._method_configs["ListTableSpecs"].retry,
                default_timeout=self._method_configs["ListTableSpecs"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListTableSpecsRequest(
            parent=parent, field_mask=field_mask, filter=filter_, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_table_specs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="table_specs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_table_spec(
        self,
        table_spec,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a table spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> # TODO: Initialize `table_spec`:
            >>> table_spec = {}
            >>>
            >>> response = client.update_table_spec(table_spec)

        Args:
            table_spec (Union[dict, ~google.cloud.automl_v1beta1.types.TableSpec]): The table spec which replaces the resource on the server.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.TableSpec`
            update_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): The update mask applies to the resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.TableSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_table_spec" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_table_spec"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_table_spec,
                default_retry=self._method_configs["UpdateTableSpec"].retry,
                default_timeout=self._method_configs["UpdateTableSpec"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateTableSpecRequest(
            table_spec=table_spec, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_spec.name", table_spec.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_table_spec"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_column_spec(
        self,
        name,
        field_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a column spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> name = client.column_spec_path('[PROJECT]', '[LOCATION]', '[DATASET]', '[TABLE_SPEC]', '[COLUMN_SPEC]')
            >>>
            >>> response = client.get_column_spec(name)

        Args:
            name (str): The resource name of the column spec to retrieve.
            field_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): Mask specifying which fields to read.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_column_spec" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_column_spec"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_column_spec,
                default_retry=self._method_configs["GetColumnSpec"].retry,
                default_timeout=self._method_configs["GetColumnSpec"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.GetColumnSpecRequest(name=name, field_mask=field_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_column_spec"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_column_specs(
        self,
        parent,
        field_mask=None,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists column specs in a table spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> parent = client.table_spec_path('[PROJECT]', '[LOCATION]', '[DATASET]', '[TABLE_SPEC]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_column_specs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_column_specs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource name of the table spec to list column specs from.
            field_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): Mask specifying which fields to read.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            filter_ (str): Filter expression, see go/filtering.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_column_specs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_column_specs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_column_specs,
                default_retry=self._method_configs["ListColumnSpecs"].retry,
                default_timeout=self._method_configs["ListColumnSpecs"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.ListColumnSpecsRequest(
            parent=parent, field_mask=field_mask, filter=filter_, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_column_specs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="column_specs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_column_spec(
        self,
        column_spec,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a column spec.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.AutoMlClient()
            >>>
            >>> # TODO: Initialize `column_spec`:
            >>> column_spec = {}
            >>>
            >>> response = client.update_column_spec(column_spec)

        Args:
            column_spec (Union[dict, ~google.cloud.automl_v1beta1.types.ColumnSpec]): The column spec which replaces the resource on the server.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ColumnSpec`
            update_mask (Union[dict, ~google.cloud.automl_v1beta1.types.FieldMask]): The update mask applies to the resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_column_spec" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_column_spec"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_column_spec,
                default_retry=self._method_configs["UpdateColumnSpec"].retry,
                default_timeout=self._method_configs["UpdateColumnSpec"].timeout,
                client_info=self._client_info,
            )

        request = service_pb2.UpdateColumnSpecRequest(
            column_spec=column_spec, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("column_spec.name", column_spec.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_column_spec"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
