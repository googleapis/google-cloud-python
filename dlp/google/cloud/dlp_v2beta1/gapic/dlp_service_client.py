# Copyright 2017, Google Inc. All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/privacy/dlp/v2beta1/dlp.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.privacy.dlp.v2beta1 DlpService API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gapic.longrunning import operations_client
from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.dlp_v2beta1.gapic import enums
from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2
from google.cloud.proto.privacy.dlp.v2beta1 import storage_pb2


class DlpServiceClient(object):
    """
    The DLP API is a service that allows clients
    to detect the presence of Personally Identifiable Information (PII) and other
    privacy-sensitive data in user-supplied, unstructured data streams, like text
    blocks or images.
    The service also includes methods for sensitive data redaction and
    scheduling of data scans on Google Cloud Platform based data sets.
    """

    SERVICE_ADDRESS = 'dlp.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    _RESULT_PATH_TEMPLATE = path_template.PathTemplate(
        'inspect/results/{result}')

    @classmethod
    def result_path(cls, result):
        """Returns a fully-qualified result resource name string."""
        return cls._RESULT_PATH_TEMPLATE.render({
            'result': result,
        })

    @classmethod
    def match_result_from_result_name(cls, result_name):
        """Parses the result from a result resource.

        Args:
          result_name (string): A fully-qualified path representing a result
            resource.

        Returns:
          A string representing the result.
        """
        return cls._RESULT_PATH_TEMPLATE.match(result_name).get('result')

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 app_name=None,
                 app_version='',
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.Channel`): A ``Channel`` instance through
            which to make calls.
          credentials (object): The authorization credentials to attach to
            requests. These credentials identify this application to the
            service.
          ssl_credentials (:class:`grpc.ChannelCredentials`): A
            ``ChannelCredentials`` instance for use with an SSL-enabled
            channel.
          scopes (list[string]): A list of OAuth2 scopes to attach to requests.
          client_config (dict):
            A dictionary for call options for each method. See
            :func:`google.gax.construct_settings` for the structure of
            this data. Falls back to the default config if not specified
            or the specified config is missing data points.
          app_name (string): The name of the application calling
            the service. Recommended for analytics purposes.
          app_version (string): The version of the application calling
            the service. Recommended for analytics purposes.
          lib_name (string): The API library software used for calling
            the service. (Unless you are writing an API client itself,
            leave this as default.)
          lib_version (string): The API library software version used
            for calling the service. (Unless you are writing an API client
            itself, leave this as default.)
          metrics_headers (dict): A dictionary of values for tracking
            client library metrics. Ultimately serializes to a string
            (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
            considered private.

        Returns:
          A DlpServiceClient object.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'gapic-google-cloud-dlp-v2beta1', ).version

        # Load the configuration defaults.
        default_client_config = json.loads(
            pkg_resources.resource_string(
                __name__, 'dlp_service_client_config.json').decode())
        defaults = api_callable.construct_settings(
            'google.privacy.dlp.v2beta1.DlpService',
            default_client_config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers, )
        self.dlp_service_stub = config.create_stub(
            dlp_pb2.DlpServiceStub,
            channel=channel,
            service_path=service_path,
            service_port=port,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self.operations_client = operations_client.OperationsClient(
            service_path=service_path,
            port=port,
            channel=channel,
            credentials=credentials,
            ssl_credentials=ssl_credentials,
            scopes=scopes,
            client_config=client_config,
            metrics_headers=metrics_headers, )

        self._inspect_content = api_callable.create_api_call(
            self.dlp_service_stub.InspectContent,
            settings=defaults['inspect_content'])
        self._redact_content = api_callable.create_api_call(
            self.dlp_service_stub.RedactContent,
            settings=defaults['redact_content'])
        self._create_inspect_operation = api_callable.create_api_call(
            self.dlp_service_stub.CreateInspectOperation,
            settings=defaults['create_inspect_operation'])
        self._list_inspect_findings = api_callable.create_api_call(
            self.dlp_service_stub.ListInspectFindings,
            settings=defaults['list_inspect_findings'])
        self._list_info_types = api_callable.create_api_call(
            self.dlp_service_stub.ListInfoTypes,
            settings=defaults['list_info_types'])
        self._list_root_categories = api_callable.create_api_call(
            self.dlp_service_stub.ListRootCategories,
            settings=defaults['list_root_categories'])

    # Service calls
    def inspect_content(self, inspect_config, items, options=None):
        """
        Finds potentially sensitive info in a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
          >>> name = 'EMAIL_ADDRESS'
          >>> info_types_element = {'name': name}
          >>> info_types = [info_types_element]
          >>> inspect_config = {'info_types': info_types}
          >>> type_ = 'text/plain'
          >>> value = 'My email is example@example.com.'
          >>> items_element = {'type': type_, 'value': value}
          >>> items = [items_element]
          >>> response = client.inspect_content(inspect_config, items)

        Args:
          inspect_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`]): Configuration for the inspector.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`
          items (list[Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`]]): The list of items to inspect. Items in a single request are
            considered \"related\" unless inspect_config.independent_inputs is true.
            Up to 100 are allowed per request.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectContentResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.InspectContentRequest(
            inspect_config=inspect_config, items=items)
        return self._inspect_content(request, options)

    def redact_content(self,
                       inspect_config,
                       items,
                       replace_configs,
                       image_redaction_configs=None,
                       options=None):
        """
        Redacts potentially sensitive info from a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
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
          >>> response = client.redact_content(inspect_config, items, replace_configs)

        Args:
          inspect_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`]): Configuration for the inspector.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`
          items (list[Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`]]): The list of items to inspect. Up to 100 are allowed per request.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`
          replace_configs (list[Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentRequest.ReplaceConfig`]]): The strings to replace findings text findings with. Must specify at least
            one of these or one ImageRedactionConfig if redacting images.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentRequest.ReplaceConfig`
          image_redaction_configs (list[Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentRequest.ImageRedactionConfig`]]): The configuration for specifying what content to redact from images.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentRequest.ImageRedactionConfig`
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.RedactContentRequest(
            inspect_config=inspect_config,
            items=items,
            replace_configs=replace_configs,
            image_redaction_configs=image_redaction_configs)
        return self._redact_content(request, options)

    def create_inspect_operation(self,
                                 inspect_config,
                                 storage_config,
                                 output_config,
                                 operation_config=None,
                                 options=None):
        """
        Schedules a job scanning content in a Google Cloud Platform data
        repository.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
          >>> name = 'EMAIL_ADDRESS'
          >>> info_types_element = {'name': name}
          >>> info_types = [info_types_element]
          >>> inspect_config = {'info_types': info_types}
          >>> url = 'gs://example_bucket/example_file.png'
          >>> file_set = {'url': url}
          >>> cloud_storage_options = {'file_set': file_set}
          >>> storage_config = {'cloud_storage_options': cloud_storage_options}
          >>> output_config = {}
          >>> response = client.create_inspect_operation(inspect_config, storage_config, output_config)
          >>>
          >>> def callback(operation_future):
          >>>     # Handle result.
          >>>     result = operation_future.result()
          >>>
          >>> response.add_done_callback(callback)
          >>>
          >>> # Handle metadata.
          >>> metadata = response.metadata()

        Args:
          inspect_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`]): Configuration for the inspector.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`
          storage_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.storage_pb2.StorageConfig`]): Specification of the data set to process.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.storage_pb2.StorageConfig`
          output_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.OutputStorageConfig`]): Optional location to store findings. The bucket must already exist and
            the Google APIs service account for DLP must have write permission to
            write to the given bucket.
            <p>Results are split over multiple csv files with each file name matching
            the pattern \"[operation_id]_[count].csv\", for example
            ``3094877188788974909_1.csv``. The ``operation_id`` matches the
            identifier for the Operation, and the ``count`` is a counter used for
            tracking the number of files written. <p>The CSV file(s) contain the
            following columns regardless of storage type scanned: <li>id <li>info_type
            <li>likelihood <li>byte size of finding <li>quote <li>timestamp<br/>
            <p>For Cloud Storage the next columns are: <li>file_path
            <li>start_offset<br/>
            <p>For Cloud Datastore the next columns are: <li>project_id
            <li>namespace_id <li>path <li>column_name <li>offset<br/>
            <p>For BigQuery the next columns are: <li>row_number <li>project_id
            <li>dataset_id <li>table_id
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.OutputStorageConfig`
          operation_config (Union[dict|:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.OperationConfig`]): Additional configuration settings for long running operations.
            If a dict is provided, it must be of the same form as the protobuf
            message :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.OperationConfig`
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.gax._OperationFuture` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.CreateInspectOperationRequest(
            inspect_config=inspect_config,
            storage_config=storage_config,
            output_config=output_config,
            operation_config=operation_config)
        return google.gax._OperationFuture(
            self._create_inspect_operation(request, options),
            self.operations_client, dlp_pb2.InspectOperationResult,
            dlp_pb2.InspectOperationMetadata, options)

    def list_inspect_findings(self,
                              name,
                              page_size=None,
                              page_token=None,
                              filter_=None,
                              options=None):
        """
        Returns list of results for given inspect operation result set id.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
          >>> name = client.result_path('[RESULT]')
          >>> response = client.list_inspect_findings(name)

        Args:
          name (str): Identifier of the results set returned as metadata of
            the longrunning operation created by a call to CreateInspectOperation.
            Should be in the format of ``inspect/results/{id}``.
          page_size (int): Maximum number of results to return.
            If 0, the implementation selects a reasonable value.
          page_token (str): The value returned by the last ``ListInspectFindingsResponse``; indicates
            that this is a continuation of a prior ``ListInspectFindings`` call, and that
            the system should return the next page of data.
          filter_ (str): Restricts findings to items that match. Supports info_type and likelihood.
            <p>Examples:<br/>
            <li>info_type=EMAIL_ADDRESS
            <li>info_type=PHONE_NUMBER,EMAIL_ADDRESS
            <li>likelihood=VERY_LIKELY
            <li>likelihood=VERY_LIKELY,LIKELY
            <li>info_type=EMAIL_ADDRESS,likelihood=VERY_LIKELY,LIKELY
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ListInspectFindingsResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.ListInspectFindingsRequest(
            name=name,
            page_size=page_size,
            page_token=page_token,
            filter=filter_)
        return self._list_inspect_findings(request, options)

    def list_info_types(self, category, language_code, options=None):
        """
        Returns sensitive information types for given category.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
          >>> category = 'PII'
          >>> language_code = 'en'
          >>> response = client.list_info_types(category, language_code)

        Args:
          category (str): Category name as returned by ListRootCategories.
          language_code (str): Optional BCP-47 language code for localized info type friendly
            names. If omitted, or if localized strings are not available,
            en-US strings will be returned.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ListInfoTypesResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.ListInfoTypesRequest(
            category=category, language_code=language_code)
        return self._list_info_types(request, options)

    def list_root_categories(self, language_code, options=None):
        """
        Returns the list of root categories of sensitive information.

        Example:
          >>> from google.cloud import dlp_v2beta1
          >>> client = dlp_v2beta1.DlpServiceClient()
          >>> language_code = 'en'
          >>> response = client.list_root_categories(language_code)

        Args:
          language_code (str): Optional language code for localized friendly category names.
            If omitted or if localized strings are not available,
            en-US strings will be returned.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ListRootCategoriesResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = dlp_pb2.ListRootCategoriesRequest(
            language_code=language_code)
        return self._list_root_categories(request, options)
