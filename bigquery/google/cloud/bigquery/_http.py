# Copyright 2015 Google LLC
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

"""Create / interact with Google BigQuery connections."""

import google.api_core.gapic_v1.client_info
from google.cloud import _http

from google.cloud.bigquery import __version__


class Connection(_http.JSONConnection):
    """A connection to Google BigQuery via the JSON REST API.

    :type client: :class:`~google.cloud.bigquery.client.Client`
    :param client: The client that owns the current connection.
    """

    def __init__(self, client, client_info=None):
        super(Connection, self).__init__(client)

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=__version__, client_library_version=__version__
            )
        else:
            client_info.gapic_version = __version__
            client_info.client_library_version = __version__
        self._client_info = client_info
        self._extra_headers = {}

    API_BASE_URL = "https://www.googleapis.com"
    """The base of the API call URL."""

    API_VERSION = "v2"
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = "{api_base_url}/bigquery/{api_version}{path}"
    """A template for the URL of a particular API call."""

    @property
    def USER_AGENT(self):
        return self._client_info.to_user_agent()

    @USER_AGENT.setter
    def USER_AGENT(self, value):
        self._client_info.user_agent = value

    @property
    def _EXTRA_HEADERS(self):
        self._extra_headers[
            _http.CLIENT_INFO_HEADER
        ] = self._client_info.to_user_agent()
        return self._extra_headers

    @_EXTRA_HEADERS.setter
    def _EXTRA_HEADERS(self, value):
        self._extra_headers = value
