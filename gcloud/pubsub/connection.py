# Copyright 2015 Google Inc. All rights reserved.
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

"""Create / interact with gcloud pubsub connections."""

import os

from gcloud import connection as base_connection
from gcloud.environment_vars import PUBSUB_EMULATOR


class Connection(base_connection.JSONConnection):
    """A connection to Google Cloud Pubsub via the JSON REST API.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: (Optional) HTTP object to make requests.

    :type api_base_url: string
    :param api_base_url: The base of the API call URL. Defaults to the value
                         :attr:`Connection.API_BASE_URL`.
    """

    API_BASE_URL = 'https://pubsub.googleapis.com'
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}{path}'
    """A template for the URL of a particular API call."""

    SCOPE = ('https://www.googleapis.com/auth/pubsub',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a Cloud Pub/Sub consumer."""

    def __init__(self, credentials=None, http=None, api_base_url=None):
        super(Connection, self).__init__(credentials=credentials, http=http)
        if api_base_url is None:
            emulator_host = os.getenv(PUBSUB_EMULATOR)
            if emulator_host is None:
                api_base_url = self.__class__.API_BASE_URL
            else:
                api_base_url = 'http://' + emulator_host
        self.api_base_url = api_base_url

    def build_api_url(self, path, query_params=None,
                      api_base_url=None, api_version=None):
        """Construct an API url given a few components, some optional.

        Typically, you shouldn't need to use this method.

        :type path: string
        :param path: The path to the resource.

        :type query_params: dict
        :param query_params: A dictionary of keys and values to insert into
                             the query string of the URL.

        :type api_base_url: string
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.

        :type api_version: string
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.

        :rtype: string
        :returns: The URL assembled from the pieces provided.
        """
        if api_base_url is None:
            api_base_url = self.api_base_url
        return super(Connection, self.__class__).build_api_url(
            path, query_params=query_params,
            api_base_url=api_base_url, api_version=api_version)
