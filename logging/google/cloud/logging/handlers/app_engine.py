# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Logging handler for App Engine Flexible

Logs to the well-known file that the fluentd sidecar container on App Engine
Flexible is configured to read from and send to Stackdriver Logging.

See the fluentd configuration here:

https://github.com/GoogleCloudPlatform/appengine-sidecars-docker/tree/master/fluentd_logger
"""

# This file is largely copied from:
#  https://github.com/GoogleCloudPlatform/python-compat-runtime/blob/master
# /appengine-vmruntime/vmruntime/cloud_logging.py

import logging.handlers

from google.cloud.logging.handlers.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.transports import BackgroundThreadTransport
from google.cloud.logging.resource import Resource

DEFAULT_LOGGER_NAME = 'python'

EXCLUDED_LOGGER_DEFAULTS = ('google.cloud', 'oauth2client')

_GLOBAL_RESOURCE = Resource(type='global', labels={})


class AppEngineHandler(CloudLoggingHandler):
    """A handler that directly makes Stackdriver logging API calls.

    This handler can be used to route Python standard logging messages directly
    to the Stackdriver Logging API.

    This handler supports both an asynchronous and synchronous transport.

    :type client: :class:`google.cloud.logging.client`
    :param client: the authenticated Google Cloud Logging client for this
                   handler to use

    :type name: str
    :param name: the name of the custom log in Stackdriver Logging. Defaults
                 to 'python'. The name of the Python logger will be represented
                 in the ``python_logger`` field.

    :type transport: type
    :param transport: Class for creating new transport objects. It should
                      extend from the base :class:`.Transport` type and
                      implement :meth`.Transport.send`. Defaults to
                      :class:`.BackgroundThreadTransport`. The other
                      option is :class:`.SyncTransport`.

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: Monitored resource of the entry, defaults
                     to the global resource type.
    """

    def __init__(self, client,
                 name=DEFAULT_LOGGER_NAME,
                 transport=BackgroundThreadTransport,
                 resource=_GLOBAL_RESOURCE):
        super(AppEngineHandler, self).__init__(client, name, transport)
        self.resource=resource

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See: https://docs.python.org/2/library/logging.html#handler-objects

        :type record: :class:`logging.LogRecord`
        :param record: The record to be logged.
        """
        message = super(CloudLoggingHandler, self).format(record)
        self.transport.send(record, message, self.resource)
