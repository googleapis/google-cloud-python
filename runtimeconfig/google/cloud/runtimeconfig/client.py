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

"""Client for interacting with the Google Cloud RuntimeConfig API."""


from google.cloud.client import JSONClient
from google.cloud.runtimeconfig.connection import Connection
from google.cloud.runtimeconfig.config import Config


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project:
        (Optional) The project which the client acts on behalf of.  If not
        passed, falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials:
        (Optional) The OAuth2 Credentials to use for the connection owned by
        this client. If not passed (and if no ``http`` object is passed), falls
        back to the default inferred from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http:
        (Optional) An HTTP object to make requests. If not passed, an ``http``
        object is created that is bound to the ``credentials`` for the current
        object.
    """

    _connection_class = Connection

    def config(self, config_name):
        """Factory constructor for config object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a config object owned by this client.

        :type config_name: str
        :param config_name: The name of the config to be instantiated.

        :rtype: :class:`google.cloud.runtimeconfig.config.Config`
        :returns: The config object created.
        """
        return Config(client=self, name=config_name)
