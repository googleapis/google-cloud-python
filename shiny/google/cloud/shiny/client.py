# Copyright 2016 Google Inc.
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

"""Client for interacting with the Google Shiny New API."""


from google.cloud.client import JSONClient
from google.cloud.shiny.connection import Connection
from google.cloud.shiny.unicorn import Unicorn


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for the
                        connection owned by this client. If not passed (and
                        if no ``http`` object is passed), falls back to the
                        default inferred from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: (Optional) HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def __init__(self, project=None, credentials=None, http=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, http=http)
        self.shiny_api = _JSONShinyAPI(self)

    def unicorn(self, name):
        """Create a unicorn instance bound to the current client.

        :type name: str
        :param name: The name of the unicorn.

        :rtype: :class:`~google.cloud.shiny.unicorn.Unicorn`
        :returns: A unicorn instance for the current client.
        """
        return Unicorn(name, self)


class _JSONShinyAPI(object):
    """Low-level class for making API calls via JSON-over-HTTP.

    :type client: :class:`~google.cloud.shiny.client.Client`
    :param client: The client that will make API requests.
    """

    def __init__(self, client):
        self._client = client
        self._connection = client.connection

    def do_nothing(self, unicorn_name):
        """Send a request to the Shiny API backend's "do nothing" method.

        :type unicorn_name: str
        :param unicorn_name: The name of a unicorn.
        """
        path = 'do-nothing/{}'.format(unicorn_name)
        data = {'transmogrify': 'doodad'}
        self._connection.api_request(
            method='POST', path=path, data=data)
