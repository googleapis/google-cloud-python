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

"""Basic connection for Google Cloud Natural Language API."""

from google.cloud import _http

from google.cloud.language import __version__


_CLIENT_INFO = _http.CLIENT_INFO_TEMPLATE.format(__version__)


class Connection(_http.JSONConnection):
    """A connection to Google Cloud Natural Language JSON REST API.

    :type client: :class:`~google.cloud.language.client.Client`
    :param client: The client that owns the current connection.
    """

    API_BASE_URL = 'https://language.googleapis.com'
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}/documents:{path}'
    """A template for the URL of a particular API call."""

    _EXTRA_HEADERS = {
        _http.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }
