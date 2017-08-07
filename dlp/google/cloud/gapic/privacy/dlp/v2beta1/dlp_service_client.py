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

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.gapic.privacy.dlp.v2beta1 import enums
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
            'google-cloud-dlp', ).version

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
        Find potentially sensitive info in a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2
          >>> client = dlp_service_client.DlpServiceClient()
          >>> inspect_config = dlp_pb2.InspectConfig()
          >>> items = []
          >>> response = client.inspect_content(inspect_config, items)

        Args:
          inspect_config (:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`): Configuration for the inspector.
          items (list[:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`]): The list of items to inspect. Items in a single request are
            considered \"related\" unless inspect_config.independent_inputs is true.
            Up to 100 are allowed per request.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectContentResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = dlp_pb2.InspectContentRequest(
            inspect_config=inspect_config, items=items)
        return self._inspect_content(request, options)

    def redact_content(self,
                       inspect_config,
                       items,
                       replace_configs,
                       options=None):
        """
        Redact potentially sensitive info from a list of strings.
        This method has limits on input size, processing time, and output size.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2
          >>> client = dlp_service_client.DlpServiceClient()
          >>> inspect_config = dlp_pb2.InspectConfig()
          >>> items = []
          >>> replace_configs = []
          >>> response = client.redact_content(inspect_config, items, replace_configs)

        Args:
          inspect_config (:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`): Configuration for the inspector.
          items (list[:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ContentItem`]): The list of items to inspect. Up to 100 are allowed per request.
          replace_configs (list[:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentRequest.ReplaceConfig`]): The strings to replace findings with. Must specify at least one.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.RedactContentResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = dlp_pb2.RedactContentRequest(
            inspect_config=inspect_config,
            items=items,
            replace_configs=replace_configs)
        return self._redact_content(request, options)

    def create_inspect_operation(self,
                                 inspect_config,
                                 storage_config,
                                 output_config,
                                 options=None):
        """
        Schedule a job scanning content in a Google Cloud Platform data repository.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2
          >>> from google.cloud.proto.privacy.dlp.v2beta1 import storage_pb2
          >>> client = dlp_service_client.DlpServiceClient()
          >>> inspect_config = dlp_pb2.InspectConfig()
          >>> storage_config = storage_pb2.StorageConfig()
          >>> output_config = dlp_pb2.OutputStorageConfig()
          >>> response = client.create_inspect_operation(inspect_config, storage_config, output_config)

        Args:
          inspect_config (:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.InspectConfig`): Configuration for the inspector.
          storage_config (:class:`google.cloud.proto.privacy.dlp.v2beta1.storage_pb2.StorageConfig`): Specification of the data set to process.
          output_config (:class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.OutputStorageConfig`): Optional location to store findings. The bucket must already exist and
            the Google APIs service account for DLP must have write permission to
            write to the given bucket.
            Results will be split over multiple csv files with each file name matching
            the pattern \"[operation_id] + [count].csv\".
            The operation_id will match the identifier for the Operation,
            and the [count] is a counter used for tracking the number of files written.
            The CSV file(s) contain the following columns regardless of storage type
            scanned: id, info_type, likelihood, byte size of finding, quote, time_stamp
            For cloud storage the next two columns are: file_path, start_offset
            For datastore the next two columns are: project_id, namespace_id, path,
            ::

                column_name, offset.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.longrunning.operations_pb2.Operation` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = dlp_pb2.CreateInspectOperationRequest(
            inspect_config=inspect_config,
            storage_config=storage_config,
            output_config=output_config)
        return self._create_inspect_operation(request, options)

    def list_inspect_findings(self,
                              name,
                              page_size=None,
                              page_token=None,
                              options=None):
        """
        Returns list of results for given inspect operation result set id.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> client = dlp_service_client.DlpServiceClient()
          >>> name = client.result_path('[RESULT]')
          >>> response = client.list_inspect_findings(name)

        Args:
          name (string): Identifier of the results set returned as metadata of
            the longrunning operation created by a call to CreateInspectOperation.
            Should be in the format of ``inspect/results/{id}.
          page_size (int): Maximum number of results to return.
            If 0, the implementation will select a reasonable value.
          page_token (string): The value returned by the last ``ListInspectFindingsResponse``; indicates
            that this is a continuation of a prior ``ListInspectFindings`` call, and that
            the system should return the next page of data.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.privacy.dlp.v2beta1.dlp_pb2.ListInspectFindingsResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = dlp_pb2.ListInspectFindingsRequest(
            name=name, page_size=page_size, page_token=page_token)
        return self._list_inspect_findings(request, options)

    def list_info_types(self, category, language_code, options=None):
        """
        Returns sensitive information types for given category.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> client = dlp_service_client.DlpServiceClient()
          >>> category = ''
          >>> language_code = ''
          >>> response = client.list_info_types(category, language_code)

        Args:
          category (string): Category name as returned by ListRootCategories.
          language_code (string): Optional BCP-47 language code for localized info type friendly
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
        # Create the request object.
        request = dlp_pb2.ListInfoTypesRequest(
            category=category, language_code=language_code)
        return self._list_info_types(request, options)

    def list_root_categories(self, language_code, options=None):
        """
        Returns the list of root categories of sensitive information.

        Example:
          >>> from google.cloud.gapic.privacy.dlp.v2beta1 import dlp_service_client
          >>> client = dlp_service_client.DlpServiceClient()
          >>> language_code = ''
          >>> response = client.list_root_categories(language_code)

        Args:
          language_code (string): Optional language code for localized friendly category names.
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
        # Create the request object.
        request = dlp_pb2.ListRootCategoriesRequest(
            language_code=language_code)
        return self._list_root_categories(request, options)
