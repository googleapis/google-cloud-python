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

Sends logs to the Stackdriver Logging API with the appropriate resource and labels for App Engine logs.
"""

import os

from google.cloud.logging.handlers.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.transports import BackgroundThreadTransport
from google.cloud.logging.resource import Resource

_GAE_PROJECT_ENV = 'GCLOUD_PROJECT'
_GAE_SERVICE_ENV = 'GAE_SERVICE'
_GAE_VERSION_ENV = 'GAE_VERSION'


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

    DEFAULT_LOGGER_NAME = 'app'

    def __init__(self, client,
                 transport=BackgroundThreadTransport):
        super(AppEngineHandler, self).__init__(client, name=self.DEFAULT_LOGGER_NAME,
                                               transport=transport, resource=self.gae_resource)

    @property
    def gae_resource(self):
        gae_resource = Resource(
            type='gae_app',
            labels={
                'project_id': os.environ.get(_GAE_PROJECT_ENV),
                'module_id': os.environ.get(_GAE_SERVICE_ENV),
                'version_id': os.environ.get(_GAE_VERSION_ENV),
            },
        )
        return gae_resource
