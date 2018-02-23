# Copyright 2018 Google LLC
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
"""Accesses the google.privacy.dlp.v2beta1 DlpService API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.path_template

from google.cloud.dlp_v2beta1.gapic import dlp_service_client_config
from google.cloud.dlp_v2beta1.gapic import enums
from google.cloud.dlp_v2beta1.proto import dlp_pb2
from google.cloud.dlp_v2beta1.proto import storage_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution('google-cloud-dlp',
                                                        ).version


class DlpServiceClient(object):
    """
    The DLP API is a service that allows clients
    to detect the presence of Personally Identifiable Information (PII) and other
    privacy-sensitive data in user-supplied, unstructured data streams, like text
    blocks or images.
    The service also includes methods for sensitive data redaction and
    scheduling of data scans on Google Cloud Platform based data sets.
    """

    SERVICE_ADDRESS = 'dlp.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.privacy.dlp.v2beta1.DlpService'

    @classmethod
    def result_path(cls, result):
        """Return a fully-qualified result string."""
        return google.api_core.path_template.expand(
            'inspect/results/{result}',
            result=result,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=dlp_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.dlp_service_stub = (dlp_pb2.DlpServiceStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._inspect_content = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.InspectContent,
            default_retry=method_configs['InspectContent'].retry,
            default_timeout=method_configs['InspectContent'].timeout,
            client_info=client_info,
        )
        self._redact_content = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.RedactContent,
            default_retry=method_configs['RedactContent'].retry,
            default_timeout=method_configs['RedactContent'].timeout,
            client_info=client_info,
        )
        self._deidentify_content = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.DeidentifyContent,
            default_retry=method_configs['DeidentifyContent'].retry,
            default_timeout=method_configs['DeidentifyContent'].timeout,
            client_info=client_info,
        )
        self._analyze_data_source_risk = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.AnalyzeDataSourceRisk,
            default_retry=method_configs['AnalyzeDataSourceRisk'].retry,
            default_timeout=method_configs['AnalyzeDataSourceRisk'].timeout,
            client_info=client_info,
        )
        self._create_inspect_operation = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.CreateInspectOperation,
            default_retry=method_configs['CreateInspectOperation'].retry,
            default_timeout=method_configs['CreateInspectOperation'].timeout,
            client_info=client_info,
        )
        self._list_inspect_findings = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.ListInspectFindings,
            default_retry=method_configs['ListInspectFindings'].retry,
            default_timeout=method_configs['ListInspectFindings'].timeout,
            client_info=client_info,
        )
        self._list_info_types = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.ListInfoTypes,
            default_retry=method_configs['ListInfoTypes'].retry,
            default_timeout=method_configs['ListInfoTypes'].timeout,
            client_info=client_info,
        )
        self._list_root_categories = google.api_core.gapic_v1.method.wrap_method(
            self.dlp_service_stub.ListRootCategories,
            default_retry=method_configs['ListRootCategories'].retry,
            default_timeout=method_configs['ListRootCategories'].timeout,
            client_info=client_info,
        )

    # Service calls
    def inspect_content(self,
                        inspect_config,
                        items,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Finds potentially sensitive info in a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> name = 'EMAIL_ADDRESS'
            >>> info_types_element = {'name': name}
            >>> info_types = [info_types_element]
            >>> inspect_config = {'info_types': info_types}
            >>> type_ = 'text/plain'
            >>> value = 'My email is example@example.com.'
            >>> items_element = {'type': type_, 'value': value}
            >>> items = [items_element]
            >>>
            >>> response = client.inspect_content(inspect_config, items)

        Args:
            inspect_config (Union[dict, ~google.cloud.dlp_v2beta1.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.InspectConfig`
            items (list[Union[dict, ~google.cloud.dlp_v2beta1.types.ContentItem]]): The list of items to inspect. Items in a single request are
                considered \"related\" unless inspect_config.independent_inputs is true.
                Up to 100 are allowed per request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.ContentItem`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.InspectContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.InspectContentRequest(
            inspect_config=inspect_config,
            items=items,
        )
        return self._inspect_content(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def redact_content(self,
                       inspect_config,
                       items,
                       replace_configs=None,
                       image_redaction_configs=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Redacts potentially sensitive info from a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> name = 'EMAIL_ADDRESS'
            >>> info_types_element = {'name': name}
            >>> info_types = [info_types_element]
            >>> inspect_config = {'info_types': info_types}
            >>> type_ = 'text/plain'
            >>> value = 'My email is example@example.com.'
            >>> items_element = {'type': type_, 'value': value}
            >>> items = [items_element]
            >>> name_2 = 'EMAIL_ADDRESS'
            >>> info_type = {'name': name_2}
            >>> replace_with = 'REDACTED'
            >>> replace_configs_element = {'info_type': info_type, 'replace_with': replace_with}
            >>> replace_configs = [replace_configs_element]
            >>>
            >>> response = client.redact_content(inspect_config, items, replace_configs=replace_configs)

        Args:
            inspect_config (Union[dict, ~google.cloud.dlp_v2beta1.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.InspectConfig`
            items (list[Union[dict, ~google.cloud.dlp_v2beta1.types.ContentItem]]): The list of items to inspect. Up to 100 are allowed per request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.ContentItem`
            replace_configs (list[Union[dict, ~google.cloud.dlp_v2beta1.types.ReplaceConfig]]): The strings to replace findings text findings with. Must specify at least
                one of these or one ImageRedactionConfig if redacting images.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.ReplaceConfig`
            image_redaction_configs (list[Union[dict, ~google.cloud.dlp_v2beta1.types.ImageRedactionConfig]]): The configuration for specifying what content to redact from images.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.ImageRedactionConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.RedactContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.RedactContentRequest(
            inspect_config=inspect_config,
            items=items,
            replace_configs=replace_configs,
            image_redaction_configs=image_redaction_configs,
        )
        return self._redact_content(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def deidentify_content(self,
                           deidentify_config,
                           inspect_config,
                           items,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        De-identifies potentially sensitive info from a list of strings.
        This method has limits on input size and output size.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> deidentify_config = {}
            >>> inspect_config = {}
            >>> items = []
            >>>
            >>> response = client.deidentify_content(deidentify_config, inspect_config, items)

        Args:
            deidentify_config (Union[dict, ~google.cloud.dlp_v2beta1.types.DeidentifyConfig]): Configuration for the de-identification of the list of content items.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.DeidentifyConfig`
            inspect_config (Union[dict, ~google.cloud.dlp_v2beta1.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.InspectConfig`
            items (list[Union[dict, ~google.cloud.dlp_v2beta1.types.ContentItem]]): The list of items to inspect. Up to 100 are allowed per request.
                All items will be treated as ``text/*``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.ContentItem`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.DeidentifyContentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.DeidentifyContentRequest(
            deidentify_config=deidentify_config,
            inspect_config=inspect_config,
            items=items,
        )
        return self._deidentify_content(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def analyze_data_source_risk(
            self,
            privacy_metric,
            source_table,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Schedules a job to compute risk analysis metrics over content in a Google
        Cloud Platform repository.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> privacy_metric = {}
            >>> source_table = {}
            >>>
            >>> response = client.analyze_data_source_risk(privacy_metric, source_table)
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
            privacy_metric (Union[dict, ~google.cloud.dlp_v2beta1.types.PrivacyMetric]): Privacy metric to compute.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.PrivacyMetric`
            source_table (Union[dict, ~google.cloud.dlp_v2beta1.types.BigQueryTable]): Input dataset to compute metrics over.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.BigQueryTable`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.AnalyzeDataSourceRiskRequest(
            privacy_metric=privacy_metric,
            source_table=source_table,
        )
        operation = self._analyze_data_source_risk(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            dlp_pb2.RiskAnalysisOperationResult,
            metadata_type=dlp_pb2.RiskAnalysisOperationMetadata,
        )

    def create_inspect_operation(
            self,
            inspect_config,
            storage_config,
            output_config,
            operation_config=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Schedules a job scanning content in a Google Cloud Platform data
        repository.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> name = 'EMAIL_ADDRESS'
            >>> info_types_element = {'name': name}
            >>> info_types = [info_types_element]
            >>> inspect_config = {'info_types': info_types}
            >>> url = 'gs://example_bucket/example_file.png'
            >>> file_set = {'url': url}
            >>> cloud_storage_options = {'file_set': file_set}
            >>> storage_config = {'cloud_storage_options': cloud_storage_options}
            >>> output_config = {}
            >>>
            >>> response = client.create_inspect_operation(inspect_config, storage_config, output_config)
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
            inspect_config (Union[dict, ~google.cloud.dlp_v2beta1.types.InspectConfig]): Configuration for the inspector.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.InspectConfig`
            storage_config (Union[dict, ~google.cloud.dlp_v2beta1.types.StorageConfig]): Specification of the data set to process.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.StorageConfig`
            output_config (Union[dict, ~google.cloud.dlp_v2beta1.types.OutputStorageConfig]): Optional location to store findings.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.OutputStorageConfig`
            operation_config (Union[dict, ~google.cloud.dlp_v2beta1.types.OperationConfig]): Additional configuration settings for long running operations.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dlp_v2beta1.types.OperationConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.CreateInspectOperationRequest(
            inspect_config=inspect_config,
            storage_config=storage_config,
            output_config=output_config,
            operation_config=operation_config,
        )
        operation = self._create_inspect_operation(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            dlp_pb2.InspectOperationResult,
            metadata_type=dlp_pb2.InspectOperationMetadata,
        )

    def list_inspect_findings(self,
                              name,
                              page_size=None,
                              page_token=None,
                              filter_=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Returns list of results for given inspect operation result set id.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> name = client.result_path('[RESULT]')
            >>>
            >>> response = client.list_inspect_findings(name)

        Args:
            name (str): Identifier of the results set returned as metadata of
                the longrunning operation created by a call to InspectDataSource.
                Should be in the format of ``inspect/results/{id}``.
            page_size (int): Maximum number of results to return.
                If 0, the implementation selects a reasonable value.
            page_token (str): The value returned by the last ``ListInspectFindingsResponse``; indicates
                that this is a continuation of a prior ``ListInspectFindings`` call, and that
                the system should return the next page of data.
            filter_ (str): Restricts findings to items that match. Supports info_type and likelihood.

                Examples:

                - info_type=EMAIL_ADDRESS
                - info_type=PHONE_NUMBER,EMAIL_ADDRESS
                - likelihood=VERY_LIKELY
                - likelihood=VERY_LIKELY,LIKELY
                - info_type=EMAIL_ADDRESS,likelihood=VERY_LIKELY,LIKELY
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.ListInspectFindingsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.ListInspectFindingsRequest(
            name=name,
            page_size=page_size,
            page_token=page_token,
            filter=filter_,
        )
        return self._list_inspect_findings(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_info_types(self,
                        category,
                        language_code,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Returns sensitive information types for given category.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> category = 'PII'
            >>> language_code = 'en'
            >>>
            >>> response = client.list_info_types(category, language_code)

        Args:
            category (str): Category name as returned by ListRootCategories.
            language_code (str): Optional BCP-47 language code for localized info type friendly
                names. If omitted, or if localized strings are not available,
                en-US strings will be returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.ListInfoTypesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.ListInfoTypesRequest(
            category=category,
            language_code=language_code,
        )
        return self._list_info_types(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_root_categories(self,
                             language_code,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Returns the list of root categories of sensitive information.

        Example:
            >>> from google.cloud import dlp_v2beta1
            >>>
            >>> client = dlp_v2beta1.DlpServiceClient()
            >>>
            >>> language_code = 'en'
            >>>
            >>> response = client.list_root_categories(language_code)

        Args:
            language_code (str): Optional language code for localized friendly category names.
                If omitted or if localized strings are not available,
                en-US strings will be returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dlp_v2beta1.types.ListRootCategoriesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = dlp_pb2.ListRootCategoriesRequest(
            language_code=language_code, )
        return self._list_root_categories(
            request, retry=retry, timeout=timeout, metadata=metadata)
