# Copyright 2014 Google Inc. All rights reserved.
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

""" Shared implementation of connections to API servers."""

from pkg_resources import get_distribution

import httplib2


class Connection(object):
    """A generic connection to Google Cloud Platform.

    Subclasses should understand only the basic types in method arguments,
    however they should be capable of returning advanced types.
    """

    API_BASE_URL = 'https://www.googleapis.com'
    """The base of the API call URL."""

    _EMPTY = object()
    """A pointer to represent an empty value for default arguments."""

    USER_AGENT = "gcloud-python/{0}".format(get_distribution('gcloud').version)
    """The user agent for gcloud-python requests."""

    def __init__(self, credentials=None):
        """Constructor for Connection.

        :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                           :class:`NoneType`
        :param credentials: The OAuth2 Credentials to use for this connection.
        """
        self._http = None
        self._credentials = credentials

    @property
    def credentials(self):
        """Getter for current credentials.

        :rtype: :class:`oauth2client.client.OAuth2Credentials` or
                :class:`NoneType`
        :returns: The credentials object associated with this connection.
        """
        return self._credentials

    @property
    def http(self):
        """A getter for the HTTP transport used in talking to the API.

        :rtype: :class:`httplib2.Http`
        :returns: A Http object used to transport data.
        """
        if self._http is None:
            self._http = httplib2.Http()
            if self._credentials:
                self._http = self._credentials.authorize(self._http)
        return self._http
