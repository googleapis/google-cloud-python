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
# https://github.com/google/googleapis/blob/7710ead495227e80a0f06ceb66bdf3238d926f77/google/logging/v2/logging_config.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
# Manual additions are allowed because the refresh process performs
# a 3-way merge in order to preserve those manual additions. In order to not
# break the refresh process, only certain types of modifications are
# allowed.
#
# Allowed modifications:
# 1. New methods (these should be added to the end of the class)
#
# Happy editing!

from google.gax import api_callable
from google.gax import api_utils
from google.gax import page_descriptor
from google.logging.v2 import logging_config_pb2


class ConfigServiceV2Api(object):

    # The default address of the logging service.
    _SERVICE_ADDRESS = 'logging.googleapis.com'

    # The default port of the logging service.
    _DEFAULT_SERVICE_PORT = 443

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/logging.write',
        'https://www.googleapis.com/auth/logging.admin',
        'https://www.googleapis.com/auth/logging.read',
        'https://www.googleapis.com/auth/cloud-platform.read-only',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    _LIST_SINKS_DESCRIPTOR = page_descriptor.PageDescriptor(
        'page_token',
        'next_page_token',
        'sinks',
    )

    def __init__(
            self,
            service_path=_SERVICE_ADDRESS,
            port=_DEFAULT_SERVICE_PORT,
            channel=None,
            ssl_creds=None,
            scopes=_ALL_SCOPES,
            is_idempotent_retrying=True,
            max_attempts=3,
            timeout=30):
        self.defaults = api_callable.ApiCallableDefaults(
            timeout=timeout,
            max_attempts=max_attempts,
            is_idempotent_retrying=is_idempotent_retrying)
        self.stub = api_utils.create_stub(
            logging_config_pb2.beta_create_ConfigServiceV2_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        del self.stub

    # Service calls
    def list_sinks(
            self,
            project_name='',
            **kwargs):
        """Lists sinks."""
        list_sinks_request = logging_config_pb2.ListSinksRequest(
            project_name=project_name,
            **kwargs)
        return self.list_sinks_callable()(list_sinks_request)

    def list_sinks_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_SINKS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListSinks,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def get_sink(
            self,
            sink_name='',
            **kwargs):
        """Gets a sink."""
        get_sink_request = logging_config_pb2.GetSinkRequest(
            sink_name=sink_name,
            **kwargs)
        return self.get_sink_callable()(get_sink_request)

    def get_sink_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.GetSink,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def create_sink(
            self,
            project_name='',
            sink=None,
            **kwargs):
        """Creates a sink."""
        if sink is None:
            sink = logging_config_pb2.LogSink()
        create_sink_request = logging_config_pb2.CreateSinkRequest(
            project_name=project_name,
            sink=sink,
            **kwargs)
        return self.create_sink_callable()(create_sink_request)

    def create_sink_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateSink,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def update_sink(
            self,
            sink_name='',
            sink=None,
            **kwargs):
        """Creates or updates a sink."""
        if sink is None:
            sink = logging_config_pb2.LogSink()
        update_sink_request = logging_config_pb2.UpdateSinkRequest(
            sink_name=sink_name,
            sink=sink,
            **kwargs)
        return self.update_sink_callable()(update_sink_request)

    def update_sink_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.UpdateSink,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def delete_sink(
            self,
            sink_name='',
            **kwargs):
        """Deletes a sink."""
        delete_sink_request = logging_config_pb2.DeleteSinkRequest(
            sink_name=sink_name,
            **kwargs)
        return self.delete_sink_callable()(delete_sink_request)

    def delete_sink_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.DeleteSink,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========
