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

import os
import platform

from google.gax import api_callable
from google.gax import config
from google.gax.path_template import PathTemplate
import google.gax
import yaml

from google.logging.v2 import logging_config_pb2


class ConfigServiceV2Api(object):
    """See src/api/google/logging/v2/logging.proto for documentation"""

    _CODE_GEN_NAME_VERSION = 'gapic-0.1.0'

    SERVICE_ADDRESS = 'logging.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/logging.write',
                   'https://www.googleapis.com/auth/logging.admin',
                   'https://www.googleapis.com/auth/logging.read',
                   'https://www.googleapis.com/auth/cloud-platform.read-only',
                   'https://www.googleapis.com/auth/cloud-platform', )

    _PROJECT_PATH_TEMPLATE = PathTemplate('projects/{project}')
    _SINK_PATH_TEMPLATE = PathTemplate('projects/{project}/sinks/{sink}')

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
                 scopes=_ALL_SCOPES,
                 retrying_override=None,
                 bundling_override=None,
                 timeout=30,
                 app_name=None,
                 app_version=None):
        """Constructor.

        Args:
          :keyword service_path: The DNS of the API remote host.
          :type service_path: string
          :keyword port: The port on which to connect to the remote host.
          :type port: int
          :keyword channel: A Channel object through which to make calls.
          :type channel: A grpc.beta.implementations.Channel object
          :keyword ssl_creds: A ClientCredentials for use with an SSL-
            enabled channel
          :type ssl_creds: A grpc.beta.implementations.ClientCredentials
            object
          :keyword retrying_override: A dictionary that overrides default
            retrying settings. ``retrying_override`` maps method names
            (e.g., 'list_foo') to custom RetryOptions objects, or to None.
            A value of None indicates that the method in question should not
            retry.
          :type retrying_override: dict
          :keyword bundling_override: A dictionary that overrides default
            bundling settings. ``bundling_override`` maps bundling method
            names (e.g., 'publish_foo') to custom BundleOptions objects, or to
            None. It is invalid to have a key for a method that is not
            bundling-enabled. A value of None indicates that the method in
            question should not bundle.
          :type bundling_override: dict
          :keyword timeout: The default timeout, in seconds, for calls made
            through this client
          :type timeout: int
          :keyword app_name: The codename of the calling service.
          :type app_name: string
          :keyword app_version: The version of the calling service.
          :type app_version: string
        """
        if app_name is None:
            app_name = 'gax'
        if app_version is None:
            app_version = google.gax.__version__
        bundling_override = bundling_override or dict()
        retrying_override = retrying_override or dict()
        config_filename = os.path.join(
            os.path.dirname(__file__), 'config_service_v2_api.yaml')
        with open(config_filename, 'r') as api_yaml:
            self._defaults = api_callable.construct_settings(
                yaml.load(api_yaml.read()), bundling_override,
                retrying_override, config.STATUS_CODE_NAMES, timeout)
        google_apis_agent = '{}-{}/{}/gax-{}/{}'.format(
            app_name, app_version, self._CODE_GEN_NAME_VERSION,
            google.gax.__version__,
            'python-{}'.format(platform.python_version()))
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

        :type project_name: string
        :type options: api_callable.CallOptions
        """
        req = logging_config_pb2.ListSinksRequest(project_name=project_name)
        settings = self._defaults['list_sinks'].merge(options)
        return api_callable.ApiCallable(
            self.stub.ListSinks,
            settings=settings)(req,
                               metadata=self._headers)

    def get_sink(self, sink_name='', options=None):
        """
        Gets a sink.

        :type sink_name: string
        :type options: api_callable.CallOptions
        """
        req = logging_config_pb2.GetSinkRequest(sink_name=sink_name)
        settings = self._defaults['get_sink'].merge(options)
        return api_callable.ApiCallable(
            self.stub.GetSink,
            settings=settings)(req,
                               metadata=self._headers)

    def create_sink(self, project_name='', sink=None, options=None):
        """
        Creates a sink.

        :type project_name: string
        :type sink: logging_config_pb2.LogSink
        :type options: api_callable.CallOptions
        """
        if sink is None:
            sink = logging_config_pb2.LogSink()
        req = logging_config_pb2.CreateSinkRequest(project_name=project_name,
                                                   sink=sink)
        settings = self._defaults['create_sink'].merge(options)
        return api_callable.ApiCallable(
            self.stub.CreateSink,
            settings=settings)(req,
                               metadata=self._headers)

    def update_sink(self, sink_name='', sink=None, options=None):
        """
        Creates or updates a sink.

        :type sink_name: string
        :type sink: logging_config_pb2.LogSink
        :type options: api_callable.CallOptions
        """
        if sink is None:
            sink = logging_config_pb2.LogSink()
        req = logging_config_pb2.UpdateSinkRequest(sink_name=sink_name,
                                                   sink=sink)
        settings = self._defaults['update_sink'].merge(options)
        return api_callable.ApiCallable(
            self.stub.UpdateSink,
            settings=settings)(req,
                               metadata=self._headers)

    def delete_sink(self, sink_name='', options=None):
        """
        Deletes a sink.

        :type sink_name: string
        :type options: api_callable.CallOptions
        """
        req = logging_config_pb2.DeleteSinkRequest(sink_name=sink_name)
        settings = self._defaults['delete_sink'].merge(options)
        return api_callable.ApiCallable(
            self.stub.DeleteSink,
            settings=settings)(req,
                               metadata=self._headers)
