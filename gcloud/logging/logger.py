# Copyright 2016 Google Inc. All rights reserved.
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

"""Define API Loggers."""


class Logger(object):
    """Loggers represent named targets for log entries.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.logs

    :type name: string
    :param name: the name of the logger

    :type client: :class:`gcloud.logging.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the logger (which requires a project).
    """
    def __init__(self, name, client):
        self.name = name
        self._client = client

    @property
    def client(self):
        """Clent bound to the logger."""
        return self._client

    @property
    def project(self):
        """Project bound to the logger."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in logging APIs"""
        return 'projects/%s/logs/%s' % (self.project, self.name)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`gcloud.logging.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def log_text(self, text, client=None):
        """API call:  log a text message via a POST request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries/write

        :type text: text
        :param text: the log message.

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.
        """
        client = self._require_client(client)

        data = {
            'entries': [{
                'logName': self.full_name,
                'textPayload': text,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        client.connection.api_request(
            method='POST', path='/entries:write', data=data)

    def log_struct(self, info, client=None):
        """API call:  log a text message via a POST request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries/write

        :type info: dict
        :param info: the log entry information

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current logger.
        """
        client = self._require_client(client)

        data = {
            'entries': [{
                'logName': self.full_name,
                'jsonPayload': info,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        client.connection.api_request(
            method='POST', path='/entries:write', data=data)
