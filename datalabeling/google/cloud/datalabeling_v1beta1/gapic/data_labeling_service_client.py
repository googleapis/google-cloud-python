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

"""Accesses the google.cloud.datalabeling.v1beta1 DataLabelingService API."""

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

from google.cloud.datalabeling_v1beta1.gapic import data_labeling_service_client_config
from google.cloud.datalabeling_v1beta1.gapic import enums
from google.cloud.datalabeling_v1beta1.gapic.transports import (
    data_labeling_service_grpc_transport,
)
from google.cloud.datalabeling_v1beta1.proto import annotation_spec_set_pb2
from google.cloud.datalabeling_v1beta1.proto import data_labeling_service_pb2
from google.cloud.datalabeling_v1beta1.proto import data_labeling_service_pb2_grpc
from google.cloud.datalabeling_v1beta1.proto import dataset_pb2
from google.cloud.datalabeling_v1beta1.proto import evaluation_job_pb2
from google.cloud.datalabeling_v1beta1.proto import evaluation_pb2
from google.cloud.datalabeling_v1beta1.proto import human_annotation_config_pb2
from google.cloud.datalabeling_v1beta1.proto import instruction_pb2
from google.cloud.datalabeling_v1beta1.proto import (
    operations_pb2 as proto_operations_pb2,
)
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-datalabeling"
).version


class DataLabelingServiceClient(object):
    SERVICE_ADDRESS = "datalabeling.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.datalabeling.v1beta1.DataLabelingService"

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
            DataLabelingServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def annotated_dataset_path(cls, project, dataset, annotated_dataset):
        """Return a fully-qualified annotated_dataset string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}",
            project=project,
            dataset=dataset,
            annotated_dataset=annotated_dataset,
        )

    @classmethod
    def annotation_spec_set_path(cls, project, annotation_spec_set):
        """Return a fully-qualified annotation_spec_set string."""
        return google.api_core.path_template.expand(
            "projects/{project}/annotationSpecSets/{annotation_spec_set}",
            project=project,
            annotation_spec_set=annotation_spec_set,
        )

    @classmethod
    def data_item_path(cls, project, dataset, data_item):
        """Return a fully-qualified data_item string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}/dataItems/{data_item}",
            project=project,
            dataset=dataset,
            data_item=data_item,
        )

    @classmethod
    def dataset_path(cls, project, dataset):
        """Return a fully-qualified dataset string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}", project=project, dataset=dataset
        )

    @classmethod
    def evaluation_path(cls, project, dataset, evaluation):
        """Return a fully-qualified evaluation string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}/evaluations/{evaluation}",
            project=project,
            dataset=dataset,
            evaluation=evaluation,
        )

    @classmethod
    def evaluation_job_path(cls, project, evaluation_job):
        """Return a fully-qualified evaluation_job string."""
        return google.api_core.path_template.expand(
            "projects/{project}/evaluationJobs/{evaluation_job}",
            project=project,
            evaluation_job=evaluation_job,
        )

    @classmethod
    def example_path(cls, project, dataset, annotated_dataset, example):
        """Return a fully-qualified example string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}/examples/{example}",
            project=project,
            dataset=dataset,
            annotated_dataset=annotated_dataset,
            example=example,
        )

    @classmethod
    def instruction_path(cls, project, instruction):
        """Return a fully-qualified instruction string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instructions/{instruction}",
            project=project,
            instruction=instruction,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
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
            transport (Union[~.DataLabelingServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.DataLabelingServiceGrpcTransport]): A transport
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
            client_config = data_labeling_service_client_config.config

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
                    default_class=data_labeling_service_grpc_transport.DataLabelingServiceGrpcTransport,
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
            self.transport = data_labeling_service_grpc_transport.DataLabelingServiceGrpcTransport(
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
        Creates dataset. If success return a Dataset resource.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `dataset`:
            >>> dataset = {}
            >>>
            >>> response = client.create_dataset(parent, dataset)

        Args:
            parent (str): Required. Dataset resource parent, format: projects/{project\_id}
            dataset (Union[dict, ~google.cloud.datalabeling_v1beta1.types.Dataset]): Required. The dataset to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.Dataset`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.Dataset` instance.

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

        request = data_labeling_service_pb2.CreateDatasetRequest(
            parent=parent, dataset=dataset
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
        Gets dataset by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> response = client.get_dataset(name)

        Args:
            name (str): Required. Dataset resource name, format:
                projects/{project\_id}/datasets/{dataset\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.Dataset` instance.

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

        request = data_labeling_service_pb2.GetDatasetRequest(name=name)
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
        Lists datasets under a project. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
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
            parent (str): Required. Dataset resource parent, format: projects/{project\_id}
            filter_ (str): Optional. Filter on dataset is not supported at this moment.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.Dataset` instances.
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

        request = data_labeling_service_pb2.ListDatasetsRequest(
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
        Deletes a dataset by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> client.delete_dataset(name)

        Args:
            name (str): Required. Dataset resource name, format:
                projects/{project\_id}/datasets/{dataset\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

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

        request = data_labeling_service_pb2.DeleteDatasetRequest(name=name)
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

        self._inner_api_calls["delete_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def import_data(
        self,
        name,
        input_config,
        user_email_address=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Imports data into dataset based on source locations defined in request.
        It can be called multiple times for the same dataset. Each dataset can
        only have one long running operation running on it. For example, no
        labeling task (also long running operation) can be started while
        importing is still ongoing. Vice versa.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[DATASET]')
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
            name (str): Required. Dataset resource name, format:
                projects/{project\_id}/datasets/{dataset\_id}
            input_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.InputConfig]): Required. Specify the input source of the data.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.InputConfig`
            user_email_address (str): Email of the user who started the import task and should be notified by
                email. If empty no notification will be sent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

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

        request = data_labeling_service_pb2.ImportDataRequest(
            name=name, input_config=input_config, user_email_address=user_email_address
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

        operation = self._inner_api_calls["import_data"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            proto_operations_pb2.ImportDataOperationResponse,
            metadata_type=proto_operations_pb2.ImportDataOperationMetadata,
        )

    def export_data(
        self,
        name,
        annotated_dataset,
        output_config,
        filter_=None,
        user_email_address=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Exports data and annotations from dataset.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `annotated_dataset`:
            >>> annotated_dataset = ''
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.export_data(name, annotated_dataset, output_config)
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
            name (str): Required. Dataset resource name, format:
                projects/{project\_id}/datasets/{dataset\_id}
            annotated_dataset (str): Required. Annotated dataset resource name. DataItem in Dataset and their
                annotations in specified annotated dataset will be exported. It's in
                format of
                projects/{project\_id}/datasets/{dataset\_id}/annotatedDatasets/
                {annotated\_dataset\_id}
            output_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.OutputConfig]): Required. Specify the output destination.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.OutputConfig`
            filter_ (str): Optional. Filter is not supported at this moment.
            user_email_address (str): Email of the user who started the export task and should be notified by
                email. If empty no notification will be sent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

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

        request = data_labeling_service_pb2.ExportDataRequest(
            name=name,
            annotated_dataset=annotated_dataset,
            output_config=output_config,
            filter=filter_,
            user_email_address=user_email_address,
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

        operation = self._inner_api_calls["export_data"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            proto_operations_pb2.ExportDataOperationResponse,
            metadata_type=proto_operations_pb2.ExportDataOperationMetadata,
        )

    def get_data_item(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a data item in a dataset by resource name. This API can be
        called after data are imported into dataset.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.data_item_path('[PROJECT]', '[DATASET]', '[DATA_ITEM]')
            >>>
            >>> response = client.get_data_item(name)

        Args:
            name (str): Required. The name of the data item to get, format:
                projects/{project\_id}/datasets/{dataset\_id}/dataItems/{data\_item\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.DataItem` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_data_item" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_data_item"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_data_item,
                default_retry=self._method_configs["GetDataItem"].retry,
                default_timeout=self._method_configs["GetDataItem"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetDataItemRequest(name=name)
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

        return self._inner_api_calls["get_data_item"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_data_items(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists data items in a dataset. This API can be called after data
        are imported into dataset. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_data_items(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_data_items(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Name of the dataset to list data items, format:
                projects/{project\_id}/datasets/{dataset\_id}
            filter_ (str): Optional. Filter is not supported at this moment.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.DataItem` instances.
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
        if "list_data_items" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_data_items"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_data_items,
                default_retry=self._method_configs["ListDataItems"].retry,
                default_timeout=self._method_configs["ListDataItems"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListDataItemsRequest(
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
                self._inner_api_calls["list_data_items"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="data_items",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_annotated_dataset(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an annotated dataset by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.annotated_dataset_path('[PROJECT]', '[DATASET]', '[ANNOTATED_DATASET]')
            >>>
            >>> response = client.get_annotated_dataset(name)

        Args:
            name (str): Required. Name of the annotated dataset to get, format:
                projects/{project\_id}/datasets/{dataset\_id}/annotatedDatasets/
                {annotated\_dataset\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.AnnotatedDataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_annotated_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_annotated_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_annotated_dataset,
                default_retry=self._method_configs["GetAnnotatedDataset"].retry,
                default_timeout=self._method_configs["GetAnnotatedDataset"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetAnnotatedDatasetRequest(name=name)
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

        return self._inner_api_calls["get_annotated_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_annotated_datasets(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists annotated datasets for a dataset. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_annotated_datasets(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_annotated_datasets(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Name of the dataset to list annotated datasets, format:
                projects/{project\_id}/datasets/{dataset\_id}
            filter_ (str): Optional. Filter is not supported at this moment.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.AnnotatedDataset` instances.
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
        if "list_annotated_datasets" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_annotated_datasets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_annotated_datasets,
                default_retry=self._method_configs["ListAnnotatedDatasets"].retry,
                default_timeout=self._method_configs["ListAnnotatedDatasets"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListAnnotatedDatasetsRequest(
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
                self._inner_api_calls["list_annotated_datasets"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="annotated_datasets",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def label_image(
        self,
        parent,
        basic_config,
        feature,
        image_classification_config=None,
        bounding_poly_config=None,
        polyline_config=None,
        segmentation_config=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts a labeling task for image. The type of image labeling task is
        configured by feature in the request.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>> from google.cloud.datalabeling_v1beta1 import enums
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `basic_config`:
            >>> basic_config = {}
            >>>
            >>> # TODO: Initialize `feature`:
            >>> feature = enums.LabelImageRequest.Feature.FEATURE_UNSPECIFIED
            >>>
            >>> response = client.label_image(parent, basic_config, feature)
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
            parent (str): Required. Name of the dataset to request labeling task, format:
                projects/{project\_id}/datasets/{dataset\_id}
            basic_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig]): Required. Basic human annotation config.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig`
            feature (~google.cloud.datalabeling_v1beta1.types.Feature): Required. The type of image labeling task.
            image_classification_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.ImageClassificationConfig]): Configuration for image classification task. One of
                image\_classification\_config, bounding\_poly\_config, polyline\_config
                and segmentation\_config are required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.ImageClassificationConfig`
            bounding_poly_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.BoundingPolyConfig]): Configuration for bounding box and bounding poly task. One of
                image\_classification\_config, bounding\_poly\_config, polyline\_config
                and segmentation\_config are required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.BoundingPolyConfig`
            polyline_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.PolylineConfig]): Configuration for polyline task. One of image\_classification\_config,
                bounding\_poly\_config, polyline\_config and segmentation\_config are
                required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.PolylineConfig`
            segmentation_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.SegmentationConfig]): Configuration for segmentation task. One of
                image\_classification\_config, bounding\_poly\_config, polyline\_config
                and segmentation\_config are required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.SegmentationConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "label_image" not in self._inner_api_calls:
            self._inner_api_calls[
                "label_image"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.label_image,
                default_retry=self._method_configs["LabelImage"].retry,
                default_timeout=self._method_configs["LabelImage"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            image_classification_config=image_classification_config,
            bounding_poly_config=bounding_poly_config,
            polyline_config=polyline_config,
            segmentation_config=segmentation_config,
        )

        request = data_labeling_service_pb2.LabelImageRequest(
            parent=parent,
            basic_config=basic_config,
            feature=feature,
            image_classification_config=image_classification_config,
            bounding_poly_config=bounding_poly_config,
            polyline_config=polyline_config,
            segmentation_config=segmentation_config,
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

        operation = self._inner_api_calls["label_image"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            dataset_pb2.AnnotatedDataset,
            metadata_type=proto_operations_pb2.LabelOperationMetadata,
        )

    def label_video(
        self,
        parent,
        basic_config,
        feature,
        video_classification_config=None,
        object_detection_config=None,
        object_tracking_config=None,
        event_config=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts a labeling task for video. The type of video labeling task is
        configured by feature in the request.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>> from google.cloud.datalabeling_v1beta1 import enums
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `basic_config`:
            >>> basic_config = {}
            >>>
            >>> # TODO: Initialize `feature`:
            >>> feature = enums.LabelVideoRequest.Feature.FEATURE_UNSPECIFIED
            >>>
            >>> response = client.label_video(parent, basic_config, feature)
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
            parent (str): Required. Name of the dataset to request labeling task, format:
                projects/{project\_id}/datasets/{dataset\_id}
            basic_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig]): Required. Basic human annotation config.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig`
            feature (~google.cloud.datalabeling_v1beta1.types.Feature): Required. The type of video labeling task.
            video_classification_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.VideoClassificationConfig]): Configuration for video classification task. One of
                video\_classification\_config, object\_detection\_config,
                object\_tracking\_config and event\_config is required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.VideoClassificationConfig`
            object_detection_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.ObjectDetectionConfig]): Configuration for video object detection task. One of
                video\_classification\_config, object\_detection\_config,
                object\_tracking\_config and event\_config is required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.ObjectDetectionConfig`
            object_tracking_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.ObjectTrackingConfig]): Configuration for video object tracking task. One of
                video\_classification\_config, object\_detection\_config,
                object\_tracking\_config and event\_config is required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.ObjectTrackingConfig`
            event_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.EventConfig]): Configuration for video event task. One of
                video\_classification\_config, object\_detection\_config,
                object\_tracking\_config and event\_config is required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.EventConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "label_video" not in self._inner_api_calls:
            self._inner_api_calls[
                "label_video"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.label_video,
                default_retry=self._method_configs["LabelVideo"].retry,
                default_timeout=self._method_configs["LabelVideo"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            video_classification_config=video_classification_config,
            object_detection_config=object_detection_config,
            object_tracking_config=object_tracking_config,
            event_config=event_config,
        )

        request = data_labeling_service_pb2.LabelVideoRequest(
            parent=parent,
            basic_config=basic_config,
            feature=feature,
            video_classification_config=video_classification_config,
            object_detection_config=object_detection_config,
            object_tracking_config=object_tracking_config,
            event_config=event_config,
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

        operation = self._inner_api_calls["label_video"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            dataset_pb2.AnnotatedDataset,
            metadata_type=proto_operations_pb2.LabelOperationMetadata,
        )

    def label_text(
        self,
        parent,
        basic_config,
        feature,
        text_classification_config=None,
        text_entity_extraction_config=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts a labeling task for text. The type of text labeling task is
        configured by feature in the request.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>> from google.cloud.datalabeling_v1beta1 import enums
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.dataset_path('[PROJECT]', '[DATASET]')
            >>>
            >>> # TODO: Initialize `basic_config`:
            >>> basic_config = {}
            >>>
            >>> # TODO: Initialize `feature`:
            >>> feature = enums.LabelTextRequest.Feature.FEATURE_UNSPECIFIED
            >>>
            >>> response = client.label_text(parent, basic_config, feature)
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
            parent (str): Required. Name of the data set to request labeling task, format:
                projects/{project\_id}/datasets/{dataset\_id}
            basic_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig]): Required. Basic human annotation config.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig`
            feature (~google.cloud.datalabeling_v1beta1.types.Feature): Required. The type of text labeling task.
            text_classification_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.TextClassificationConfig]): Configuration for text classification task. One of
                text\_classification\_config and text\_entity\_extraction\_config is
                required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.TextClassificationConfig`
            text_entity_extraction_config (Union[dict, ~google.cloud.datalabeling_v1beta1.types.TextEntityExtractionConfig]): Configuration for entity extraction task. One of
                text\_classification\_config and text\_entity\_extraction\_config is
                required.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.TextEntityExtractionConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "label_text" not in self._inner_api_calls:
            self._inner_api_calls[
                "label_text"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.label_text,
                default_retry=self._method_configs["LabelText"].retry,
                default_timeout=self._method_configs["LabelText"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            text_classification_config=text_classification_config,
            text_entity_extraction_config=text_entity_extraction_config,
        )

        request = data_labeling_service_pb2.LabelTextRequest(
            parent=parent,
            basic_config=basic_config,
            feature=feature,
            text_classification_config=text_classification_config,
            text_entity_extraction_config=text_entity_extraction_config,
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

        operation = self._inner_api_calls["label_text"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            dataset_pb2.AnnotatedDataset,
            metadata_type=proto_operations_pb2.LabelOperationMetadata,
        )

    def get_example(
        self,
        name,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an example by resource name, including both data and annotation.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.example_path('[PROJECT]', '[DATASET]', '[ANNOTATED_DATASET]', '[EXAMPLE]')
            >>>
            >>> response = client.get_example(name)

        Args:
            name (str): Required. Name of example, format:
                projects/{project\_id}/datasets/{dataset\_id}/annotatedDatasets/
                {annotated\_dataset\_id}/examples/{example\_id}
            filter_ (str): Optional. An expression for filtering Examples. Filter by
                annotation\_spec.display\_name is supported. Format
                "annotation\_spec.display\_name = {display\_name}"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.Example` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_example" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_example"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_example,
                default_retry=self._method_configs["GetExample"].retry,
                default_timeout=self._method_configs["GetExample"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetExampleRequest(name=name, filter=filter_)
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

        return self._inner_api_calls["get_example"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_examples(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists examples in an annotated dataset. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.annotated_dataset_path('[PROJECT]', '[DATASET]', '[ANNOTATED_DATASET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_examples(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_examples(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Example resource parent.
            filter_ (str): Optional. An expression for filtering Examples. For annotated datasets
                that have annotation spec set, filter by annotation\_spec.display\_name
                is supported. Format "annotation\_spec.display\_name = {display\_name}"
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.Example` instances.
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
        if "list_examples" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_examples"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_examples,
                default_retry=self._method_configs["ListExamples"].retry,
                default_timeout=self._method_configs["ListExamples"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListExamplesRequest(
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
                self._inner_api_calls["list_examples"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="examples",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_annotation_spec_set(
        self,
        parent,
        annotation_spec_set,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an annotation spec set by providing a set of labels.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `annotation_spec_set`:
            >>> annotation_spec_set = {}
            >>>
            >>> response = client.create_annotation_spec_set(parent, annotation_spec_set)

        Args:
            parent (str): Required. AnnotationSpecSet resource parent, format:
                projects/{project\_id}
            annotation_spec_set (Union[dict, ~google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet]): Required. Annotation spec set to create. Annotation specs must be
                included. Only one annotation spec will be accepted for annotation specs
                with same display\_name.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_annotation_spec_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_annotation_spec_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_annotation_spec_set,
                default_retry=self._method_configs["CreateAnnotationSpecSet"].retry,
                default_timeout=self._method_configs["CreateAnnotationSpecSet"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.CreateAnnotationSpecSetRequest(
            parent=parent, annotation_spec_set=annotation_spec_set
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

        return self._inner_api_calls["create_annotation_spec_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_annotation_spec_set(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an annotation spec set by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.annotation_spec_set_path('[PROJECT]', '[ANNOTATION_SPEC_SET]')
            >>>
            >>> response = client.get_annotation_spec_set(name)

        Args:
            name (str): Required. AnnotationSpecSet resource name, format:
                projects/{project\_id}/annotationSpecSets/{annotation\_spec\_set\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_annotation_spec_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_annotation_spec_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_annotation_spec_set,
                default_retry=self._method_configs["GetAnnotationSpecSet"].retry,
                default_timeout=self._method_configs["GetAnnotationSpecSet"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetAnnotationSpecSetRequest(name=name)
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

        return self._inner_api_calls["get_annotation_spec_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_annotation_spec_sets(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists annotation spec sets for a project. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_annotation_spec_sets(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_annotation_spec_sets(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Parent of AnnotationSpecSet resource, format:
                projects/{project\_id}
            filter_ (str): Optional. Filter is not supported at this moment.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet` instances.
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
        if "list_annotation_spec_sets" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_annotation_spec_sets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_annotation_spec_sets,
                default_retry=self._method_configs["ListAnnotationSpecSets"].retry,
                default_timeout=self._method_configs["ListAnnotationSpecSets"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListAnnotationSpecSetsRequest(
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
                self._inner_api_calls["list_annotation_spec_sets"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="annotation_spec_sets",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_annotation_spec_set(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an annotation spec set by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.annotation_spec_set_path('[PROJECT]', '[ANNOTATION_SPEC_SET]')
            >>>
            >>> client.delete_annotation_spec_set(name)

        Args:
            name (str): Required. AnnotationSpec resource name, format:
                ``projects/{project_id}/annotationSpecSets/{annotation_spec_set_id}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_annotation_spec_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_annotation_spec_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_annotation_spec_set,
                default_retry=self._method_configs["DeleteAnnotationSpecSet"].retry,
                default_timeout=self._method_configs["DeleteAnnotationSpecSet"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.DeleteAnnotationSpecSetRequest(name=name)
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

        self._inner_api_calls["delete_annotation_spec_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_instruction(
        self,
        parent,
        instruction,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an instruction for how data should be labeled.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `instruction`:
            >>> instruction = {}
            >>>
            >>> response = client.create_instruction(parent, instruction)
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
            parent (str): Required. Instruction resource parent, format: projects/{project\_id}
            instruction (Union[dict, ~google.cloud.datalabeling_v1beta1.types.Instruction]): Required. Instruction of how to perform the labeling task.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.Instruction`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_instruction" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_instruction"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_instruction,
                default_retry=self._method_configs["CreateInstruction"].retry,
                default_timeout=self._method_configs["CreateInstruction"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.CreateInstructionRequest(
            parent=parent, instruction=instruction
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

        operation = self._inner_api_calls["create_instruction"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            instruction_pb2.Instruction,
            metadata_type=proto_operations_pb2.CreateInstructionMetadata,
        )

    def get_instruction(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an instruction by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.instruction_path('[PROJECT]', '[INSTRUCTION]')
            >>>
            >>> response = client.get_instruction(name)

        Args:
            name (str): Required. Instruction resource name, format:
                projects/{project\_id}/instructions/{instruction\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.Instruction` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_instruction" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_instruction"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_instruction,
                default_retry=self._method_configs["GetInstruction"].retry,
                default_timeout=self._method_configs["GetInstruction"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetInstructionRequest(name=name)
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

        return self._inner_api_calls["get_instruction"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_instructions(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists instructions for a project. Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_instructions(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_instructions(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Instruction resource parent, format: projects/{project\_id}
            filter_ (str): Optional. Filter is not supported at this moment.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.Instruction` instances.
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
        if "list_instructions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_instructions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_instructions,
                default_retry=self._method_configs["ListInstructions"].retry,
                default_timeout=self._method_configs["ListInstructions"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListInstructionsRequest(
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
                self._inner_api_calls["list_instructions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="instructions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_instruction(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an instruction object by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.instruction_path('[PROJECT]', '[INSTRUCTION]')
            >>>
            >>> client.delete_instruction(name)

        Args:
            name (str): Required. Instruction resource name, format:
                projects/{project\_id}/instructions/{instruction\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_instruction" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_instruction"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_instruction,
                default_retry=self._method_configs["DeleteInstruction"].retry,
                default_timeout=self._method_configs["DeleteInstruction"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.DeleteInstructionRequest(name=name)
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

        self._inner_api_calls["delete_instruction"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_evaluation(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an evaluation by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.evaluation_path('[PROJECT]', '[DATASET]', '[EVALUATION]')
            >>>
            >>> response = client.get_evaluation(name)

        Args:
            name (str): Required. Name of the evaluation. Format:
                'projects/{project\_id}/datasets/{dataset\_id}/evaluations/{evaluation\_id}'
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.Evaluation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_evaluation" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_evaluation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_evaluation,
                default_retry=self._method_configs["GetEvaluation"].retry,
                default_timeout=self._method_configs["GetEvaluation"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetEvaluationRequest(name=name)
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

        return self._inner_api_calls["get_evaluation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_evaluations(
        self,
        parent,
        filter_,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Searchs evaluations within a project. Supported filter: evaluation\_job,
        evaluation\_time.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_evaluations(parent, filter_):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_evaluations(parent, filter_).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Evaluation search parent. Format: projects/{project\_id}
            filter_ (str): Optional. Support filtering by model id, job state, start and end time.
                Format: "evaluation\_job.evaluation\_job\_id = {evaluation\_job\_id} AND
                evaluation\_job.evaluation\_job\_run\_time\_start = {timestamp} AND
                evaluation\_job.evaluation\_job\_run\_time\_end = {timestamp} AND
                annotation\_spec.display\_name = {display\_name}"
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.Evaluation` instances.
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
        if "search_evaluations" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_evaluations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_evaluations,
                default_retry=self._method_configs["SearchEvaluations"].retry,
                default_timeout=self._method_configs["SearchEvaluations"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.SearchEvaluationsRequest(
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
                self._inner_api_calls["search_evaluations"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="evaluations",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def search_example_comparisons(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Searchs example comparisons in evaluation, in format of examples
        of both ground truth and prediction(s). It is represented as a search with
        evaluation id.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.evaluation_path('[PROJECT]', '[DATASET]', '[EVALUATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_example_comparisons(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_example_comparisons(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Name of the Evaluation resource to search example comparison
                from. Format:
                projects/{project\_id}/datasets/{dataset\_id}/evaluations/{evaluation\_id}
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.ExampleComparison` instances.
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
        if "search_example_comparisons" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_example_comparisons"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_example_comparisons,
                default_retry=self._method_configs["SearchExampleComparisons"].retry,
                default_timeout=self._method_configs[
                    "SearchExampleComparisons"
                ].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.SearchExampleComparisonsRequest(
            parent=parent, page_size=page_size
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
                self._inner_api_calls["search_example_comparisons"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="example_comparisons",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_evaluation_job(
        self,
        parent,
        job,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an evaluation job.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `job`:
            >>> job = {}
            >>>
            >>> response = client.create_evaluation_job(parent, job)

        Args:
            parent (str): Required. Evaluation job resource parent, format:
                projects/{project\_id}.
            job (Union[dict, ~google.cloud.datalabeling_v1beta1.types.EvaluationJob]): Required. The evaluation job to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_evaluation_job,
                default_retry=self._method_configs["CreateEvaluationJob"].retry,
                default_timeout=self._method_configs["CreateEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.CreateEvaluationJobRequest(
            parent=parent, job=job
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

        return self._inner_api_calls["create_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_evaluation_job(
        self,
        evaluation_job,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an evaluation job.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> # TODO: Initialize `evaluation_job`:
            >>> evaluation_job = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_evaluation_job(evaluation_job, update_mask)

        Args:
            evaluation_job (Union[dict, ~google.cloud.datalabeling_v1beta1.types.EvaluationJob]): Required. Evaluation job that is going to be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob`
            update_mask (Union[dict, ~google.cloud.datalabeling_v1beta1.types.FieldMask]): Optional. Mask for which field in evaluation\_job should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datalabeling_v1beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_evaluation_job,
                default_retry=self._method_configs["UpdateEvaluationJob"].retry,
                default_timeout=self._method_configs["UpdateEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.UpdateEvaluationJobRequest(
            evaluation_job=evaluation_job, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("evaluation_job.name", evaluation_job.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_evaluation_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets an evaluation job by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.evaluation_job_path('[PROJECT]', '[EVALUATION_JOB]')
            >>>
            >>> response = client.get_evaluation_job(name)

        Args:
            name (str): Required. Name of the evaluation job. Format:
                'projects/{project\_id}/evaluationJobs/{evaluation\_job\_id}'
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_evaluation_job,
                default_retry=self._method_configs["GetEvaluationJob"].retry,
                default_timeout=self._method_configs["GetEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.GetEvaluationJobRequest(name=name)
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

        return self._inner_api_calls["get_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def pause_evaluation_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Pauses an evaluation job. Pausing a evaluation job that is already in
        PAUSED state will be a no-op.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.evaluation_job_path('[PROJECT]', '[EVALUATION_JOB]')
            >>>
            >>> client.pause_evaluation_job(name)

        Args:
            name (str): Required. Name of the evaluation job that is going to be paused. Format:
                'projects/{project\_id}/evaluationJobs/{evaluation\_job\_id}'
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "pause_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "pause_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.pause_evaluation_job,
                default_retry=self._method_configs["PauseEvaluationJob"].retry,
                default_timeout=self._method_configs["PauseEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.PauseEvaluationJobRequest(name=name)
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

        self._inner_api_calls["pause_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def resume_evaluation_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Resumes a paused evaluation job. Deleted evaluation job can't be resumed.
        Resuming a running evaluation job will be a no-op.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.evaluation_job_path('[PROJECT]', '[EVALUATION_JOB]')
            >>>
            >>> client.resume_evaluation_job(name)

        Args:
            name (str): Required. Name of the evaluation job that is going to be resumed.
                Format: 'projects/{project\_id}/evaluationJobs/{evaluation\_job\_id}'
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "resume_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "resume_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.resume_evaluation_job,
                default_retry=self._method_configs["ResumeEvaluationJob"].retry,
                default_timeout=self._method_configs["ResumeEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ResumeEvaluationJobRequest(name=name)
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

        self._inner_api_calls["resume_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_evaluation_job(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Stops and deletes an evaluation job.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> name = client.evaluation_job_path('[PROJECT]', '[EVALUATION_JOB]')
            >>>
            >>> client.delete_evaluation_job(name)

        Args:
            name (str): Required. Name of the evaluation job that is going to be deleted.
                Format: 'projects/{project\_id}/evaluationJobs/{evaluation\_job\_id}'
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_evaluation_job" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_evaluation_job"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_evaluation_job,
                default_retry=self._method_configs["DeleteEvaluationJob"].retry,
                default_timeout=self._method_configs["DeleteEvaluationJob"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.DeleteEvaluationJobRequest(name=name)
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

        self._inner_api_calls["delete_evaluation_job"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_evaluation_jobs(
        self,
        parent,
        filter_,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all evaluation jobs within a project with possible filters.
        Pagination is supported.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `filter_`:
            >>> filter_ = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_evaluation_jobs(parent, filter_):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_evaluation_jobs(parent, filter_).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Evaluation resource parent. Format: "projects/{project\_id}"
            filter_ (str): Optional. Only support filter by model id and job state. Format:
                "evaluation\_job.model\_id = {model\_id} AND evaluation\_job.state =
                {EvaluationJob::State}"
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.datalabeling_v1beta1.types.EvaluationJob` instances.
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
        if "list_evaluation_jobs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_evaluation_jobs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_evaluation_jobs,
                default_retry=self._method_configs["ListEvaluationJobs"].retry,
                default_timeout=self._method_configs["ListEvaluationJobs"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.ListEvaluationJobsRequest(
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
                self._inner_api_calls["list_evaluation_jobs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="evaluation_jobs",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_annotated_dataset(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an annotated dataset by resource name.

        Example:
            >>> from google.cloud import datalabeling_v1beta1
            >>>
            >>> client = datalabeling_v1beta1.DataLabelingServiceClient()
            >>>
            >>> client.delete_annotated_dataset()

        Args:
            name (str): Required. Name of the annotated dataset to delete, format:
                projects/{project\_id}/datasets/{dataset\_id}/annotatedDatasets/
                {annotated\_dataset\_id}
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_annotated_dataset" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_annotated_dataset"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_annotated_dataset,
                default_retry=self._method_configs["DeleteAnnotatedDataset"].retry,
                default_timeout=self._method_configs["DeleteAnnotatedDataset"].timeout,
                client_info=self._client_info,
            )

        request = data_labeling_service_pb2.DeleteAnnotatedDatasetRequest(name=name)
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

        self._inner_api_calls["delete_annotated_dataset"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
