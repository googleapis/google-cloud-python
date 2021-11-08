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

import os
import pkg_resources

from google.cloud import _http  # type: ignore  # pytype: disable=import-error
from google.cloud.bigquery import __version__


# TODO: Increase the minimum version of google-cloud-core to 1.6.0
# and remove this logic. See:
# https://github.com/googleapis/python-bigquery/issues/509
if os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE") == "true":  # pragma: NO COVER
    release = pkg_resources.get_distribution("google-cloud-core").parsed_version
    if release < pkg_resources.parse_version("1.6.0"):
        raise ImportError("google-cloud-core >= 1.6.0 is required to use mTLS feature")


class Connection(_http.JSONConnection):
    """A connection to Google BigQuery via the JSON REST API.

    Args:
        client (google.cloud.bigquery.client.Client): The client that owns the current connection.

        client_info (Optional[google.api_core.client_info.ClientInfo]): Instance used to generate user agent.

        api_endpoint (str): The api_endpoint to use. If None, the library will decide what endpoint to use.
    """

    DEFAULT_API_ENDPOINT = "https://bigquery.googleapis.com"
    DEFAULT_API_MTLS_ENDPOINT = "https://bigquery.mtls.googleapis.com"

    def __init__(self, client, client_info=None, api_endpoint=None):
        super(Connection, self).__init__(client, client_info)
        self.API_BASE_URL = api_endpoint or self.DEFAULT_API_ENDPOINT
        self.API_BASE_MTLS_URL = self.DEFAULT_API_MTLS_ENDPOINT
        self.ALLOW_AUTO_SWITCH_TO_MTLS_URL = api_endpoint is None
        self._client_info.gapic_version = __version__
        self._client_info.client_library_version = __version__

    API_VERSION = "v2"
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = "{api_base_url}/bigquery/{api_version}{path}"
    """A template for the URL of a particular API call."""
