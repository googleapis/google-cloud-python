# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/logging/v2/logging_config.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.logging.v2 ConfigServiceV2 API."""

import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.logging.v2 import logging_config_pb2

_PageDesc = google.gax.PageDescriptor


class ConfigServiceV2Api(object):
    SERVICE_ADDRESS = 'logging.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _CODE_GEN_NAME_VERSION = 'gapic/0.1.0'

    _GAX_VERSION = pkg_resources.get_distribution('google-gax').version

    _DEFAULT_TIMEOUT = 30

    _PAGE_DESCRIPTORS = {
        'list_sinks': _PageDesc('page_token', 'next_page_token', 'sinks')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/logging.write',
                   'https://www.googleapis.com/auth/logging.admin',
                   'https://www.googleapis.com/auth/logging.read',
                   'https://www.googleapis.com/auth/cloud-platform.read-only',
                   'https://www.googleapis.com/auth/cloud-platform', )

    _PROJECT_PATH_TEMPLATE = path_template.PathTemplate('projects/{project}')
    _SINK_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/sinks/{sink}')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return cls._PROJECT_PATH_TEMPLATE.instantiate({'project': project, })

    @classmethod
    def sink_path(cls, project, sink):
        """Returns a fully-qualified sink resource name string."""
        return cls._SINK_PATH_TEMPLATE.instantiate({
            'project': project,
            'sink': sink,
        })

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 ssl_creds=None,
                 scopes=None,
                 retrying_override=None,
                 bundling_override=None,
                 timeout=_DEFAULT_TIMEOUT,
                 app_name='gax',
                 app_version=_GAX_VERSION):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.beta.implementations.Channel`): A ``Channel``
            object through which to make calls.
          ssl_creds (:class:`grpc.beta.implementations.ClientCredentials`):
            A `ClientCredentials` for use with an SSL-enabled channel.
          retrying_override (dict[string, :class:`google.gax.RetryOptions`]): A
            dictionary that overrides default retrying settings.
            ``retrying_override`` maps method names (e.g., ``'list_foo'``) to
            custom RetryOptions objects, or to None. A value of None indicates
            that the method in question should not retry.
          bundling_override (dict[string, :class:`google.gax.BundleOptions`]): A
            dictionary that overrides default bundling settings.
            ``bundling_override`` maps bundling method names (e.g.,
            'publish_foo') to custom BundleOptions objects, or to None. It is
            invalid to have a key for a method that is not bundling-enabled. A
            value of None indicates that the method in question should not
            bundle.
          timeout (int): The default timeout, in seconds, for calls made
            through this client
          app_name (string): The codename of the calling service.
          app_version (string): The version of the calling service.

        Returns:
          A ConfigServiceV2Api object.
        """
        if scopes is None:
            scopes = self._ALL_SCOPES
        bundling_override = bundling_override or {}
        retrying_override = retrying_override or {}
        client_config = pkg_resources.resource_string(
            __name__, 'config_service_v2_client_config.json')
        self._defaults = api_callable.construct_settings(
            'google.logging.v2.ConfigServiceV2',
            json.loads(client_config),
            bundling_override,
            retrying_override,
            config.STATUS_CODE_NAMES,
            timeout,
            page_descriptors=self._PAGE_DESCRIPTORS)
        google_apis_agent = '{}/{};{};gax/{};python/{}'.format(
            app_name, app_version, self._CODE_GEN_NAME_VERSION,
            self._GAX_VERSION, platform.python_version())
        self._headers = [('x-google-apis-agent', google_apis_agent)]
        self.stub = config.create_stub(
            logging_config_pb2.beta_create_ConfigServiceV2_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    # Service calls
    def list_sinks(self, project_name='', options=None):
        """
        Lists sinks.

        Args:
          project_name (string): Required. The resource name of the project containing the sinks.
            Example: `"projects/my-logging-project"`, `"projects/01234567890"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Yields:
          Instances of :class:`google.logging.v2.logging_config_pb2.LogSink`
          unless page streaming is disabled through the call options. If
          page streaming is disabled, a single
          :class:`google.logging.v2.logging_config_pb2.ListSinksResponse` instance
          is returned.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_config_pb2.ListSinksRequest(project_name=project_name)
        settings = self._defaults['list_sinks'].merge(options)
        api_call = api_callable.create_api_call(self.stub.ListSinks,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def get_sink(self, sink_name='', options=None):
        """
        Gets a sink.

        Args:
          sink_name (string): The resource name of the sink to return.
            Example: `"projects/my-project-id/sinks/my-sink-id"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_config_pb2.LogSink` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_config_pb2.GetSinkRequest(sink_name=sink_name)
        settings = self._defaults['get_sink'].merge(options)
        api_call = api_callable.create_api_call(self.stub.GetSink,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def create_sink(self, project_name='', sink=None, options=None):
        """
        Creates a sink.

        Args:
          project_name (string): The resource name of the project in which to create the sink.
            Example: `"projects/my-project-id"`.

            The new sink must be provided in the request.
          sink (:class:`google.logging.v2.logging_config_pb2.LogSink`): The new sink, which must not have an identifier that already
            exists.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_config_pb2.LogSink` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if sink is None:
            sink = logging_config_pb2.LogSink()
        req = logging_config_pb2.CreateSinkRequest(project_name=project_name,
                                                   sink=sink)
        settings = self._defaults['create_sink'].merge(options)
        api_call = api_callable.create_api_call(self.stub.CreateSink,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def update_sink(self, sink_name='', sink=None, options=None):
        """
        Creates or updates a sink.

        Args:
          sink_name (string): The resource name of the sink to update.
            Example: `"projects/my-project-id/sinks/my-sink-id"`.

            The updated sink must be provided in the request and have the
            same name that is specified in `sinkName`.  If the sink does not
            exist, it is created.
          sink (:class:`google.logging.v2.logging_config_pb2.LogSink`): The updated sink, whose name must be the same as the sink
            identifier in `sinkName`.  If `sinkName` does not exist, then
            this method creates a new sink.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.logging.v2.logging_config_pb2.LogSink` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        if sink is None:
            sink = logging_config_pb2.LogSink()
        req = logging_config_pb2.UpdateSinkRequest(sink_name=sink_name,
                                                   sink=sink)
        settings = self._defaults['update_sink'].merge(options)
        api_call = api_callable.create_api_call(self.stub.UpdateSink,
                                                settings=settings)
        return api_call(req, metadata=self._headers)

    def delete_sink(self, sink_name='', options=None):
        """
        Deletes a sink.

        Args:
          sink_name (string): The resource name of the sink to delete.
            Example: `"projects/my-project-id/sinks/my-sink-id"`.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        req = logging_config_pb2.DeleteSinkRequest(sink_name=sink_name)
        settings = self._defaults['delete_sink'].merge(options)
        api_call = api_callable.create_api_call(self.stub.DeleteSink,
                                                settings=settings)
        api_call(req, metadata=self._headers)
